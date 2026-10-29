import pygame

class Video_Settings:
    """Simplified display settings."""
    def __init__(self):
        self.framerate = 60
        self.virtual_resolution = (800, 640)

        info = pygame.display.Info()
        self.native_resolution = (info.current_w, info.current_h)

        # Options: 'FULLSCREEN', 'NATIVE', 'FIXED'
        self.display_mode = 'FIXED'
        self.fixed_resolution = (960, 540)
        self.maintain_aspect_ratio = False
        self.animation = Animation_Settings()

    def get_display_setup(self):
        """Return (width, height, flags) based on mode."""
        if self.display_mode == 'FULLSCREEN':
            width, height = self.native_resolution
            flags = pygame.FULLSCREEN
        elif self.display_mode == 'NATIVE':
            # Windowed but maximized, leave space for title bar
            border_offset = 60  # Approximate OS title bar height
            width = self.native_resolution[0]
            height = self.native_resolution[1] - border_offset
            flags = pygame.RESIZABLE
        else:  # FIXED
            width, height = self.fixed_resolution
            flags = pygame.RESIZABLE

        return (width, height), flags

class Animation_Settings:
    def __init__(self):
        self.player_animations = True
        self.world_animations = True

class Audio_Settings:
    def __init__(self):
        self.master_volume = 0.5
        self.music_volume = 0.5
        self.player_volume = 0.5
        self.level_volume = 0.5
        self.enemy_volume = 0.5

# --- GAME SETTINGS ---
class Debug_Settings:
    def __init__(self):
        self.show_hitboxes = False
        self.show_fps = True
        self.god_mode = False
        self.debug_loading = False
        self.debug_player = True
        self.debug_fps = True
        self.debug_missing_files = False

class Game_Settings:
    def __init__(self, video=None, debug=None, audio=None):
        # Om inget skickas in, använd default-objekt
        self.video = video if video else Video_Settings()
        self.debug = debug if debug else Debug_Settings()
        self.audio = audio if audio else Audio_Settings()

    def to_dict(self):
        """Konverterar objektet till en dictionary för JSON."""
        return {
            "video": {k: v for k, v in self.video.__dict__.items() if k != 'animation'},
            "animation": self.video.animation.__dict__,
            "debug": self.debug.__dict__,
            "audio": self.audio.__dict__
        }

    @classmethod
    def from_dict(cls, data):
        """Skapar ett Game_Settings-objekt från en dictionary."""
        settings = cls()
        try:
            settings.video.__dict__.update(data.get("video", {}))
            settings.video.animation.__dict__.update(data.get("animation", {}))
            settings.debug.__dict__.update(data.get("debug", {}))
            settings.audio.__dict__.update(data.get("audio", {}))
            return settings
        except Exception:
            return None # Indikerar att datan var trasig