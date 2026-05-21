from __future__ import annotations

from prismane import Spritesheet, Animation, AssetLoader
from prismane import Entity, EntityGroup
from prismane import Event

import pygame as pg
from pathlib import Path


class LevelEntity(Entity):
    def __init__(self, camera_name, hitbox, collision_type: str = "static", singleton: bool = False) -> None:
        super().__init__(singleton)
        self.camera = self.element_tree[camera_name]
        self.hitbox: pg.FRect = hitbox  # NOTE: hitbox is measured in relation to the top-left corner of the entity (its position)
        self.collision_type = collision_type

    @property
    def collision_box(self) -> pg.FRect:
        return self.hitbox.move(*self.pos)

    def collides_with(self, entity: LevelEntity):
        return self.collision_box.colliderect(entity.collision_box)

    def collidepoint(self, point):
        return self.collision_box.collidepoint(point)

    def draw(self):
        self.element_tree["Renderer"].queue_draw(self.image, self.z, self.target, pg.Vector2(self.pos[0] - self.camera.scroll[0], self.pos[1] - self.camera.scroll[1]) + self.draw_offset)


class Mushroom(LevelEntity):
    def __init__(self, pos: pg.Vector2) -> None:
        super().__init__("MainCamura", pg.FRect(0, 0, 166, 114), "mushroom")
        hazards = self.element_tree["AssetLoader"].get_spritesheet(Path("./assets/tiles/hazards.json"))
        self.image = hazards["mushroom"]
        self.pos = pos


class Spike(LevelEntity):
    def __init__(self, pos: pg.Vector2) -> None:
        super().__init__("MainCamura", pg.FRect(0, 0, 57, 74), "spike")
        hazards = self.element_tree["AssetLoader"].get_spritesheet(Path("./assets/tiles/hazards.json"))
        self.image = hazards["spike"]
        self.pos = pos

