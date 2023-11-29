"""
Some general classes that are neither data or to do with communicating
with the API.
"""

from data_models import *
import time
import vlc


class Queue():
    """
    Class representing a queue of songs.
    """

    song_list: list[Song]
    current: Song
    curr_index: int
    elapsed: timedelta
    position: float
    duration: timedelta

    def __init__(self):
        lib.TODO("Queue/init")

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


class VlcMediaPlayer(Player):
    """
    A player that uses vlc to play songs.
    """

    player: vlc.MediaPlayer

    def __init__(self, queue):
        self.queue = queue
        self.player = vlc.MediaPlayer(queue.current._path)

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
