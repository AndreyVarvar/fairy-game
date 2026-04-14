from prismane import Engine
from src.stages import MainMenuStage

# setup
screen_size = (800, 600)
game = Engine(screen_size, title="prototype")

game.populate_scenes({"main menu": MainMenuStage}, "main menu")

# launch
game.start()
