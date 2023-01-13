#!/usr/bin/env python

"""
This program creates an overlay with a small blue button
to toggle&check mute status in BigBlueButton conferences
"""

import tkinter as tk
from overlay import Window
import argparse
import subprocess


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTIONS] [WindowTitle]...",
        description="Toggle&check mute status in BigBlueButton windows",
    )
    parser.add_argument("-a", "--alpha", type=float, default="0.85")
    parser.add_argument("-s", "--sleep", type=float, default="0.1")
    parser.add_argument('-r', '--raise', dest="winRaise", action='store_true')
    parser.add_argument("title")
    return parser

def toggleMute(winTitle, sleepTime) -> None:
    subprocess.run(["xdotool", "search", str(winTitle), "windowfocus",
                    "sleep", str(sleepTime), "key", "alt+M"],
                    check=True)

def raiseWindow(winTitle) -> None:
    subprocess.run(["xdotool", "search", str(winTitle), "windowraise"],
                    check=True)


def sbbCallBack(winTitle, sleepTime, winRaise) -> None:
    toggleMute(winTitle, sleepTime)
    if winRaise:
        raiseWindow(winTitle)

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()

    win = Window(size = (140, 140), alpha=args.alpha)

    # Load BBB Logo
    bbbLogo = tk.PhotoImage(file = 'logo.png')

    # Create button and image
    sbb = tk.Button(win.root, image = bbbLogo, borderwidth = 0,
                    command = lambda: sbbCallBack(args.title, args.sleep, args.winRaise))
    sbb.pack()

    Window.launch()

if __name__ == "__main__":
    main()