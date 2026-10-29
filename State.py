class State():
    def __init__(self, game):
        self.game = game
        self.prev_state = None

    def update(self):
        pass
    
    def render(self, display):
        pass

    def event(self, events):
        pass

    def enter_state(self, stack):
        if len(stack) > 1:
            self.prev_state = stack[-1]
        stack.append(self)

    def exit_state(self, stack):
        stack.pop()

    def get_asset(self, category, key):
        try:
            return self.game.assets[category].get(key, None)
        except FileNotFoundError as e:
            if self.game.settings.debug.debug_missing_files:
                self.game.glogger.log(f"Asset not found - Category: {category}, Key: {key}")
            return None
        
    def get_single_frame(self, category, key):
        frames = self.get_asset(category, key)
        return frames[0] if frames and len(frames) > 0 else None

    def __str__(self):
        return "state"