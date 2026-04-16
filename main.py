from prismane import Engine
from src.stages import MainMenuStage, GameStage
import pygame as pg

# setup
screen_size = (1920, 1080)
game = Engine(screen_size, title="prototype", flags=pg.FULLSCREEN)

game.populate_stages({"main menu": MainMenuStage, "game": GameStage}, "main menu")

# launch
game.start()
