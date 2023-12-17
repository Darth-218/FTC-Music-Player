#!/bin/python
from time import sleep
from models import *

ahti = Artist("Ahti")
sanpath = \
"/mnt/c/users/zeinh/Desktop/d/songs/OST Control - Sankarin Tango (Finnish Tango) (320 kbps).mp3"
sankarin = Song(
    "Sankarin Tango",
    ahti,
    sanpath,
    timedelta(minutes=3, seconds=19)
)
ahti.songs.append(sankarin)

imagine = Artist("Imagine Dragons")
imapath = \
"/mnt/c/Users/zeinh/Desktop/D/songs/radioactive but every lyric is i'm waking up.mp3"
radioactive = Song("Radioactive", imagine, imapath, timedelta(seconds=57))
imagine.songs.append(radioactive)

carly = Artist("Carly Rae")
thuspath = \
"/mnt/c/Users/zeinh/Desktop/D/songs/thus spoke carly rae.mp3"
thus = Song(
    "Thus Spoke Carly Rae",
    carly,
    thuspath,
    timedelta(minutes=3, seconds=17)
)
carly.songs.append(thus)

queue = Queue([sankarin, radioactive, thus])

player = VlcMediaPlayer({}, queue)

player.play()
sleep(player.queue.current.duration.total_seconds() // 2)

player.next()

player.play()
sleep(player.queue.current.duration.total_seconds() // 2)

player.next()

player.play()
sleep(player.queue.current.duration.total_seconds() // 2)

player.stop()
