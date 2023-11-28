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

    list: list[Song]
    current: Song
    curr_index: int
    elapsed: timedelta
    duration: timedelta


class Player():
    """
    Abstract class to represent a music player.
    """

    queue: Queue

    def play(self):
        raise NotImplementedError

    def next(self):
        raise NotImplementedError

    def prev(self):
        raise NotImplementedError

    def seek(self, time: timedelta):
        raise NotImplementedError

    
class VlcMediaPlayer(Player):
    """
    A player that uses vlc to play songs.
    """
    
    def play(self):
        """
        Start playing the current song at the current elapsed time.
        """

        current = self.queue.current
        elapsed = self.queue.elapsed

        lib.logger("VlcMediaPlayer/play",
                   f"Now playing {current.name}.")
        player = vlc.MediaPlayer(current._path)
        player.play()
        time.sleep(current.duration.total_seconds() - elapsed.total_seconds())
