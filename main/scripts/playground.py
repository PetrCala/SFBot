import win32gui
import warnings
import sys
from pathlib import Path
import path
import os

from static import *

def winEnumHandler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        print(hex(hwnd), win32gui.GetWindowText(hwnd))
       
def main():
    win32gui.EnumWindows(winEnumHandler, None)

if __name__ == '__main__':
    pass
