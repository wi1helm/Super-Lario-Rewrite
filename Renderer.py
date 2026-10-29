import pygame

class Renderer:
    def __init__(self, game, virtual_res, window_res, flags, maintain_aspect_ratio):
        self.game = game
        self.v_w, self.v_h = virtual_res
        self.w_w, self.w_h = window_res
        self.flags = flags
        self.maintain_aspect_ratio = maintain_aspect_ratio
        
        # Core surfaces
        self.canvas = pygame.Surface((self.v_w, self.v_h))
        self.screen = pygame.display.set_mode((self.w_w, self.w_h), self.flags)
        
        # Pre-calculated scaling values
        self.render_size = (0, 0)
        self.render_pos = (0, 0)
        self.recalculate_scale()

    def recalculate_scale(self):
        """Calculates how to blit the virtual canvas onto the physical window."""
        if self.maintain_aspect_ratio:
            scale = min(self.w_w / self.v_w, self.w_h / self.v_h)
            new_width = int(self.v_w * scale)
            new_height = int(self.v_h * scale)
            self.render_size = (new_width, new_height)
            self.render_pos = ((self.w_w - new_width) // 2, (self.w_h - new_height) // 2)
        else:
            self.render_size = (self.w_w, self.w_h)
            self.render_pos = (0, 0)

    def handle_resize(self, width, height):
        """Called when the user drags the window corner."""
        self.w_w, self.w_h = width, height
        self.screen = pygame.display.set_mode((self.w_w, self.w_h), self.flags)
        self.recalculate_scale()

    def render(self, state_stack):
        """The final step of the frame: takes the canvas to the screen."""
        # 1. Clear the canvas (Internal game world)
        self.canvas.fill((0, 0, 0))
        
        # 2. Tell the top state to draw itself onto our canvas
        if state_stack:
            state_stack[-1].render(self.canvas)
        
        # 3. Clear the physical screen (Letterbox bars)
        self.screen.fill((0, 0, 0))
    
        # 4. Scale canvas and blit to screen
        scaled_surf = pygame.transform.scale(self.canvas, self.render_size)
        self.screen.blit(scaled_surf, self.render_pos)

        if self.game.settings.debug.show_fps:
            fps = self.game.clock.get_fps()
            font = pygame.font.SysFont("Arial", 18)
            fps_text = font.render(f"FPS: {int(fps)}", True, (255, 255, 255))
            self.screen.blit(fps_text, (10, 10))

        # 5. Flip
        pygame.display.flip()

    @property
    def size(self):
        return (self.v_w, self.v_h)

    @property
    def width(self):
        return self.v_w

    @property
    def height(self):
        return self.v_h
    @property
    def center(self):
        return (self.v_w // 2, self.v_h // 2)

    def get_rect(self):
        return self.canvas.get_rect()