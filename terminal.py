#!/usr/bin/env /usr/bin/python3
import curses
from curses import wrapper

welcome_message = "Welcome to ComMusic!"

def initialise_subwin(scr, w, h, x, y):
    subwindow = scr.subwin(w, h, x, y)
    subwindow.border()
    subwindow.refresh()
    return subwindow

def main(stdscr):
    stdscr.clear()
    cols = curses.COLS
    lines = curses.LINES

    songbar_width    = cols - 4
    songbar_height   = lines // 5

    playlists_width  = cols // 4
    playlists_height = lines - songbar_height

    queue_width      = cols // 4
    queue_height     = lines - lines // 5

    songs_width      = cols  - (playlists_width + queue_width) - 4
    songs_height     = lines - songbar_height

    songbar = initialise_subwin(
        stdscr,
        songbar_height - 1,
        songbar_width,
        lines - songbar_height + 1, 2
    )

    playlists = initialise_subwin(
        stdscr,
        playlists_height,
        playlists_width,
        1, 2
    )

    queue = initialise_subwin(
        stdscr,
        queue_height,
        queue_width,
        1, queue_width * 3
    )

    songs = curses.newpad(songs_height, songs_width)

    stdscr.addstr(0, curses.COLS // 2 - len(welcome_message) // 2, welcome_message)

    stdscr.refresh()
    songs.border()
    songs.refresh(0, 0, 1, playlists_width + 2, songs_height, songs_width)

    stdscr.getkey()


wrapper(main)
