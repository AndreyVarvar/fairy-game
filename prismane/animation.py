from .entity import Entity
from .panels import TimeControlPanel
from .spritesheet import Spritesheet



class Animation(Entity):
    def __init__(self, spritesheet: Spritesheet, fps: float, initial_frame_index: int = 0, loop: bool = True):
        super().__init__()
        self.spritesheet = spritesheet
        self.total_frames = len(self.spritesheet)
        self.fps = fps
        self.loop = loop

        self.end = False

        self.current_frame = initial_frame_index
        self.current_frame_time = 0.0  # sec
        self.spf = 1 / self.fps  # seconds per frame
        
    def reset(self):
        self.current_frame_time = 0.0
        self.current_frame = 0

    def update(self):
        time_panel: TimeControlPanel = self.element_tree["TimeControlPanel"]
        self.current_frame_time += time_panel.dt

        while self.current_frame_time > self.spf:
            self.current_frame += 1
            self.current_frame_time -= self.spf
        
        if self.loop:
            self.end = (self.current_frame >= self.total_frames-1)
            self.current_frame = self.current_frame % self.total_frames
        else:
            self.current_frame = min(self.current_frame, self.total_frames-1)
            self.end = (self.current_frame == self.total_frames-1)
        
    
    def get_frame(self):
        return self.spritesheet[self.current_frame]
