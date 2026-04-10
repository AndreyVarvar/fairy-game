import pygame as pg


class MasterControlPanel():
    def __init__(self):
        self.game_panel = GameControlPanel()
        self.input_panel = InputControlPanel()
        self.sound_panel = SoundControlPanel()
        self.music_panel = MusicControlPanel()

    def update(self, dt: float, events):
        self.game_panel.update(dt)
        self.input_panel.update(events)
        self.sound_panel.update()
        self.music_panel.update(dt)


class GameControlPanel():
    def __init__(self):
        self.run_time = 0
        self.dt: float

    def update(self, dt):
        self.dt = dt
        self.run_time += dt


class InputControlPanel():
    def __init__(self):
        self.keys_pressed = pg.key.get_pressed()
        self.keys_just_pressed = pg.key.get_pressed()

        self.mouse_pressed: list[bool] = [False, False, False]
        self.mouse_just_pressed: list[bool] = [False, False, False]
        self.mouse_just_released: list[bool] = [False, False, False]
        self.mouse_click_pos: list[int] = [0, 0]
        self.mouse_release_pos: list[int] = [0, 0]
        self.mouse_pos: list[int] = [0, 0]

        self.cursor_queue = []

    def update(self, events: list[pg.Event]):
        self.keys_pressed = pg.key.get_pressed()
        self.keys_just_pressed = []

        self.mouse_just_pressed = [False, False, False]
        self.mouse_just_released = [False, False, False]
        
        self.mouse_pos = pg.mouse.get_pos()

        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                self.mouse_pressed[event.button-1] = True
                self.mouse_just_pressed[event.button-1] = True
            elif event.type == pg.MOUSEBUTTONUP:
                self.mouse_pressed[event.button-1] = False
                self.mouse_just_released[event.button-1] = True
            elif event.type == pg.KEYDOWN:
                self.keys_just_pressed.append(event.key)

        if self.mouse_just_pressed[0]:
            self.mouse_click_pos = pg.mouse.get_pos()
        
        if self.mouse_just_released[0]:
            self.mouse_release_pos = pg.mouse.get_pos()
        
        if len(self.cursor_queue) == 0:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        else:
            pg.mouse.set_cursor(self.cursor_queue[0])
            self.cursor_queue.clear()
    
    def queue_cursor(self, cursor: pg.Cursor):
        self.cursor_queue.append(cursor)

    def consume_mouse_click(self):
        self.mouse_just_pressed = [False, False, False]
        

class SoundControlPanel():
    def __init__(self):
        self.sound_queue = []
        self.channel_count = pg.mixer.get_num_channels()

        self.volume = 1
        self.mute = False

    def update(self):
        self.mute = (self.volume == 0)

    def queue_sound(self, sound: pg.Sound, channel_id:int=0, volume:float=1.0, polite:bool=False, loops:int=0):
        """Queues a sound to be played next frame.

        Args:
            sound (pygame.Sound): pygame.Sound instance to be played.
            channel_id (int, optional): ID of the channel the sound should be played in. Defaults to 0.
            volume (float, optional): Sound volume. Ranges from 0.0 to 1.0. Defaults to 1.0.
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

    def play_sound_queue(self) -> pg.Sound:
        for _ in range(len(self.sound_queue)):
            sound, channel, volume, polite, loops = self.sound_queue.pop(0)
            sound.set_volume(volume * self.volume)

            if polite:
                if pg.mixer.Channel(channel).get_busy():
                    continue
            
            pg.mixer.Channel(channel).play(sound, loops=loops)

    def clear_sound_queue(self):
        self.sound_queue.clear()
        

class MusicControlPanel():
    def __init__(self):
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
