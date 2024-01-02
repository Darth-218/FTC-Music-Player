# Imports
import os
import flet as ft
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
import data_models as dm
from data_models import *
import lib


class Local:

    # init function to initialize main UI elements
    def __init__(self):

        # A ListView that contains all the songs whether from the selected album or directory
        self.songlist = ft.ListView(expand=1, spacing=10, padding=20)

        # A ListView that contains all the albums in a certain directory
        self.albumlist = ft.ListView(expand=1, spacing=12, padding=20, horizontal = True)

        self.albumlistcontainer = ft.Container(content = self.albumlist)

        # An ElevatedButton that returns to view the songs in the main selected directory
        self.albumreset = ft.ElevatedButton("All songs", icon=ft.icons.MUSIC_NOTE, tooltip="Return to the main directory", on_click = lambda _: self.songdisplay(self.songs, self.songlist))


        self.pick_files_dialog = ft.FilePicker(on_result=lambda e: Localclass.pick_files_result(e))
        # An ElevatedButton that is used to pick a song directory
        self.picker = ft.ElevatedButton("Pick Directory", icon=ft.icons.UPLOAD_FILE_ROUNDED, tooltip="Click here to choose a song directory",  on_click=lambda _: self.pick_files_dialog.get_directory_path())

        # A list of subdirectories
        self.paths = []
        # A dictionary that stores the song with its name as a key and the value as another dict "songmeta"
        self.filepaths = {}

        self.song = dm.Song
        # a dictionary that stores a song's data: path, artist name, album name, duration
        self.songmeta = {}

        self.songs = []

        # A list with all albums in the chosen directory
        self.albums = list()
        # A directory with all songs in a selected album
        self.albumsongs = {}

    # Functions
    # Function to get the songs in the main music directory and takes two parameters: "songbox" to be able to view and select songs in the directory, "selected" which is the directory path
    def getfolder(self, songbox: ft.ListView, selected):

        selected_folder = selected

        # At the moment of getting the directory path
        if selected_folder:

            # clears songbox for new songs to appear
            songbox.clean()

            # Obtaining files to show on window from the path variable
            for path, subdir, files in os.walk(selected_folder):

                self.paths.append(path.split("/")[-1])

                # Loops in through the files in the chosen directory and adds the path to the main dictionary
                for fname in files:

                    if fname.endswith(".mp3"):

                        self.getdetails(os.path.join(path, fname))

                        self.filepaths[fname] = {"name": fname, "path": os.path.join(path, fname), "album": self.songmeta["album"], "artist": self.songmeta["artist"], "duration": self.songmeta["duration"], "cover": self.songmeta["coverart"]}
                        self.songs.append(self.song)

            self.songs

            self.display(self.songs)


    # A function that takes a parameter "target" and gets metadata for all paths in it
    def display(self, target: list):

        # Creates a directory to store album covers
        outdir = "covers"
        os.makedirs(outdir, exist_ok = True)

        c = 0

        for i in target:

            self.localsongwidget(target, target.index(i),
                                 self.songlist,
                                    i.cover_art,
                                    i.name,
                                    i.artist,
                                    i.duration,
                                    i.album)
            self.albums.append(i.album)

            c += 1

            # Opens a file with the song name and writes the cover data
            with open(os.path.join(outdir, f'{c}.jpg'), 'wb') as image:
                image.write(i.cover_art)

            self.localalbumwidget(self.albumlist,
                                    ft.Image(src = os.path.join(outdir, f'{c}.jpg'), width = 255, height = 255),
                                    i.album,
                                    i.artist)

    # A function that displays the songs in a given dictionary "target" and views it in the "songbox" ListView
    def songdisplay(self, target: list, songbox: ft.ListView):

        songbox.clean()

        c = 0

        for i in target:

            self.localsongwidget(target, c,self.songlist, i.cover_art, i.name, i.artist, i.duration, i.album)

            c += 1

    # A function that gets a directory's path from a file dialog
    def pick_files_result(self, e: ft.FilePickerResultEvent):

        lib.logger("pick_file_result", "Clicked the pick button")

        self.folder_name = (e.path if e.path else "Cancelled")

        lib.logger("The selected folder is:", self.folder_name)

        self.getfolder(self.songlist, self.folder_name)

        return self.folder_name

    def getdetails(self, filepath):

        audio = EasyID3(filepath)

        try:

            imageaudio = ID3(filepath)

            for key in imageaudio.keys():

                if key.startswith("APIC"):

                    cover = imageaudio[key].data

        except:

            self.songmeta["coverart"] = "N/A"

        title = audio["title"][0] if "title" in audio else "N/A"
        artist = audio["artist"][0] if "artist" in audio else "N/A"
        album = audio['album'][0] if 'album' in audio else "N/A"
        duration = audio.info.length if hasattr(audio, 'info') and hasattr(audio.info, 'length') else "N/A"

        self.songmeta["title"] = title
        self.songmeta["artist"] = artist
        self.songmeta["album"] = album
        self.songmeta["duration"] = duration
        self.songmeta["coverart"] = cover

        self.song = dm.Song(self.songmeta["title"], self.songmeta["artist"], filepath, self.songmeta["duration"], self.songmeta["coverart"], self.songmeta["album"])

        return self.songmeta, self.song

    # Function used to get the name of the selected file in the listbox "musiclist"
    def getselectedsong(self, songname, target):

        self.song._path = target[songname]["path"]

        return self.song._path

    def getselectedalbum(self, albumname, target, songdict):

        songsinalbum = [x for x in target if x.album == albumname]

        self.albumsongs = [i for i in songsinalbum]

        self.songdisplay(self.albumsongs, self.songlist)

    # A function to clear the queue
    def quclear(self): # to be re-created

        qu.clear()

    def localsongwidget(self, songdict: list, data: int, songbox: ft.ListView, songart: ft.Image, songname: str, artistname: str = "N/A", songduration: str = "N/A", songalbum: str = "N/A"):

        self.songcontainer = ft.Container(content = ft.Column([
            ft.Row([ft.Text(songname.strip('.mp3'), size = 18)]),
            ft.Row([ft.Text(f"{songduration}  |  {artistname}  |  {songalbum}")])]),
                                          on_click = lambda _: Localclassview.playlocal(songdict, data))

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
            ft.Text(artistname)]), width = 255, on_click = lambda _: self.getselectedalbum(albumname, self.songs, self.albumlist))

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

        return ft.Column([Localclass.albumlist, Localclass.songlist, ft.Row([Localclass.picker, Localclass.pick_files_dialog, Localclass.albumreset])], expand = 1)

    def playlocal(self, queuetarget: list, selected_song: int):

        song_list = [i for i in queuetarget]
        queue = Queue(song_list, selected_song)

        lib.logger("The queue list is: ", "\n".join(i.name  + str(selected_song) for i in song_list))

        while self.page is None:

            pass

        lib.logger("Loop 1", "done")

        while self.page.bottom_appbar is None:

            pass

        lib.logger("Loop 2", "done")

        self.page.bottom_appbar.content.player.change_queue(queue=queue) # Change the queue of the player.
        self.page.bottom_appbar.content.play() # Play the song in the player widget.

        lib.logger("Currently should play: ", str(selected_song))


Localclass = Local()
Localclassview = LocalView()


def main(page: ft.Page):

    page.add(LocalView())


if __name__ == "__main__":

    ft.app(target=main)

