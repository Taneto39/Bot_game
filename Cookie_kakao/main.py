import os
import random
import datetime
import autopy
import time
from linebot import LineBotApi
from linebot.models import TextSendMessage
from dotenv import load_dotenv

load_dotenv()
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
MY_USER_ID = os.getenv("MY_USER_ID")
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

GET_BOX_LOCATION = ((541, 642), (730, 701))
FAST_START_LOCATION = ((588, 318), (695, 428))
CLEAR_ALL_LOCATION = (890, 95)


def game_pos():
    screen = autopy.bitmap.capture_screen()
    icon = autopy.bitmap.Bitmap.open('pic\\blueStackIcon.png')
    return screen.find_bitmap(icon)


def click(pic_name, loop, sec, ep):
    for _ in range(loop):
        screen = autopy.bitmap.capture_screen()
        a = autopy.bitmap.Bitmap.open(f'pic\\{ep}\\{pic_name}')
        print(f'Find {pic_name} in screen...')
        pos = screen.find_bitmap(a)
        if pos:
            print(f'Found! click.')
            autopy.mouse.move(pos[0] + random.randrange(a.width()), pos[1] + random.randrange(a.height()))
            autopy.mouse.click()
            break
        print('Not found! Find again.')
        time.sleep(sec)
    else:
        record_error()
        return


def open_box(ep):
    for _ in range(10):
        screen = autopy.bitmap.capture_screen()
        a = autopy.bitmap.Bitmap.open(f'pic\\open_box.png')
        print(f'Find open_box.png in screen...')
        pos = screen.find_bitmap(a)
        if pos:
            print(f'Found! click.')
            autopy.mouse.move(pos[0] + random.randrange(a.width()), pos[1] + random.randrange(a.height()))
            autopy.mouse.click()
            break
        print('Not found! Find again.')
        time.sleep(1)
    else:
        return
    get_box(10, 1, ep)


def get_box(loop, sec, ep):
    for _ in range(loop):
        print('Get reward.')
        autopy.mouse.move(game_pos()[0] + random.randrange(GET_BOX_LOCATION[0][0], GET_BOX_LOCATION[1][0]),
                          game_pos()[1] + random.randrange(GET_BOX_LOCATION[0][1], GET_BOX_LOCATION[1][1]))
        autopy.mouse.click()
        time.sleep(sec)
        screen = autopy.bitmap.capture_screen()
        a = autopy.bitmap.Bitmap.open(f'pic/{ep}/start1.png')
        if screen.find_bitmap(a):
            print('Got reward.')
            return
        print('Can\'t get reward. Try again...')
    else:
        record_error()
        return


def is_run_correct(fast: bool):
    if not fast:
        for _ in range(10):
            print('Is cookie running?')
            screen = autopy.bitmap.capture_screen()
            a = autopy.bitmap.Bitmap.open('pic/heart.png')
            if screen.find_bitmap(a):
                print('Cookie\'s running')
                return
            print('No, maybe try again.')
            time.sleep(5)
        else:
            record_error()
            return
    if fast:
        for _ in range(500):
            print('Is cookie running?')
            screen = autopy.bitmap.capture_screen()
            a = autopy.bitmap.Bitmap.open('pic/heart.png')
            pos = game_pos()
            if screen.find_bitmap(a):
                print('Cookie\'s running')
                autopy.mouse.move(pos[0] + random.randrange(FAST_START_LOCATION[0][1], FAST_START_LOCATION[1][0]),
                                  pos[1] + random.randrange(FAST_START_LOCATION[0][1], FAST_START_LOCATION[1][1]))
                autopy.mouse.click()
                return
            print('No, maybe try again.')
            time.sleep(0.1)
        else:
            record_error()
            return


def captcha_check():
    for _ in range(3):
        print('Is captcha appear?')
        screen = autopy.bitmap.capture_screen()
        captcha = autopy.bitmap.Bitmap.open('captcha\\captcha.png')
        if screen.find_bitmap(captcha):
            print('Captcha\'s caught. Send Notification.')
            input()
        time.sleep(1)
    else:
        return


