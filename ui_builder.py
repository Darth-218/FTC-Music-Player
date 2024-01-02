"""Initialise the GUI window.
"""
import flet as ft
import ui_widgets as uiWidgets
import player


class UI:
    """Initialise the GUI window.
    """

    def __init__(self, player: player.Player) -> None:
        self.player = player # The player that will play all audio.
        ft.app(self.open_home) # Open the home page.

    def open_home(self, page: ft.Page):
        page.theme_mode = ft.ThemeMode.DARK
        page.bgcolor = ft.colors.BLACK
        page.fonts = {"lilitaone": "./Assets/Fonts/LilitaOne-Regular.ttf"} # Add the Lilita One font to the page.
        page.add(uiWidgets.Home(self.player)) # Add the home page to the window.
        page.bottom_appbar = ft.BottomAppBar(
            uiWidgets.PlayerWidget(self.player),
            height=120,
            padding=ft.Padding(top=0, bottom=0, left=0, right=0),
        ) # Add the player widget to the bottom app bar.
        page.dialog = ft.AlertDialog(title=ft.Text(''), content=ft.Text('')) # Add the alert dialog to the page.
        page.update() # Update the page.


