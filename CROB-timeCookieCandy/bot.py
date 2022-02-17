import autopy
import time
# import datetime


def find_game_pos(screen):
    bs_icon = autopy.bitmap.Bitmap.open('blueStackIcon.png')
    pos = screen.find_bitmap(bs_icon)
    if pos:
        return pos


def is_game_run_correct(game_pos):
    coin_icon = autopy.bitmap.Bitmap.open('coinStart.png')
    for count in range(30):
        screen = autopy.bitmap.capture_screen()
        time.sleep(1.0)
        print(f'find coin {count+1}/30')
        if screen.find_bitmap(coin_icon):
            print('Game run correct!!')
            break
    else:
        reset_game(game_pos)


def get_item(game_pos):
    screen = autopy.bitmap.capture_screen()
    camera_icon = autopy.bitmap.Bitmap.open('cameraIcon.png')
    # count = 0
    # while not screen.find_bitmap(camera_icon):  # find camera_icon until found
    #     time.sleep(1.0)
    #     count += 1
    #     if count == 67:
    #         press_slide(game_pos)
    #     if count >= 600:
    #         reset_game(game_pos)
    #     print(f'Game not finish yet. {count}')
    #     screen = autopy.bitmap.capture_screen()
    # else:  # found camera_icon
    #     print('Game is finish')
    for count in range(600):
        if not screen.find_bitmap(camera_icon):
            print(f'Game not finish yet. {count+1}')
            # if count+1 == 67:
            #     press_slide(game_pos)
            time.sleep(1.0)
            screen = autopy.bitmap.capture_screen()
        else:
            print('Game is finish')
            break
    else:
        reset_game(game_pos)
    press_confirm(game_pos, 'cookieIcon.png', 1.0)


def press_confirm(game_pos, name, sec):
    screen = autopy.bitmap.capture_screen()
    cookie_icon = autopy.bitmap.Bitmap.open(f'{name}')
    # while not screen.find_bitmap(cookie_icon):  # find cookieIcon until found
    #     time.sleep(1.0)
    #     print('cookieIcon not found. <press button>')
    #     autopy.mouse.move(game_pos[0]+403, game_pos[1]+517)
    #     autopy.mouse.click()
    #     time.sleep(sec)
    #     screen = autopy.bitmap.capture_screen()
    for count in range(10):
        if not screen.find_bitmap(cookie_icon):
            print(f'{name} not found. <press button>')
            autopy.mouse.move(game_pos[0]+403, game_pos[1]+517)
            autopy.mouse.click()
            time.sleep(sec)
            screen = autopy.bitmap.capture_screen()
    else:
        reset_game(game_pos)


def click_play(game_pos):
    print('<Press play button>')
    autopy.mouse.move(game_pos[0]+714, game_pos[1]+486)
    autopy.mouse.click()


def purchase_crystal(game_pos):
    time.sleep(2.0)
    print('Does cookie get tired? ', end='')
    screen = autopy.bitmap.capture_screen()
    cookie_run_out = autopy.bitmap.Bitmap.open('cookieRunOut.png')
    if not screen.find_bitmap(cookie_run_out):
        print('No.')
    else:
        print('Yes.')
        print('Wake up cookie!!')
        autopy.mouse.move(game_pos[0]+648, game_pos[1]+421)
        autopy.mouse.click()
        time.sleep(3.0)
    click_play(game_pos)


def press_slide(game_pos):
    autopy.mouse.move(game_pos[0]+714, game_pos[1]+486)
    autopy.mouse.toggle(down=True)
    time.sleep(5.0)
    autopy.mouse.toggle(down=False)


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
    time.sleep(60.0)
    screen = autopy.bitmap.capture_screen()
    confirm_icon = autopy.bitmap.Bitmap.open('confirmIcon.png')
    if screen.find_bitmap(confirm_icon):
        autopy.mouse.move(game_pos[0]+477, game_pos[1]+383)
        autopy.mouse.click()
        press_confirm(game_pos, 'myCookieIcon.png', 15.0)
    click_icon('myCookieIcon.png')
    time.sleep(15.0)
    click_icon('timeCookieIcon.png')
    time.sleep(15.0)
    click_icon('challengeIcon.png')


def start_game():
    screen = autopy.bitmap.capture_screen()
    game_pos = find_game_pos(screen)
    click_play(game_pos)
    while True:
        is_game_run_correct(game_pos)
        get_item(game_pos)
        time.sleep(3.0)
        click_play(game_pos)
        purchase_crystal(game_pos)


start_game()
