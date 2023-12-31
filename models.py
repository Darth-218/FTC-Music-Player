"""
Some general classes that are neither data or to do with communicating
with the API.
"""

from data_models import *
from player_handlers import *
from enum import Enum, auto
from typing import Callable, Any
import vlc


class Queue:
    """
    Class representing a song queue with methods for interacting with
    it, for example jumping to the next song, etc.
    """

    song_list: list[Song] = []
    current: Song
    curr_index: int = 0
    elapsed: timedelta = timedelta(0)
    position: float = 0
    duration: timedelta = timedelta(0)

    def __init__(
        self,
        song_list: list[Song] = [],
        curr_index: int = 0,
    ):
        self.current = (
            song_list[curr_index]
            if song_list
            else Song("No Song Selected", Artist("FTC"), "./none", timedelta(seconds=0))
        )
        self.song_list = song_list

    def _reset(self):
        self.position = 0
        self.current = self.song_list[self.curr_index]
        self.duration = self.current.duration

    def next(self):
        """Go to the next song in the queue. If we're already at the
        last song, reset the current state but otherwise do nothing.
        """
        if self.curr_index == len(self.song_list) - 1:
            self._reset()
            return
        self.curr_index += 1
        self._reset()

    def prev(self):
        """Go to the previous song in the queue. If we're already at the
        first song, reset the current state but otherwise do nothing.
        """
        if self.curr_index == 0:
            self._reset()
            return
        self.curr_index -= 1
        self._reset()

    def add_song(self, song: Song):
        """Add a song to the queue.

        - `song` -- A `Song` object to add to the end of the queue.
        """
        self.song_list.append(song)

    def play_next(self, song: Song):
        """Insert a song into the queue to be played directly after
        the current song.

        - `song` -- A `Song` object to insert to the queue.
        """
        self.song_list.insert(self.curr_index + 1, song)


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
    handlers: dict[HandlerType, Callable[[], None]]
    player: Any | None
    state: PlayerState

    def __init__(self, handlers, queue):
        self.queue = queue
        self.handlers = handlers
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

    def stop(self):
        """Stop playing the current song."""
        self.player.stop() if self.player else lib.passive()

    def change_queue(self, queue: Queue):
        """Swap the current queue of songs to another one."""
        self.queue = queue

    def add_to_queue(self, song: Song):
        """Add a song to the current queue."""
        self.queue.add_song(song)


class VlcMediaPlayer(Player):
    """
    A player that uses VLC to play audio.
    """

    player: vlc.MediaPlayer | None

    def __init__(self, handlers: dict[HandlerType, Callable[[], None]], queue: Queue):
        super().__init__(handlers, queue)
        self.player = vlc.MediaPlayer(self.queue.current._path)

    def play(self):
        self.state = PlayerState.playing
        current = self.queue.current
        self.player = vlc.MediaPlayer(current._path)
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
        self.handlers.get(HandlerType.on_source_changed, lib.passive)

    def _add_handler(self, handler: Callable[[], None], type: HandlerType):
        self.handlers[type] = handler
