from .entity import EntityGroup, Entity
from .element import Element


class Stage(Element):
    def __init__(self):
        super().__init__(singleton=True)  # each stage should be a singleton

        self.groups: dict[str, EntityGroup] = {}

        self.change_scenes = False
        self.next_scene: str

    def populate_group(self, group: str, *entities: Entity):
        self.groups[group] = EntityGroup(*entities)

    def queue_next_scene(self, next_scene_name):
        self.change_scenes = True
        self.next_scene = next_scene_name
    
    def load(self):
        pass

    def unload(self):
        pass

    def update(self):
        for group in self.groups:
            for entity in self.groups[group]:
                entity.update()

    def draw(self):
        for group in self.groups:
            for entity in self.groups[group]:
                entity.queue_draw()

