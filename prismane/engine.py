import pygame as pg
import pygame._sdl2.video as sdl2

from prismane.assets import AssetLoader
from .panels import MasterControlPanel
from .stage import Stage
from .renderer import Renderer
from .element import Element
from .settings import Settings

import asyncio

class Engine(Element):
    def __init__(self, window_size: tuple[int, int], title: str, logical_size: tuple[int, int] = None, fps: int = 60, fullscreen: bool = False):
        super().__init__(singleton=True)

        pg.mixer.pre_init(buffer=2048)
        pg.init()

        self.asset_loader: AssetLoader = AssetLoader()
        self.settings: Settings = Settings()

        self.window = pg.Window(title=title, size=window_size, fullscreen=fullscreen)
 
        # internal variables
        self.running: bool
        self.events: list

        self.clock = pg.time.Clock()
        self.FPS = fps
        self.max_dt = 1/self.FPS

        self.master_panel = MasterControlPanel()

        self.window_renderer = sdl2.Renderer(self.window)
        self.window_renderer.logical_size = logical_size if logical_size else window_size

        self.asset_renderer = Renderer()

        self.stages = {}
        self.current_stage: Stage

    def populate_stages(self, stages: dict[str, type[Stage]], initial_stage_name: str):
        self.stages = stages
        self.current_stage = self.stages[initial_stage_name]()

    def update(self):
        dt = min(self.clock.tick(self.FPS) / 1000, self.max_dt)  # divide by 1000 to get seconds since last call
        self.master_panel.update(dt, self.events)

        self.current_stage.update()
        self.master_panel.sound_panel.play_sound_queue()  # play all queued sounds

        if self.current_stage.change_stages:
            self.change_stage()

    def change_stage(self):
        new_stage: str = self.current_stage.next_stage
        self.master_panel.music_panel.stop_music()

        # delete old information
        self.current_stage.unload()  # custom defined function
        self.current_stage.destroy()  # function to remove self from the element tree. Always here

        # load new information
        self.current_stage = self.stages[new_stage]()
        self.current_stage.load()

    def check_events(self):
        self.events = pg.event.get()
        for event in self.events:
            if event.type == pg.QUIT:
                self.running = False

    def draw(self):
        self.current_stage.draw()
        self.asset_renderer.draw()
        
        self.window_renderer.present()
        self.window_renderer.clear()

    async def run(self):
        self.running = True
        while self.running:
            self.check_events()
            self.update()
            self.draw()

            await asyncio.sleep(0)

    def start(self):
        if self.current_stage is None:
            raise Exception("No initial stage was defined.")

        asyncio.run(self.run())
