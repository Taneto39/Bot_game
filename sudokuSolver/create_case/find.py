import autopy


def find():
    screen = autopy.bitmap.capture_screen()
    a = autopy.bitmap.Bitmap.open('blank.PNG', )
    print(screen.find_bitmap(a))


find()
