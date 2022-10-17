import autopy
import time
import datetime


def find_game_pos(screen):
    bs_icon = autopy.bitmap.Bitmap.open('blueStackIcon.png')
    pos = screen.find_bitmap(bs_icon)
    if pos:
        return pos


def record_trans(count, txt):
    with open("run_record.csv", mode='a', newline='', encoding='UTF-8') as f:
        dt = datetime.datetime.now().strftime('%m%d/%y-%I:%M:%S %p')
        f.write(f'{dt}, {txt}, {count} times in total.\n')


def record_error():
    dt = datetime.datetime.now().strftime('%m%d.%y_%H%M%S')
    autopy.bitmap.capture_screen().save(f'error{dt}.png')


def is_game_run_correct(game_pos):
    heart_icon = autopy.bitmap.Bitmap.open('heartIcon.png')
    for count in range(30):
        screen = autopy.bitmap.capture_screen()
        time.sleep(1.0)
        print(f'find heartIcon.png {count + 1}/30')
        if screen.find_bitmap(heart_icon, rect=((221, 32), (64, 64))):
            print('Game run correct!!')
            globals()['run_count'] += 1
            record_trans(globals()['run_count'], 'Run')
            break
    else:
        reset_game(game_pos, play=True)


def get_item(game_pos):
    screen = autopy.bitmap.capture_screen()
    camera_icon = autopy.bitmap.Bitmap.open('cameraIcon.png')
    for count in range(300):
        if not screen.find_bitmap(camera_icon, rect=((843, 460), (120, 120))):
            print(f'Game not finish yet. {count + 1}')
            if count + 1 == 75:
                press_slide(game_pos)
            time.sleep(1.0)
            screen = autopy.bitmap.capture_screen()
        else:
            print('Game is finish')
            break
    else:
        reset_game(game_pos, play=False)
    press_confirm(game_pos, 'cookieIcon.png', 1.0)


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
        reset_game(game_pos, play=False)


def click_play(game_pos):
    print('<Press play button>')
    autopy.mouse.move(game_pos[0] + 714, game_pos[1] + 486)
    autopy.mouse.click()
    purchase_crystal(game_pos)


def purchase_crystal(game_pos):
    time.sleep(2.0)
    print('Does cookie get tired? ', end='')
    screen = autopy.bitmap.capture_screen()
    cookie_run_out = autopy.bitmap.Bitmap.open('cookieRunOut.png')
    if not screen.find_bitmap(cookie_run_out, rect=((440, 250), (90, 60))):
        print('No.')
    else:
        print('Yes.')
        print('Wake up cookie!!')
        # exit()
        autopy.mouse.move(game_pos[0] + 648, game_pos[1] + 421)
        autopy.mouse.click()
        time.sleep(3.0)
        click_play(game_pos)


def press_slide(game_pos):
    autopy.mouse.move(game_pos[0] + 714, game_pos[1] + 486)
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


def reset_game(game_pos, play):
    globals()['error_count'] += 1
    record_error()
    record_trans(globals()['error_count'], 'Reset')
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
    get_ready(game_pos, 15.0, play=play)


def get_ready(game_pos, sec, play):
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
    time.sleep(5.0)
    # click basic
    autopy.mouse.move(game_pos[0]+198, game_pos[1]+116)
    autopy.mouse.click()
    time.sleep(5.0)
    # click challenge
    click_icon('challengeIcon.png')
    time.sleep(sec)
    # click box
    autopy.mouse.move(game_pos[0]+887, game_pos[1]+116)
    autopy.mouse.click()
    time.sleep(5.0)
    # click favorite
    autopy.mouse.move(game_pos[0]+890, game_pos[1]+305)
    autopy.mouse.click()
    time.sleep(5.0)
    # click time cookie
    click_icon('timeCookieIcon.png')
    time.sleep(sec)
    if play:
        click_play(game_pos)
    """
    click_icon('myCookieIcon.png')
    time.sleep(15.0)
    click_icon('timeCookieIcon.png')
    time.sleep(15.0)
    click_icon('challengeIcon.png')
    """


def start_game():
    screen = autopy.bitmap.capture_screen()
    game_pos = find_game_pos(screen)
    click_play(game_pos)
    globals()['run_count'] = 0
    globals()['error_count'] = 0
    while True:
        is_game_run_correct(game_pos)
        get_item(game_pos)
        time.sleep(3.0)
        click_play(game_pos)


start_game()
