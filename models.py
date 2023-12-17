"""
Some general classes that are neither data or to do with communicating
with the API.
"""

from data_models import *
from player_handlers import *
from enum import Enum, auto
from typing import Callable, Any
import vlc

class Queue():
    """
    Class representing a queue of songs.
    """

    song_list: list[Song] = []
    current: Song
    # = Song(name="Test Song",
    #        artist="Test Artist",
    #        duration=timedelta(minutes=8, seconds=15),
    #        path="test path")
    curr_index: int = 0
    elapsed: timedelta = timedelta(0)
    position: float = 0
    duration: timedelta = timedelta(0)

    def __init__(
            self,
            song_list: list[Song] = [],
            curr_index: int = 0,
            ):
        if song_list: self.current = song_list[curr_index]
        self.song_list = song_list


    def _reset(self):
        self.position = 0
        self.current = self.song_list[self.curr_index]
        self.duration = self.current.duration

    def next(self):
        if self.curr_index == len(self.song_list) - 1:
            self._reset()
        self.curr_index += 1
        self._reset()

    def prev(self):
        if self.curr_index == 0:
            self._reset()
        self.curr_index -= 1
        self._reset()

class Player():
    """
    Abstract class to represent a music player.
    """

    queue: Queue
    handlers: dict[HandlerType, Callable[[], None]]
    player: Any | None

    def __init__(self):
        self.queue = Queue()
        self.handlers = {}

    def play(self):
        """
        Start playing the current song at the current elapsed time.
        """
        raise NotImplementedError

    def next(self):
        """
        Skip the rest of the current song and move to the next one in
        the queue.
        """
        raise NotImplementedError

    def prev(self):
        """
        Stop playing the current song and return to the previous one
        in the queue.
        """
        raise NotImplementedError

    def seektime(self, time: timedelta):
        """
        Jump to a specific time stamp in the current song.
        """
        raise NotImplementedError

    def seekpos(self, pos: float):
        """
        Jump to a specific position in the current song.
        """
        raise NotImplementedError

    def stop(self):
        self.player.stop() if self.player else lib.passive()


class VlcMediaPlayer(Player):
    """
    A player that uses vlc to play songs.
    """

    player: vlc.MediaPlayer

    def __init__(self, handlers: dict[HandlerType, Callable[[], None]], queue: Queue):
        super().__init__()
        self.player = vlc.MediaPlayer(self.queue.current._path)
        self.handlers = handlers
        self.queue = queue

    def play(self):
        current = self.queue.current
        lib.logger("VlcMediaPlayer/play",
            f"Now playing {current.name}.")
        self.player.play()

    def next(self):
        self.player.stop()
        self.queue.next()
        self.play()

    def prev(self):
        self.player.stop()
        self.queue.prev()
        self.play()

    def seektime(self, time: timedelta):
        pos = lib.calc_pos(self.queue.duration, time)
        self.seekpos(pos)

    def seekpos(self, pos):
        self.player.set_position(pos)

    def _change_song(self, queue: Queue):
        self.player.stop()
        self.queue = queue
        self.play()
        self.handlers.get(HandlerType.on_source_changed, lib.passive)

    def _add_handler(self, handler: Callable[[], None], type: HandlerType):
        self.handlers[type] = handler


class PlayerState(Enum):
    playing     = auto()
    paused      = auto()
    finished    = auto()
    not_started = auto()
