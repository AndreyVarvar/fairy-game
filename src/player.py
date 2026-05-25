from prismane import InputControlPanel
from prismane import Animation
from prismane import Event
from prismane.assets import AssetLoader
from prismane.panels import TimeControlPanel

from .level import LevelEntity, Level
from .level_entities import Tile, Spike, Mushroom, Butterfly, Gnome

from pathlib import Path

import pygame as pg

class Player(LevelEntity):
    def __init__(self, pos: pg.Vector2) -> None:
        super().__init__(camera_name="MainCamura", hitbox=pg.FRect(70, 0, 70, 232))
        self.pos = pos
        self.velocity: pg.Vector2 = pg.Vector2(0, 0)
        self.max_velocity: int = 320
        self.acceleration: pg.Vector2 = pg.Vector2(0, 0)

        self.gravity: pg.Vector2 = pg.Vector2(0, 1000)
        self.on_ground = False

        self.initial_health = 3
        self.health = self.initial_health
        self.max_health = 5
        self.damage_cooldown = 2
        self.damage_cooldown_timer_id = 0

        self.max_speed_from_input = 300
        self.jump_velocity = -600

        self.butterflies_collected = 0

        asset_loader: AssetLoader = self.element_tree["AssetLoader"]

        self.states = {
            "idle left":    Animation(asset_loader.get_spritesheet(Path("assets/entities/models/idle_l/idle_l.json")),         10),
            "idle right":   Animation(asset_loader.get_spritesheet(Path("assets/entities/models/idle_r/idle_r.json")),         10),
            "walk left":    Animation(asset_loader.get_spritesheet(Path("assets/entities/models/walk_l/walk_l.json")),         10),
            "walk right":   Animation(asset_loader.get_spritesheet(Path("assets/entities/models/walk_r/walk_r.json")),         10),
            "jump left":    Animation(asset_loader.get_spritesheet(Path("assets/entities/models/jump_left/jump_left.json")),   50, loop=False),
            "jump right":   Animation(asset_loader.get_spritesheet(Path("assets/entities/models/jump_right/jump_right.json")), 50, loop=False),
            "fall left":    Animation(asset_loader.get_spritesheet(Path("assets/entities/models/fall_l/fall_l.json")),         10, loop=False),
            "fall right":   Animation(asset_loader.get_spritesheet(Path("assets/entities/models/fall_r/fall_r.json")),         10, loop=False),
            "attack left":  Animation(asset_loader.get_spritesheet(Path("assets/entities/models/attack_l/attack_l.json")),     10, loop=False),
            "attack right": Animation(asset_loader.get_spritesheet(Path("assets/entities/models/attack_r/attack_r.json")),     10, loop=False)
        }
        self.current_state = "idle left"

        self.facing = "left"
        self.attacking = False
        self.offsets = {
            "attack left": pg.Vector2(-110, 0),
            "attack right": pg.Vector2(15, 0)
        }

        input_panel: InputControlPanel = self.element_tree["InputControlPanel"]

        # conditions for switching from state A to state B
        self.switch_conditions = [
            Event(action=lambda: self.set_state("walk left"),    condition=lambda: self.on_ground and self.velocity.x < 0),
            Event(action=lambda: self.set_state("walk right"),   condition=lambda: self.on_ground and self.velocity.x > 0),
            Event(action=lambda: self.set_state("idle left"),    condition=lambda: self.velocity.x == 0 and self.facing == "left" and self.on_ground and not self.attacking),
            Event(action=lambda: self.set_state("idle right"),   condition=lambda: self.velocity.x == 0 and self.facing == "right" and self.on_ground and not self.attacking),
            Event(action=lambda: self.set_state("jump left"),    condition=lambda: self.velocity.y < 0 and not self.on_ground and self.facing == "left"),
            Event(action=lambda: self.set_state("jump right"),   condition=lambda: self.velocity.y < 0 and not self.on_ground and self.facing == "right"),
            Event(action=lambda: self.set_state("fall left"),    condition=lambda: self.velocity.y > 0 and not self.on_ground and self.facing == "left"),
            Event(action=lambda: self.set_state("fall right"),   condition=lambda: self.velocity.y > 0 and not self.on_ground and self.facing == "right"),
            Event(action=lambda: self.set_state("attack left"),  condition=lambda: self.current_state == "idle left" and self.on_ground and pg.K_p in input_panel.keys_just_pressed and not self.attacking and self.has_control),
            Event(action=lambda: self.set_state("attack right"), condition=lambda: self.current_state == "idle right" and self.on_ground and pg.K_p in input_panel.keys_just_pressed and not self.attacking and self.has_control),
        ]

        self.image = self.states[self.current_state].get_frame()  # TODO: currenly player hitbox is tied to image

        self.z = 1
        self.size = pg.Vector2(self.image.get_size())

        self.has_control = True

    def set_state(self, state: str):
        jump_states = ["jump left", "jump right"]
        fall_states = ["fall left", "fall right"]
        attack_states = ["attack left", "attack right"]
        for resetable_state in [jump_states, fall_states, attack_states]:
            if state in resetable_state and self.current_state not in resetable_state:
                self.states[state].reset()

        self.current_state = state


    @property
    def dead(self):
        return self.health <= 0

    def process_input(self):
        input_panel: InputControlPanel = self.element_tree["InputControlPanel"]

        input_acceleration = pg.Vector2(0, 0)

        accel = 5000

        if input_panel.keys_pressed[pg.K_d]:
            input_acceleration.x = accel
        if input_panel.keys_pressed[pg.K_a]:
            input_acceleration.x = -accel

        if abs(self.velocity.x) < self.max_speed_from_input or input_acceleration.x * self.velocity.x < 0:
            self.acceleration += input_acceleration

        if pg.K_SPACE in input_panel.keys_just_pressed and self.on_ground:  # jump
            self.velocity.y = self.jump_velocity

    def damage(self):
        time_panel: TimeControlPanel = self.element_tree["TimeControlPanel"]
        if time_panel.check_timer(self.damage_cooldown_timer_id) == 0:
            self.health -= 1
            self.damage_cooldown_timer_id = time_panel.queue_timer(self.damage_cooldown)

    def update(self):
        # movement
        self.acceleration = pg.Vector2(0, 0)
        self.acceleration += self.gravity

        self.has_control = "dialogue" not in self.element_tree["CurrentStage"].singletons["level"].singletons
        
        if self.has_control:
            self.process_input()
        else:
            self.velocity.x = 0
            self.acceleration.x = 0

        dt = self.element_tree["TimeControlPanel"].dt
        self.velocity += self.acceleration * dt  # acceleration
        if self.on_ground:
            self.velocity.x /= 10**dt  # friction

        self.velocity.x = max(-self.max_velocity, min(self.max_velocity, self.velocity.x)) # blud forgot to cap velocity :skull:

        if abs(self.velocity.x) < 50:
            self.velocity.x = 0
        self.velocity.clamp_magnitude_ip(10_000)

        # collision
        level: Level = self.element_tree["CurrentStage"].singletons["level"]

        # collision with tiles
        self.pos.x += self.velocity.x * dt
        tile: LevelEntity = level.get_collision_with(self, "tiles")
        if tile is not None:
            if self.velocity.x > 0:
                self.pos.x = tile.collision_box.left - self.hitbox.right
            else:
                self.pos.x = tile.collision_box.right - self.hitbox.left
            self.velocity.x = 0
            self.acceleration.x = 0


        self.pos.y += self.velocity.y * dt
        self.on_ground = False
        tile: Tile = level.get_collision_with(self, "tiles")
        if tile is not None:
            if self.velocity.y >= 0:
                self.on_ground = True
                self.pos.y = tile.collision_box.top - self.rect.height
            else:
                self.pos.y = tile.collision_box.bottom
            self.velocity.y = 0
            self.acceleration.y = 0

        # collision with spikes
        spike: Spike = level.get_collision_with(self, "spikes")
        if spike is not None:
            self.damage()

        # collision with mushrooms
        mushroom: Mushroom = level.get_collision_with(self, "mushrooms")
        if mushroom is not None:
            if self.velocity.y > 0:
                self.velocity.y = -1000

        # collision with butterflies
        butterfly: Butterfly | None = level.get_collision_with(self, "butterflies")
        if butterfly is not None:
            if not butterfly.is_being_talked_to:
                self.butterflies_collected += 1
                self.element_tree["CurrentStage"].singletons["level"].start_dialogue(Path(f"./assets/dialogues/butterfly{self.butterflies_collected}.json"))
                butterfly.is_being_talked_to = True

        # collision with gnomes
        gnome: Gnome | None = level.get_collision_with(self, "gnomes")
        if gnome is not None:
            if gnome.talked_to is False:
                gnome.talked_to = True
                self.element_tree["CurrentStage"].singletons["level"].start_dialogue(Path("./assets/dialogues/gnome.json"))

        # states
        if self.velocity.x != 0:
            if self.velocity.x > 0:
                self.facing = "right"
            else:
                self.facing = "left"
        
        self.attacking = self.current_state in ["attack left", "attack right"] and not self.states[self.current_state].end
        
        for event in self.switch_conditions:
            event.update()
        
        # DO NOT USE self.attacking HERE!!!!
        # it will cause a visual jitter the moment states switch
        # it's related to the animation.end condition
        if self.current_state in ["attack left", "attack right"]:
            self.draw_offset = self.offsets[self.current_state]
        else:
            self.draw_offset = pg.Vector2(0, 0)
        
        # animations
        time_panel: TimeControlPanel = self.element_tree["TimeControlPanel"]

        self.states[self.current_state].update()
        flicker_cd = 0.5
        flicker = (time_panel.check_timer(self.damage_cooldown_timer_id) % flicker_cd) > (flicker_cd/2)
        
        if flicker:
            self.image = self.states[self.current_state].get_frame().copy()
            self.image.fill((255, 0, 0), special_flags=pg.BLENDMODE_MUL)
        else:
            self.image = self.states[self.current_state].get_frame()
        
        # self.image = self.states[self.current_state].get_frame().copy()
        # pg.draw.rect(self.image, (255, 0, 0), self.hitbox.move(-self.draw_offset), 5)

