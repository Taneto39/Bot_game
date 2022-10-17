import autopy
import time

box_size = 47


def print_every_num(game_pos):
    for num in range(1, 10):
        globals()[f'pic_{num}'] = autopy.bitmap.Bitmap.open(f'{num}.png')
    for row in range(9):
        for column in range(9):
            autopy.mouse.move(game_pos[0] + (column * 47) + 23.5, game_pos[1] + (row * 47) + 23.5)
            autopy.mouse.click()
            box = autopy.bitmap.capture_screen(rect=((game_pos[0] + (column * 47), game_pos[1] + (row * 47)), (47, 47)))
            for num in range(1, 10):
                if box.find_bitmap(globals()[f'pic_{num}'], tolerance=0.55):
                    print(num, end=' ')
                    break
            else:
                print(0, end=' ')
        else:
            print('\n')


def findGamePos():
    screen = autopy.bitmap.capture_screen()
    icon = autopy.bitmap.Bitmap.open('suIcon.PNG')
    icon_pos = screen.find_bitmap(icon)
    return icon_pos[0] + 5, icon_pos[1] + 115


def clickBlank(game_pos):
    screen = autopy.bitmap.capture_screen(rect=((game_pos[0], game_pos[1]), (float(47*9), float(47*9))))
    blank = autopy.bitmap.Bitmap.open('blank.PNG')
    blank_pos = screen.find_bitmap(blank)
    autopy.mouse.move(game_pos[0]+blank_pos[0]+15, game_pos[1]+blank_pos[1]+15)
    autopy.mouse.click()


def start_create():
    game_pos = findGamePos()
    if not game_pos:
        print('Game scope not found!!')
        exit()
    # clickBlank(game_pos)
    print_every_num(game_pos)


start_create()
