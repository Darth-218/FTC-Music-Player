import flet as ft

class HorizontalListView(ft.Row):
    listView: ft.ListView
    def __init__(self):
        self.listView = ft.ListView(horizontal=True, expand=1, height=250)
        scrollToLeft = ft.IconButton(icon=ft.icons.ARROW_LEFT, icon_size=30, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25),), width=50, height=50, on_click=self.scrollLeft)
        scrollToRight = ft.IconButton(icon=ft.icons.ARROW_RIGHT, icon_size=30, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25),), width=50, height=50, on_click=self.scrollRight)
        super().__init__(controls=[scrollToLeft, self.listView, scrollToRight])

    def append(self, item: ft.Control):
        self.listView.controls.append(item)

    def scrollLeft(self, e):
        self.listView.scroll_to(delta=-170, duration=1000)

    def scrollRight(self, e):
        self.listView.scroll_to(delta=170, duration=1000)
