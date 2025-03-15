import os
import random
import datetime
import autopy
import time
from linebot import LineBotApi
from linebot.models import TextSendMessage
from dotenv import load_dotenv
import easyocr
import mss
import numpy as np

load_dotenv()
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
MY_USER_ID = os.getenv("MY_USER_ID")
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

reader = easyocr.Reader(['en'], gpu=True)

CLEAR_ALL_LOCATION = (890, 95)
GET_BOX_LOCATION = ((541, 642), (730, 701))
FAST_START_LOCATION = ((588, 318), (695, 428))
BOX_AMOUNT_LOCATION = ((1050, 243), (1113, 290))
COIN_AMOUNT_LOCATION = ((962, 404), (1123, 464))
EXP_AMOUNT_LOCATION = ((962, 483), (1123, 547))


def game_pos():
    screen = autopy.bitmap.capture_screen()
    icon = autopy.bitmap.Bitmap.open('pic\\blueStackIcon.png')
    pos = screen.find_bitmap(icon)
    if pos is None:
        print("Error: BlueStack icon not found!")
        return None
    return pos


def click(pic_name, loop, sec, ep):
    for _ in range(loop):
        screen = autopy.bitmap.capture_screen()
        a = autopy.bitmap.Bitmap.open(f'pic\\{ep}\\{pic_name}')
        print(f'Find {pic_name} in screen...')
        pos = screen.find_bitmap(a)
        if pos:
            print(f'Found! click.')
            if pic_name == "result.png":
                time.sleep(5)
                record_result()
            autopy.mouse.move(pos[0] + random.randrange(a.width), pos[1] + random.randrange(a.height))
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
            autopy.mouse.move(pos[0] + random.randrange(a.width), pos[1] + random.randrange(a.height))
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


def capture(count):
    if count % 20 == 0:
        autopy.bitmap.capture_screen().save(
            'C:\\Users\\tanet\\OneDrive\\รูปภาพ\\Samsung Gallery\\CookieRun\\recently.png')


def text_reader(region, pos):
    x1, y1 = region[0]
    x2, y2 = region[1]

    # Calculate the correct width & height
    width, height = x2 - x1, y2 - y1
    x1, y1 = region[0][0] + int(pos[0]), region[0][1] + int(pos[1])

    with mss.mss() as sct:
        screenshot = sct.grab({"top": y1, "left": x1, "width": width, "height": height})

    img_array = np.array(screenshot)
    result = reader.readtext(img_array, detail=0)
    if result:
        return result
    else:
        return 0


def record_result():
    with open("C:\\Users\\tanet\\OneDrive\\รูปภาพ\\Samsung Gallery\\CookieRun\\run_record.csv", mode='a', newline='',
              encoding='UTF-8') as f:
        box: list = text_reader(BOX_AMOUNT_LOCATION, game_pos())
        coin: list = text_reader(COIN_AMOUNT_LOCATION, game_pos())
        exp: list = text_reader(EXP_AMOUNT_LOCATION, game_pos())

        box_value = box[0][-1] if box else "N/A"
        coin_value = coin[0].replace(',', '') if coin else "N/A"
        exp_value = exp[0].replace(',', '') if exp else "N/A"
        f.write(
            f'{box_value}, {coin_value}, {exp_value}, ')


def record_trans(count, status):
    with open("C:\\Users\\tanet\\OneDrive\\รูปภาพ\\Samsung Gallery\\CookieRun\\run_record.csv", mode='a', newline='',
              encoding='UTF-8') as f:
        dt = datetime.datetime.now().strftime('%Y/%m/%d %I:%M:%S %p')
        if status == 0:
            f.write(f'{dt}, ')
        if status == 1:
            f.write(f'{dt}, {count} times in total.\n')


def record_error():
    with open("C:\\Users\\tanet\\OneDrive\\รูปภาพ\\Samsung Gallery\\CookieRun\\run_record.csv", mode='a', newline='',
              encoding='UTF-8') as f:
        dt = datetime.datetime.now().strftime('%Y/%m/%d %I:%M:%S %p')
        f.write(f'{dt}, Error.\n')
    dt = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
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
            autopy.mouse.move(pos[0] + random.randrange(app_icon.width), pos[1] + random.randrange(app_icon.height))
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
        record_trans(run_count, 0)
        is_run_correct(fast)
        click('result.png', 60, 5, ep)
        run_count += 1
        record_trans(run_count, 1)
        open_box(ep)
        captcha_check()
        check_before_next_loop(ep)
        capture(run_count)


if __name__ == '__main__':
    main()
