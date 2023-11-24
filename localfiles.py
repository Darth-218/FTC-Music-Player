"""
Testing how to select a main music folder and a song to play
"""

# Imports

# To find files and directories
import os
# To make a window with widgets
import tkinter as tk
from tkinter import filedialog, Listbox, Tk, StringVar, Button, Label, EW

# Main window variables

root = Tk()
root.title("FTC - Music Player")
root.geometry("500x400")

# Functions

# Funtion to get the main music folder's path
def getfile(listbox):

    flist = []

    # Getting the folder path as a variable
    foldername = filedialog.askdirectory(initialdir="/", title="Select File")
    
    # At the moment of getting the directory path
    if foldername:

        #Removing old files shown in the listbox
        listbox.delete(0, tk.END)

        # Obtaining files to show on window from the path variable
        for path, subdir, files in os.walk(foldername):
            
            for fname in files:
                
                if fname.endswith(".mp3"):
                    
                    # Adds all files with ".mp3" extention to the Listbox "musiclist"
                    flist.append(os.path.join(fname))
        print(flist, '\n')

        # Inserts all songs in the chosen directory into the listbox
        for song in flist:

            listbox.insert(tk.END, song)


# Function used to get the name of the selected file in the listbox "musiclist"
def getselected(event, listbox):

    global selectedfile

    # A variable that hold the index of the selected item
    selectedindex = listbox.curselection()
    
    if selectedindex:

        selectedfile = listbox.get(selectedindex[0])

        # Sets the test label to the selected file from the listbox
        pathstring.set(selectedfile)
        print(selectedfile)


# Function used to create queue
def addtoqu(listbox):

    qu = []

    if selectedfile:

        qu.append(selectedfile)

        for song in qu:

            listbox.insert(tk.END, song)


def quclear(listbox):

    listbox.delete(0, tk.END)


# Basic widgets

# Test label to show the selected song
pathstring = StringVar()
pathlabel = Label(root, textvariable=pathstring)

# Test frame showing the list of music in a directory
musiclist = Listbox(root, width=55)
#Using the mouse left-click to trigger the functon "getselected"
musiclist.bind("<Double-Button-1>", lambda event: getselected(event, musiclist))

#Test button to get the folder path
pathfinder = Button(root, text="Select Music folder", command=lambda: getfile(musiclist))

#Queue listbox that tests the addtoqu Function
qulist = Listbox(root, width=55, height=25)

#Test button that adds songs to queue
qubutton = Button(root, text="Add to Queue", command=lambda: addtoqu(qulist))

#Test button that clears the queue
clearqu = Button(root, text="Clear Queue", command=lambda: quclear(qulist))

pathlabel.grid(row=0, columnspan=2, sticky=EW)
musiclist.grid(row=1, columnspan=2, sticky=EW)
pathfinder.grid(row=2, columnspan=2, sticky=EW)
qubutton.grid(row=3, column=0, sticky=EW)
clearqu.grid(row=3, column=1, sticky=EW)
qulist.grid(row=4, columnspan=2, sticky=EW)


root.mainloop()
