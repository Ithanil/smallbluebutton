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

def getControlImage(coords) -> ImageTk.BitmapImage:
    W, H = 100, 100
    dsp = display.Display()
    win = dsp.create_resource_object('window', 102760451)
    raw = win.get_image(coords[0], coords[1], W, H, X.ZPixmap, 0xffffffff)
    image = Image.frombytes("1", (W, H), raw.data)#, "raw", "BGRX")
    return ImageTk.BitmapImage(image)
    
def updateControlImageLoop(winObj, coords):
    img = getControlImage(coords)
    tk.Label(winObj.root, image=img).pack()
    winObj.after(2000, lambda: updateControlImageLoop(winObj, coords))

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

    #checkMuteLoop(win, args.title, (1000,1000))
    updateControlImageLoop(win, (100, 100))

    Window.launch()

if __name__ == "__main__":
    main()