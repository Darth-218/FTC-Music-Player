# Imports
import os
import flet as ft
from mutagen.easyid3 import EasyID3
import data_models as dm
from data_models import *


class Local:

    def __init__(self):

        self.songlist = ft.ListView(expand=1, spacing=10, padding=20)
        self.albumlist = ft.ListView(expand=1, spacing=12, padding=20, horizontal = True)

        self.pick_files_dialog = ft.FilePicker(on_result=lambda e: Localclass.pick_files_result(e))
        self.picker = ft.ElevatedButton("Pick Directory", icon=ft.icons.UPLOAD_FILE_ROUNDED, tooltip="Click here to choose a song directory",  on_click=lambda _: self.pick_files_dialog.get_directory_path())

        self.paths = []
        self.filepaths = {}

        self.song = dm.Song
        self.songmeta = {}

        self.albums = list()
        self.albumsongs = {}

    # Functions
    # Function to get the main music folder's path
    def getfolder(self, songbox: ft.ListView, selected):

        selected_folder = selected

        # At the moment of getting the directory path
        if selected_folder:

            songbox.clean()

            # Obtaining files to show on window from the path variable
            for path, subdir, files in os.walk(selected_folder):

                self.paths.append(path.split("/")[-1])

                for fname in files:

                    if fname.endswith(".mp3"):

                        # Adds all files with ".mp3" extension and their paths to a dictionary"
                        self.filepaths[fname] = os.path.join(path, fname)

            for i in self.filepaths:

                self.getdetails(self.filepaths[i])

                self.song.name = i

                self.localsongwidget(self.songlist,
                                        self.song.name,
                                        self.songmeta["artist"],
                                        self.songmeta["duration"],
                                        self.songmeta["album"])

                self.albums.append(self.songmeta["album"])

                self.localalbumwidget(self.albumlist, self.songmeta["album"])

        return selected_folder

    def songsinalbum(self, albumnames):

        for i in albumnames:

            self.localalbumwidget(self.albumlist, albumnames, i)

    def pick_files_result(self, e: ft.FilePickerResultEvent):

        self.folder_name = (e.path if e.path else "Cancelled")

        print(f"The selected folder is:", self.folder_name)

        self.getfolder(self.songlist, self.folder_name)

        return self.folder_name

    def getdetails(self, filepath):

        #try:

        audio = EasyID3(filepath)

        title = audio["title"][0] if "title" in audio else None
        artist = audio["artist"][0] if "artist" in audio else None
        album = audio['album'][0] if 'album' in audio else None
        duration = audio.info.length if hasattr(audio, 'info') and hasattr(audio.info, 'length') else None

        self.songmeta["title"] = title
        self.songmeta["artist"] = artist
        self.songmeta["album"] = album
        self.songmeta["duration"] = duration

        return self.songmeta

        #except Exception as e:

            #print(f"Error reading metadata for the file {filepath}")
    
    # Function used to get the name of the selected file in the listbox "musiclist"
    def getselected(self, songname):

        self.song._path = self.filepaths[songname]

        return self.song._path

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

    def localsongwidget(self, songbox: ft.ListView, songname: str, artistname: str = "N/A", songduration: str = "N/A", songalbum: str = "N/A"):

        self.songcontainer = ft.Container(content = ft.Column([
            ft.Row([ft.Text(f"{songname.strip('.mp3')}  |  "),
                    ft.Text(songalbum)]),
            ft.Row([ft.Text(f"{songduration}  |  "),
                    ft.Text(artistname)])]),
                                          on_click = lambda _: print(self.getselected(songname)))

        self.songcontainer.border = ft.border.all(1, ft.colors.GREY)
        self.songcontainer.border_radius = ft.border_radius.all(7)
        self.songcontainer.padding = 5
        self.songcontainer.margin = 2

        songbox.controls.append(self.songcontainer)
        # print(f"built {songname}")

        songbox.update()

    def localalbumwidget(self, albumbox, albumname: str = "N/A", artistname: str = "N/A"):

        self.albumcontainer = ft.Container(content = ft.Column([ft.Text(albumname), ft.Text(artistname)]))

        self.albumcontainer.border = ft.border.all(1, ft.colors.GREY)
        self.albumcontainer.border_radius = ft.border_radius.all(7)
        self.albumcontainer.padding = 5
        self.albumcontainer.margin = 2

        albumbox.controls.append(self.albumcontainer)
        # print(f"built {albumname}")

        albumbox.update()

Localclass = Local()


def main(page: ft.Page):

    page.overlay.append(Localclass.pick_files_dialog)
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER


    page.add(ft.Column([Localclass.albumlist, Localclass.songlist, Localclass.picker], expand = 1))

    page.update()


if __name__ == "__main__":

    ft.app(target=main)

