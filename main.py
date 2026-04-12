from prismane import Engine

# setup
screen_size = (800, 600)
game = Engine(screen_size, "prototype")

game.populate_scenes([], "gameplay")

# launch
game.start()
