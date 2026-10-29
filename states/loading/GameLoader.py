import json
from State import State
from states.loading.MixerLoader import MixerLoader
from states.loading.SettingsLoader import SettingsLoader
from states.loading.GraphicsLoader import GraphicsLoader
from states.loading.AssetsLoader import AssetsLoader
import os

from states.Title import Title

class GameLoader(State):
    def __init__(self, game):
        State.__init__(self, game)

        self.settings = SettingsLoader(self.game)
        self.video = GraphicsLoader(self.game)
        self.assets = AssetsLoader(self.game)
        self.mixer = MixerLoader(self.game)

    def update(self):
        for state in [self.settings, self.video, self.assets, self.mixer]:
            if not state.done:    
                state.enter_state(self.game.state_stack)
                break
        else:
            self.game.glogger.log("--- Game Loading Complete ---")
            Title(self.game).enter_state(self.game.state_stack)
            
