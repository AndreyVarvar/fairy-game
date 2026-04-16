from .entity import Entity
from .panels import InputControlPanel

import pygame as pg


class Button(Entity):
    def __init__(
        self, 
        rect: pg.Rect, 
        z=1, 
    ):
        super().__init__()
        self.z = z
        self.pos = pg.Vector2(rect.topleft)
        self.size = rect.size
        self.pressed = False
        self.was_pressed_on_self = False
        self.was_released_on_self = False
        self.hovering = False

    def update(self):
        # this implementation assumes that all UI elements are updated based on the z-index
        # If not, them the UI element which consumes the mouse click is not deterministic
        self.pressed = False

        input_panel: InputControlPanel = self.element_tree["InputControlPanel"]

        self.hovering = self.rect.collidepoint(input_panel.mouse_pos)
        if self.hovering:
            input_panel.queue_cursor(pg.SYSTEM_CURSOR_HAND)

        if input_panel.mouse_just_pressed[0]:
            if self.rect.collidepoint(input_panel.mouse_click_pos):
                self.was_pressed_on_self = True
                input_panel.consume_mouse_click()
            else:
                self.was_pressed_on_self = False
        
        if input_panel.mouse_just_released[0]:
            if self.rect.collidepoint(input_panel.mouse_release_pos):
                self.was_released_on_self = True
            else:
                self.was_released_on_self = False

        if self.was_pressed_on_self and self.was_released_on_self:
            self.was_pressed_on_self = False
            self.was_released_on_self = False

            self.pressed = True  # will be True until next update

