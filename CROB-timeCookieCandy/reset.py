import time
import autopy
# import bot


def press_confirm(game_pos, name, sec):
    screen = autopy.bitmap.capture_screen()
    cookie_icon = autopy.bitmap.Bitmap.open(f'{name}')
    for count in range(30):
        time.sleep(0.5)
        if not screen.find_bitmap(cookie_icon, rect=((480, 480), (70, 70))):
            print(f'{name} not found. <press button>')
            autopy.mouse.move(game_pos[0] + 403, game_pos[1] + 517)
            autopy.mouse.click()
            time.sleep(sec)
            screen = autopy.bitmap.capture_screen()
        else:
            break
    else:
        reset_game(game_pos)


def click_icon(name):
    screen = autopy.bitmap.capture_screen()
    icon = autopy.bitmap.Bitmap.open(f'{name}')
    pos = screen.find_bitmap(icon)
    if pos:
        autopy.mouse.move(pos[0], pos[1])
        autopy.mouse.click()
    else:
        print(f'{name} not found!!-')


def reset_game(game_pos):
    # close all apps
    click_icon('recentIcon.png')
    time.sleep(5.0)
    # click clear all
    autopy.mouse.move(703, 82)
    autopy.mouse.click()
    # open game
    time.sleep(5.0)
    click_icon('CROB_Icon.png')
    time.sleep(30.0)
    # time.sleep(60.0)
    get_ready(game_pos, 2.0)


def get_ready(game_pos, sec):
    screen = autopy.bitmap.capture_screen()
    confirm_icon = autopy.bitmap.Bitmap.open('confirmIcon.png')
    if screen.find_bitmap(confirm_icon):
        autopy.mouse.move(game_pos[0]+477, game_pos[1]+383)
        autopy.mouse.click()
        press_confirm(game_pos, 'myCookieIcon.png', sec)
    # click play
    autopy.mouse.move(game_pos[0]+811, game_pos[1]+516)
    autopy.mouse.click()
    time.sleep(sec)
    # click special
    autopy.mouse.move(game_pos[0]+385, game_pos[1]+116)
    autopy.mouse.click()
    time.sleep(sec)
    # click basic
    autopy.mouse.move(game_pos[0]+198, game_pos[1]+116)
    autopy.mouse.click()
    time.sleep(sec)
    # click challenge
    click_icon('challengeIcon.png')
    time.sleep(sec)
    # click box
    autopy.mouse.move(game_pos[0]+887, game_pos[1]+116)
    autopy.mouse.click()
    time.sleep(sec)
    # click favorite
    autopy.mouse.move(game_pos[0]+890, game_pos[1]+305)
    autopy.mouse.click()
    time.sleep(sec)
    # click time cookie
    click_icon('timeCookieIcon.png')
    time.sleep(sec)
    """
    click_icon('myCookieIcon.png')
    time.sleep(15.0)
    click_icon('timeCookieIcon.png')
    time.sleep(15.0)
    click_icon('challengeIcon.png')
    """


game_pos = (6, 6)
reset_game(game_pos)
