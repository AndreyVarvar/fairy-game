from prismane import Engine

from scenes import GameplayScene

# setup
screen_size = (800, 600)
game = Engine(screen_size, "prototype")

game.populate_scenes([GameplayScene], "gameplay")

# launch
game.start()
