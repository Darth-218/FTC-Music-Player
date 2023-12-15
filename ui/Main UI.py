import sys
sys.path.append('./')
import flet as ft
import api_client.Youtube.youtube as yt
import api_client.Youtube.api_models as yt_models
import Suggestions


def main(page: ft.Page):

    request = yt_models.GetSuggestionsRequest(3,3,5)
    suggestions = yt.getSuggestions(request=request)
    results_widget = Suggestions.SuggestionsWidget(suggestions)

    rail = ft.NavigationRail(
        selected_index=0,
        group_alignment= - 0.95,
        destinations=[
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.HOME, size=35),
                selected_icon_content=ft.Icon(ft.icons.HOME, size=35),
                label="Home"
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.FIND_IN_PAGE_ROUNDED, size=35),
                selected_icon_content=ft.Icon(ft.icons.FIND_IN_PAGE_ROUNDED, size=35),
                label="Browse",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.SETTINGS, size=35),
                selected_icon_content=ft.Icon(ft.icons.SETTINGS, size=35),
                label="Settings",
            )
        ],
        on_change=lambda e: print("Selected destination:", e.control.selected_index)
    )
    row = ft.Row(
            [
                rail,
                ft.VerticalDivider(width=10),
                ft.Column([results_widget], alignment=ft.MainAxisAlignment.END, expand=True),
            ],  height=1200
    )

    pick_file = ft.FilePicker()

    theme_btn = ft.IconButton(icon='nightlight_outlined', icon_size=30)
    label = ft.Text('Dark Theme')

    row2 = ft.Row(controls=[theme_btn,label],
                 vertical_alignment=ft.MainAxisAlignment.END)





    page.add(row)

ft.app(main)