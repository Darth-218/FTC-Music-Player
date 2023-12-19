#!/bin/python
from time import sleep
from models import *
import ui_builder

player = VlcMediaPlayer({}, queue=Queue([]))

interface = ui_builder.UI(player=player)