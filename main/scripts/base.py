from abc import abstractproperty
from ctypes import windll
import cv2
from PIL import ImageGrab
from cv2 import mean #Capturing screen
#import pytesseract #Text recognition
import numpy as np
from directKeys import click, queryMousePosition, moveMouseTo #For mouse movement
from pynput.keyboard import Key, Controller
import time
import math
import sys

from static import *

windll.user32.SetProcessDPIAware() #Make windll properly aware of your hardware
keyboard = Controller()

class SFBase():
    def __init__(self):
        '''A constructor for the SFBase class.
        '''
        self.screen_size = self.getScreenSize()
        self.screen_pos = self.getScreenCoordinates(self.screen_size) #Position/coordinates of the screen
        self.neutral_screen = self.getGameNeutralCoords()
        self.open_window = None
        self.setBaseWindow()

    def main(self):
        '''Main method of the Base class
        '''
        return None
    
    def setBaseWindow(self):
        '''Open the default window and set the 'open_window' property to this window.
        '''
        self.focusGame()
        self.changeWindow(SF_BASE_WINDOW, force = True, reset = False)
        return None

    def focusGame(self):
        '''Bring the game window into focus. Allows for keyboard input.
        '''
        x, y = self.neutral_screen[0], self.neutral_screen[1]
        return click(x,y)

    def getGameNeutralCoords(self):
        '''Return the coordinates, where the game window is neutral and can be clicked without
            triggering an event.
        '''
        x = 10 #TBA
        y = 150 #TBA
        return [x, y]

    def changeWindow(self, window_name, force = True, reset = True):
        '''Change the open window. Must be a different window than the current one, if force is not True.
        Also change the information about the open window to the one being opened.

        :args:
            window_name[str] - Name of the window which shall be opened.
            force[bool] - If true, force the windows change, regardless of whether the window is open or not.
                Defauts to True.
            reset[bool] - If true, also queue a window change to base window before the actual change, in
                order to get the base form of the window to be opened. Defaults to True.
        '''
        if not window_name in SF_WINDOWS:
            raise ValueError(f'{window_name} is not a recognized window.')
        if window_name is self.open_window and not force: #Window already open
            return None
        if reset:
            self.getWindow(SF_BASE_WINDOW)
        self.getWindow(window_name)
        self.open_window = window_name
        return None

    def getWindow(self, window_name):
        '''Send the application a hotkey which corresponds to the window which should be open.

        Does not change the information about which window is open.
        '''
        if not window_name in SF_WINDOWS:
            raise ValueError(f'{window_name} is not a recognized window.')
        key = SF_WINDOWS_HOTKEYS.get(window_name)
        self.useKey(key)
        return None

    def createScreen(self, screen_pos = None):
        screen_pos = self.screen_pos if screen_pos is None else screen_pos #Defaults to the whole screen
        screen = np.array(ImageGrab.grab(bbox=screen_pos))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB) #Original color scale
        #screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY) #Grey color scale
        return screen

    def openScreen(self):
        '''Open the screenshot for viewing.
        '''
        win_name = 'Ekura screenshot'
        window_res = [int(self.screen_size[0]*0.9), int(self.screen_size[1]*0.9)]

        screen = self.createScreen() #Take a screenshot
        
        cv2.namedWindow(win_name, cv2.WINDOW_NORMAL) # Create a Named Window
        cv2.moveWindow(win_name, 0, 0) # Move it to (X,Y)
        cv2.imshow(win_name, screen) # Show the Image in the Window
        cv2.resizeWindow(win_name, window_res[0], window_res[1])   # Resize the Window
        cv2.waitKey(0); cv2.destroyAllWindows(); cv2.waitKey(1) #Handle closing of the window
        return None

    def getPixelRGB(self):
        '''Get a RGB value of the pixel the mouse is pointing at.
        Returns:
            list: RGB value returned as a list in the order R,G,B.
        '''
        assert self.mouseOnScreen(self.screen_pos), 'The mouse is not on screen'
        mouse = queryMousePosition() #Get mouse position
        x, y = mouse.x, mouse.y
        screen = self.createScreen() #Computer screen snapshot
        (r, g, b) = screen[y,x]
        print(f"Pixel at ({x}, {y}) - Red: {r}, Green: {g}, Blue: {b}")
        return [r,g,b]

    def pixelsOnScreen(self, rgb):
        '''
        Enter the r,g,b value of desirable pixel values and return a list with coordinates
            where these match on the screen.
        Arg:
            rgb [list] - This must be a nested list of possible rgb combinations, which should be
                searched.
        Returns:
            [list]: A list of the coordinates where the match was found
        '''
        assert any(isinstance(i, list) for i in rgb), 'The argument must be a nested list'
        print(f'Searching for pixel with rgb value {rgb}...')
        screen = self.createScreen() #Take a snapshot of the screen
        match_count = 0
        match_list = []
        start_time = time.time()
        for y in range(self.screen_size[1]):
            for x in range(self.screen_size[0]):
                pixel_rgb = screen[y,x].tolist()
                if pixel_rgb in rgb:
                    match_count = match_count + 1
                    print(f'Found a match at position ({x}, {y})')
                    match_list.append([x,y])
        search_time = round(time.time() - start_time, 2)
        print(f'Search complete.\nFound {match_count} matching pixels.\nThe search took {search_time} seconds.')
        return match_list

    def printMousePosition(self):
        m = queryMousePosition()
        x = m.x
        y = m.y
        print(f'The mouse position is\nx:{x}\ny:{y}')
        return None

    def useKeys(self, keys:list):
        '''For each key in a list of strings, press this key.
        '''
        for key in keys:
            self.useKey(key)
        return None

    @staticmethod
    def useKey(key):
        '''Press and release a given key.
        '''
        keyboard.press(key)
        keyboard.release(key)
        time.sleep(0.2)
        return None

    @staticmethod
    def mouseOnScreen(screen_pos):
        '''Specify the screen position as a list of coordinates and check whether the mouse is within these coordinates.
        Args:
            screen_pos ([type]): [description]
        Returns:
            bool: True if the mouse is within the specified coordinates, False otherwise.
        '''
        assert isinstance(screen_pos, list) and len(screen_pos) == 4, 'The screen element is misspecified'
        pos = queryMousePosition() #Get mouse position
        on_screen = screen_pos[0] < pos.x < screen_pos[2] and screen_pos[1] < pos.y < screen_pos[3]
        return True if on_screen else False

    @staticmethod
    def getScreenCoordinates(screen_size):
        '''Return a list of 4 coordinates marking the beginning and end of the screen.
        Args:
            screen_size ([list]): A 2 elements long list denoting the screen size.
        Returns:
            list: A list of coordinates in the form [x1,y1, x2, y2].
        '''
        screen_pos = [0,0] + screen_size
        return screen_pos

    @staticmethod
    def getScreenSize():
        '''
        A class method for retrieving the screen resolution.
        Returns:
            list: A list of two coordinates marking the bottom right part of the screen.
        '''
        if sys.platform[0:3] == 'win':
            user32 = windll.user32
            return [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        else:
            raise SystemError('The code must be ran on the Windows platform')

    @staticmethod
    def dist(x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)