class Oleni(LevelEntity):
    def __init__(self, pos: pg.Vector2) -> None:
        super().__init__(camera_name="MainCamura", hitbox=pg.FRect(0, 16, 160, 208))
        self.pos = pos
        self.velocity: pg.Vector2 = pg.Vector2(0, 0)
        self.acceleration: pg.Vector2 = pg.Vector2(0, 0)

        self.gravity: pg.Vector2 = pg.Vector2(0, 1000)
        self.on_ground = False

        self.collision_type = "oleni"

        asset_loader: AssetLoader = self.element_tree["AssetLoader"]

        self.states = {
            "idle left":    Animation(asset_loader.get_spritesheet(Path("assets/entities/models/oleni_idle_l/oleni_idle_l.json")), 10),
            "idle right":   Animation(asset_loader.get_spritesheet(Path("assets/entities/models/oleni_idle_r/oleni_idle_r.json")), 10),
            "walk left":    Animation(asset_loader.get_spritesheet(Path("assets/entities/models/oleni_walk_l/oleni_walk_l.json")), 10),
            "walk right":   Animation(asset_loader.get_spritesheet(Path("assets/entities/models/oleni_walk_r/oleni_walk_r.json")), 10),
            "attack left":  Animation(asset_loader.get_spritesheet(Path("assets/entities/models/oleni_attack_l/oleni_attack_l.json")), 10),
            "attack right": Animation(asset_loader.get_spritesheet(Path("assets/entities/models/oleni_attack_r/oleni_attack_r.json")), 10)
        }
        self.current_state = "idle left"

        self.facing = "right"
        self.attacking = False
        self.offsets = {
            "attack left": pg.Vector2(-205, 0),
            "attack right": pg.Vector2(-52, 0)
        }

        # conditions for switching from state A to state B
        self.switch_conditions = [
            Event(action=lambda: self.set_state("walk left"), condition=lambda: self.on_ground and self.velocity.x < 0),
            Event(action=lambda: self.set_state("walk right"), condition=lambda: self.on_ground and self.velocity.x > 0),
            Event(action=lambda: self.set_state("idle left"), condition=lambda: self.velocity.x == 0 and self.facing == "left" and self.on_ground and not self.attacking),
            Event(action=lambda: self.set_state("idle right"), condition=lambda: self.velocity.x == 0 and self.facing == "right" and self.on_ground and not self.attacking),
            Event(action=lambda: self.set_state("attack left"), condition=lambda: self.current_state == "idle left" and self.on_ground and not self.attacking and self.element_tree["CurrentStage"].singletons["player"].rect.colliderect(self.left)),
            Event(action=lambda: self.set_state("attack right"), condition=lambda: self.current_state == "idle right" and self.on_ground and not self.attacking and self.element_tree["CurrentStage"].singletons["player"].rect.colliderect(self.right)),
        ]

        self.image = self.states[self.current_state].get_frame()
        self.size = pg.Vector2(self.image.get_size())
        self.z = 1

    @property
    def left(self) -> pg.FRect:
        return pg.FRect(self.hitbox.x, self.hitbox.y, 136, 225)

    @property
    def right(self) -> pg.FRect:
        return pg.FRect(self.hitbox.right, self.hitbox.y, 136, 225)

    def set_state(self, state: str):
        jump_states = ["jump left", "jump right"]
        fall_states = ["fall left", "fall right"]
        attack_states = ["attack left", "attack right"]
        for resetable_state in [jump_states, fall_states, attack_states]:
            if state in resetable_state and self.current_state not in resetable_state:
                self.states[state].reset()

        self.current_state = state

    def roam(self):
        if not self.on_ground:
            return

        acceleration = 5000
        # self.acceleration.x += acceleration * ((self.facing == "right") - (self.facing == "left"))

        level: Level = self.element_tree["CurrentStage"].groups["level"][0]

        bottomright = self.rect.bottomright
        bottomleft = self.rect.bottomleft
        right_check = level.collidepoint((bottomright[0], bottomright[1] + 10))
        left_check = level.collidepoint((bottomleft[0], bottomleft[1] + 10))
        # TODO: if needed we can add conditions for when it is in the air, tho I don't know why that would ever occur
        if self.velocity.x > 0 and ((not right_check) or (not left_check)):
            self.velocity.x *= -1

    def update(self):
        # movement
        self.acceleration = pg.Vector2(0, 0)
        self.acceleration += self.gravity

        self.roam()

        dt = self.element_tree["TimeControlPanel"].dt
        self.velocity += self.acceleration * dt  # acceleration
        if self.on_ground:
            # why do you put 10 to the power dt? - Aiden
            self.velocity.x /= 10**dt  # friction

        # collision
        level: Level = self.element_tree["CurrentStage"].groups["level"][0]

        self.pos.x += self.velocity.x * dt
        entity = level.get_collision_with(self)
        if entity is not None:
            if self.velocity.x > 0:
                self.pos.x = entity.collision_box.left - self.hitbox.right
            else:
                self.pos.x = entity.collision_box.right - self.hitbox.left
            self.velocity.x = 0
            self.acceleration.x = 0

        self.pos.y += self.velocity.y * dt
        self.on_ground = False
        entity = level.get_collision_with(self)
        if entity is not None:
            if self.velocity.y >= 0:
                self.on_ground = True
                self.pos.y = entity.collision_box.top - self.rect.height
            else:
                self.pos.y = entity.collision_box.bottom
            self.velocity.y = 0
            self.acceleration.y = 0

        if abs(self.velocity.x) < 50:
            self.velocity.x = 0
        self.velocity.clamp_magnitude_ip(10_000)

        if self.velocity.x != 0:
            if self.velocity.x > 0:
                self.facing = "right"
            else:
                self.facing = "left"

        # states
        self.attacking = self.current_state in ["attack left", "attack right"] and not self.states[self.current_state].end

        for event in self.switch_conditions:
            event.update()

        # HAHA self.attacking goes BBRRRRRRRRrrrrr
        if self.current_state in ["attack left", "attack right"]:
            self.draw_offset = self.offsets[self.current_state]
        else:
            self.draw_offset = pg.Vector2(0, 0)

        # animations
        self.states[self.current_state].update()
        self.image = self.states[self.current_state].get_frame().copy()

        pg.draw.rect(self.image, (255, 0, 0), (self.hitbox.x + self.draw_offset.x, self.hitbox.y + self.draw_offset.y, self.hitbox.w, self.hitbox.h), 5)
        pg.draw.rect(self.image, (0, 255, 0), (self.hitbox.x + self.draw_offset.x - 136, self.hitbox.y + self.draw_offset.y, 136, 225), 5)


