

from states.Container import Container
from State import State
import pygame

class Title(State):
    def __init__(self, game):
        super().__init__(game)
        self.background = None
        self.load_background()
        self.play_music()
        self.container = Container(game)

    def update(self):
        pass

    def render(self, display):
        # We check if background exists, otherwise fill with a color
        if self.background:
            display.blit(self.background, (0, 0))
        else:
            display.fill((10, 10, 10))

    def event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.container.enter_state(self.game.state_stack)
               

    def load_background(self):
        raw_bg = self.get_single_frame("sprites", "menu/background")
        
        if raw_bg:
            # We scale the background to fit the Virtual Canvas exactly
            self.background = pygame.transform.scale(raw_bg, self.game.renderer.size)

    def play_music(self):
        music = self.get_asset("sounds", "menu/music")
        self.game.music_channel.play(music, loops=-1)
