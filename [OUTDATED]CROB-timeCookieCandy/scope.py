import autopy
import tkinter


def get_pos():
    return autopy.mouse.location()


def location():
    screen = autopy.bitmap.capture_screen()
    bs_icon = autopy.bitmap.Bitmap.open('blueStackIcon.png')
    game_pos = screen.find_bitmap(bs_icon)
    if game_pos:
        pass


location()
