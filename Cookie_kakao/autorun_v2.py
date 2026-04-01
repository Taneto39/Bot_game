# from concurrent.futures import ThreadPoolExecutor
import subprocess
import datetime
import random
import time
import os
import pyautogui as pag
from dotenv import load_dotenv
# import easyocr
# import mss
# import numpy as np
import requests
import logging

load_dotenv()
NTFY_USERNAME = os.getenv("NTFY_USERNAME")
NTFY_PASSWORD = os.getenv("NTFY_PASSWORD")

# CLEAR_ALL_LOCATION = (890, 95)
GET_BOX_LOCATION = ((541, 642), (730, 701))
FAST_START_LOCATION = ((598, 342), (685, 414))
BOX_AMOUNT_LOCATION = ((1050, 243), (1113, 290))
COIN_AMOUNT_LOCATION = ((962, 404), (1123, 464))
EXP_AMOUNT_LOCATION = ((962, 483), (1123, 547))

CLICK_CONFIG = {
    "start1.png": {"loop": 30, "delay": 1},
    "start2.png": {"loop": 30, "delay": 1},
    "result.png": {"loop": 80, "delay": 5},
}

# READER = easyocr.Reader(['en'], gpu=False)
# executor = ThreadPoolExecutor(max_workers=1)
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format='"%(asctime)s","%(levelname)s","%(message)s"',
    encoding="utf-8",
    filemode="a",
)

pag.useImageNotFoundException(False)


def ntfy_publish(title, msg, priority=3):
    requests.post(
        url="http://ntfy.papaneko.cc/cookierun_bot",
        data=msg.encode('utf-8'),
        auth=(NTFY_USERNAME, NTFY_PASSWORD),
        headers={
            "Title": title,
            "Priority": str(priority),
        },
        timeout=3
    )


def record_error(type_error):
    logging.error(f"Error: {type_error}")
    with open(r"C:\Users\tanet\OneDrive\รูปภาพ\Samsung Gallery\CookieRun\run_record.csv", mode='a', newline='',
              encoding='UTF-8') as f:
        dt = datetime.datetime.now().strftime('%Y/%m/%d %I:%M:%S %p')
        f.write(f'{dt}, Error.\n')
    dt = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    pag.screenshot(fr"C:\Users\tanet\OneDrive\รูปภาพ\Samsung Gallery\CookieRun\error_pic\error_{dt}.png")
    ntfy_publish(title="Error", msg=f"Error got caught: {type_error}")


def record_trans(count):
    with open(r"C:\Users\tanet\OneDrive\รูปภาพ\Samsung Gallery\CookieRun\run_record.csv", mode='a', newline='',
              encoding='UTF-8') as f:
        dt = datetime.datetime.now().strftime('%Y/%m/%d %I:%M:%S %p')
        f.write(f'{dt}, Run no:{count}')


# def text_reader(region, pos):
#     x1, y1 = region[0]
#     x2, y2 = region[1]
#
#     # Calculate the correct width & height
#     width, height = x2 - x1, y2 - y1
#     x1, y1 = region[0][0] + int(pos[0]), region[0][1] + int(pos[1])
#
#     with mss.mss() as sct:
#         screenshot = sct.grab({"top": y1, "left": x1, "width": width, "height": height})
#
#     img_array = np.array(screenshot)
#     result = READER.readtext(img_array, detail=0)
#
#     value = result[0] if result else "N/A"
#
#     with open(r"C:\Users\tanet\OneDrive\รูปภาพ\Samsung Gallery\CookieRun\run_record.csv", "a",
#               encoding="UTF-8") as f:
#         f.write(f"{value}, ")


# def text_reader_async(region, pos):
#     return executor.submit(text_reader, region, pos)


def game_pos():
    pos = pag.locateOnScreen(r"pic\blueStackIcon.png")  # left top width height
    if not pos:
        logging.error("Error: BlueStack icon not found!")
        return None
    return pos


