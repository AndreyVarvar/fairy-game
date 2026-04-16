import pygame as pg
from .panels import MasterControlPanel
from .stage import Stage
from .renderer import Renderer
from .element import Element

import asyncio

class Engine(Element):
    def __init__(self, screen_size: tuple[int, int], title: str, fps: int=60, flags=0):
        super().__init__(singleton=True)

        pg.mixer.pre_init(buffer=2048)
        pg.init()

        self.screen_size = self.screen_width, self.screen_height = screen_size
        # TODO: make self.window for the shenanigans with resizing or whatever
        self.window = pg.display.set_mode(screen_size, flags=flags)
        pg.display.set_caption(title)

        # internal variables
        self.running: bool
        self.events: list

        self.clock = pg.time.Clock()
        self.FPS = fps

        self.master_panel = MasterControlPanel()

        self.renderer = Renderer()

        self.scenes = {}
        self.current_scene: Stage

    def populate_scenes(self, scenes: dict[str, type[Stage]], initial_scene_name: str):
        self.scenes = scenes
        self.current_scene = self.scenes[initial_scene_name]()

    def update(self):
        dt = self.clock.tick(self.FPS) / 1000  # divide by 1000 to get seconds since last call
        self.master_panel.update(dt, self.events)

        self.current_scene.update()
        self.master_panel.sound_panel.play_sound_queue()  # play all queued sounds

        if self.current_scene.change_scenes:
            new_scene: str = self.current_scene.next_scene
            self.master_panel.music_panel.stop_music()
            self.current_scene.unload()  # custom defined function
            self.current_scene.destroy()  # function to remove self from the element tree. Always here
            self.current_scene = self.scenes[new_scene]()
            self.current_scene.load()

    def check_events(self):
        self.events = pg.event.get()
        for event in self.events:
            if event.type == pg.QUIT:
                self.running = False

    def draw(self):
        self.window.fill((0, 0, 0))

        self.current_scene.draw() 

        pg.display.update()

    async def run(self):
        self.running = True
        while self.running:
            self.check_events()
            self.update()
            self.draw()

            await asyncio.sleep(0)

    def start(self):
        if self.current_scene is None:
            raise Exception("No initial scene was defined.")

        asyncio.run(self.run())
