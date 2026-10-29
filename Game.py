import pygame
from states.loading.GameLoader import GameLoader
from utils.Glogger import Glogger
class Game:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()    
        # Set process to be running
        self.running = True
        self.renderer = None
        self.settings = None
        # Create state stack
        self.state_stack = []
        # Create Glogger
        self.glogger = Glogger(2)
        # Load States
        self.load()

    def load(self):
        GameLoader(self).enter_state(self.state_stack)
        
    def update(self):
        self.state_stack[-1].update()

        self.glogger.flush()

    def render(self):
        if not self.renderer or not self.settings:
            return
        self.renderer.render(self.state_stack)

    def event(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            
            # Delegate resize to the renderer object
            if event.type == pygame.VIDEORESIZE and self.renderer:
                self.renderer.handle_resize(event.w, event.h)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        self.state_stack[-1].event(events)

if __name__ == "__main__":
    g = Game()
    while g.running:
        g.event()
        g.update()
        g.render()

    g.glogger.log("Shutting down game.")
    g.glogger.flush_all()