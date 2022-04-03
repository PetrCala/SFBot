from ctypes import windll
import cv2
from cv2 import mean #Capturing screen
from PIL import ImageGrab
import pywintypes
import win32.win32gui as win32gui
import webbrowser

import warnings
import sys
from pathlib import Path
from os import path

from static import *
from base import SFBase, keyboard

def winEnumHandler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        print(hex(hwnd), win32gui.GetWindowText(hwnd))
       
def main():
    win32gui.EnumWindows(winEnumHandler, None)

if __name__ == '__main__':
    pass