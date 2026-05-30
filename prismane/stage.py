from .entity import EntityGroup, Entity
from .element import Element
from .event import Event


class Stage(Element):
    """
    Stages are my implementation of states for a game. A given stage oversees all objects currently loaded.
    Each scene can also implement custom behaviour for certain elements (e.g. if the player reaches 0 health, change the scene)
    """
    def __init__(self):
        super().__init__(singleton=True, name="CurrentStage")  # each stage should be a singleton

        self.singletons: dict[str, Entity] = {}
        self.groups: dict[str, EntityGroup] = {}
        self.events: list[Event] = []

        self.queue: list[EntityGroup] = []
        self.locked = True

        self.change_stages = False
        self.next_stage: str

    def add_singleton(self, name: str, entity: Entity):
        self.singletons[name] = entity

    def populate_group(self, group: str, *entities: Entity):
        self.groups[group] = EntityGroup(*entities)

    def add_to_group(self, group: str, entity: Entity):
        self.groups[group].add(entity)

    def populate_events(self, *events: Event):
        self.events = [*events]

    def add_event(self, event: Event):
        self.events.append(event)

    def queue_next_stage(self, next_scene_name):
        self.change_stages = True
        self.next_stage = next_scene_name
    
    def load(self):
        pass

    def unload(self):
        pass

    def update(self):
        for group in self.groups.values():
            group.update()

        for singleton in list(self.singletons.values()):
            singleton.update()

        for event in self.events[::-1]:
            event.update()
            if event.inactive:
                self.events.remove(event)


    def draw(self):
        self.element_tree["Renderer"].clear()
        for singleton in self.singletons.values():
            singleton.draw()

        for group in self.groups.values():
            group.draw()

        self.element_tree["Renderer"].draw()

    def clear(self):
        window = self.element_tree["Engine"].window
        display = self.element_tree["Engine"].display
        display.image.fill("black")
        window.fill("black")
