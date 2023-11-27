#!/usr/bin/env /usr/bin/python3
"""
Definitions of some generally useful functions to use throughout the
project.
"""

import colorama as c

def TODO(s: str):
    print(c.Fore.YELLOW + ">>=UNIMPLEMENTED{. %s .}=<<" %(s),
          c.Style.RESET_ALL)

def logger(name: str, s: str):
    """
    General logging function for use by the library.

    - `name`: Name of the calling module/function.   
    - `s`   : Displayed log.
    """
    print(c.Fore.GREEN + "#[LOG{. %s .}]=||" %(name), s, c.Style.RESET_ALL)

def err(name: str, e: str):
    """
    General function for logging errors.

    - `name`: Name of the calling module/function.   
    - `s`   : Displayed log.
    """
    print(c.Fore.RED + "#[ERROR{. %s .}]=!=|" %(name), e, c.Style.RESET_ALL)

if __name__ == "__main__":
    TODO("lib/testing")
    logger("lib", "Hello, world!")
    err("lib", "418 - I am a Teapot.")
    logger("lib", "Nevermind I figured it out.")
