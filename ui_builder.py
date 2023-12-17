import flet as ft
import ui.ui_widgets as uiWidgets
import models

class UI():
    def __init__(self, player: models.Player) -> None:
        self.player = player
        ft.app(self.open_home)
    
    def open_home(self, page: ft.Page):
        page.fonts = {
            "lilitaone": "./Assets/Fonts/LilitaOne-Regular.ttf"
        }
        page.add(uiWidgets.Home(self.player))
        page.controls[0].onContentChange(0)