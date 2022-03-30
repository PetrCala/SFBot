from directKeys import click, queryMousePosition, moveMouseTo #For mouse movement
from pynput.keyboard import Key

from static import *
from base import SFBase, keyboard


class TavernBot(SFBase):
    def __init__(self):
        '''Constructor for the TavernBot class.
        '''
        super().__init__()

    def main(self):
        '''Main method of the TavernBot class.
        '''
        if not self.game_focused:
            self.focusGame()
        self.drinkBeer()
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

if __name__ == '__main__':
    B = TavernBot()
    B.main()
    