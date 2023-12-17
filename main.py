#!/bin/python
from time import sleep
from models import *
import ui_builder

queue = Queue([])
player = VlcMediaPlayer({}, queue=queue)

interface = ui_builder.UI(player=player)

