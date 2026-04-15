from .entity import EntityGroup, Entity
from .element import Element


class Stage(Element):
    """
    Stages are my implementation of states for a game. A given stage oversees all objects currently loaded.
    Each scene can also implement custom behaviour for certain elements (e.g. if the player reaches 0 health, change the scene)
    """
    def __init__(self):
        super().__init__(singleton=True, name="CurrentStage")  # each stage should be a singleton

        self.groups: dict[str, EntityGroup] = {}

        self.change_stages = False
        self.next_stage: str

    def populate_group(self, group: str, *entities: Entity):
        self.groups[group] = EntityGroup(*entities)

    def queue_next_stage(self, next_scene_name):
        self.change_stages = True
        self.next_stage = next_scene_name
    
    def load(self):
        pass

    def unload(self):
        pass

    def update(self):
        for group in self.groups:
            for entity in self.groups[group]:
                entity.update()

    def draw(self):
        self.element_tree["Renderer"].clear()
        for group in self.groups:
            for entity in self.groups[group]:
                entity.queue_draw()