def record_trans(count, txt):
    # dt = datetime.datetime.now().strftime('%m%d.%y_%H%M%S')
    # autopy.bitmap.capture_screen().save(f'trans_pic\\{count:04}-{dt}.png')
    if count % 20 == 0:
        autopy.bitmap.capture_screen().save(
            'C:\\Users\\tanet\\OneDrive\\รูปภาพ\\Samsung Gallery\\CookieRun\\recently.png')
    with open("C:\\Users\\tanet\\OneDrive\\รูปภาพ\\Samsung Gallery\\CookieRun\\run_record.csv", mode='a', newline='',
              encoding='UTF-8') as f:
        dt = datetime.datetime.now().strftime('%m%d/%y-%I:%M:%S %p')
        f.write(f'{dt}, {txt}, {count} times in total.\n')


def record_error():
    with open("C:\\Users\\tanet\\OneDrive\\รูปภาพ\\Samsung Gallery\\CookieRun\\run_record.csv", mode='a', newline='',
              encoding='UTF-8') as f:
        dt = datetime.datetime.now().strftime('%m%d/%y-%I:%M:%S %p')
        f.write(f'{dt}, Error.\n')
    dt = datetime.datetime.now().strftime('%m%d.%y_%H%M%S')
    autopy.bitmap.capture_screen().save(
        f'C:\\Users\\tanet\\OneDrive\\รูปภาพ\\Samsung Gallery\\CookieRun\\error_pic\\error_{dt}.png')


def start1_pos(ep):
    screen = autopy.bitmap.capture_screen()
    start1 = autopy.bitmap.Bitmap.open(f'pic/{ep}/start1.png')
    return screen.find_bitmap(start1)


def check_before_next_loop(ep):
    if start1_pos(ep):
        return
    else:
        reset_game(ep)


def reset_game(ep):
    message = TextSendMessage(text="Some error got caught.")
    line_bot_api.push_message(MY_USER_ID, message)
    record_error()
    print('Error! Reset game...')
    while True:
        print('Find recent button.')
        screen = autopy.bitmap.capture_screen()
        recent_button = autopy.bitmap.Bitmap.open('pic\\recent_app.png')
        pos = screen.find_bitmap(recent_button)
        if pos:
            print('Found! click.')
            autopy.mouse.move(pos[0] + random.randrange(20), pos[1] + random.randrange(20))
            autopy.mouse.click()
            time.sleep(1)
        else:
            continue
        print('Click clear all.')
        autopy.mouse.move(game_pos()[0] + CLEAR_ALL_LOCATION[0], game_pos()[1] + CLEAR_ALL_LOCATION[1])
        autopy.mouse.click()
        time.sleep(1)
        print('Find CookieRun Icon.')
        screen = autopy.bitmap.capture_screen()
        app_icon = autopy.bitmap.Bitmap.open('pic\\app_icon.png')
        pos = screen.find_bitmap(app_icon)
        if pos:
            print('Found! click.')
            autopy.mouse.move(pos[0] + random.randrange(app_icon.width()), pos[1] + random.randrange(app_icon.height()))
            autopy.mouse.click()
            time.sleep(1)
        else:
            continue
        # time.sleep(15)
        # print('Is game ready?')
        # pos = start1_pos()
        # if pos:
        #     print('Game\'s ready!!')
        #     return
        for _ in range(12):
            time.sleep(5)
            print('Is game ready?')
            pos = start1_pos(ep)
            if pos:
                print('Game\'s ready!!')
                return
            else:
                print('Not found! Find again..')


def main():
    ep = int(input("Enter Ep.:"))
    fast = True if not input("Enable faststart? type something for Unable:") else False
    run_count = 0
    while True:
        click('start1.png', 30, 1, ep)
        click('start2.png', 30, 1, ep)
        is_run_correct(fast)
        click('result.png', 60, 5, ep)
        open_box(ep)
        captcha_check()
        check_before_next_loop(ep)
        run_count += 1
        record_trans(run_count, 'Run')


if __name__ == '__main__':
    main()
