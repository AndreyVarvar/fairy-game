from prismane import Spritesheet, EntityGroup
from prismane.camera import Camera

from .level import Level
from .background import Background
from .level_entities import LightPole, Tile, Mushroom, Spike, Gnome, Oleni, Butterfly
from .player import Player

from pathlib import Path
import pygame as pg


class Level1(Level):
    def __init__(self) -> None:
        super().__init__(pg.Vector2(144, 1169))
        w, h = 115, 75  # tile width and tile height, shortened for conveniece in the monstrocity you see below (yes, it was manually written. Every single entry. Every single tile. You could say it woul've been better to write a script to do that for me, but I am too lazy to write the autotiler, and even though it would've taken me 30 minutes I'd rather spend the next 2 hours manually writing everyghing down)
        tileset = Spritesheet(Path("./assets/tiles/pink.json"))
        tile_hitbox = pg.FRect(0, 51, 115, 75)

        self.camera = Camera("MainCamura", 0, 0, 0, 0)
        self.camera.bounds = pg.FRect(-2*w - 40, 0, w * 57, h * 60 + 40)

        self.events = []

        self.groups: dict[str, EntityGroup] = {
            "tiles": EntityGroup(
                Tile(pg.Vector2(-1*w, 3*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(0*w, 3*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(-1*w, 9*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(0*w, 9*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(1*w, 9*h), tileset["top-right"], tile_hitbox),
                Tile(pg.Vector2(-1*w, 10*h+tile_hitbox.y), tileset["bottom-left"]),
                Tile(pg.Vector2(0*w, 10*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(1*w, 10*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(0*w, 11*h+tile_hitbox.y), tileset["bottom-left"]),
                Tile(pg.Vector2(1*w, 11*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(2*w, 11*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(4*w, 7*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(5*w, 7*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(6*w, 7*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(7*w, 7*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(8*w, 7*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(9*w, 5*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(10*w, 5*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(11*w, 5*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(13*w, 5*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(14*w, 5*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(15*w, 5*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(16*w, 5*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(18*w, 7*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(19*w, 7*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(20*w, 7*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(22*w, 6*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(23*w, 6*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(25*w, 5*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(26*w, 5*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(15*w, 10*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(16*w, 10*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(24*w, 11*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(25*w, 11*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(26*w, 11*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(27*w, 11*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(4*w, 17*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(5*w, 17*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(10*w, 15*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(11*w, 15*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(12*w, 15*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(17*w, 17*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(18*w, 17*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(19*w, 17*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(20*w, 17*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(21*w, 17*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(22*w, 17*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(1*w, 18*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(2*w, 18*h), tileset["top-right"], tile_hitbox),
                Tile(pg.Vector2(1*w, 19*h+tile_hitbox.y), tileset["bottom-left"]),
                Tile(pg.Vector2(2*w, 19*h+tile_hitbox.y), tileset["bottom-right"]),
                
                Tile(pg.Vector2(7*w, 17*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(8*w, 17*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(9*w, 17*h), tileset["top-right"], tile_hitbox),
                Tile(pg.Vector2(7*w, 18*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(8*w, 18*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(9*w, 18*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(7*w, 19*h+tile_hitbox.y), tileset["bottom-left"]),
                Tile(pg.Vector2(8*w, 19*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(9*w, 19*h+tile_hitbox.y), tileset["bottom-right"]),
                
                Tile(pg.Vector2(12*w, 17*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(13*w, 17*h), tileset["top-right"], tile_hitbox),
                Tile(pg.Vector2(13*w, 18*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(14*w, 18*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(15*w, 18*h), tileset["top-right"], tile_hitbox),
                Tile(pg.Vector2(13*w, 19*h+tile_hitbox.y), tileset["bottom-left"]),
                Tile(pg.Vector2(14*w, 19*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(15*w, 19*h+tile_hitbox.y), tileset["bottom-right"]),
                
                Tile(pg.Vector2(24*w, 18*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(25*w, 18*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(26*w, 18*h), tileset["top-right"], tile_hitbox),
                Tile(pg.Vector2(24*w, 19*h+tile_hitbox.y), tileset["bottom-left"]),
                Tile(pg.Vector2(25*w, 19*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(26*w, 19*h+tile_hitbox.y), tileset["bottom-right"])
            ),
            "mushrooms": EntityGroup(
                # MUSHROOMs
                Mushroom(pg.Vector2(4*w, 6*h+10)),
                Mushroom(pg.Vector2(4*w, 16*h+10)),
                Mushroom(pg.Vector2(11.75*w, 14*h+10)),
            ),
            "spikes": EntityGroup(
                # Spikes
                Spike(pg.Vector2(11*w+40, 4*h+50)),
                Spike(pg.Vector2(18*w+40, 6*h+50)),
                Spike(pg.Vector2(11*w+40, 14*h+50)),
            ),
            "butterflies": EntityGroup(
                # Butterflies
                Butterfly(pg.Vector2(-1*w-10, 2*h-50), orientation="right"),
                Butterfly(pg.Vector2(26*w-10, 4*h-50), orientation="left"),
                Butterfly(pg.Vector2(16*w-10, 9*h-50), orientation="left"),
            ),
            "olenis": EntityGroup(
                # Oleni
                Oleni(pg.Vector2(18*w, 14*h)),
            ),
            "gnomes": EntityGroup(
                Gnome(pg.Vector2(8*w-40, 6*h-30))
            ),
            "light poles": EntityGroup(
                LightPole(pg.Vector2(24*w, 14*h))
            )
        }

        asset_loader = self.element_tree["AssetLoader"]

        self.singletons = {
            "background": Background(asset_loader.get_image(Path("./assets/backgrounds/pink.png"))),
            "player": Player(self.player_start_pos)
        }
        
        self.camera.target = self.singletons["player"]
        
        self.dialogue_termination_event = None

    def reset(self):
        self.__init__()

    def update(self):
        super().update()
        self.camera.follow_target()
        if self.singletons["player"].health <= 0:
            self.reset()

class Level2(Level):
    def __init__(self) -> None:
        super().__init__(pg.Vector2(11, 946))
        self.camera = Camera("MainCamura", 0, 0, 0, 0)
        
        w, h = 115, 75  # tile width and tile height, shortened for conveniece in the monstrocity you see below (yes, it was manually written. Every single entry. Every single tile. You could say it woul've been better to write a script to do that for me, but I am too lazy to write the autotiler, and even though it would've taken me 30 minutes I'd rather spend the next 2 hours manually writing everyghing down)
        tileset = Spritesheet(Path("./assets/tiles/green.json"))
        tile_hitbox = pg.FRect(0, 53, 115, 75)

        self.events = []

        self.groups: dict[str, EntityGroup] = {
            "tiles": EntityGroup(
                Tile(pg.Vector2(0*w, 1*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(1*w, 1*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(2*w, 1*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(3*w, 1*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(6*w, 0*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(7*w, 0*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(9*w, 0*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(10*w, 0*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(11*w, 0*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(12*w, 0*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(2*w, 4*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(3*w, 4*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(4*w, 4*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(1*w, 8*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(2*w, 8*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(7*w, 7*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(8*w, 7*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(9*w, 7*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(10*w, 7*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(12*w, 6*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(13*w, 6*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(14*w, 6*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(16*w, 7*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(17*w, 7*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(18*w, 5*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(19*w, 5*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(20*w, 5*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(21*w, 5*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(22*w, 3*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(23*w, 3*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(24*w, 3*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(3*w, 10*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(4*w, 10*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(5*w, 10*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(24*w, 9*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(25*w, 9*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(26*w, 9*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(27*w, 9*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(7*w, 13*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(8*w, 13*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(0*w, 15*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(1*w, 15*h), tileset["top-right"], tile_hitbox),
                Tile(pg.Vector2(0*w, 16*h+tile_hitbox.y), tileset["bottom-left"]),
                Tile(pg.Vector2(1*w, 16*h+tile_hitbox.y), tileset["bottom-right"]),
                
                Tile(pg.Vector2(3*w, 16*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(4*w, 16*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(5*w, 16*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(6*w, 16*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(7*w, 16*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(9*w, 15*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(10*w, 15*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(11*w, 15*h), tileset["top-right"], tile_hitbox),
                Tile(pg.Vector2(9*w, 16*h+tile_hitbox.y), tileset["bottom-left"]),
                Tile(pg.Vector2(10*w, 16*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(11*w, 16*h+tile_hitbox.y), tileset["bottom-right"]),
                
                Tile(pg.Vector2(13*w, 14*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(14*w, 14*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(15*w, 14*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(16*w, 14*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(17*w, 14*h), tileset["top-middle 2"], tile_hitbox),
                Tile(pg.Vector2(18*w, 14*h), tileset["top-right"], tile_hitbox),
                
                Tile(pg.Vector2(20*w, 15*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(21*w, 15*h), tileset["top-right"], tile_hitbox),
                Tile(pg.Vector2(20*w, 16*h+tile_hitbox.y), tileset["bottom-left"]),
                Tile(pg.Vector2(21*w, 16*h+tile_hitbox.y), tileset["bottom-right"]),
                
                Tile(pg.Vector2(23*w, 14*h), tileset["top-left"], tile_hitbox),
                Tile(pg.Vector2(24*w, 14*h), tileset["top-middle 1"], tile_hitbox),
                Tile(pg.Vector2(25*w, 14*h), tileset["top-right"], tile_hitbox),
                Tile(pg.Vector2(23*w, 15*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(24*w, 15*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(25*w, 15*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(23*w, 16*h+tile_hitbox.y), tileset["bottom-left"]),
                Tile(pg.Vector2(24*w, 16*h+tile_hitbox.y), tileset["middle"]),
                Tile(pg.Vector2(25*w, 16*h+tile_hitbox.y), tileset["bottom-right"]),
            ),
            "mushrooms": EntityGroup(
                # MUSHROOMs
            ),
            "spikes": EntityGroup(
                # Spikes
            ),
            "olenis": EntityGroup(
                # Oleni
                Oleni(pg.Vector2(18*w, 14*h)),
            )
        }

        asset_loader = self.element_tree["AssetLoader"]

        self.singletons = {
            "background": Background(asset_loader.get_image(Path("./assets/backgrounds/pink.png"))),
            "player": Player(self.player_start_pos)
        }
        
        self.camera.target = self.singletons["player"]


    def update(self):
        super().update()
        self.camera.follow_target()
        if self.singletons["player"].health <= 0:
            self.reset()


