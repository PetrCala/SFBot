from directKeys import queryMousePosition, moveMouseTo #For mouse movement
import win32gui
from pynput.keyboard import Key

from static import *
from base import SFBase, keyboard

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
        if not self.gameIsFocused():
            self.focusGame()
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
        self.attributes = {
            'STR': [782, 700],
            'DEX': [782, 770],
            'INT': [782, 840],
            'HP': [1081, 700],
            'LUCK': [1081, 770],
        }

    def upgradeAttributes(self, attr:str, times:int = 1):
        '''Focus the character window and upgrade the desired attributes
        using the 'upgradeAttribute' method.
        '''
        self.focusGame()
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
        attr_names = list(self.attributes.keys())
        attr = attr.upper()
        if not attr in attr_names:
            raise ValueError(f'A non existent attribute. Must be one of the following: {attr_names}')
        attr_coords = self.attributes.get(attr)
        for _ in range(times):
            self.click(attr_coords[0], attr_coords[1], sleep = True)
        return None

    def main(self):
        self.upgradeAttributes('str', times = 2)

if __name__ == '__main__':
    B = CharacterBot()
    B.main()
    