import customtkinter
from typing import Callable

class ListView(customtkinter.CTkScrollableFrame):
    def __init__(self, master, dataTemplate: Callable[[], None], data: list):
        super().__init__(master)

        