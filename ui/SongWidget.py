import flet as ft
import api_client.Youtube.api_models as yt_models
import data_models as dm
import flet_audio_player as fap
import Main_UI

class SongWidget(ft.TextButton):
    def __init__(self, song: dm.Song, songList: list[dm.Song]):
        self.songList: list[dm.Song] = songList
        super().__init__(content=ft.Container(content=ft.Row(
                    [
                        ft.Image(src=song.cover_art, width=100, height=100, border_radius=15, fit=ft.ImageFit.COVER),
                        ft.Column(controls=[
                            ft.Text(song.name),
                            ft.Text(song.duration),
                            ]
                        ),
                    ],
                ),
                padding=ft.Padding(top=10, bottom=10, left=0, right=0),
            ),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25),),
        )

class SquareSongWidget(ft.TextButton):
    def __init__(self, song: yt_models.OnlineSong, songList: list[dm.Song]):
        self.song: yt_models.OnlineSong = song
        self.songList: list[dm.Song] = songList
        
        super().__init__(content=ft.Container(content=ft.Column(
                    [
                        ft.Image(src=song.cover_art, width=150, height=150, border_radius=15, fit=ft.ImageFit.COVER),
                        ft.Column(controls=[
                            ft.Text(song.name, text_align=ft.TextAlign.CENTER, no_wrap=True, overflow=ft.TextOverflow.FADE),
                            ft.Text(song.duration),
                            ]
                        ),
                    ],
                    alignment=ft.alignment.center,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.Padding(top=10, bottom=10, left=0, right=0),
                alignment=ft.alignment.center,
            ),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25),),
            width=170,
            on_click=self.onSongClicked,
        )

    def onSongClicked(self, e):
        print(self.song.name)
        queue = fap.Queue(self.songList, self.songList.index(self.song))
        Main_UI.player.configPlayer(queue)
        Main_UI.player.player.update()
        Main_UI.player.resume()
        Main_UI.player.pause()


