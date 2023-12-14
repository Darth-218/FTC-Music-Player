import flet as ft
import api_client.Youtube.api_models as yt_models

class SongWidget(ft.TextButton):
    def __init__(self, song: yt_models.OnlineSong):
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
    def __init__(self, song: yt_models.OnlineSong):
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
        )