# Imports
# os to find files and directories
import os
# curses to create the UI
import flet as ft


flist = []
pathlist = []
paths = []
qu = []


class Local:

    # Functions
    # Function to get the main music folder's path
    def getfolder(self, listbox: ft.ListView, selected):

        global flist, pathlist

        flist = []
        pathlist = []
        paths = []

        selected_folder = selected

        # At the moment of getting the directory path
        if selected_folder:

            # Obtaining files to show on window from the path variable
            for path, subdir, files in os.walk(selected_folder):

                paths.append(path.split("/")[-1])

                for fname in files:

                    if fname.endswith(".mp3"):

                        # Adds all files with ".mp3" extension and their paths to the respective lists"
                        flist.append(os.path.join(fname.rstrip(".mp3")))
                        pathlist.append(os.path.join(path, fname))

                for i in flist:

                    listbox.controls.append(ft.TextButton(f"{i}"))

                    listbox.update()

            print(paths, flist, pathlist)

        return selected_folder

    def pick_files_result(self, e: ft.FilePickerResultEvent):

        folder_name = (e.path if e.path else "Cancelled")

        print(folder_name)

        Local.getfolder(self, listv, folder_name)

        return folder_name

    # Function used to get the name of the selected file in the listbox "musiclist"
    def getselected(self, event, listbox):

        global selectedfile

        # A variable that hold the index of the selected item
        selectedindex = listbox.curselection() # get replaced with mouse coordinates

        if selectedindex:

            selectedfile = listbox.get(selectedindex[0]) # replace with position in subwindow

            # Sets the test label to the selected file from the listbox
            selectedpath = pathlist[flist.index(selectedfile)]
            print(selectedpath)

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


Localclass = Local()


def main(page: ft.Page):

    global listv

    listv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    pick_files_dialog = ft.FilePicker(on_result=lambda e: Localclass.pick_files_result(e))

    page.overlay.append(pick_files_dialog)
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    picker = ft.ElevatedButton("Pick Directory", icon=ft.icons.UPLOAD_FILE_ROUNDED, on_click=lambda _: pick_files_dialog.get_directory_path())

    page.add(ft.Column([picker, listv]))

    page.update()


if __name__ == "__main__":

    ft.app(target=main)

