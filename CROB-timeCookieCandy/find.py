import autopy


def find():
    screen = autopy.bitmap.capture_screen()
    a = autopy.bitmap.Bitmap.open('blueStackIcon.png')
    print(screen.find_bitmap(a))


find()
