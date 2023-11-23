# Testing how to select a main music folder

# Imports

import os

import tkinter as tk
from tkinter import filedialog, Listbox, Tk, StringVar, Button, Label

# Main window variables

root = Tk()
root.title("FTC - Music Player")
root.geometry("500x300")


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

    # A variable that hold the index of the selected item
    selectedindex = listbox.curselection()
    
    if selectedindex:

        selectedfile = listbox.get(selectedindex[0])

        # Sets the test label to the selected file from the listbox
        pathstring.set(selectedfile)
        print(selectedfile)


# Basic widgets

# Test label to show the selected song
pathstring = StringVar()
pathlabel = Label(root, textvariable=pathstring)
pathlabel.pack()

# Test frame showing the list of music in a directory
musiclist = Listbox(root, width=50)
musiclist.pack()
#Using the mouse left-click to trigger the functon "getselected"
musiclist.bind("<Double-Button-1>", lambda event: getselected(event, musiclist))

#Test button to get the folder path
pathfinder = Button(root, text="Select Music folder", command=lambda: getfile(musiclist))
pathfinder.pack()



root.mainloop()
