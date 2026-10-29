import os, pygame
from State import State

class AssetsLoader(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.done = False
        self.base_dir = "assets"
        self.required_categories = ["sprites", "sounds", "font"]
        self.tasks = []
        self.current_task_idx = 0
        self.initialized = False
        self.game.assets = {}
        
        # We need a temporary font to show text while loading
        # Using SysFont ensures we have something before our assets are ready
        self.temp_font = pygame.font.SysFont("Arial", 18)

    def update(self):
        # 1. Initialize
        if not self.initialized:
            if not self.startup_check():
                self.game.glogger.error("FATAL: Asset directory structure is broken.")
                self.game.running = False 
                return
            
            for cat in self.required_categories:
                self.game.assets[cat] = {}

            self.tasks = self.generate_tasks()
            self.initialized = True
            return

        # 2. Check if finished
        if self.current_task_idx >= len(self.tasks):
            if self.game.settings.debug.debug_loading:
                self.game.glogger.log("--- All Assets Loaded ---")
            self.done = True
            self.exit_state(self.game.state_stack)
            return

        # 3. Load one asset
        load_func, path, key, category = self.tasks[self.current_task_idx]
        load_func(path, key, category)
        
        if self.game.settings.debug.debug_loading:
            self.game.glogger.log(f"Loaded {category}: {key}")

        self.current_task_idx += 1

    def startup_check(self):
        if not os.path.exists(self.base_dir):
            self.game.glogger.error(f"Missing: {os.path.abspath(self.base_dir)}")
            return False
        for folder in self.required_categories:
            path = os.path.join(self.base_dir, folder)
            if not os.path.exists(path):
                self.game.glogger.error(f"Missing: {os.path.abspath(path)}")
                return False
        return True
    
    def generate_tasks(self):
        task_list = []
        loader_map = {"sprites": self.load_sprite, "sounds": self.load_sound, "font": self.load_font}
        for cat in self.required_categories:
            cat_path = os.path.join(self.base_dir, cat)
            for root, _, files in os.walk(cat_path):
                for file in files:
                    rel_path = os.path.relpath(os.path.join(root, file), cat_path)
                    key = os.path.splitext(rel_path)[0]
                    key = key.replace(os.sep, '/')

                    # Remove trailing frame numbers
                    key = key.rsplit('/', 1)[0] if key.split('/')[-1].isdigit() else key
                    task_list.append((loader_map[cat], os.path.join(root, file), key, cat))
        return task_list

    def load_sprite(self, path, key, cat):
        try:
            img = pygame.image.load(path).convert_alpha()

            # If key already exists, append (animation frame)
            if key in self.game.assets[cat]:
                self.game.assets[cat][key].append(img)
            else:
                self.game.assets[cat][key] = [img]

        except Exception as e:
            self.game.glogger.error(f"Failed loading sprite {key}: {e}")


    def load_sound(self, path, key, cat):
        if not path.endswith(('.mp3', '.wav', '.ogg')): return
        try: self.game.assets[cat][key] = pygame.mixer.Sound(path)
        except: pass

    def load_font(self, path, key, cat):
        self.game.assets[cat][key] = path
    def render(self, display):
        # 'display' is the self.game.renderer.canvas
        if not self.tasks or not self.game.renderer: 
            return
            
        # Clear the internal canvas
        display.fill((20, 20, 20)) 
        
        progress = self.current_task_idx / len(self.tasks)
        
        # Use Renderer shortcuts for centering
        # No need to store v_w or v_h in local variables
        width, height = self.game.renderer.width // 2, 24
        x = (self.game.renderer.width - width) // 2
        y = (self.game.renderer.height - height) // 2
        
        # 1. Draw Loading Text
        if self.current_task_idx < len(self.tasks):
            _, _, key, cat = self.tasks[self.current_task_idx]
            text_surf = self.temp_font.render(f"Loading {cat}: {key}...", True, (200, 200, 200))
            text_rect = text_surf.get_rect(center=(self.game.renderer.center[0], y - 20))
            display.blit(text_surf, text_rect)

        # 2. Draw Progress Bar Background
        pygame.draw.rect(display, (255, 255, 255), (x, y, width, height), 2)
        
        # 3. Draw Progress Fill
        fill_width = int((width - 4) * progress)
        if fill_width > 0:
            pygame.draw.rect(display, (50, 200, 50), (x + 2, y + 2, fill_width, height - 4))