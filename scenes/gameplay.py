from prismane import Scene
from prismane import MasterControlPanel

class GameplayScene(Scene):
    def __init__(self):
        super().__init__("gameplay")
    
    def update(self, master_panel):
        super().update(master_panel)

    def draw(self, surface, game_data):
        super().draw(surface, game_data)
