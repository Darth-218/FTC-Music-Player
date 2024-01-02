#!/usr/bin/env /usr/bin/python3
"""
Definitions of some generally useful functions to use throughout the
project.
"""

from datetime import timedelta
import colorama as c


def calc_pos(duration: timedelta, time: timedelta):
    dursecs = duration.total_seconds()
    timesecs = time.total_seconds()
    return timesecs / dursecs


def TODO(s: str):
    """
    Mark a function or method as unimplemented.

    * `s` -- name.
    """
    print(c.Fore.YELLOW + ">>=UNIMPLEMENTED{. %s .}=<<" % (s), c.Style.RESET_ALL)


def logger(name: str, s: str):
    """
    General logging function for use by the library.

    - `name`: Name of the calling module/function.
    - `s`   : Displayed log.
    """
    print(c.Fore.GREEN + "#[LOG{. %s .}]=||" % (name), s, c.Style.RESET_ALL)


def err(name: str, e: str):
    """
    General function for logging errors.

    - `name`: Name of the calling module/function.
    - `s`   : Displayed log.
    """
    print(c.Fore.RED + "#[ERROR{. %s .}]=!=|" % (name), e, c.Style.RESET_ALL)


def passive():
    """Sometimes you need to pass a function as a parametre to
    another, or sometimes you need an expression for the interpreter
    to stop complaining. This allows you to do so while also not doing
    anything.
    """
    pass


def timelambda(delta: timedelta) -> tuple:
    hours = delta // timedelta(hours=1)
    minutes = delta // timedelta(minutes=1) - hours * 60
    seconds = delta // timedelta(seconds=1) - (minutes * 60 + hours * 60 * 60)
    return hours, minutes, seconds


def str_to_delta(simga: str | None) -> timedelta:
    if not str:
        return timedelta()
    h, m, s = simga.split(":")
    return timedelta(hours=int(h), minutes=int(m), seconds=float(s))


if __name__ == "__main__":
    # Demo code
    TODO("lib/testing")
    logger("lib", "Hello, world!")
    err("lib", "418 - I am a Teapot.")
    logger("lib", "Nevermind I figured it out.")
