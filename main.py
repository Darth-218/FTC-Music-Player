#!/usr/bin/env python3
"""The main file that will initialise the GUI and start the program process.
It first initialises a "player", which communicates with an external library
to play the actual audio. It then initialises the GUI (graphical user
interface) and starts the program.
"""

from time import sleep
from models import *
import ui_builder
import api_client.Youtube.youtube as yt

if __name__ == "__main__":
    # Initialise the actual audio player (in this case, one based on
    # VLC) that will play all audio throughout the program process.
    player = VlcMediaPlayer({}, queue=Queue([]))

    # Initialise the GUI and start the window.
    interface = ui_builder.UI(player=player)
