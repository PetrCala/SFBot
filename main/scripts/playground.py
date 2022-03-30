import win32gui

def winEnumHandler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        print(hex(hwnd), win32gui.GetWindowText(hwnd))
       

def main():
    win32gui.EnumWindows(winEnumHandler, None)




if __name__ == '__main__':
    main()
