from prismane import AssetLoader, Animation, Event

from .level import LevelEntity, Level

from pathlib import Path
import pygame as pg 
import pygame._sdl2.video as sdl2


class Mushroom(LevelEntity):
    def __init__(self, pos: pg.Vector2) -> None:
        super().__init__("MainCamura", pg.FRect(0, 0, 166, 114))
        hazards = self.element_tree["AssetLoader"].get_spritesheet(Path("./assets/tiles/hazards.json"))
        self.image = hazards["mushroom"]["texture"]
        self.source = hazards["mushroom"]["source"]
        self.pos = pos

        self.size = pg.Vector2(self.source.size)


class Spike(LevelEntity):
    def __init__(self, pos: pg.Vector2) -> None:
        super().__init__("MainCamura", pg.FRect(0, 0, 57, 74))
        hazards = self.element_tree["AssetLoader"].get_spritesheet(Path("./assets/tiles/hazards.json"))
        self.image = hazards["spike"]["texture"]
        self.source = hazards["spike"]["source"]
        self.pos = pos
        self.size = pg.Vector2(self.source.size)

class Oleni(LevelEntity):
    def __init__(self, pos: pg.Vector2) -> None:
        super().__init__(camera_name="MainCamura", hitbox=pg.FRect(0, 16, 160, 208))
        self.pos = pos
        self.velocity: pg.Vector2 = pg.Vector2(0, 0)
        self.max_velocity: int = 30
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
            Event(action=lambda: self.set_state("attack left"), condition=lambda: self.current_state == "idle left" and self.on_ground and not self.attacking and self.element_tree["CurrentStage"].singletons["level"].singletons["player"].rect.colliderect(self.left)),
            Event(action=lambda: self.set_state("attack right"), condition=lambda: self.current_state == "idle right" and self.on_ground and not self.attacking and self.element_tree["CurrentStage"].singletons["level"].singletons["player"].rect.colliderect(self.right)),
        ]

        self.image = self.states[self.current_state].get_frame()["texture"]
        self.size = pg.Vector2(self.image.get_rect().size)
        self.z = 1

    @property
    def left(self) -> pg.FRect:
        return pg.FRect(self.collision_box.x - 136, self.collision_box.y, 136, 225)

    @property
    def right(self) -> pg.FRect:
        return pg.FRect(self.collision_box.right, self.collision_box.y, 136, 225)

    def set_state(self, state: str):
        jump_states = ["jump left", "jump right"]
        fall_states = ["fall left", "fall right"]
        attack_states = ["attack left", "attack right"]
        for resetable_state in [jump_states, fall_states, attack_states]:
            if state in resetable_state and self.current_state not in resetable_state:
                self.states[state].reset()

        self.current_state = state

    def roam(self):
        if not self.on_ground or (self.facing == "left" and self.element_tree["CurrentStage"].singletons["level"].singletons["player"].rect.colliderect(self.left)) or (self.element_tree["CurrentStage"].singletons["level"].singletons["player"].rect.colliderect(self.right) and self.facing == "right"):
            return

        acceleration = 3000
        self.acceleration.x += acceleration * ((self.facing == "right") - (self.facing == "left"))

        level: Level = self.element_tree["CurrentStage"].singletons["level"]

        bottomright = self.collision_box.bottomright
        bottomleft = self.collision_box.bottomleft
        right_check = level.collidepoint((bottomright[0], bottomright[1] + 1), "tiles")
        left_check = level.collidepoint((bottomleft[0], bottomleft[1] + 1), "tiles")
        if not right_check and self.on_ground:
            self.facing = "left"
            self.velocity.x *= -1
            self.acceleration.x *= -2
        elif not left_check and self.on_ground:
            self.facing = "right"
            self.velocity.x *= -1
            self.acceleration.x *= -2

    def update(self):
        # movement
        self.acceleration = pg.Vector2(0, 0)
        self.acceleration += self.gravity

        self.roam()

        dt = self.element_tree["TimeControlPanel"].dt
        self.velocity += self.acceleration * dt  # acceleration
        if self.on_ground:
            #NOTE: why do you put 10 to the power dt? - Aiden
            self.velocity.x /= 10**dt  # friction

        self.velocity.x = max(-self.max_velocity, min(self.max_velocity, self.velocity.x))

        if abs(self.velocity.x) < 20:
            self.velocity.x = 0
        self.velocity.clamp_magnitude_ip(10_000)

        # collision
        level: Level = self.element_tree["CurrentStage"].singletons["level"]

        self.pos.x += self.velocity.x * dt
        entity: LevelEntity = level.get_collision_with(self, "tiles")
        if entity is not None:
            if self.velocity.x > 0:
                self.pos.x = entity.collision_box.left - self.hitbox.right
            else:
                self.pos.x = entity.collision_box.right - self.hitbox.left
            self.velocity.x = 0
            self.acceleration.x = 0


        self.pos.y += self.velocity.y * dt
        self.on_ground = False
        entity: LevelEntity = level.get_collision_with(self, "tiles")
        if entity is not None:
            if self.velocity.y >= 0:
                self.on_ground = True
                self.pos.y = entity.collision_box.top - self.rect.height
            else:
                self.pos.y = entity.collision_box.bottom
            self.velocity.y = 0
            self.acceleration.y = 0

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
        self.image = self.states[self.current_state].get_frame()["texture"]
        self.size = pg.Vector2(self.image.get_rect().size)


class Tile(LevelEntity):
    def __init__(self, pos: pg.Vector2, texture: dict, hitbox: pg.FRect = pg.FRect(0, 0, 0, 0)) -> None:
        super().__init__("MainCamura", hitbox)
        self.size = pg.Vector2(200, 200)
        self.image = texture["texture"]
        self.source = texture["source"]
        self.size = pg.Vector2(self.source.size)

        self.pos = pos
        self.z = 2

        self.hitbox = hitbox if hitbox else pg.FRect(0, 0, *self.source.size)


class Butterfly(LevelEntity):
    def __init__(self, pos: pg.Vector2, orientation: str) -> None:
        super().__init__("MainCamura", pg.FRect(0,0, 170, 179))
        self.image = self.element_tree["AssetLoader"].get_image(Path("./assets/entities/butterfly.png"))
        self.pos = pos
        self.size = pg.Vector2(self.image.get_rect().size)

        self.is_being_talked_to = False

        if orientation == "right":
            self.flip_x = True

    def update(self):
        super().update()

        if self.is_being_talked_to:
            if "dialogue" not in self.element_tree["CurrentStage"].singletons["level"].singletons:
                self.destroy()
                self.element_tree["CurrentStage"].singletons["level"].groups["butterflies"].remove(self)

class Gnome(LevelEntity):
    def __init__(self, pos: pg.Vector2) -> None:
        super().__init__("MainCamura", pg.FRect(0, 0, 151, 165))
        self.pos = pos
        self.image = self.element_tree["AssetLoader"].get_image(Path("./assets/entities/gnome.png"))
        self.size = pg.Vector2(self.image.get_rect().size)

        self.talked_to = False


class LightPole(LevelEntity):
    def __init__(self, pos: pg.Vector2) -> None:
        super().__init__("MainCamura", pg.FRect(0, 0, 292, 346))
        self.image = self.element_tree["AssetLoader"].get_image(Path("./assets/objects/lantern.png"))
        self.pos = pos
        self.size = pg.Vector2(self.image.get_rect().size)