class Tile(LevelEntity):
    def __init__(self, pos: pg.Vector2, image: pg.Surface, hitbox: pg.FRect = pg.FRect(0, 0, 0, 0)) -> None:
        super().__init__("MainCamura", hitbox)
        self.size = pg.Vector2(200, 200)
        self.image = image

        self.pos = pos
        self.z = 2

        self.hitbox = hitbox if hitbox else pg.FRect(0, 0, *self.image.get_size())


class Butterfly(LevelEntity):
    def __init__(self, pos: pg.Vector2, orientation: str) -> None:
        super().__init__("MainCamura", pg.FRect(0,0, 170, 179), "butterfly")
        self.image = self.element_tree["AssetLoader"].get_image(Path("./assets/entities/butterfly.png"))
        self.pos = pos

        if orientation == "right":
            self.image = pg.transform.flip(self.image, flip_x=True, flip_y=False)

class Level(Entity):
    def __init__(self, entities: EntityGroup, player_start_pos: pg.Vector2) -> None:
        super().__init__()

        self.entities: EntityGroup = entities
        self.player_start_pos = player_start_pos

    def get_collision_with(self, entity: LevelEntity):
        for level_entity in self.entities:
            if level_entity.collides_with(entity):
                return level_entity
        return None

    def collidepoint(self, point):
        for level_entity in self.entities:
            if level_entity.collidepoint(point):
                return level_entity
        return None

    def update(self):
        self.entities.update()

    def draw(self):
        self.entities.draw()


