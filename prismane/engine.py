import pygame as pg
from .panels import MasterControlPanel
from .scene import Scene

import asyncio

class Engine():
    def __init__(self, screen_size: tuple[int, int], title: str, fps: int=60):
        pg.mixer.pre_init(buffer=2048)
        pg.init()
        
        self.screen_size = self.screen_width, self.screen_height = screen_size
        self.display = pg.display.set_mode(screen_size)
        pg.display.set_caption(title)

        # internal variables
        self.running: bool
        self.events: list

        self.clock = pg.time.Clock()
        self.FPS = fps

        self.master_panel = MasterControlPanel()

        self._init_scenes()
    
    def populate_scenes(self, scenes: list[Scene], initial_scene_name: str):
        for scene in scenes:
            self.scenes[scene().name] = scene
        
        self.current_scene: Scene = self.scenes[initial_scene_name]()

    def _init_scenes(self):
        self.scenes = {}
        self.current_scene: Scene = None
    
    def add_scene(self, scene: Scene):
        if self.current_scene is None:
            self.current_scene = scene
    
    def update(self):
        dt = self.clock.tick(self.FPS) / 1000  # divide by 1000 to get seconds since last call
        self.master_panel.update(dt, self.events)

        self.current_scene.update(self.master_panel)

        if self.current_scene.change_scenes:
            new_scene = self.current_scene.next_scene
            self.master_panel.stop_music()
            
            self.current_scene.unload()
            self.current_scene = self.scenes[new_scene](self.master_panel)
            self.current_scene.load()

    def check_events(self):
        self.events = pg.event.get()
        for event in self.events:
            if event.type == pg.QUIT:
                self.running = False


    def draw(self):
        self.display.fill((255, 255, 255))

        self.current_scene.draw(self.display, self.master_panel)

        pg.display.update()

    async def _run(self):
        self.running = True
        while self.running:
            self.check_events()
            self.update()
            self.draw()

            await asyncio.sleep(0)

    def start(self):
        if self.current_scene is None:
            raise Exception("No initial scene was defined.")

        asyncio.run(self._run())
