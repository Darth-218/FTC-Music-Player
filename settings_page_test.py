#!/usr/bin/env python3
import flet as ft
from config import intrests


class Settings(ft.UserControl):
    def build(self):
        interests = {
            interest: weight
            for interest, weight in (tmp.split("--)") for tmp in intrests.split("|*|"))
        }
        sorted_interests = sorted(interests.keys(), key=interests.get, reverse=True)
        cfg_interests_field = ft.TextField(
            value="\n".join(sorted_interests), multiline=True, min_lines=15
        )
        return cfg_interests_field


if __name__ == "__main__":

    def main(page):
        page.add(Settings())

    ft.app(target=main)
