from prismane import Entity

from pathlib import Path
import json
import pygame as pg

from prismane.assets import AssetLoader
from prismane.panels import InputControlPanel, SoundControlPanel
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
        rect = self.dialogue_box.get_rect(midbottom=pg.Vector2(settings.logical_width//2, settings.logical_height-100))
        self.pos = pg.Vector2(rect.topleft)

        self.end = False

        self.z = 10

        self.selected_option = 0

        self.text_color = pg.Color(107, 67, 130)
        self.size = pg.Vector2(self.dialogue_box.get_rect().size)

        self.choice_sound = asset_loader.get_sound(Path("./assets/sfx/category-selection-sound.ogg"))
        self.selection_sound = asset_loader.get_sound(Path("./assets/sfx/podtverjdenie--myagkiy-schelchok.ogg"))
        self.continue_sound = asset_loader.get_sound(Path("./assets/sfx/novoe-soobschenie--myagkiy-ping.ogg"))

    def update(self):
        super().update()

        input_panel: InputControlPanel = self.element_tree["InputControlPanel"]
        sound_panel: SoundControlPanel = self.element_tree["SoundControlPanel"]
        
        if self.dialogue[self.current_dialogue]["type"] == "option":
            # switching 
            if pg.K_LEFT in input_panel.keys_just_pressed:
                self.selected_option -= 1
                sound_panel.queue_sound(self.choice_sound, 0)
            elif pg.K_RIGHT in input_panel.keys_just_pressed:
                self.selected_option += 1
                sound_panel.queue_sound(self.choice_sound, 0)
            self.selected_option = self.selected_option % len(self.dialogue[self.current_dialogue]["options"])
    
            # selecting
            if any([key in input_panel.keys_just_pressed for key in [pg.K_SPACE, pg.K_RETURN]]):
                self.current_dialogue = self.dialogue[self.current_dialogue]["options"][self.selected_option]["link"]
                sound_panel.queue_sound(self.selection_sound, 0)

        elif self.dialogue[self.current_dialogue]["type"] == "text":
            if any([key in input_panel.keys_just_pressed for key in [pg.K_SPACE, pg.K_RETURN]]):
                sound_panel.queue_sound(self.continue_sound, 0)
                if self.dialogue[self.current_dialogue]["link"] != None:
                    self.current_dialogue = self.dialogue[self.current_dialogue]["link"]
                else:
                    self.end = True

        else:
            raise Exception("Unknown dialogue type: " + self.dialogue[self.current_dialogue]["type"])
            

    def draw(self):
        scale = 2

        renderer: Renderer = self.element_tree["Renderer"]

        renderer.queue_draw(self.dialogue_box, self.z, destination=self.rect.move(self.draw_offset).scale_by(scale))

        text = self.dialogue[self.current_dialogue]["author"] + ": " + self.dialogue[self.current_dialogue]["text"]
        text_texture = self.element_tree["AssetLoader"].texture_from_surface(self.font.render(text, True, self.text_color))
        text_texture_rect = text_texture.get_rect().scale_by(scale).move(self.pos + self.draw_offset + pg.Vector2(50, 100))
        text_texture_rect.left = self.rect.move(self.draw_offset).scale_by(scale).left + scale*50
        renderer.queue_draw(text_texture, self.z+1, destination=text_texture_rect)

        if self.dialogue[self.current_dialogue]["type"] == "option":
            option_count = len(self.dialogue[self.current_dialogue]["options"])

            for i, option in enumerate(self.dialogue[self.current_dialogue]["options"]):
                text = self.font.render(option["text"], True, self.text_color)
                text_rect = text.get_rect()
                
                if i == self.selected_option:
                    pg.draw.rect(text, self.text_color, text_rect, 5, 10)
                
                text_rect.scale_by_ip(scale)
                text_rect.center = pg.Vector2(self.rect.scale_by(scale).move(self.draw_offset).topleft) + scale*pg.Vector2((i+1)*(self.size.x/(option_count+1)), 200)
                renderer.queue_draw(self.element_tree["AssetLoader"].texture_from_surface(text), self.z+1, text_rect)
        




