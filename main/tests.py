import unittest
import pywintypes
import win32.win32gui as win32gui

from scripts.static import *
from scripts.base import SFBase
from scripts.tavernBot import TavernBot, CharacterBot

class testBase(unittest.TestCase):
    def test_game_pos(self):
        B = SFBase()
        game_pos = B.game_pos
        screen_pos = B.screen_pos

        self.assertIsInstance(game_pos, list)
        self.assertIsInstance(screen_pos, list)
        self.assertEqual(len(game_pos), len(screen_pos))
        for i, j in game_pos, screen_pos:
            self.assertLessEqual(i, j)
    
    def test_calculate_coords(self):
        B = SFBase()
        game_pos = B.game_pos
        scale_coords = [0.3, 0.7]
        pixel_coords = [int(game_pos[0]*0.3), int(game_pos[1]*0.3)]
        pixelated_coords = B.calculateCoords(scale_coords)
        scaled_coords = B.calculateCoords(pixel_coords, from_scale = False)

        # Test common attributes
        coords_set = [pixelated_coords, scaled_coords]
        for coords in coords_set:
            self.assertIsInstance(coords, list)
            self.assertEqual(len(coords), 2)
        
        # Test unique attributes
        for i, coord in enumerate(pixelated_coords):
            self.assertTrue(game_pos[i] <= coord <= game_pos[i + 2])

        for coord in scaled_coords:
            self.assertTrue(0 <= coord <= 1)

    def test_focus_game(self):
        browser = BROWSER_NAME
        B = SFBase()
        B.focusGame()
        hwnd_1 = win32gui.GetForegroundWindow()
        hwnd_2 = B.getWindowHwnd(browser)

        self.assertIs(hwnd_1, hwnd_2)
        self.assertIsInstance(hwnd_1, int)


if __name__ == '__main__':
    unittest.main()