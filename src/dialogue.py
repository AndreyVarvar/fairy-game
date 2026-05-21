from prismane import Entity

from pathlib import Path
import json
import pygame as pg

from prismane.assets import AssetLoader
from prismane.panels import InputControlPanel
from prismane.settings import Settings


class DialogueBox(Entity):
    def __init__(self, dialogue_json_path: Path):
        super().__init__()
        
        with open(dialogue_json_path, "r") as file:
            self.dialogue = json.load(file)

        asset_loader: AssetLoader = self.element_tree["AssetLoader"]

        self.dialogue_box = asset_loader.get_image(Path("./assets/ui/dialogue_box.png"))

        self.current_dialogue = "1"

        self.font = pg.font.SysFont("arial", 50)

        settings: Settings = self.element_tree["Settings"]
        rect = self.dialogue_box.get_rect(midbottom=pg.Vector2(settings.window_width//2, settings.window_height-100))
        self.pos = pg.Vector2(rect.topleft)

        self.z = 10

    def update(self):
        super().update()

        input_panel: InputControlPanel = self.element_tree["InputControlPanel"]
        
 
    def draw(self):
        self.element_tree["Renderer"].queue_draw(self.dialogue_box, self.z, self.target, self.pos + self.draw_offset)

        text = self.dialogue[self.current_dialogue]["text"]
        self.element_tree["Renderer"].queue_draw(self.font.render(text, True, (255, 255, 255)), self.z+1, self.target, self.pos + self.draw_offset + pg.Vector2(50, 100))

        




