import pywintypes
import win32.win32gui as win32gui
from pynput.keyboard import Key
from PIL import ImageGrab, Image
import pywintypes
import pytesseract

from static import *
from base import SFBase, keyboard
from directKeys import queryMousePosition, moveMouseTo #For mouse movement

import time


class TavernBot(SFBase):
    def __init__(self):
        '''Constructor for the TavernBot class.
        '''
        super().__init__()

    def main(self):
        '''Main method of the TavernBot class.
        '''
        #hwnd = self.getWindowHwnd(SF_NAME)
        #if not self.game_focused:
        #    self.focusGame()
        #self.drinkBeer()
        #click(423,69) #Navbar
        return None

    def getQuestInfo(self):
        '''Search the screen and read the quest information for all quests.
        Return this information as a dictionary.
        '''
        pass

    def calculateOptimalQuest(self):
        '''Calculate the optimal quest based on the specified parameters (gold/exp).
        '''
        pass

    def startOptimalQuest(self):
        '''Start the optimal quest based on the information about its quality.
        '''
        pass

    def doQuest(self):
        '''
        Open a tavern window, select the best quest based on the desired parameters,
        go on this quest and optionally skip it and get the rewards.
        '''
        self.changeGameWindow(SF_WINDOW_TAVERN)
        self.useKey(Key.enter) #Open quest log
        self.calculateOptimalQuest()
        self.startOptimalQuest()
        self.useKey(Key.esc) #Close quest log
        return None

    def drinkBeer(self, beers:int = 1, get_window = False):
        '''Drink a beer in the tavern.

        :args:
            beers[int] - Number of beers to be drank. Defaults to one.
            get_window[bool] - If True, fetch the base tavern window. Defaults to False.
        '''
        if not beers > 0:
            raise ValueError('You must drink at least one beer')
        self.changeGameWindow(SF_WINDOW_TAVERN)
        keys = [Key.right]
        [keys.append(Key.enter) for i in range(beers)]
        keys.append(Key.esc)
        self.useKeys(keys) #Drink
        return None

    def startCityGuard(self):
        '''Start a city guard duty.
        '''
        pass

class CharacterBot(SFBase):
    def __init__(self):
        '''Constructor for the TavernBot class.
        '''
        super().__init__()

    def upgradeAttributes(self, attr:str, times:int = 1):
        '''Focus the character window and upgrade the desired attributes
        using the 'upgradeAttribute' method.
        '''
        self.changeGameWindow(SF_WINDOW_CHARACTER)
        self.upgradeAttribute(attr, times = times)
        return None

    def upgradeAttribute(self, attr:str, times:int = 1):
        '''Upgrade an attribute of your character.
        Assumes the character window to be open.

        :args:
            attr[str] - Name of the attribute to be upgraded.
            times[int] - Number of times the attribute should be upgraded.
        '''
        attr_names = list(CHAR_ATTRIBUTES.keys())
        attr = attr.upper()
        if not attr in attr_names:
            raise ValueError(f'A non existent attribute. Must be one of the following: {attr_names}')
        attr_coords = CHAR_ATTRIBUTES.get(attr)
        for _ in range(times):
            self.click(attr_coords, sleep = True)
        return None

    def main(self):
        pass
        #self.upgradeAttribute('LUCK', times = 2)
        #coords = self.calculateCoords([1081, 770], from_scale=False)
        #print(coords)
        #self.openScreen('Test window')
        #print(self.openScreen('Test window'))
        #self.upgradeAttributes('str', times = 2)

if __name__ == '__main__':
    B = CharacterBot()
    B.focusGame()
    #text = B.readTextInRange(FORT_FIGHT_BUTTON)
    #a = pytesseract.get_languages(config='')
    #B.main()
    #B = TavernBot()
    #B.drinkBeer()