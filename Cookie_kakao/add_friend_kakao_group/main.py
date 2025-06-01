import random

import pyautogui as pag
import pyscreeze

pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = False


def main():
    while True:
        try:
            some_button = list(pag.locateAllOnScreen("add_friend.png", confidence=.9, region=(0, 0, 380, 800)))
        except pag.ImageNotFoundException:
            continue
        for pos in some_button:
            print(pos)
            pag.click(pos.left + random.randrange(pos.width), pos.top + random.randrange(pos.height))
            pag.sleep(.1)
            try:
                error = pag.locateOnScreen("error.png", confidence=.9, region=(0, 0, 380, 800))
            except pag.ImageNotFoundException:
                continue
            ok = pag.locateOnScreen("ok.png", confidence=.9, region=(0, 0, 380, 800))
            if ok:
                pag.click(ok.left + random.randrange(ok.width), ok.top + random.randrange(ok.height))
                pag.sleep(.1)
        pag.sleep(.3)
        pag.press("pageup")


if __name__ == '__main__':
    main()
