#!/usr/bin/env python

"""
This program creates an overlay with a small blue button
to toggle&check mute status in BigBlueButton conferences
"""

import argparse
import subprocess
import tkinter as tk
from overlay import Window
from Xlib import display, X
from PIL import Image, ImageTk
from numpy import array
from dataclasses import dataclass


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
    subprocess.run(["xdotool", "search", "--name", str(winTitle), "windowfocus",
                    "sleep", str(sleepTime), "key", "alt+M"],
                    check=True)

def raiseWindow(winTitle) -> None:
    subprocess.run(["xdotool", "search", "--name", str(winTitle), "windowraise"],
                    check=True)


def sbbCallBack(winTitle, sleepTime, winRaise) -> None:
    toggleMute(winTitle, sleepTime)
    if winRaise:
        raiseWindow(winTitle)

def getControlImage(winID, coords) -> ImageTk.BitmapImage:
    W, H = 200, 200
    dsp = display.Display()
    win = dsp.create_resource_object('window', winID)
    raw = win.get_image(coords[0], coords[1], W, H, X.ZPixmap, 0xffffffff)
    return ImageTk.BitmapImage(Image.frombytes("1", (W, H), raw.data))

    
def updateControlImageLoop(gd, coords):
    img = getControlImage(gd.bbbwid, coords)
    gd.controls.configure(image=img)
    gd.window.after(2000, lambda: updateControlImageLoop(gd, coords))

#def getPixelRGB(pixName) -> array:
#    pix = Image.open(pixName)
#    pixMatrix = array(pix)
#    return (pixMatrix[0][0])
#
#def checkMuteStatus(winTitle, coords) -> bool:
#    subprocess.run(["import -silent -window $(xdotool search --name "
#                     + str(winTitle) + ") -crop 1x1+"
#                     + str(coords[0]) + "+" + str(coords[1])
#                     + " /tmp/grab.bmp"],
#                    check=True, shell=True)
#    pixRGB = getPixelRGB("/tmp/grab.bmp")
#    print(pixRGB)

#def checkMuteLoop(winObj, winTitle, coords):
#    checkMuteStatus(winTitle, coords)
#    winObj.after(2000, lambda: checkMuteLoop(winObj, winTitle, coords))

@dataclass
class GlobalData:
# "Global" Data to hold all TK objects
# and the window ID of the BBB conference
    window: Window # Window from overlay submodule
    button: tk.Button # the small blue button
    controls: tk.Label # peek view of BBB controls
    bbbwid: int = 0 # window ID of BBB conference window

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

    # Create label for image of controls
    ctrl = tk.Label(win.root)
    ctrl.pack()

    # populate global data tuple
    gd = GlobalData(window = win, button = sbb, controls = ctrl)

    gd.bbbwid = 83886120
    updateControlImageLoop(gd, (100, 100))

    Window.launch()

if __name__ == "__main__":
    main()