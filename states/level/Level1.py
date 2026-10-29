import pygame
from states.level.Level import Level
from states.level.object.LevelObject import LevelObject
class LevelOne(Level):
    def __init__(self, game):
        super().__init__(game)

        self.start_x = 50
        self.start_y = 550
    
    def load_assets(self):
        """Load level-specific assets here."""
        # Single-frame backgrounds
        self.background = self.get_single_frame("sprites", "levels/level1/background")
        # Multi-frame objects (like bricks or lava)
        self.brick_frames = self.get_asset("sprites", "levels/level1/brick") or []
        self.lava_frames = self.get_asset("sprites", "levels/level1/lava") or []
        self.pipe_body_frames = self.get_asset("sprites", "levels/pipe_up") or []
        self.pipe_top_frames = self.get_asset("sprites", "levels/pipe_end_up") or []

    def load_collision_geometry(self):
        """Create collidable objects using a simple grid layout."""
        tile_width = 32
        tile_height = 32

        # How many map rows/columns sit outside the visible area
        # (above / left of the screen).
        rows_offscreen_top = 6
        cols_offscreen_left = 1

        level_map = [
            "0ooooooooooooooooooooooooo0",
            "0ooooooooooooooooooooooooo0",
            "0ooooooooooooooooooooooooo0",
            "0ooooooooooooooooooooooooo0",
            "0ooooooooooooooooooooooooo0",
            "0ooooooooooooooooooooooooo0",
            "0ooooooooooooooooooooooooo0",
            "0ooooooooooooooooooooooooo0",
            "0ooxxxxoooxxoooxoooooxxooo0",
            "0ooooooooooooooxoooooooxoo0",
            "0ooooooooooooooxoooooooooo0",
            "0Toooooooooooooooooooooooo0",
            "0pooooooooooooooooooooooox0",
            "0poooooooooooooxooooooooox0",
            "0poooooooooooooxooooooooox0",
            "0pooooooooxxxooxooooooooxx0",
            "0poxxxoooooooooxoooooooooo0",
            "0poooooooooooooxoooxxooooo0",
            "0poooooooooooooxoooooooooo0",
            "0poooooooooooooooooooooooo0",
            "0xxxxxxxoooooooooooooooooo0",
            "0xoooooxooxxoooooooooooooo0",
            "0xoooooxoooooooooooooooooo0",
            "0xooooooooooooxooooooooooo0",
            "0xooooooooooooxlllllllllll0",
            "0xxxxxxxxxllxxxxxxxxxxxxxx0",
            "000000000000000000000000000",
        ]

        offset_x = cols_offscreen_left * tile_width
        offset_y = rows_offscreen_top * tile_height

        for row_idx, row in enumerate(level_map):
            for col_idx, cell in enumerate(row):
                x = col_idx * tile_width - offset_x
                y = row_idx * tile_height - offset_y
                if cell == 'o':
                    obj = LevelObject(
                        x=x, y=y,
                        width=tile_width, height=tile_height,
                        frames=[pygame.Surface((tile_width, tile_height), pygame.SRCALPHA)],
                        obj_type="air",
                        friction=100.0
                    )
                    self.objects.add(obj)

                if cell == 'x':
                    obj = LevelObject(
                        x=x, y=y,
                        width=tile_width, height=tile_height,
                        frames=self.brick_frames,
                        obj_type="solid",
                        friction=1000.0
                    )
                    self.objects.add(obj)

                elif cell == 'l':
                    obj = LevelObject(
                        x=x, y=y,
                        width=tile_width, height=tile_height,
                        frames=self.lava_frames,
                        obj_type="lava"
                    )
                    self.objects.add(obj)

                elif cell == '0':
                    # Invisible solid
                    obj = LevelObject(
                        x=x, y=y,
                        width=tile_width, height=tile_height,
                        frames=[pygame.Surface((tile_width, tile_height), pygame.SRCALPHA)],
                        obj_type="solid"
                    )
                    self.objects.add(obj)
                elif cell == 'T':
                    obj = LevelObject(
                        x=x, y=y,
                        width=tile_width, height=tile_height,
                        frames=self.pipe_top_frames,
                        obj_type="solid",
                        friction=1000.0
                    )
                    self.objects.add(obj)

                elif cell == 'p':
                    obj = LevelObject(
                        x=x, y=y,
                        width=tile_width, height=tile_height,
                        frames=self.pipe_body_frames,
                        obj_type="solid",
                        friction=1000.0
                    )
                    self.objects.add(obj)
