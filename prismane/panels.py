import pygame as pg
from .element import Element
from .display import Display


class MasterControlPanel(Element):  # used to update all the panels in one place
    def __init__(self):
        super().__init__(singleton=True)
        self.time_panel = TimeControlPanel()
        self.input_panel = InputControlPanel()
        self.sound_panel = SoundControlPanel()
        self.music_panel = MusicControlPanel()

    def update(self, dt: float, events):
        self.time_panel.update(dt)
        self.input_panel.update(events)
        self.sound_panel.update()
        self.music_panel.update(dt)


class TimeControlPanel(Element):
    def __init__(self):
        super().__init__(singleton=True)
        self.run_time = 0
        self.dt: float

        self.timers: dict[int, tuple[float | int, float | int]] = {}  # tuples of (duration, run_time + duration)
        self.timer_id = 0

    def queue_timer(self, duration: float | int) -> int:
        self.timer_id += 1
        self.timers[self.timer_id] = (duration, self.run_time + duration)
        return self.timer_id  # return the timer id so that the object that queued the timer can access the timer later

    def check_timer(self, timer_id: int) -> float:
        """
        timer_id: int. The ID of the timer given when the timer was initialized.
        Returns the remaining time till the end of the timer
        """
        if timer_id not in self.timers:
            return 0.0
        
        return pg.math.clamp(self.timers[timer_id][1] - self.run_time, 0, self.timers[timer_id][0])

    def check_timer_completion(self, timer_id: int) -> float:
        """
        timer_id: int. The ID of the timer given when the timer was initialized.
        Returns the completion percentage of the timer.
        """
        remaining_time = self.check_timer(timer_id)
        if remaining_time == 0.0:
            return 1.0
        
        return 1.0 - remaining_time/self.timers[timer_id][0]

    def fps(self):
        return 1/self.dt

    def update(self, dt):
        self.dt = dt
        self.run_time += dt

        completed_timers_id = []
        for timer_id in self.timers.keys():
            if self.timers[timer_id][1] - self.run_time <= 0:
                completed_timers_id.append(timer_id)
        for id in completed_timers_id:
            del self.timers[id]


class InputControlPanel(Element):
    def __init__(self):
        super().__init__(singleton=True)
        self.keys_pressed = pg.key.get_pressed()
        self.keys_just_pressed = pg.key.get_pressed()

        self.mouse_pressed: list[bool] = [False, False, False]
        self.mouse_just_pressed: list[bool] = [False, False, False]
        self.mouse_just_released: list[bool] = [False, False, False]
        self.mouse_click_pos: pg.Vector2 = pg.Vector2(0, 0)
        self.mouse_release_pos: pg.Vector2 = pg.Vector2(0, 0)
        self.mouse_pos: pg.Vector2 = pg.Vector2(0, 0)

        self.scroll: tuple[int, int] = (0, 0)  # scroll wheel intensity

        self.cursor_queue = []


    def get_scaled_mouse_pos(self) -> pg.Vector2:
        mouse_pos = pg.Vector2(*pg.mouse.get_pos())
        display: Display = self.element_tree["Display"]
        offset = display.pos
        scale = display.scale

        mouse_pos -= offset
        mouse_pos /= scale

        return mouse_pos


    def update(self, events: list[pg.Event]):
        self.keys_pressed = pg.key.get_pressed()
        self.keys_just_pressed = []

        self.mouse_just_pressed = [False, False, False]
        self.mouse_just_released = [False, False, False]
        
        self.mouse_pos = self.get_scaled_mouse_pos()

        for event in events:
            match event.type:
                case pg.MOUSEWHEEL:
                    self.scroll = (event.x, event.y)
                case pg.MOUSEBUTTONDOWN:
                    if event.button <= 3:
                        self.mouse_pressed[event.button-1] = True
                        self.mouse_just_pressed[event.button-1] = True
                case pg.MOUSEBUTTONUP:
                    if event.button <= 3:
                        self.mouse_pressed[event.button-1] = False
                        self.mouse_just_released[event.button-1] = True
                case pg.KEYDOWN:
                    self.keys_just_pressed.append(event.key)

        if self.mouse_just_pressed[0]:
            self.mouse_click_pos = self.get_scaled_mouse_pos()
        
        if self.mouse_just_released[0]:
            self.mouse_release_pos = self.get_scaled_mouse_pos()
        
        if len(self.cursor_queue) == 0:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        else:
            pg.mouse.set_cursor(self.cursor_queue[0])
            self.cursor_queue.clear()
   
    def queue_cursor(self, cursor: int):
        """
        cursor: int. An instance of a pygame system cursor. Example: pygame.SYSTEM_CURSOR_ARROW
        """
        self.cursor_queue.append(cursor)

    def consume_mouse_click(self):
        self.mouse_just_pressed = [False, False, False]
        

