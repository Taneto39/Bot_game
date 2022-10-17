import autopy

icon = autopy.bitmap.Bitmap.open('bonustimeItem.png')
while True:
    screen = autopy.bitmap.capture_screen()
    pos = screen.find_bitmap(icon)
    if pos:
        print(f'Found icon at {pos}')
    else:
        print('Not found!!!!')