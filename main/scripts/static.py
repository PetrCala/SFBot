APP_NAME = 'SFBot'
SF_WEBSITE = 's26.sfgame.cz'
SF_NAME = 'Shakes & Fidget'

BROWSER_NAME = 'Google Chrome'
BROWSER_PATHS = ['C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
                 'C:/Program Files/Google/Chrome/Application/chrome.exe']

#Static variables
SF_WINDOW_ARENA = 'ARENA'
SF_WINDOW_CHARACTER = 'CHARACTER'
SF_WINDOW_OPTIONS = 'OPTIONS'
SF_WINDOW_TAVERN = 'TAVERN'
SF_WINDOWS = [SF_WINDOW_ARENA, SF_WINDOW_CHARACTER, SF_WINDOW_OPTIONS, SF_WINDOW_TAVERN]
SF_WINDOWS_HOTKEYS = {
    SF_WINDOW_ARENA: 'a',
    SF_WINDOW_CHARACTER: 'c',
    SF_WINDOW_OPTIONS: 'o',
    SF_WINDOW_TAVERN: 't',
}
SF_BASE_WINDOW = SF_WINDOW_OPTIONS



# Character
CHAR_ATTR_NAMES = ['STR', 'DEX', 'INT', 'HP', 'LUCK']
CHAR_ATTRIBUTES = {
    'STR': [0.390, 0.634], 
    'DEX': [0.390, 0.711],
    'INT': [0.390, 0.789],
    'HP': [0.576, 0.634],
    'LUCK': [0.576, 0.711],
}


# FORTRESS
FORT_FIGHT_BUTTON = [0.239, 0.876, 0.39, 0.949]

