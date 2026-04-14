from prismane.ui import Button
from prismane.assets import get_image
from pathlib import Path

import pygame as pg


class StartButton(Button):
    def __init__(self, z=1):
        img = get_image(Path("assets/ui/start_button.png"))
        super().__init__(img.get_rect(), z)
        self.image = img
