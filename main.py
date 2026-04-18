from prismane import Engine
from src.stages import MainMenuStage, GameStage
import pygame as pg
from prismane.settings import WINDOW_SIZE

# setup
game = Engine(WINDOW_SIZE, title="prototype", flags=pg.FULLSCREEN)

game.populate_stages({"main menu": MainMenuStage, "game": GameStage}, "main menu")

# launch
game.start()
