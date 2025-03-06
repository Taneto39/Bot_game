import time

import autopy


def find():
    screen = autopy.bitmap.capture_screen()
    a = autopy.bitmap.Bitmap.open('pic\\get_box.png')
    print(screen.find_bitmap(a))


if __name__ == '__main__':
    while True:
        find()
        time.sleep(.1)
