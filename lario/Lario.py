
import pygame
from State import State


class Lario(State):

    def __init__(self, game):
        super().__init__(game)

        # Physics state
        self.acceleration = [0.0, 0.0]
        self.velocity = [0.0, 0.0]
        self.position = [0.0, 0.0]
        self.friction = [0.0, 0.0]

        self.size = (32, 32)
        self.mass = 60.0

        # Input state
        self.actions = {
            "left": False,
            "right": False,
            "jump": False,
            "smash": False,
        }

        # Force values
        self.RUNNING_FORCE = 50000.0
        self.JUMP_FORCE = 640000.0
        self.SMASH_FORCE = 400000.0
        self.ACTION_FORCE_DURATION = 0.05
        self.MAX_RUN_SPEED = 150.0  # pixels per second
        
        self.AIR_CONTROL = 0.6      # fraction of run force available in midair
        self.move_input = 0         # -1, 0, 1: read by physics

        self.JUMP_BUFFER_TIME = 0.1   # seconds
        self.jump_buffer = 0.0

        # Player state
        self.state = "still"
        self.facing = "right"
        self.on_ground = False
        self.is_airborne = False
        self.is_smashing = False
        self.can_smash = False

        # One-shot action requests
        self.smash_requested = False

        # Animation state
        self.current_frame = 0
        self.last_frame_update = 0.0

        self.rect = pygame.Rect(
            int(self.position[0]),
            int(self.position[1]),
            self.size[0],
            self.size[1],
        )

        self.close_objects = []

        self.load()

    def update(self, physics):
        self.move_input = 0
        control = 1.0 if self.on_ground else self.AIR_CONTROL

        # No steering while smashing.
        if not self.is_smashing:
            if self.actions["left"] and not self.actions["right"]:
                self.facing = "left"
                self.move_input = -1
                physics.add_force(self, -self.RUNNING_FORCE * control, 0)

            elif self.actions["right"] and not self.actions["left"]:
                self.facing = "right"
                self.move_input = 1
                physics.add_force(self, self.RUNNING_FORCE * control, 0)
                
        # Jump
        if self.jump_buffer > 0:
            if self.on_ground:
                physics.apply_impulse(self, 0, -self.JUMP_FORCE, duration=self.ACTION_FORCE_DURATION)
                self.jump_buffer = 0.0
                self.on_ground = False
            else:
                self.jump_buffer -= physics.dt

        # Smash
        if self.smash_requested and self.is_airborne and self.can_smash:
            physics.apply_impulse(self, 0, self.SMASH_FORCE, duration=self.ACTION_FORCE_DURATION)
            self.smash_requested = False
            self.can_smash = False
            self.is_smashing = True
            self.velocity[0] = 0.0      # cancel sideways momentum

        if self.smash_requested and not self.can_smash:
            self.smash_requested = False

        physics.update(self)

        self.is_airborne = not self.on_ground

        # Pick the animation state AFTER physics, from persistent conditions.
        if self.on_ground:
            self.is_smashing = False

        if self.is_smashing:
            self.state = "smash"
        elif self.is_airborne:
            self.state = "jumping"
        elif self.move_input != 0:
            self.state = "running"
        else:
            self.state = "still"

        self.animate(physics.dt)

    
    def render(self, display):
        display.blit(self.curr_image, (round(self.position[0]), round(self.position[1])))

    def event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.actions["left"] = True

                elif event.key == pygame.K_d:
                    self.actions["right"] = True

                elif event.key == pygame.K_w:
                    # Request one jump per key press.
                    if not self.actions["jump"]:
                        self.jump_buffer = self.JUMP_BUFFER_TIME
                    self.actions["jump"] = True

                elif event.key == pygame.K_s:
                    # Request one smash per key press.
                    if not self.actions["smash"]:
                        self.smash_requested = True
                    self.actions["smash"] = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.actions["left"] = False

                elif event.key == pygame.K_d:
                    self.actions["right"] = False

                elif event.key == pygame.K_w:
                    self.actions["jump"] = False

                elif event.key == pygame.K_s:
                    self.actions["smash"] = False

    def animate(self, dt):
        if not self.game.settings.video.animation.player_animations:
            return

        key_map = {
            ("still", "right"): "still",
            ("still", "left"): "still",
            ("running", "right"): "run_right",
            ("running", "left"): "run_left",
            ("jumping", "right"): "jump_right",
            ("jumping", "left"): "jump_left",
            ("smash", "right"): "smash",
            ("smash", "left"): "smash",
        }

        sprite_key = key_map.get(
            (self.state, self.facing), "still"
        )

        new_anim_list = self.sprite_sets.get(
            sprite_key, self.sprite_sets["still"]
        )

        if new_anim_list != getattr(self, "curr_anim_list", None):
            self.curr_anim_list = new_anim_list
            self.current_frame = 0
            self.last_frame_update = 0.0

        self.last_frame_update += dt

        FRAME_DURATION = 0.15

        if self.last_frame_update >= FRAME_DURATION:
            self.last_frame_update -= FRAME_DURATION
            self.current_frame = (
                self.current_frame + 1
            ) % len(self.curr_anim_list)

        self.curr_image = self.curr_anim_list[self.current_frame]

    def load(self):
        """Load and scale Lario's sprite animations."""
        self.sprite_sets = {
            "still": [],
            "run_right": [],
            "run_left": [],
            "jump_right": [],
            "jump_left": [],
            "smash": [],
        }

        sprite_mapping = {
            "still": "still",
            "run_right": "run_right",
            "run_left": "run_left",
            "jump_right": "jump_right",
            "jump_left": "jump_left",
            "smash": "smash",
        }

        for state, folder in sprite_mapping.items():
            frames = self.get_asset("sprites", f"lario/{folder}")

            if frames:
                self.sprite_sets[state] = [pygame.transform.smoothscale(img, self.size) for img in frames]
            else:
                if self.game.settings.debug.debug_missing_files:
                    self.game.glogger.warning(f"Missing sprite asset: lario/{folder}")

                placeholder = pygame.Surface(self.size, pygame.SRCALPHA)
                placeholder.fill((255, 0, 255))
                self.sprite_sets[state] = [placeholder]

        self.curr_anim_list = self.sprite_sets["still"]
        self.curr_image = self.curr_anim_list[0]
        self.current_frame = 0
        self.last_frame_update = 0.0

    def set_close_objects(self, objects):
        self.close_objects = list(objects) if objects else []

    def set_position(self, x, y):
        self.position[0] = float(x)
        self.position[1] = float(y)
        self.rect.topleft = (round(self.position[0]), round(self.position[1]))

    def __str__(self):
        return "lario"
