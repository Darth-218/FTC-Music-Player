"""Initialise the GUI window.
"""
import flet as ft
# import ui_widgets as uiWidgets
import ui_widgets_test as uiWidgets
import models


class UI:
    """Initialise the GUI window.
    """

    def __init__(self, player: models.Player) -> None:
        self.player = player # The player that will play all audio.
        ft.app(self.open_home) # Open the home page.

    def open_home(self, page: ft.Page):
        page.fonts = {"lilitaone": "./Assets/Fonts/LilitaOne-Regular.ttf"} # Add the Lilita One font to the page.
        page.add(uiWidgets.Home(self.player)) # Add the home page to the window.
        page.bottom_appbar = ft.BottomAppBar(
            uiWidgets.PlayerWidget(self.player, page),
            height=120,
            padding=ft.Padding(top=0, bottom=0, left=0, right=0),
        ) # Add the player widget to the bottom app bar.
        page.update() # Update the page.

        # page.add(uiWidgets.Home(self.player, page=page))
        # page.bottom_appbar = ft.BottomAppBar(
        #     uiWidgets.PlayerWidget(self.player, page),
        #     height=120,
        #     padding=ft.Padding(top=0, bottom=0, left=0, right=0),
        # )
        # page.update()
        # page.controls[0].onContentChange(0)
