#!/usr/bin/env python3
import flet as ft
from datetime import timedelta
from threading import Timer
from enum import Enum, auto
from typing import Callable, Any
from data_models import *
import lib
import vlc


class PlayerState(Enum):
    """An enumeration representing the current state of the player."""

    playing = auto()
    paused = auto()
    finished = auto()
    not_started = auto()


class Player:
    """
    Abstract class to represent a music player, i.e., an API to
    communicate with an external audio playing application from within
    the program.

    - `queue` -- A `Queue` object representing the queue of songs the
    player will play when prompted.
    - `handlers` -- A dict of handler functions to interact with the
    UI.
    - `player` -- The actual player object that will allow us to
    communicate with whatever external library we use to play audio.
    """

    queue: Queue
    # handlers: dict[HandlerType, Callable[[], None]]
    player: Any | None
    state: PlayerState

    def __init__(self, queue):
        self.queue = queue
        self.state = PlayerState.not_started

    def play(self):
        """Start playing the current song at the current elapsed time."""

        self.state = PlayerState.playing
        raise NotImplementedError

    def pause(self):
        """Pause playing the current song."""
        match self.state:
            case PlayerState.playing:
                self.state = PlayerState.paused
            case PlayerState.paused:
                self.state = PlayerState.playing
        self.player.pause() if self.player else lib.passive()

    def next(self):
        """Skip the rest of the current song and move to the next one in
        the queue.
        """
        raise NotImplementedError

    def prev(self):
        """Stop playing the current song and return to the previous one
        in the queue.
        """
        raise NotImplementedError

    def seektime(self, time: timedelta):
        """Jump to a specific time stamp in the current song."""
        raise NotImplementedError

    def seekpos(self, pos: float):
        """Jump to a specific position in the current song."""
        raise NotImplementedError

    def getpos(self) -> float:
        return self.player.get_position() if self.player else lib.passive()

    def gettime(self) -> int:
        return self.player.get_time() if self.player else lib.passive()

    def getpos(self) -> float:
        return self.player.get_position() if self.player else lib.passive()

    def stop(self):
        """Stop playing the current song."""
        self.player.stop() if self.player else lib.passive()

    def change_queue(self, queue: Queue):
        """Swap the current queue of songs to another one."""
        self.queue = queue
        lib.logger("Player/change_queue", f"Selected index: {queue.curr_index}")
        self.queue._reset()

    def add_to_queue(self, song: Song):
        """Add a song to the current queue."""
        self.queue.add_song(song)


class VlcMediaPlayer(Player):
    """
    A player that uses VLC to play audio.
    """

    player: vlc.MediaPlayer | None

    def __init__(self, queue: Queue):
        super().__init__(queue=queue)
        self.player = vlc.MediaPlayer(self.queue.current._path)

    def play(self):
        self.state = PlayerState.playing
        current = self.queue.current
        try:
            current_path = current.get_path()
        except Exception as e:
            raise e
        self.player = vlc.MediaPlayer(current.get_path())
        lib.logger(
            "VlcMediaPlayer/play", f"Now playing {current.name}.\nFrom {current._path}."
        )
        self.player.play() if self.player else lib.passive()

    def next(self):
        self.player.stop() if self.player else lib.passive()
        self.queue.next()
        self.play()

    def prev(self):
        self.player.stop() if self.player else lib.passive()
        self.queue.prev()
        self.play()

    def seektime(self, time: timedelta):
        pos = lib.calc_pos(self.queue.duration, time)
        self.seekpos(pos)

    def seekpos(self, pos):
        self.player.set_position(pos) if self.player else lib.passive()

    def _change_song(self, queue: Queue):
        self.player.stop() if self.player else lib.passive()
        self.queue = queue
        self.play()