def click(pic_name, ep):
    cfg = CLICK_CONFIG.get(pic_name, {})
    loop = cfg.get("loop", 30)
    delay = cfg.get("delay", 1)
    path = f"pic/{ep}/{pic_name}"

    for _ in range(loop):
        print(f'Find {pic_name}...')

        pos = pag.locateOnScreen(path)

        if pos:
            logging.info(f"{pic_name} found! click.")

            if pic_name == "result.png":
                time.sleep(5)
                # record_result()

            x, y, w, h = pos
            pag.click(
                x + random.randrange(w),
                y + random.randrange(h)
            )
            return True

        print('Not found! retry...')
        time.sleep(delay)

    record_error(pic_name)
    return False


def is_run_correct(fast: bool):
    loop = 500 if fast else 10
    delay = 0.1 if fast else 5

    for _ in range(loop):
        print("Is cookie running?")

        if pag.locateOnScreen(r"pic/heart.png"):
            logging.info("Cookie is running")

            if fast:
                pos = game_pos()
                if not pos:
                    record_error("no game pos")
                    return
                pag.click(
                    pos[0] + random.randrange(FAST_START_LOCATION[0][0], FAST_START_LOCATION[1][0]),
                    pos[1] + random.randrange(FAST_START_LOCATION[0][1], FAST_START_LOCATION[1][1])
                )

            return True

        print("No, maybe try again.")
        time.sleep(delay)

    record_error("Not run")
    return False


def get_box(ep):
    for _ in range(10):
        print("Get reward.")
        pos = game_pos()
        if not pos:
            record_error("no game pos")
            return
        pag.click(pos[0] + random.randrange(GET_BOX_LOCATION[0][0], GET_BOX_LOCATION[1][0]),
                  pos[1] + random.randrange(GET_BOX_LOCATION[0][1], GET_BOX_LOCATION[1][1]))
        time.sleep(1)
        if pag.locateOnScreen(fr"pic/{ep}/start1.png"):
            logging.info("Got reward.")
            return
        print("Can't get reward. Try again...")
    else:
        record_error("Can't get box.")


def open_box(ep):
    for _ in range(10):
        print(f"Find open_box.png in screen...")
        pos = pag.locateOnScreen(r"pic/open_box.png")
        if pos:
            logging.info(f"Box is found ! click.")
            pag.click(pos[0] + random.randrange(pos.width), pos[1] + random.randrange(pos.height))
            break
        print("Not found! Find again.")
        time.sleep(1)
    else:
        return
    get_box(ep)


def check_before_next_loop(ep):
    if pag.locateOnScreen(f'pic/{ep}/start1.png'):
        return True
    record_error("notification interrupted")
    reset_game(ep)
    return False


def reset_game(ep):
    logging.error('Error! Reset game...')
    # while True:
    for _ in range(3):
        print("Reopen Bluestack.")
        subprocess.run(["taskkill", "/im", "HD-Player.exe", "/f"])
        os.startfile(r"C:\Users\tanet\OneDrive\เดสก์ท็อป\쿠키런 - BlueStacks App Player 15.lnk")
        for _ in range(12):
            time.sleep(5)
            print('Is game ready?')
            if pag.locateOnScreen(fr"pic/{ep}/start1.png"):
                logging.info(f"Game is ready!!")
                return
            else:
                print('Not found! Find again..')


def capture(count):
    if count % 20 == 0:
        pag.screenshot(r"C:\Users\tanet\OneDrive\รูปภาพ\Samsung Gallery\CookieRun\recently.png")


# def record_result():
#     pos = game_pos()
#     if not pos:
#         record_error("no game pos")
#         return
#     text_reader_async(BOX_AMOUNT_LOCATION, pos)
#     text_reader_async(COIN_AMOUNT_LOCATION, pos)
#     text_reader_async(EXP_AMOUNT_LOCATION, pos)


def main():
    ep = int(input("Enter Ep.:"))
    fast = True if not input("Enable faststart? type something for Unable:") else False
    run_count = 0
    while True:
        click('start1.png', ep)
        click('start2.png', ep)
        # record_trans(run_count)
        is_run_correct(fast)
        click('result.png', ep)
        run_count += 1
        open_box(ep)
        check_before_next_loop(ep)
        capture(run_count)


if __name__ == '__main__':
    main()
