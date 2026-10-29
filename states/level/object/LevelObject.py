import pygame
class LevelObject(pygame.sprite.Sprite):
    FRAME_TIME = 0.15

    def __init__(self, x, y, width, height, frames, obj_type="solid",
                 repeat_x=False, repeat_y=False, friction=0.0):
        super().__init__()

        self.type = obj_type
        self.friction = friction

        # Frames list (always a list, even if single frame)
        self.frames = self._scale_frames(frames, width, height)
        self.frame_index = 0
        self.timer = 0.0

        # Optional tiling
        if repeat_x or repeat_y:
            self.frames = [self._tile_surface(self.frames[0], width, height)]

        # Sprite basics
        self.image = self.frames[0]
        self.rect = pygame.Rect(x, y, width, height)
        
    # -----------------------
    # Frame scaling helper
    # -----------------------
    def _scale_frames(self, frames, width, height):
        if not frames:
            placeholder = pygame.Surface((width, height), pygame.SRCALPHA)
            placeholder.fill((255, 0, 255))
            return [placeholder]
        return [pygame.transform.smoothscale(f, (width, height)) for f in frames]

    # -----------------------
    # Tiling helper
    # -----------------------
    def _tile_surface(self, img, w, h):
        tile_w, tile_h = img.get_size()
        surface = pygame.Surface((w, h), pygame.SRCALPHA)
        for x in range(0, w, tile_w):
            for y in range(0, h, tile_h):
                surface.blit(img, (x, y))
        return surface

    # -----------------------
    # Logic update (physics / movement)
    # -----------------------
    def update(self, physics, settings):
        self.animate(physics.dt, settings)
        # Handle movement, friction, collisions, etc.
        # For now just a placeholder
        pass

    # -----------------------
    # Animation update
    # -----------------------
    def animate(self, dt, settings):
        if not settings.video.animation.world_animations:
            return

        if len(self.frames) > 1:
            self.timer += dt
            if self.timer >= self.FRAME_TIME:
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.image = self.frames[self.frame_index]
                self.timer = 0
