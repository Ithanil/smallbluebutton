#!/usr/bin/env python

"""
This program creates an overlay with a small blue button
to toggle&check mute status in BigBlueButton conferences
"""

import tkinter as tk
from overlay import Window
import argparse
import sys


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [WindowID]...",
        description="Toggle&check mute status in BigBlueButton windows",
    )
    parser.add_argument("-a", "--alpha", type=float, default='0.85')
    #parser.add_argument("winid")
    return parser

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()

    win = Window(size = (140, 140), alpha=args.alpha)

    # Load BBB Logo
    bbb_logo = tk.PhotoImage(file = 'logo.png')

    # Create button and image
    bbb_btn = tk.Button(win.root, image = bbb_logo, borderwidth = 0)
    bbb_btn.pack()

    Window.launch()

if __name__ == "__main__":
    main()