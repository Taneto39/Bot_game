import autopy


def click():
    screen = autopy.bitmap.capture_screen()
    bs_icon = autopy.bitmap.Bitmap.open('pic\\blueStackIcon.png')
    game_pos = screen.find_bitmap(bs_icon)
    if game_pos:
        autopy.mouse.move(game_pos[0]+930,game_pos[1]+825)
        autopy.mouse.click()


click()