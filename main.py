from prismane import Engine
from src.stages import MainMenuStage, GameStage
import pygame as pg

# setup
game = Engine(window_size=(2880, 1620), logical_size=(2880, 1620), title="prototype")

game.populate_stages({"main menu": MainMenuStage, "game": GameStage}, "main menu")

# launch
game.start()
