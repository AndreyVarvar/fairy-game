from prismane import Entity

from pathlib import Path
import json
import pygame as pg

from prismane.assets import AssetLoader
from prismane.panels import InputControlPanel
from prismane.settings import Settings
from prismane.renderer import Renderer


class DialogueBox(Entity):
    def __init__(self, dialogue_json_path: Path):
        super().__init__()
        
        with open(dialogue_json_path, "r") as file:
            self.dialogue = json.load(file)

        asset_loader: AssetLoader = self.element_tree["AssetLoader"]

        self.dialogue_box = asset_loader.get_image(Path("./assets/ui/dialogue_box.png"))

        self.current_dialogue = "1"

        self.font = pg.font.SysFont("comic sans", 30)

        settings: Settings = self.element_tree["Settings"]
        rect = self.dialogue_box.get_rect(midbottom=pg.Vector2(settings.window_width//2, settings.window_height-100))
        self.pos = pg.Vector2(rect.topleft)

        self.end = False

        self.z = 10

        self.selected_option = 0

        self.text_color = pg.Color(107, 67, 130)

    def update(self):
        super().update()

        input_panel: InputControlPanel = self.element_tree["InputControlPanel"]
        
        if self.dialogue[self.current_dialogue]["type"] == "option":
            # switching 
            if pg.K_LEFT in input_panel.keys_just_pressed:
                self.selected_option -= 1
            elif pg.K_RIGHT in input_panel.keys_just_pressed:
                self.selected_option += 1
            self.selected_option = self.selected_option % len(self.dialogue[self.current_dialogue]["options"])
    
            # selecting
            if any([key in input_panel.keys_just_pressed for key in [pg.K_SPACE, pg.K_RETURN]]):
                self.current_dialogue = self.dialogue[self.current_dialogue]["options"][self.selected_option]["link"]

        elif self.dialogue[self.current_dialogue]["type"] == "text":
            if any([key in input_panel.keys_just_pressed for key in [pg.K_SPACE, pg.K_RETURN]]):
                if self.dialogue[self.current_dialogue]["link"] != None:
                    self.current_dialogue = self.dialogue[self.current_dialogue]["link"]
                else:
                    self.end = True

        else:
            raise Exception("Unknown dialogue type: " + self.dialogue[self.current_dialogue]["type"])
            

    def draw(self):
        renderer: Renderer = self.element_tree["Renderer"]

        renderer.queue_draw(self.dialogue_box, self.z, self.target, self.pos + self.draw_offset)

        text = self.dialogue[self.current_dialogue]["author"] + ": " + self.dialogue[self.current_dialogue]["text"]
        renderer.queue_draw(self.font.render(text, True, self.text_color), self.z+1, self.target, self.pos + self.draw_offset + pg.Vector2(50, 100))

        if self.dialogue[self.current_dialogue]["type"] == "option":
            option_count = len(self.dialogue[self.current_dialogue]["options"])

            for i, option in enumerate(self.dialogue[self.current_dialogue]["options"]):
                text = self.font.render(option["text"], True, self.text_color)
                text_rect = text.get_rect()
                
                if i == self.selected_option:
                    pg.draw.rect(text, self.text_color, text_rect, 5, 10)
                
                text_rect.center = self.pos + self.draw_offset + pg.Vector2((i+1)*(1302/(option_count+1)), 200)
                renderer.queue_draw(text, self.z+1, self.target, text_rect)
        




