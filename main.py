# /// script
# dependencies = [
#  "pygame-ce",
# ]
# ///

from prismane import Engine
from src.stages import MainMenuStage, GameStage

# setup
game = Engine(window_size=(2880, 1620), logical_size=(1920, 1080), title="prototype", fullscreen=True)

game.populate_stages({"main menu": MainMenuStage, "game": GameStage}, "main menu")

# launch
game.start()