class Level1(Level):
    def __init__(self) -> None:
        w, h = 115, 75  # tile width and tile height, shortened for conveniece in the monstrocity you see below (yes, it was manually written. Every single entry. Every single tile. You could say it woul've been better to write a script to do that for me, but I am too lazy to write the autotiler, and even though it would've taken me 30 minutes I'd rather spend the next 2 hours manually writing everyghing down)
        tileset = Spritesheet(Path("./assets/tiles/pink.json"))
        tile_hitbox = pg.FRect(0, 51, 115, 75)
        entities: EntityGroup = EntityGroup(
            # tiles
            Tile(pg.Vector2(-1*w, 3*h), tileset["top-left"], tile_hitbox),
            Tile(pg.Vector2(0*w, 3*h), tileset["top-right"], tile_hitbox),
            
            Tile(pg.Vector2(-1*w, 9*h), tileset["top-left"], tile_hitbox),
            Tile(pg.Vector2(0*w, 9*h), tileset["top-middle 1"], tile_hitbox),
            Tile(pg.Vector2(1*w, 9*h), tileset["top-right"], tile_hitbox),
            Tile(pg.Vector2(-1*w, 10*h+tile_hitbox.y), tileset["bottom-left"]),
            Tile(pg.Vector2(0*w, 10*h+tile_hitbox.y), tileset["middle"]),
            Tile(pg.Vector2(1*w, 10*h+tile_hitbox.y), tileset["middle"]),
            Tile(pg.Vector2(0*w, 11*h+tile_hitbox.y), tileset["bottom-left"]),
            Tile(pg.Vector2(1*w, 11*h+tile_hitbox.y), tileset["middle"]),
            Tile(pg.Vector2(2*w, 11*h), tileset["top-right"], tile_hitbox),
            
            Tile(pg.Vector2(4*w, 7*h), tileset["top-left"], tile_hitbox),
            Tile(pg.Vector2(5*w, 7*h), tileset["top-middle 2"], tile_hitbox),
            Tile(pg.Vector2(6*w, 7*h), tileset["top-middle 1"], tile_hitbox),
            Tile(pg.Vector2(7*w, 7*h), tileset["top-middle 2"], tile_hitbox),
            Tile(pg.Vector2(8*w, 7*h), tileset["top-right"], tile_hitbox),
            
            Tile(pg.Vector2(9*w, 5*h), tileset["top-left"], tile_hitbox),
            Tile(pg.Vector2(10*w, 5*h), tileset["top-middle 1"], tile_hitbox),
            Tile(pg.Vector2(11*w, 5*h), tileset["top-right"], tile_hitbox),
            
            Tile(pg.Vector2(13*w, 5*h), tileset["top-left"], tile_hitbox),
            Tile(pg.Vector2(14*w, 5*h), tileset["top-middle 1"], tile_hitbox),
            Tile(pg.Vector2(15*w, 5*h), tileset["top-middle 2"], tile_hitbox),
            Tile(pg.Vector2(16*w, 5*h), tileset["top-right"], tile_hitbox),
            
            Tile(pg.Vector2(18*w, 7*h), tileset["top-left"], tile_hitbox),
            Tile(pg.Vector2(19*w, 7*h), tileset["top-middle 1"], tile_hitbox),
            Tile(pg.Vector2(20*w, 7*h), tileset["top-right"], tile_hitbox),
            
            Tile(pg.Vector2(22*w, 6*h), tileset["top-left"], tile_hitbox),
            Tile(pg.Vector2(23*w, 6*h), tileset["top-right"], tile_hitbox),
            
            Tile(pg.Vector2(25*w, 5*h), tileset["top-left"], tile_hitbox),
            Tile(pg.Vector2(26*w, 5*h), tileset["top-right"], tile_hitbox),
            
            Tile(pg.Vector2(15*w, 10*h), tileset["top-left"], tile_hitbox),
            Tile(pg.Vector2(16*w, 10*h), tileset["top-right"], tile_hitbox),
            
            Tile(pg.Vector2(24*w, 11*h), tileset["top-left"], tile_hitbox),
            Tile(pg.Vector2(25*w, 11*h), tileset["top-middle 1"], tile_hitbox),
            Tile(pg.Vector2(26*w, 11*h), tileset["top-middle 2"], tile_hitbox),
            Tile(pg.Vector2(27*w, 11*h), tileset["top-right"], tile_hitbox),
            
            Tile(pg.Vector2(4*w, 17*h), tileset["top-left"], tile_hitbox),
            Tile(pg.Vector2(5*w, 17*h), tileset["top-right"], tile_hitbox),
            
            Tile(pg.Vector2(10*w, 15*h), tileset["top-left"], tile_hitbox),
            Tile(pg.Vector2(11*w, 15*h), tileset["top-middle 1"], tile_hitbox),
            Tile(pg.Vector2(12*w, 15*h), tileset["top-right"], tile_hitbox),
            
            Tile(pg.Vector2(17*w, 17*h), tileset["top-left"], tile_hitbox),
            Tile(pg.Vector2(18*w, 17*h), tileset["top-middle 2"], tile_hitbox),
            Tile(pg.Vector2(19*w, 17*h), tileset["top-middle 1"], tile_hitbox),
            Tile(pg.Vector2(20*w, 17*h), tileset["top-middle 2"], tile_hitbox),
            Tile(pg.Vector2(21*w, 17*h), tileset["top-middle 1"], tile_hitbox),
            Tile(pg.Vector2(22*w, 17*h), tileset["top-right"], tile_hitbox),
            
            Tile(pg.Vector2(1*w, 18*h), tileset["top-left"], tile_hitbox),
            Tile(pg.Vector2(2*w, 18*h), tileset["top-right"], tile_hitbox),
            Tile(pg.Vector2(1*w, 19*h+tile_hitbox.y), tileset["bottom-left"]),
            Tile(pg.Vector2(2*w, 19*h+tile_hitbox.y), tileset["bottom-right"]),
            
            Tile(pg.Vector2(7*w, 17*h), tileset["top-left"], tile_hitbox),
            Tile(pg.Vector2(8*w, 17*h), tileset["top-middle 1"], tile_hitbox),
            Tile(pg.Vector2(9*w, 17*h), tileset["top-right"], tile_hitbox),
            Tile(pg.Vector2(7*w, 18*h+tile_hitbox.y), tileset["middle"]),
            Tile(pg.Vector2(8*w, 18*h+tile_hitbox.y), tileset["middle"]),
            Tile(pg.Vector2(9*w, 18*h+tile_hitbox.y), tileset["middle"]),
            Tile(pg.Vector2(7*w, 19*h+tile_hitbox.y), tileset["bottom-left"]),
            Tile(pg.Vector2(8*w, 19*h+tile_hitbox.y), tileset["middle"]),
            Tile(pg.Vector2(9*w, 19*h+tile_hitbox.y), tileset["bottom-right"]),
            
            Tile(pg.Vector2(12*w, 17*h), tileset["top-left"], tile_hitbox),
            Tile(pg.Vector2(13*w, 17*h), tileset["top-right"], tile_hitbox),
            Tile(pg.Vector2(13*w, 18*h+tile_hitbox.y), tileset["middle"]),
            Tile(pg.Vector2(14*w, 18*h), tileset["top-middle 1"], tile_hitbox),
            Tile(pg.Vector2(15*w, 18*h), tileset["top-right"], tile_hitbox),
            Tile(pg.Vector2(13*w, 19*h+tile_hitbox.y), tileset["bottom-left"]),
            Tile(pg.Vector2(14*w, 19*h+tile_hitbox.y), tileset["middle"]),
            Tile(pg.Vector2(15*w, 19*h+tile_hitbox.y), tileset["bottom-right"]),
            
            Tile(pg.Vector2(24*w, 18*h), tileset["top-left"], tile_hitbox),
            Tile(pg.Vector2(25*w, 18*h), tileset["top-middle 1"], tile_hitbox),
            Tile(pg.Vector2(26*w, 18*h), tileset["top-right"], tile_hitbox),
            Tile(pg.Vector2(24*w, 19*h+tile_hitbox.y), tileset["bottom-left"]),
            Tile(pg.Vector2(25*w, 19*h+tile_hitbox.y), tileset["middle"]),
            Tile(pg.Vector2(26*w, 19*h+tile_hitbox.y), tileset["bottom-right"]),
        
            # MUSHROOMs
            Mushroom(pg.Vector2(4*w, 6*h+10)),
            Mushroom(pg.Vector2(4*w, 16*h+10)),
            Mushroom(pg.Vector2(11.75*w, 14*h+10)),

            # Spikes
            Spike(pg.Vector2(11*w+40, 4*h+50)),
            Spike(pg.Vector2(18*w+40, 6*h+50)),
            Spike(pg.Vector2(11*w+40, 14*h+50)),

            # Butterflies
            Butterfly(pg.Vector2(-1*w-10, 2*h-50), orientation="right"),
            Butterfly(pg.Vector2(26*w-10, 4*h-50), orientation="left"),
            Butterfly(pg.Vector2(16*w-10, 9*h-50), orientation="left"),

            # Oleni
            Oleni(pg.Vector2(11*w+40, 14*h - 200))
        )
        super().__init__(entities, pg.Vector2(144, 1169))

