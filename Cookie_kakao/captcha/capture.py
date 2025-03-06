import autopy


def main():
    screen = autopy.bitmap.capture_screen()
    bs_icon = autopy.bitmap.Bitmap.open('D:\\Github\\Bot_game\\Cookie_kakao\\pic\\blueStackIcon.png')
    game_pos = screen.find_bitmap(bs_icon)
    for row in range(0, 2):
        for column in range(0, 3):
            x, y = game_pos[0] + 440 + (column * 240), game_pos[1] + 270 + (row * 320)
            screen = autopy.bitmap.capture_screen(((x, y), (170, 250)))
            screen.save(f'{row}{column}.png')
    # c_screen = autopy.bitmap.capture_screen(((game_pos[0] + 440 + (2 * 240), game_pos[1] + 270 + ), (170, 250)))
    # c_screen.save(f'{r}')


if __name__ == '__main__':
    main()

