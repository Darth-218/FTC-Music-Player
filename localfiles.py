# Imports
import os
import flet as ft
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
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
                        self.getdetails(os.path.join(path, fname))

                        self.filepaths[fname] = {"name": fname, "path": os.path.join(path, fname), "album": self.songmeta["album"], "artist": self.songmeta["artist"], "duration": self.songmeta["duration"], "cover": self.songmeta["coverart"]}

            self.display(self.filepaths)

    def display(self, target):

        for i in target:

            self.localsongwidget(self.songlist,
                                    target[i]["cover"],
                                    target[i]["name"],
                                    target[i]["artist"],
                                    target[i]["duration"],
                                    target[i]["album"])

            outdir = "covers"
            os.makedirs(outdir, exist_ok = True)

            with open(os.path.join(outdir, target[i]["name"]), 'wb') as image:
                image.write(target[i]["cover"])

            self.localalbumwidget(self.albumlist,
                                    ft.Image(src = os.path.join(outdir, target[i]["name"]), width = 255, height = 255),
                                    target[i]["album"],
                                    target[i]["artist"])

    def songdisplay(self, target, songbox):

        songbox.clean()

        for i in target:

            self.localsongwidget(self.songlist, self.songmeta["coverart"], target[i]["name"], target[i]["artist"], target[i]["duration"], target[i]["album"])

    def pick_files_result(self, e: ft.FilePickerResultEvent):

        self.folder_name = (e.path if e.path else "Cancelled")

        print(f"The selected folder is:", self.folder_name)

        self.getfolder(self.songlist, self.folder_name)

        return self.folder_name

    def getdetails(self, filepath):

        #try:

        audio = EasyID3(filepath)
        imageaudio = ID3(filepath)

        for key in imageaudio.keys():

            if key.startswith("APIC"):

                cover = imageaudio[key].data

        title = audio["title"][0] if "title" in audio else None
        artist = audio["artist"][0] if "artist" in audio else None
        album = audio['album'][0] if 'album' in audio else None
        duration = audio.info.length if hasattr(audio, 'info') and hasattr(audio.info, 'length') else "N/A"

        self.songmeta["title"] = title
        self.songmeta["artist"] = artist
        self.songmeta["album"] = album
        self.songmeta["duration"] = duration
        self.songmeta["coverart"] = cover

        return self.songmeta

    # Function used to get the name of the selected file in the listbox "musiclist"
    def getselectedsong(self, songname, target):

        self.song._path = target[songname]["path"]

        return self.song._path

    def getselectedalbum(self, albumname, target):

        songsinalbum = [x for x in target if target[x]["album"] == albumname]

        self.albumsongs = {}

        for i in songsinalbum:

            self.albumsongs[i] = target[i]

        self.songdisplay(self.albumsongs, self.songlist)

    # A function to clear the queue
    def quclear(self): # to be re-created

        qu.clear()

    def localsongwidget(self, songbox: ft.ListView, songart: ft.Image, songname: str, artistname: str = "N/A", songduration: str = "N/A", songalbum: str = "N/A"):

        self.songcontainer = ft.Container(content = ft.Column([
            ft.Row([ft.Text(songname.strip('.mp3'), size = 18)]),
            ft.Row([ft.Text(f"{songduration}  |  {artistname}  |  {songalbum}")])]),
                                          on_click = lambda _: print(self.getselectedsong(songname, self.filepaths)))

        self.songcontainer.border = ft.border.all(1, ft.colors.GREY)
        self.songcontainer.border_radius = ft.border_radius.all(7)
        self.songcontainer.padding = 5
        self.songcontainer.margin = 2

        songbox.controls.append(self.songcontainer)

        songbox.update()

    def localalbumwidget(self, albumbox, albumcover: ft.Image, albumname: str = "N/A", artistname: str = "N/A"):

        self.albumcontainer = ft.Container(content = ft.Column([
            albumcover,
            ft.Text(albumname,
                    size = 18),
            ft.Text(artistname)]), width = 255, on_click = lambda _: print(self.getselectedalbum(albumname, self.filepaths)))

        self.albumcontainer.height = 275
        self.albumcontainer.border = ft.border.all(1, ft.colors.GREY)
        self.albumcontainer.border_radius = ft.border_radius.all(7)
        self.albumcontainer.padding = 5
        self.albumcontainer.margin = 2

        albumbox.controls.append(self.albumcontainer)

        albumbox.update()

    def uinit(self, page: ft.Page):

        page.overlay.append(Localclass.pick_files_dialog)
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        page.add(ft.Column([Localclass.albumlist, Localclass.songlist, Localclass.picker], expand = 1))

        page.update()


class LocalView(ft.UserControl):

    def build(self):

        return ft.Column([Localclass.albumlist, Localclass.songlist, Localclass.picker, Localclass.pick_files_dialog], expand = 1)

Localclass = Local()


def main(page: ft.Page):

    page.add(LocalView())


if __name__ == "__main__":

    ft.app(target=main)

