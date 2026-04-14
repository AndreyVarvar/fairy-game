import pygame as pg

from .element import Element

# I swear this wasn't stolen
class Renderer(Element):
    def __init__(self) -> None:
        super().__init__(singleton=True)
        self.queue: dict[str, list] = {
            "window": []
        }

        self.order: int = 0

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

    def draw(self, targets: dict[str, pg.Surface]):
        """
        targets: dict[str, pygame.Surface]. A dictonary with keys being the target name and the surface (target meaning where to draw)
        Draws everything queued so far. Should be called once per frame.
        """
        for target_name, target in targets.items():
            if target_name in self.queue:
                self.queue[target_name].sort(key = lambda x:x[0])
                for sprite in self.queue[target_name]:
                    target.blit(sprite[2], sprite[3])

