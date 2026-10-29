import json
import os

from State import State
from settings.Settings import Game_Settings

class SettingsLoader(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.done = False
        self.dir_path = "config"
        self.file_path = os.path.join(self.dir_path, "settings.json")

    def update(self):
        """
        Main update loop for the loader. 
        Each method returns True on success. If a method returns False,
        we return from update to retry the same step in the next frame.
        """
        # 1. Ensure the configuration directory exists
        if not self.ensure_directory_exists():
            return 

        # 2. Attempt to load the raw data from the disk
        # Returns (Success, Data)
        success, raw_data = self.load_raw_data()
        if not success:
            return

        # 3. Parse the dictionary into a Game_Settings object
        settings_obj = self.parse_settings(raw_data)
        if not settings_obj:
            return

        # 4. Finalize and apply the settings to the main game object
        self.apply_settings(settings_obj)
        
        self.done = True
        self.exit_state(self.game.state_stack)

    def ensure_directory_exists(self):
        """Returns True if the directory exists or was successfully created."""
        if os.path.exists(self.dir_path):
            return True
        
        try:
            os.makedirs(self.dir_path)
            self.game.glogger.warning(f"Directory '{self.dir_path}' was missing. Created successfully.")
            return True
        except OSError as e:
            # If we lack permissions or disk is full, this will fail and retry next frame
            self.game.glogger.error(f"CRITICAL: OS could not create directory {self.dir_path}: {e}")
            return False

    def load_raw_data(self):
        """
        Tries to read the JSON file. 
        Returns (True, data) if file exists or is new. 
        Returns (False, None) if a read error occurs.
        """
        if not os.path.exists(self.file_path):
            # No file is not a failure, we just pass an empty dict to the parser
            return True, {} 

        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
                return True, data
        except (json.JSONDecodeError, IOError) as e:
            self.game.glogger.error(f"File Read Error: {e}. Retrying...")
            return False, None

    def parse_settings(self, data):
        """
        Converts dict data to Game_Settings object. 
        Returns the object on success, or None if creation/saving fails.
        """
        # If data is empty (file didn't exist), create and save defaults
        if not data: 
            self.game.glogger.warning("No settings file found. Creating default settings...")
            obj = Game_Settings() 
            if self.save_settings(obj): 
                return obj
            return None

        # Try to map the JSON data to our class structure
        settings_obj = Game_Settings.from_dict(data)
        if settings_obj:
            return settings_obj
        
        # If from_dict returned None (broken structure), reset to default
        self.game.glogger.error("Invalid settings format. Resetting to default...")
        default_obj = Game_Settings()
        if self.save_settings(default_obj):
            return default_obj
        return None

    def apply_settings(self, settings_obj):
        """Assigns the validated settings object to the game instance."""
        self.game.settings = settings_obj
        debug = self.game.settings.debug
        if debug.debug_loading:
            self.game.glogger.log("Settings loaded and applied to Game instance.")

    def save_settings(self, settings_obj):
        """Attempts to write the settings object to the disk. Returns True on success."""
        try:
            with open(self.file_path, "w") as f:
                json.dump(settings_obj.to_dict(), f, indent=4)
            return True
        except IOError as e:
            self.game.glogger.error(f"Disk Write Error: {e}. Check folder permissions.")
            return False