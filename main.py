from prismane import Engine
from src.stages import MainMenuStage, GameStage
import pygame as pg

# setup
# 2880, 1620
# 1920, 1080
game = Engine(window_size=(2880, 1620), title="prototype", flags=pg.FULLSCREEN|pg.RESIZABLE)

game.populate_stages({"main menu": MainMenuStage, "game": GameStage}, "main menu")

# launch
game.start()
