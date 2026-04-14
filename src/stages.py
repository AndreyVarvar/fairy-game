from prismane import Stage
from .ui import StartButton



class MainMenuStage(Stage):
    def __init__(self):
        super().__init__()
        self.populate_group("ui", StartButton(z=1))



