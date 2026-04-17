from prismane import Engine
from src.stages import MainMenuStage, GameStage
import pygame as pg
from prismane.settings import WINDOW_SIZE

# setup
game = Engine()

game.create_window(
    title="prototype",
    size=WINDOW_SIZE,
    fullscreen_desktop=True
)
game.populate_stages({"main menu": MainMenuStage, "game": GameStage}, "main menu")

# launch
game.start()