class SoundControlPanel(Element):
    def __init__(self):
        super().__init__(singleton=True)
        self.sound_queue = []
        self.channel_count = pg.mixer.get_num_channels()

        self.volume = 1
        self.mute = False

    def update(self):
        self.volume = min(1, max(0, self.volume))
        self.mute = (self.volume == 0)

    def queue_sound(self, sound: pg.mixer.Sound, channel_id: int = 0, volume: float = 1.0, polite: bool = False, loops: int = 0):
        """Queues a sound to be played next frame.

        Args:
            sound (pygame.Sound): pygame.Sound instance to be played.
            channel_id (int, optional): ID of the channel the sound should be played in. Defaults to 0.
            volume (float, optional): Sound volume. Defaults to 1.0.
            polite (bool, optional): Polite sounds will not interupt currently playing sounds. Defaults to False.
            loops (int, optional): How many additional loops to play. Value of -1 indicates the sound is played continuesly. Defaults to 0.

        Raises:
            TypeError: sound is not an instance of pygame.Sound.
        """
        if not isinstance(sound, pg.Sound):
            raise TypeError(f"sound={sound} is not an instance of pygame.Sound")
        if not isinstance(polite, bool):
            raise TypeError(f"polite={polite} is not an instance of bool.")

        self.sound_queue.append((sound, channel_id, volume, polite, loops))

    def stop_channel(self, channel_id):
        pg.mixer.Channel(channel_id).stop()

    def play_sound_queue(self):
        while len(self.sound_queue) > 0:
            sound, channel, volume, polite, loops = self.sound_queue.pop(0)  # FIFO
            sound.set_volume(volume * self.volume)

            if polite and pg.mixer.Channel(channel).get_busy():
                continue
            
            pg.mixer.Channel(channel).play(sound, loops=loops)

    def clear_sound_queue(self):
        self.sound_queue.clear()
        

class MusicControlPanel(Element):
    def __init__(self):
        super().__init__(singleton=True)
        self.music_running = False

        self.fadeout_volume = 1
        self.fadeout_time = 0
        self.fadeout_elapsed_time = 0
        self.fadeout = False

        self.volume = 1
        self.music_set_volume = 1  # volume of the music set when it was set
        self.music_loop = None

    def update(self, dt: float):
        pg.mixer.music.set_volume(self.volume * self.fadeout_volume * self.music_set_volume)

        if self.fadeout:
            self.fadeout_elapsed_time += dt
            self.fadeout_volume = max(0, 1 - self.fadeout_elapsed_time / self.fadeout_time)

            if self.fadeout_elapsed_time >= self.fadeout_time:
                self.fadeout = False
        else:
            self.fadeout_volume = 1

        self.music_running = pg.mixer.music.get_busy()

        if self.music_loop is not None and self.music_running is False:
            self.set_music(self.music_loop, volume=self.music_set_volume)

    def set_music(self, loop_music, intro_music=None, volume=1):
        self.music_loop = loop_music
        self.music_set_volume = volume

        if intro_music is None:
            pg.mixer.music.load(loop_music)
            pg.mixer.music.play(loops=-1)
        else:
            pg.mixer.music.load(intro_music)
            pg.mixer.music.play(loops=0)

    def stop_music(self):
        pg.mixer.music.stop()
        self.music_loop = None

    def fadeout_music(self, fadeout_time):
        self.fadeout = True
        self.fadeout_elapsed_time = 0
        self.fadeout_time = fadeout_time

    def pause_music(self):
        self.volume = 0

    def start_music(self):
        self.volume = 1
