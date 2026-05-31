from __future__ import annotations

from prismane import Entity, EntityGroup, Renderer, Event, TimeControlPanel
from prismane.settings import Settings

from .dialogue import DialogueBox
from .ui import SafeUI

import pygame as pg
from pathlib import Path

from math import floor, ceil


class LevelEntity(Entity):
    def __init__(self, camera_name, hitbox, singleton: bool = False) -> None:
        super().__init__(singleton)
        self.camera = self.element_tree[camera_name]
        self.hitbox: pg.FRect = hitbox # NOTE: hitbox is measured in relation to the top-left corner of the entity (its position)

    @property
    def collision_box(self) -> pg.FRect:
        return self.hitbox.move(self.pos)

    def collides_with(self, entity: LevelEntity):
        return self.collision_box.colliderect(entity.collision_box)

    def collidepoint(self, point):
        return self.collision_box.collidepoint(point)

    def draw(self):
        renderer: Renderer = self.element_tree["Renderer"]

        dst = self.frect.move(self.draw_offset)
        dst = pg.FRect(floor(dst.x * self.scale), floor(dst.y * self.scale), ceil(dst.w * self.scale) + 1, ceil(dst.h * self.scale) + 1)
        dst.move_ip((int(-self.camera.scroll.x), int(-self.camera.scroll.y)))

        renderer.queue_draw(
            texture=self.image, 
            z=self.z, 
            source=self.source, 
            destination=dst, 
            flip_x=self.flip_x, 
            flip_y=self.flip_y, 
            angle=self.angle, 
            pivot=self.pivot,
            color=self.color,
            alpha=self.alpha,
            blend_mode=self.blend_mode
        )


class Level(Entity):
    def __init__(self, player_start_pos: pg.Vector2) -> None:
        super().__init__()

        self.events: list
        self.groups: dict[str, EntityGroup]
        self.singletons: dict[str, Entity]
 
        self.player_start_pos = player_start_pos

        self.safe_timer = -1

    def reset(self):
        self.__init__(self.player_start_pos)

    def start_safe(self):
        time_panel: TimeControlPanel = self.element_tree["TimeControlPanel"]
        if time_panel.check_timer(self.safe_timer) == 0 and self.singletons.get("safe") == None:
            settings: Settings = self.element_tree["Settings"]
            self.singletons["safe"] = SafeUI(pg.Vector2(settings.logical_width//2 - 656, 456))
            self.events.append(Event(action=lambda: self.element_tree["CurrentStage"].next_level(1), condition=lambda: self.singletons["safe"].correct, activations_limit=1, termination_condition=lambda: self.singletons.get("safe") == None))
            self.events.append(Event(action=lambda: self.stop_safe(), condition=lambda: self.singletons["safe"].end, activations_limit=1))

    def stop_safe(self):
        if "safe" in self.singletons:
            time_panel: TimeControlPanel = self.element_tree["TimeControlPanel"]
            self.safe_timer = time_panel.queue_timer(2)
            self.singletons["safe"].destroy()
            del self.singletons["safe"]

    def start_dialogue(self, dialogue_json_path: Path = None, text: dict = None):
        if text == None:
            self.singletons["dialogue"] = DialogueBox(dialogue_json_path=dialogue_json_path)
        else:
            self.singletons["dialogue"] = DialogueBox(text=text)

        self.events.append(Event(action=lambda: self.stop_dialogue(), condition=lambda: self.singletons["dialogue"].end, activations_limit=1))

    def stop_dialogue(self):
        if "dialogue" in self.singletons:
            self.singletons["dialogue"].destroy()
            del self.singletons["dialogue"]

    def get_collision_with(self, entity: LevelEntity, group: str):
        if group not in self.groups:
            return None

        for level_entity in self.groups[group]:
            if level_entity.collides_with(entity):
                return level_entity
        return None

    def collidepoint(self, point, group):
        for level_entity in self.groups[group]:
            if level_entity.collidepoint(point):
                return level_entity
        return None

    def update(self):
        for group in self.groups.values():
            group.update()

        for singleton in list(self.singletons.values()):
            singleton.update()
        
        events_to_clear = []
        for event in self.events:
            event.update()
            if event.inactive:
                events_to_clear.append(event)

        for event in events_to_clear:
            self.events.remove(event)

    def draw(self):
        for group in self.groups.values():
            group.draw()

        for singleton in self.singletons.values():
            singleton.draw()


