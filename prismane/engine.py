import pygame as pg
from .panels import MasterControlPanel
from .stage import Stage
from .renderer import Renderer
from .element import Element

import asyncio

class Engine(Element):
    def __init__(self, fps: int = 60):
        super().__init__(singleton=True)

        pg.mixer.pre_init(buffer=2048)
        pg.init()

        # TODO: make self.window for the shenanigans with resizing or whatever
        self.window: pg.Window = None
        self.display: pg.Surface

        # internal variables
        self.running: bool
        self.events: list

        self.clock = pg.time.Clock()
        self.FPS = fps

        self.master_panel = MasterControlPanel()

        self.renderer = Renderer()

        self.stages = {}
        self.current_stage: Stage = None
        self.starting_stage: str = None

    def populate_stages(self, stages: dict[str, type[Stage]], initial_stage_name: str):
        self.stages = stages
        self.starting_stage = initial_stage_name

    def create_window(
        self, 
        title: str = "Prismane Window",
        size: tuple[int, int] = (640, 480),
        position: int | tuple[int, int] = pg.WINDOWPOS_CENTERED,
        fullscreen: bool = False,
        fullscreen_desktop: bool = False,
        opengl: bool = False,
        vulkan: bool = False,
        hidden: bool = False,
        borderless: bool = False,
        resizable: bool = False,
        minimized: bool = False,
        maximized: bool = False,
        mouse_grabbed: bool = False,
        keyboard_grabbed: bool = False,
        input_focus: bool = False,
        mouse_focus: bool = False,
        allow_high_dpi: bool = False,
        mouse_capture: bool = False,
        always_on_top: bool = False,
        utility: bool = False
    ):
        window = pg.Window(
            title=title,
            size=size,
            position=position,
            fullscreen=fullscreen,
            fullscreen_desktop=fullscreen_desktop,
            opengl=opengl,
            vulkan=vulkan,
            hidden=hidden,
            borderless=borderless,
            resizable=resizable,
            minimized=minimized,
            maximized=maximized,
            mouse_grabbed=mouse_grabbed,
            keyboard_grabbed=keyboard_grabbed,
            input_focus=input_focus,
            mouse_focus=mouse_focus,
            allow_high_dpi=allow_high_dpi,
            mouse_capture=mouse_capture,
            always_on_top=always_on_top,
            utility=utility,
        )

        if self.window is None:
            self.window = window
        else:
            # TODO: support for multiple windows
            print("Newly created window was ignored. No implementation for handling multiple windows has been implemented.")

    def update(self):
        dt = self.clock.tick(self.FPS) / 1000  # divide by 1000 to get seconds since last call
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
        self.window.flip()

    async def run(self):
        self.running = True
        while self.running:
            self.check_events()
            self.update()
            self.draw()

            await asyncio.sleep(0)

    def start(self):
        if self.window is None:
            raise Exception("No window was created.")

        if self.starting_stage is None:
            raise Exception("No initial stage was defined.")

        self.display = self.window.get_surface()
        self.current_stage = self.stages[self.starting_stage]()

        asyncio.run(self.run())
