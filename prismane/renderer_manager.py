import pygame as pg
import pygame._sdl2 as sdl2

from .element import Element

class RendererManager(Element):
    def __init__(self) -> None:
        super().__init__(singleton=True)
        self.queue: dict[str, list] = {}
        self.order: int = 0

        self.targets: dict[str, sdl2.Renderer] = {}

    def clear(self):
        self.order = 0
        for target_name in self.queue.keys():
            self.queue[target_name] = []

    def queue_draw(self, surface: pg.Surface, z: int, target: str, pos):
        """
        surface: pygame.Surface. The image to be drawn.
        z: int. z-index of the object. Lower values increase the draw priority
        Used by objects to "queue" themselves into the drawing queue, after which they will be drawn alongside every other element
        """
        if target not in self.queue:
            self.queue[target] = []

        self.queue[target].append([z, self.order, surface, pos])
        self.order += 1

    def register_renderer(self, renderer: sdl2.Renderer, name: str):
        self.targets[name] = renderer

    def destroy_renderer(self, name: str):
        if name in self.targets:
            del self.targets[name]

    def draw(self):
        """
        targets: dict[str, pygame.Surface]. A dictonary with keys being the target name and the surface (target meaning where to draw)
        Draws everything queued so far. Should be called once per frame.
        """
        for target_name, target in self.targets.items():
            if target_name in self.queue:
                self.queue[target_name].sort(key = lambda x:x[0])
                for sprite in self.queue[target_name]:
                    target.blit(sprite[2], sprite[3])
