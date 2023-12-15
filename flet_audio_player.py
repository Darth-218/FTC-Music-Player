import flet as ft
from datetime import timedelta
import models
import data_models as dm
import api_client.Youtube.api_models as yt_models
import api_client.Youtube.youtube as yt

class Queue():
    songs: list[dm.Song]
    current: yt_models.OnlineSong
    curr_index: int = 0

    def __init__(self, songs: list[dm.Song], selectedIndex: int = 0):
        self.songs = songs
        self.curr_index = selectedIndex
        self.current = songs[selectedIndex]
        self.getPath()

    def next(self):
        if self.curr_index == len(self.songs) - 1:
            self.curr_index = 0
        else:
            self.curr_index += 1
        self.current = self.songs[self.curr_index]
        self.getPath()

    def prev(self):
        if self.curr_index == 0:
            self.curr_index = len(self.songs) - 1
        else:
            self.curr_index -= 1
        self.current = self.songs[self.curr_index]
        self.getPath()

    def getPath(self):
        if type(self.current) is yt_models.OnlineSong:
            response = yt.getSongUrl(self.current.id)
            if not response.has_error:
                self.current._path = response.url
            else:
                print(response.error)


class FletAudioPlayer():
    playerState = 'stopped'
    queue: Queue
    duration: timedelta
    position: timedelta
    onStateChangedHandlers: list[callable] = []
    onPositionChangedHandlers: list[callable] = []
    
    def __init__(self):
        self.player = ft.Audio(volume=1, autoplay=True, src="https://rr3---sn-t0a7ln7d.googlevideo.com/videoplayback?expire=1702665534&ei=3kh8ZenALpm9_9EPsdqR2A0&ip=158.69.27.152&id=o-ANggUaXg2XAweRpS4cAYDxJhseU3ye66rsI0pSgMiwAn&itag=139&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&mh=1T&mm=31%2C29&mn=sn-t0a7ln7d%2Csn-t0a7sn7d&ms=au%2Crdu&mv=m&mvi=3&pl=24&pcm2=no&vprv=1&mime=audio%2Fmp4&gir=yes&clen=23169298&dur=3799.527&lmt=1693635632243331&mt=1702643880&fvip=1&keepalive=yes&fexp=24007246&c=ANDROID_TESTSUITE&txp=4532434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cpcm2%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AJfQdSswRgIhAIRtq0fokKGxezf3BBp7vGOxAy5BBHNDR1svqmJXE5W_AiEA9UI59xrVkxxrQIXs6H8J1t_eWIwACmsxtSsjtHH8AJ4%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl&lsig=AAO5W4owRQIhAJn4LANpBUu04UUerzuCxK-W3oWI4I8nNgIMUzGpp3rJAiBZ7nUL3S1EqRrzQYehffKsUxVa2lcg8NrgkDwD2OrUWA%3D%3D")
        self.player.on_state_changed = lambda e: self.stateChangedHandler(e.data)

    def stateChangedHandler(self, data):
        self.playerState = data
        for handler in self.onStateChangedHandlers:
            handler(data)

    def positionChangedHandler(self, data):
        self.position = data
        for handler in self.onPositionChangedHandlers:
            handler(data)

    def addStateChangedHandler(self, handler: callable):
        self.onStateChangedHandlers.append(handler)

    def addPositionChangedHandler(self, handler: callable):
        self.onPositionChangedHandlers.append(handler)

    def configPlayer(self, queue: Queue):
        self.queue = queue
        self.player.src = queue.current._path
        self.player.update()
        print(self.player.src)
        # self.player.play()

    def pause(self):
        self.player.pause()
        self.playerState = 'paused'

    def resume(self):
        self.player.resume()
        self.playerState = 'playing'



# def main(page: ft.Page):
#     page.add(ft.Container(content=ft.ProgressRing(), alignment=ft.alignment.center, expand=True))
#     request = yt_models.SearchRequest(query="Jacob's Piano", artist_count=3, album_count=3, song_count=10)
#     results = yt.search(request=request)
#     queue = Queue(songs=results.songs)
#     # print(queue.current.name)
#     # print(queue.current._path)
#     player = FletAudioPlayer()
#     page.overlay.append(player.player)
#     page.update()
#     player.startPlayer(queue=queue)
#     while True:
#         cmd = input("Enter a command:")

#         if cmd == "p":
#             player.pause()
#             print(player.playerState)
#         elif cmd == "r":
#             player.resume()
#             print(player.playerState)

# ft.app(target=main)
