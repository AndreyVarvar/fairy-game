import pygame as pg
from .element import Element
from .settings import Settings


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
        self.music_panel.update()


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

        self.just_pressed_anything: bool = False

        self.scroll: tuple[int, int] = (0, 0)  # scroll wheel intensity

        self.cursor_queue = []


    def get_scaled_mouse_pos(self) -> pg.Vector2:
        mouse_pos = pg.Vector2(pg.mouse.get_pos())
        
        settings: Settings = self.element_tree["Settings"]

        # we draw onto screen -> resize to logical_size
        # that means we get mouse coordinates in screen size
        # and have to translate it into logical_size since
        # that is where we operate with it
        # TODO: make sure to account for offests

        mouse_pos.x *= settings.logical_width / settings.window_width
        mouse_pos.y *= settings.logical_height / settings.window_height

        return mouse_pos


    def update(self, events: list[pg.Event]):
        self.keys_pressed = pg.key.get_pressed()
        self.keys_just_pressed = []

        self.mouse_just_pressed = [False, False, False]
        self.mouse_just_released = [False, False, False]

        self.just_pressed_anything = False
        
        self.mouse_pos = self.get_scaled_mouse_pos()

        for event in events:
            match event.type:
                case pg.MOUSEWHEEL:
                    self.scroll = (event.x, event.y)
                case pg.MOUSEBUTTONDOWN:
                    if event.button <= 3:
                        self.just_pressed_anything = True
                        self.mouse_pressed[event.button-1] = True
                        self.mouse_just_pressed[event.button-1] = True
                case pg.MOUSEBUTTONUP:
                    if event.button <= 3:
                        self.mouse_pressed[event.button-1] = False
                        self.mouse_just_released[event.button-1] = True
                case pg.KEYDOWN:
                    self.keys_just_pressed.append(event.key)
                    self.just_pressed_anything = True

        if self.mouse_just_pressed[0]:
            self.mouse_click_pos = self.get_scaled_mouse_pos()

        if self.mouse_just_released[0]:
            self.mouse_release_pos = self.get_scaled_mouse_pos()

        if len(self.cursor_queue) == 0:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        else:
            pg.mouse.set_cursor(self.cursor_queue[0])
            self.cursor_queue.clear()
        # if self.mouse_just_pressed[0]:
        #     print(self.mouse_click_pos)

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
            volume (float, optional): Sound volume (from 0.0 to 1.0). Defaults to 1.0.
            polite (bool, optional): Polite sounds will not interupt currently playing sounds. Defaults to False.
            loops (int, optional): How many additional loops to play. Value of -1 indicates the sound is played repeatedly. Defaults to 0.

        Raises:
            TypeError: sound is not an instance of pygame.Sound.
        """
        if not isinstance(sound, pg.mixer.Sound):
            raise TypeError(f"sound={sound} is not an instance of pygame.Sound")
        if not isinstance(polite, bool):
            raise TypeError(f"polite={polite} is not an instance of bool.")

        self.sound_queue.append((sound, channel_id, volume, polite, loops))

    def stop_channel(self, channel_id: int):
        """
        Stops the channel from playing any sounds, effectively resetting it.

        Arg:
            channel_id (int, mandatory): ID of the channel the sound should be played in. Defaults to 0.
        """
        pg.mixer.Channel(channel_id).stop()

    def play_sound_queue(self):
        """
        This function is supposed to run every frame, playing every sound that was queued in the queue.
        """
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

        self.volume = 1
        self.music_volume = 1  # volume of the music when it was set
        self.music = None

    def update(self):
        pg.mixer.music.set_volume(self.volume * self.music_volume)

    def set_music(self, music, volume=1):
        self.music = music
        self.music_set_volume = volume

        pg.mixer.music.load(music)
        pg.mixer.music.play(loops=-1)

    def stop_music(self):
        pg.mixer.music.stop()
        self.music = None

    def pause_music(self):
        self.volume = 0

    def start_music(self):
        self.volume = 1
