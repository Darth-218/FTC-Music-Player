"""
Testing the functions to select a main music folder and a song to play
"""

# Imports

# To find files and directories
import os
import curses

# Functions

# Funtion to get the main music folder's path
def getfile(listbox): # to be re-created

    global flist, pathlist

    flist = []
    pathlist = []

    # Getting the folder path as a variable
    foldername = filedialog.askdirectory(initialdir="/", title="Select File") # find curses alternitave
    
    # At the moment of getting the directory path
    if foldername:

        # Obtaining files to show on window from the path variable
        for path, subdir, files in os.walk(foldername):
            
            for fname in files:
                
                if fname.endswith(".mp3"):
                    
                    # Adds all files with ".mp3" extention to the Listbox "musiclist"
                    flist.append(os.path.join(fname))
                    pathlist.append(os.path.join(path, fname))

        print(flist, '\n')
        print(pathlist, "\n")

# Function used to get the name of the selected file in the listbox "musiclist"
def getselected(event, listbox):

    global selectedfile

    # A variable that hold the index of the selected item
    selectedindex = listbox.curselection() # get replaced with mouse coordinates

    if selectedindex:

        selectedfile = listbox.get(selectedindex[0]) # replace with position in subwindow

        # Sets the test label to the selected file from the listbox
        selectedpath = pathlist[flist.index(selectedfile)]
        print(selectedpath)


# Function used to create queue
def addtoqu(listbox):

    global qu

    qu = []

    # Gets selected file
    if selectedfile:

        # Adds selected file to queue
        qu.append(selectedfile)

        for song in qu: # Adds all songs in queue to the queue subwindow

            pass

# A function to clear the queue
def quclear(listbox):

    qu.clear()

