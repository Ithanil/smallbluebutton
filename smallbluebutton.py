#!/usr/bin/env python

"""
This script creates an overlay with a small blue button
to toogle&check mute status in BigBlueButton conferences
"""

import tkinter as tk
from overlay import Window

win = Window(size = (140, 140), alpha=0.85)

# Load BBB Logo
bbb_logo = tk.PhotoImage(file = 'logo.png')

# Create button and image
bbb_btn = tk.Button(win.root, image = bbb_logo, borderwidth = 0)
bbb_btn.pack()

Window.launch()
