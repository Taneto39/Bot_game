import autopy


def location():
    screen = autopy.bitmap.capture_screen()
    bs_icon = autopy.bitmap.Bitmap.open('suIcon.PNG')
    game_pos = screen.find_bitmap(bs_icon)
    if game_pos:
        while True:
            current_pos = autopy.mouse.location()
            print((current_pos[0]-game_pos[0], current_pos[1]-game_pos[1]))


location()
