
from Physics import Physics
from State import State
from lario.Lario import Lario
from states.level.Level1 import LevelOne

class Container(State):
    #znopp
    def __init__(self, game):
        super().__init__(game)

        self.physics = Physics(game)
        self.player = Lario(game)
        
        self.levels = [
            LevelOne(game),
            # LevelTwo(game),
        ]
        self.current_level = 0

        self.player_stack = []
        self.level_stack = []

        self.load() 
    
    def load(self):
        self.player.enter_state(self.player_stack)
        self.levels[self.current_level].enter_state(self.level_stack)
        self.levels[self.current_level].spawn_player(self.player)    


    def update(self):
        level_state = self.level_stack[-1]
        player_state = self.player_stack[-1]
        level_state.update(self.physics)
        # get close objects and update player
        player_state.set_close_objects(level_state.get_close_objects(player_state))
        player_state.update(self.physics)
        
        pass

    def render(self, display):
        self.level_stack[-1].render(display)
        self.player_stack[-1].render(display)

    def event(self, events):
        self.player_stack[-1].event(events)
        

