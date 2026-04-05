import cv2
import subprocess
import datetime
import random
import time
import os
from dotenv import load_dotenv
# import easyocr
# import mss
import numpy as np
import requests
import logging

load_dotenv()
NTFY_USERNAME = os.getenv("NTFY_USERNAME")
NTFY_PASSWORD = os.getenv("NTFY_PASSWORD")

FAST_START_LOCATION = (739, 352, 160, 160)  # x y w h

CLICK_CONFIG = {
    "start1.png": {"loop": 30, "delay": 1},
    "start2.png": {"loop": 30, "delay": 1},
    "result.png": {"loop": 80, "delay": 5},
    "open_box.png": {"loop": 10, "delay": 1},
    "get_reward.png": {"loop": 10, "delay": 1},
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
    adb_save_screenshot(fr"C:\Users\tanet\OneDrive\รูปภาพ\Samsung Gallery\CookieRun\error_pic\error_{dt}.png")
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


def adb_save_screenshot(output_file):
    try:
        with open(output_file, "wb") as f:
            subprocess.run(
                ["adb", "exec-out", "screencap", "-p"],
                stdout=f,
                check=True
            )
        print(f"Saved screenshot to {output_file}")
    except subprocess.CalledProcessError:
        print("ADB command failed")


def adb_screenshot_to_cv2():
    result = subprocess.run(
        args=["adb", "exec-out", "screencap", "-p"],
        stdout=subprocess.PIPE
    )

    img_bytes = result.stdout

    img_array = np.frombuffer(img_bytes, np.uint8)
    def_img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    return def_img


def random_point_in_template(box):
    x, y, w, h = box
    return random.randint(x, x + w - 1), random.randint(y, y + h - 1)


def template_pos(template_path):
    screen = adb_screenshot_to_cv2()
    template = cv2.imread(template_path)

    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val > 0.8:
        h, w = template.shape[:2]
        x, y = max_loc
        return random_point_in_template((x, y, w, h))

    return None


def adb_tap(pos):
    subprocess.run(["adb", "shell", "input", "tap", str(pos[0]), str(pos[1])])


def click(template_file):
    cfg = CLICK_CONFIG.get(template_file, {})
    loop = cfg.get("loop", 30)
    delay = cfg.get("delay", 1)
    path = f"template/{template_file}"

    for _ in range(loop):
        print(f'Find {template_file}...')

        pos = template_pos(path)

        if pos:
            logging.info(f"{template_file} found! click.")

            if template_file == "result.png":
                time.sleep(5)
                # record_result()

            adb_tap(pos)
            return True

        print('Not found! retry...')
        time.sleep(delay)

    record_error(template_file)
    return False


def is_run_correct(fast: bool):
    loop = 500 if fast else 10
    delay = 0.1 if fast else 5

    for _ in range(loop):
        print("Is cookie running?")

        if template_pos(r"template/heart.png"):
            logging.info("Cookie is running")

            if fast:
                adb_tap(random_point_in_template(FAST_START_LOCATION))

            return True

        print("No, maybe try again.")
        time.sleep(delay)

    record_error("Not run")
    reset_game()
    return False


def check_before_next_loop():
    time.sleep(5)
    if template_pos(f"template/start1.png"):
        return True
    record_error("popup interrupted")
    reset_game()
    return False


def reset_game(pkg="com.devsisters.CookieRunForKakao"):
    # ปิดเกม
    subprocess.run(["adb", "shell", "am", "force-stop", pkg])

    # รอให้ระบบเคลียร์ process
    time.sleep(1)

    # เปิดเกมใหม่
    subprocess.run([
        "adb", "shell", "monkey",
        "-p", pkg,
        "-c", "android.intent.category.LAUNCHER",
        "1"
    ])

    # รอโหลดเกม
    time.sleep(5)


def capture(count):
    if count % 20 == 0:
        adb_save_screenshot(r"C:\Users\tanet\OneDrive\รูปภาพ\Samsung Gallery\CookieRun\recently.png")


# def record_result():
#     pos = game_pos()
#     if not pos:
#         record_error("no game pos")
#         return
#     text_reader_async(BOX_AMOUNT_LOCATION, pos)
#     text_reader_async(COIN_AMOUNT_LOCATION, pos)
#     text_reader_async(EXP_AMOUNT_LOCATION, pos)


def main():
    # ep = int(input("Enter Ep.:"))
    fast = True if not input("Enable faststart? type something for Unable:") else False
    run_count = 0
    while True:
        click('start1.png')
        click('start2.png')
        # record_trans(run_count)
        is_run_correct(fast)
        click('result.png')
        run_count += 1
        # open_box(ep)
        click("open_box.png")
        click("get_reward.png")
        check_before_next_loop()
        capture(run_count)
        time.sleep(5)


if __name__ == '__main__':
    main()
