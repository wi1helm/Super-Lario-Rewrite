import pygame
from State import State

class MixerLoader(State):
    def __init__(self, game):
        State.__init__(self, game)
        
        self.done = False
    
    def update(self):
        debug = self.game.settings.debug
        self.audio = self.game.settings.audio

        self.load_mixer()
        self.load_volume()

        if debug.debug_loading:
            self.game.glogger.log("Mixer prepared.")

        self.done = True
        self.exit_state(self.game.state_stack)

    def load_mixer(self):
        pygame.mixer.init()
        pygame.mixer.set_reserved(4) # Reserve channels for SFX
        self.game.player_channel = pygame.mixer.Channel(1)  # Dedicated audio channel for Player
        self.game.level_channel = pygame.mixer.Channel(2)  # Dedicated audio channel for Level
        self.game.music_channel = pygame.mixer.Channel(3)  # Dedicated audio channel for Music
        self.game.enemy_channel = pygame.mixer.Channel(4)  # Dedicated audio channel for Enemies
        self.load_volume()
    def load_volume(self):
        self.game.player_channel.set_volume(self.audio.player_volume * self.game.settings.audio.master_volume)
        self.game.level_channel.set_volume(self.audio.level_volume * self.game.settings.audio.master_volume)
        self.game.music_channel.set_volume(self.audio.music_volume * self.game.settings.audio.master_volume)
        self.game.enemy_channel.set_volume(self.audio.enemy_volume * self.game.settings.audio.master_volume)