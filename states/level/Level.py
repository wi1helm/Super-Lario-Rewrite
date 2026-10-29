from State import State
import pygame
class Level(State):
    def __init__(self, game):
        super().__init__(game)
        self.objects = pygame.sprite.Group()
        self.start_x = 50
        self.start_y = 50
        self.background = None
        self.load_assets()
        self.load_collision_geometry()
        self.on_enter()

    def on_enter(self) -> None:
        """Overwrite in subclasses for actions on level start."""
        pass
    
    def load_assets(self) -> None:
        """Override in subclasses to load level-specific assets."""
        pass

    def load_collision_geometry(self) -> list:
        """Override in subclasses to create objects."""
        pass

    def update(self, physics) -> None:
        self.objects.update(physics, self.game.settings)

    def render(self, display):
        if self.background:
            bg_scaled = pygame.transform.smoothscale(self.background, display.get_size())
            display.blit(bg_scaled, (0, 0))
        
        self.objects.draw(display)

         # 4. Debug hitboxes
        if self.game.settings.debug.show_hitboxes:
            for platform in self.platforms:
                pygame.draw.rect(display, (255, 0, 0), platform, 1)

        
    def get_close_objects(self, player):
        player_rect = player.rect.copy()
        player_rect.topleft = (
            round(player.position[0]),
            round(player.position[1]),
        )

        margin = 64
        search_rect = player_rect.inflate(margin * 2, margin * 2)

        return [
            obj for obj in self.objects
            if search_rect.colliderect(obj.rect)
        ]

    
    def distance(self, a, b, c, d):    
        return abs((a*a + b*b)**0.5 - (c*c + d*d)**0.5)

    @property
    def platforms(self):
        """Return rects of solid objects only"""
        return [obj for obj in self.objects if obj.type == "solid"]

    # Level
    def spawn_player(self, player):
        player.set_position(self.start_x, self.start_y)