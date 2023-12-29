# Imports
import os
import flet as ft
import data_models as dm
from data_models import *


class Local:

    def __init__(self):

        self.listv = ft.ListView(expand=1, spacing=10, padding=20)

        self.paths = []
        self.filepaths = {}

        self.song = dm.Song

    # Functions
    # Function to get the main music folder's path
    def getfolder(self, listbox: ft.ListView, selected):

        selected_folder = selected

        # At the moment of getting the directory path
        if selected_folder:

            listbox.clean()

            # Obtaining files to show on window from the path variable
            for path, subdir, files in os.walk(selected_folder):

                self.paths.append(path.split("/")[-1])

                for fname in files:

                    if fname.endswith(".mp3"):

                        # Adds all files with ".mp3" extension and their paths to a dictionary"
                        self.filepaths[fname] = os.path.join(path, fname)

                for i in self.filepaths:

                    self.song.name = i

                    self.localsongwidget(self.listv, self.song.name)

            print(self.paths)

        return selected_folder
    
    def pick_files_result(self, e: ft.FilePickerResultEvent):

        self.folder_name = (e.path if e.path else "Cancelled")

        print(self.folder_name)

        self.getfolder(self.listv, self.folder_name)

        return self.folder_name

    def getdetails(filename):

        pass
    
    # Function used to get the name of the selected file in the listbox "musiclist"
    def getselected(self, songname):

        chosenpath = self.filepaths[songname]

        return chosenpath

    # Function used to create queue
    def addtoqu(self):

        # Gets selected file
        if selectedfile:

            # Adds selected file to queue
            qu.append(selectedfile)

            for song in qu: # Adds all songs in queue to the queue subwindow

                pass

    # A function to clear the queue
    def quclear(self): # to be re-created

        qu.clear()

    def localsongwidget(self, listbox: ft.ListView, songname: str, artistname: str = "N/A"):

        self.songcontainer = ft.Container(content = ft.Column([ft.Text(songname), ft.Text(artistname)]), on_click = lambda _: print(self.getselected(songname)))

        self.songcontainer.border = ft.border.all(1, ft.colors.GREY)
        self.songcontainer.border_radius = ft.border_radius.all(7)
        self.songcontainer.padding = 5
        self.songcontainer.margin = 2

        listbox.controls.append(self.songcontainer)

        listbox.update()


Localclass = Local()


def main(page: ft.Page):

    pick_files_dialog = ft.FilePicker(on_result=lambda e: Localclass.pick_files_result(e))

    page.overlay.append(pick_files_dialog)
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    picker = ft.ElevatedButton("Pick Directory", icon=ft.icons.UPLOAD_FILE_ROUNDED, on_click=lambda _: pick_files_dialog.get_directory_path())

    page.add(ft.Column([picker, Localclass.listv], expand = 1))

    page.update()


if __name__ == "__main__":

    ft.app(target=main)

