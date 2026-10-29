
class Physics:
    def __init__(self, game):
        self.game = game
        self.dt = 0.0

        # Acceleration due to gravity (pixels/s²).
        self.gravity = 900.0
        self.air_drag = 0.0   # try 0.5–2.0 if you want some drag; see note below

        # Force accumulators, keyed by entity.
        self.forces = {}
        self.impulses = {}

        # Short force durations used for jump/smash.
        self.impulse_duration = 0.05



    def update(self, entity):
        self.get_dt()

        if entity.mass <= 0 or self.dt <= 0:
            return

        key = str(entity)

        # Consume forces requested by the entity this frame.
        fx, fy = self.forces.pop(key, (0.0, 0.0))

        # Gravity.
        fy += entity.mass * self.gravity

        # Convert time-limited forces into the average force
        # acting during this frame.
        pending = self.impulses.get(key, [])
        remaining = []

        for ix, iy, time_left in pending:
            duration = min(self.dt, time_left)

            fx += ix * duration / self.dt
            fy += iy * duration / self.dt

            time_left -= duration

            if time_left > 1e-9:
                remaining.append((ix, iy, time_left))

        if remaining:
            self.impulses[key] = remaining
        else:
            self.impulses.pop(key, None)

        # Apply friction directly to the current frame's force,
        # rather than queuing it for the next frame.
        vx = entity.velocity[0]

        if entity.on_ground:
            # Friction only when not pushing, or when pushing against current motion.
            pushing_with_motion = entity.move_input != 0 and entity.move_input * vx > 0

            if not pushing_with_motion and abs(vx) > 1e-6:
                coefficient = max(
                    (
                        max(0.0, obj.friction)
                        for obj in entity.close_objects
                        if obj.type == "solid"
                        and entity.rect.bottom <= obj.rect.top + 2
                        and entity.rect.right > obj.rect.left
                        and entity.rect.left < obj.rect.right
                    ),
                    default=0.0,
                )

                friction_force = min(
                    entity.mass * coefficient,
                    entity.mass * abs(vx) / self.dt,   # never reverse direction
                )
                fx -= (1 if vx > 0 else -1) * friction_force
        else:
            # Optional light air drag (linear)
            fx -= entity.mass * self.air_drag * vx
        
        
        # Newton's second law.
        entity.acceleration[0] = fx / entity.mass
        entity.acceleration[1] = fy / entity.mass

        # Integrate velocity.
        entity.velocity[0] += entity.acceleration[0] * self.dt
        entity.velocity[1] += entity.acceleration[1] * self.dt

        # Clamp horizontal speed.
        entity.velocity[0] = max(-entity.MAX_RUN_SPEED, min(entity.velocity[0], entity.MAX_RUN_SPEED))

        # Resolve movement and collisions.
        self.check_collisions(entity, entity.close_objects)

        if self.game.settings.debug.debug_player:
            self.game.glogger.log(f"Force: ({fx:.2f}, {fy:.2f})")
            self.game.glogger.log(f"Acceleration: {entity.acceleration}")
            self.game.glogger.log(f"Velocity: {entity.velocity}")
            self.game.glogger.log(f"Position: {entity.position}")

    
    def add_force(self, entity, fx, fy):
        """Apply force for the current physics frame."""
        key = str(entity)
        old_fx, old_fy = self.forces.get(key, (0.0, 0.0))
        self.forces[key] = (old_fx + fx, old_fy + fy)

    def apply_impulse(self, entity, fx, fy, duration=None):
        """Apply a force for a short, defined duration."""
        if duration is None:
            duration = self.impulse_duration

        if duration <= 0:
            return

        key = str(entity)
        self.impulses.setdefault(key, []).append(
            (float(fx), float(fy), float(duration))
        )


    def check_collisions(self, entity, objects):
        rect = entity.rect
        solids = [obj for obj in objects if obj.type == "solid"]

        # --- Horizontal movement ---
        new_x = entity.position[0] + entity.velocity[0] * self.dt
        rect.x = round(new_x)

        for obj in solids:
            if rect.colliderect(obj.rect):
                if entity.velocity[0] > 0:
                    rect.right = obj.rect.left
                    new_x = float(rect.x)
                    entity.velocity[0] = 0.0
                elif entity.velocity[0] < 0:
                    rect.left = obj.rect.right
                    new_x = float(rect.x)
                    entity.velocity[0] = 0.0

        entity.position[0] = new_x

        # --- Vertical movement ---
        old_y = entity.position[1]
        old_bottom = old_y + rect.height
        new_y = old_y + entity.velocity[1] * self.dt

        rect.y = round(new_y)
        entity.on_ground = False

        for obj in solids:
            horizontal_overlap = (
                rect.right > obj.rect.left
                and rect.left < obj.rect.right
            )

            if not horizontal_overlap:
                continue

            # Landing on a platform while moving downward.
            if entity.velocity[1] >= 0:
                new_bottom = new_y + rect.height

                if old_bottom <= obj.rect.top and new_bottom >= obj.rect.top:
                    new_y = float(obj.rect.top - rect.height)
                    rect.y = round(new_y)
                    entity.velocity[1] = 0.0
                    entity.on_ground = True
                    entity.can_smash = True

            # Hitting the underside of a platform.
            elif entity.velocity[1] < 0 and rect.colliderect(obj.rect):
                rect.top = obj.rect.bottom
                new_y = float(rect.y)
                entity.velocity[1] = 0.0

        entity.position[1] = new_y
        rect.y = round(new_y)

    
    def get_dt(self):
        raw_dt = (self.game.clock.tick(self.game.settings.video.framerate) / 1000.0)
        self.dt = min(raw_dt, 0.05)

        if (raw_dt > 1.0 / self.game.settings.video.framerate and self.game.settings.debug.debug_fps):
            self.game.glogger.warning(
                f"FRAME SPIKE dt={raw_dt:.4f}s "
                f"({1 / raw_dt:.1f} FPS)"
            )
