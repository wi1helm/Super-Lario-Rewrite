import pygame
from State import State
from Renderer import Renderer

class GraphicsLoader(State):
    def __init__(self, game):
        State.__init__(self, game)
        
        self.done = False
    
    def update(self):
        debug = self.game.settings.debug
        video = self.game.settings.video

        resolution, flags = video.get_display_setup()

        # Create the Renderer object and attach it to the game
        self.game.renderer = Renderer(
            self.game,
            video.virtual_resolution,
            resolution,
            flags,
            video.maintain_aspect_ratio
        )

        if debug.debug_loading:
            self.game.glogger.log("Graphics settings loaded and prepared.")

        self.done = True
        self.exit_state(self.game.state_stack)
