import pygame as pg

from prismane import Element

# I swear this wasn't stolen
class Renderer(Element):
    def __init__(self, targets: list[str]) -> None:
        super().__init__(True)
        self.targets = targets + ["window"]
        self.queue: dict[str, list] = {target_name: [] for target_name in self.targets}
        self.order: int = 0

    def clear(self):
        self.order = 0
        for target_name in self.targets:
            self.queue[target_name] = []

    def blit(self, z: int, target: str, surface: pg.Surface, pos):
        self.queue[target].append([z, self.order, surface, pos])
        self.order += 1

    def render(self, targets: dict[str, pg.Surface]):
        for target_name, target in targets.items():
            if target_name in self.queue:
                self.queue[target_name].sort(key = lambda x:x[0])
                for sprite in self.queue[target_name]:
                    target.blit(sprite[2], sprite[3])