class PlayerWidget(ft.UserControl):
    """A Player widget at the bottom of the screen having buttons
    for playing/pausing, skipping forwards and backwards, shuffling etc.
    as well as a slider for the current song.
    """

    btn_shuffle: ft.IconButton
    btn_prev: ft.IconButton
    btn_play_pause: ft.IconButton
    btn_next: ft.IconButton
    btn_repeat: ft.IconButton
    slider: ft.Slider
    repeating_song: bool | None

    def __init__(self, player: Player):
        super().__init__()
        self.player = player

    def build(self):
        self.bgcolor = "#000000"
        self.padding = ft.Padding(0, 0, 0, 10)

        self.btn_shuffle = ft.IconButton(
            icon=ft.icons.SHUFFLE, on_click=self.shuffle, icon_size=40
        )
        self.btn_prev = ft.IconButton(
            icon=ft.icons.SKIP_PREVIOUS,
            on_click=lambda e: self.player.prev(),
            icon_size=40,
        )
        self.btn_play_pause = ft.IconButton(
            icon=ft.icons.PLAY_CIRCLE, on_click=self.play_pause, icon_size=40
        )
        self.btn_next = ft.IconButton(
            icon=ft.icons.SKIP_NEXT, on_click=lambda e: self.player.next(), icon_size=40
        )
        self.btn_repeat = ft.IconButton(icon=ft.icons.REPEAT, on_click=self.toggle_repeat, icon_size=40)
        self.slider = ft.Slider(min=0.0, max=1.0, on_change=self.slider_seek, value=0.0)
        return ft.Container(
            bgcolor="#000000",
            content=ft.Column(
                controls=[
                    ft.Container(self.slider, width=500, alignment=ft.alignment.center),
                    ft.Row(
                        controls=[
                            self.btn_shuffle,
                            self.btn_prev,
                            self.btn_play_pause,
                            self.btn_next,
                            self.btn_repeat,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.alignment.center,
                        expand=False,
                    ),
                ],
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.alignment.center,
            ),
        )

    def play_pause(self, event=None) -> None:
        """Toggles the player's currently paused/resumed state."""
        match self.player.state:
            case PlayerState.playing:
                self.player.pause()
                setattr(self.btn_play_pause, "icon", ft.icons.PLAY_CIRCLE)
            case PlayerState.paused:
                self.player.pause()
                setattr(self.btn_play_pause, "icon", ft.icons.PAUSE_CIRCLE)
        self.update()

    def play(self):
        setattr(self.btn_play_pause, "icon", ft.icons.PAUSE_CIRCLE)
        self.player.stop()
        try:
            self.player.play()
        except Exception as e:
            setattr(self.page.dialog, 'modal', False)
            setattr(self.page.dialog, 'title', ft.Text("Error"))
            setattr(self.page.dialog, 'content', ft.Text(e))
            setattr(self.page.dialog, 'open', True)
            self.page.update()
        if self.player.state == PlayerState.not_started:
            self.update_slider()

    def pause(self):
        self.play_pause()

    def update_slider(self):
        Timer(0.2, self.update_slider).start()
        current_position = self.player.getpos()
        if current_position == self.slider.value:
            return
        setattr(self.slider, "value", current_position)
        # current_time_in_ms = self.player.gettime()
        # current_time = timedelta(milliseconds=current_time_in_ms)
        # lib.logger("PlayerWidget/update_slider", f"Updating to {current_time}")
        if self.slider.value == 1:
            match self.repeating_song:
                case None:
                    if (
                        self.player.queue.curr_index
                        != len(self.player.queue.song_list) - 1
                    ):
                        self.player.next()
                    else:
                        self.player.state = PlayerState.finished
                case False:
                    if (
                        self.player.queue.curr_index
                        != len(self.player.queue.song_list) - 1
                    ):
                        self.player.next()
                    else:
                        self.player.queue.curr_index = 0
                        self.play()
                case True:
                    self.slider_seek(val=0)
        self.update()

    def slider_seek(self, e=None, val=None):
        new_val = e.control.value if e else val
        self.player.seekpos(new_val)
        current_time_in_ms = self.player.gettime()
        current_time = timedelta(milliseconds=current_time_in_ms)
        lib.logger("PlayerWidget/slider_seek", f"Moved to {current_time}")

    def shuffle(self, e=None):
        self.player.queue.shuffle()

    def toggle_repeat(self, e=None):
        match self.repeating_song:
            case None:
                self.repeating_song = False
                setattr(self.btn_repeat, 'icon', ft.icons.REPEAT_ON)
            case False:
                self.repeating_song = True
                setattr(self.btn_repeat, 'icon', ft.icons.REPEAT_ONE_ON)
            case True:
                self.repeating_song = None
                setattr(self.btn_repeat, 'icon', ft.icons.REPEAT)
        self.update()
