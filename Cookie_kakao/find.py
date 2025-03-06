import time

import autopy


def find():
    screen = autopy.bitmap.capture_screen()
    pics_name = ['heart.png', 'result.png', 'start1.png', 'start2.png']
    ep = int(input("ep:"))
    for pic_name in pics_name:
        a = autopy.bitmap.Bitmap.open(f'pic\\{ep}\\{pic_name}')
        print(screen.find_bitmap(a))


if __name__ == '__main__':
    while True:
        find()
        time.sleep(1)
