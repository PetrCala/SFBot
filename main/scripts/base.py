from ctypes import windll
import cv2
from cv2 import mean #Capturing screen
from PIL import ImageGrab
import win32gui
import webbrowser
#import pytesseract #Text recognition

from directKeys import click, queryMousePosition, moveMouseTo #For mouse movement
from pynput.keyboard import Key, HotKey, Controller

import numpy as np
import time
import math
import sys

from static import *

windll.user32.SetProcessDPIAware() #Make windll properly aware of your hardware
keyboard = Controller()

class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()

class SFBase():
    def __init__(self):
        '''A constructor for the SFBase class.
        '''
        self.game_pos = self.getGameCoordinates(self.screen_pos) # Position/coordinates of the game
        self.game_window = None # Currently open window in game

    def main(self):
        '''Main method of the Base class
        '''
        return None
    
    @property
    def numbers(self):
        '''A list of the 10 roman numbers as strings. Used for keyboard input.
        '''
        return [str(i) for i in range(11)]
        
    def focusGame(self):
        '''Bring the game window into focus. Allows for keyboard input.
        '''
        hwnd = self.getWindowHwnd(SF_NAME)
        if hwnd is None:
            return self.openGame() # Automatic focus
        win32gui.SetForegroundWindow(hwnd)
        self.maximizeWindow()
        return time.sleep(0.2)

    def openGame(self):
        '''Open the Shakes & Fidget game in browser. Automatically opens the browser and
            sets this window into foreground.
        '''
        webbrowser.get(BROWSER_PATH).open(SF_WEBSITE)
        time.sleep(15)
        return None

    def maximizeWindow(self):
        '''Maximize a window, which is currently in the foreground.
        '''
        self.useKey(Key.cmd, method = 'press', sleep = False)
        self.useKey(Key.up, sleep = False)
        self.useKey(Key.cmd, method = 'release', sleep = False)
        return None

    def setBaseWindow(self):
        '''Open the default game window and set the 'game_window' property to this window.
        '''
        self.focusGame()
        self.changeGameWindow(SF_BASE_WINDOW, force = True, reset = False)
        return None

    def changeGameWindow(self, window_name, force = True, reset = True):
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
        if window_name is self.game_window and not force: #Window already open
            return None
        if reset:
            self.getGameWindow(SF_BASE_WINDOW)
        self.getGameWindow(window_name)
        self.game_window = window_name
        return None

    def getGameWindow(self, window_name):
        '''Send the application a hotkey which corresponds to the window which should be open.

        Does not change the information about which window is open.
        '''
        if not window_name in SF_WINDOWS:
            raise ValueError(f'{window_name} is not a recognized window.')
        key = SF_WINDOWS_HOTKEYS.get(window_name)
        self.useKey(key)
        return None

    def getGameCoordinates(self, screen_pos:list, focus:bool = True):
        '''Return a list of 4 coordinates marking the game screen.

        :args:
            screen_pos[list] - Position of the screen.
            focus[bool] - If True, focus the game before calculating the coordinates.
                Defaults to True.
        '''
        if focus:
            self.focusGame()

        # Find X axis coordinates of the game screen
        x_start, x_end = screen_pos[0], screen_pos[2] # Left and right screen border - x axis
        y_middle = int(screen_pos[2]/2) # Middle pixel of screen on the y axis
        y_slice = self.createScreen([x_start, y_middle, x_end, y_middle + 1])[0] # Take a slice of the screen
        if not len(y_slice) == x_end:
            raise SystemError('Failed to take the screenshot')
        while y_slice[x_start] == 0:
            x_start += 1 # Find left edge of game screen
        while y_slice[x_end - 1] == 0:
            x_end -= 1 # Find right edge of game screen
        if x_start == screen_pos[2] or x_end == screen_pos[0]:
            raise ValueError('Game not found or in full screen.') # Possibly handle this case later

        # Find Y axis coordinates of the game screen
        y_start, y_end = screen_pos[1], screen_pos[3]
        x_slice = self.createScreen([x_start, y_start, x_start + 1, y_end])#.flatten()
        if not len(x_slice) == y_end:
            raise SystemError('Failed to take the screenshot')
        while x_slice[y_start] > 50: # Might be adjusted
            y_start += 1
        while x_slice[y_end - 1] > 50:
            y_end -= 1
        if y_start == screen_pos[3] or y_end == screen_pos[1]:
            raise ValueError('Game not found or in full screen.')

        return [x_start, y_start, x_end, y_end]

    def getScaleFactors(self):
        '''Return a list of two floats representing factors by which
        to scale when calculating distance.

        Args:
            game_pos[list]: Coordinates of the game window.
        '''
        pass

    def createScreen(self, screen_pos:list, color_scale = 'gray'):
        '''Return a numpy array representing pixels on a screen. Specify the range
        of the screen with "screen_pos".

        :args:
            screen_pos[list] - A list of 4 integers specifying the range where
                the screen should be taken.
            color_scale[str] - Color scale which the screenshot should take.
                Can be set to 'gray', 'orig'.
        '''
        if not len(screen_pos) == 4:
            raise ValueError('The screen_pos argument must be a list of length 4')
        screen = np.array(ImageGrab.grab(bbox=screen_pos))
        if color_scale == 'gray':
            return cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        elif color_scale == 'orig':
            return cv2.cvtColor(screen, cv2.COLOR_BGR2RGB) #Original color scale
        raise ValueError('The color_scale argument is misspecified.')

    def openScreen(self, win_name = 'Window'):
        '''Open the screenshot for viewing.

        :args:
            win_name[str] - Name of the window.
        '''
        screen_size = self.getScreenSize()
        window_res = [int(screen_size[0]*0.9), int(screen_size[1]*0.9)]
        game_coords = self.getGameCoordinates()
        screen = self.createScreen(game_coords) #Take a screenshot
    
        cv2.namedWindow(win_name, cv2.WINDOW_NORMAL) # Create a Named Window
        cv2.moveWindow(win_name, 0, 0) # Move it to (X,Y)
        cv2.imshow(win_name, screen) # Show the Image in the Window
        cv2.resizeWindow(win_name, window_res[0], window_res[1])   # Resize the Window
        cv2.waitKey(0); cv2.destroyAllWindows(); cv2.waitKey(1) #Handle closing of the window
        return None

    def getPixelRGB(self):
        '''Get a RGB value of the pixel the mouse is pointing at.
        
        :return:
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

    def num_key(self, key):
        '''Convert the string corresponding to a roman number to a key code legible by the keyboard.
        '''
        if not key in self.numbers:
            raise ValueError('Only roman numbers can be converted.')
        return keyboard._KeyCode(char = key)

    def useKeys(self, keys, sleep = True):
        '''For each key in keys, press this key. Keys can be any iterable object.
        '''
        for key in keys:
            self.useKey(key, sleep = sleep)
        return None

    def useKey(self, key, method = 'tap', sleep = True):
        '''An extended method for handling more complex key pressing.

        :args:
            key - Key to be pressed. Accepts all inputs of pynput, along with roman numbers in a string form (i.e. '5').
            method[str] - Method by which the key shall be used. Must be an attribute of the keyboard.
            sleep[bool] - If true, insert a 0.2 sleep time after the key press. Defaults to True.
        '''
        if not hasattr(keyboard, method):
            raise ValueError('You are trying to perform an invalid operation on the keyboard.')
        if key in self.numbers:
            key = self.num_key(key) #Parse a roman number
        getattr(keyboard, method)(key) #Tap, press,... the key
        if sleep:
            time.sleep(0.7)
        return None

    @staticmethod
    def click(x:int, y:int, sleep:bool = True):
        click(x, y)
        if sleep:
            time.sleep(0.7)
        return None

    @staticmethod
    def getWindowHwnd(window_name:str):
        '''Specify a window name and return its window handle. Must have only one window with said name open.

        :return:
            hwnd -  Handle of the said window.
        '''
        windows = []
        def callback(hwnd, extra):
            if window_name in win32gui.GetWindowText(hwnd):
                windows.append(hwnd)
            return True
        win32gui.EnumWindows(callback, None)
        if windows == []: #Window not found
            return None
        elif len(windows) > 1:
            raise ValueError('Multiple windows open.')
        return windows[0]

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

    @classproperty
    def screen_pos(cls):
        '''
        Return a list of 4 coordinates marking the beginning and end of the screen
            in the form [x1,y1, x2, y2].
        '''
        return [0,0] + cls.screen_size

    @classproperty
    def screen_size(cls):
        '''
        A static property defining the screen resolution.
        
        :return:
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

if __name__ == '__main__':
    B = SFBase()