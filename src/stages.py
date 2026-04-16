from prismane import Stage
from prismane.assets import get_image
from pathlib import Path
from prismane.settings import WINDOW_WIDTH

from .ui import FButton



class MainMenuStage(Stage):
    def __init__(self):
        super().__init__()

        start_button = FButton(pos=(WINDOW_WIDTH//2, 200), image=get_image(Path("assets/ui/start_button.png")), z=1)


        self.populate_group("ui", 
                            start_button
        )

    def draw(self):
        super().draw()
        window = self.element_tree["Engine"].window
        window.fill("white")
        self.element_tree["Renderer"].draw({"window": window})

class GameStage(Stage):
    def __init__(self):
        super().__init__()
        pass

    def draw(self):
        super().draw()
        window = self.element_tree["Engine"].window
        window.fill("blue")
