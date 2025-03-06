import autopy
from line_notify import LineNotify


def main():
    screen = autopy.bitmap.capture_screen()
    bs_icon = autopy.bitmap.Bitmap.open('D:\\Github\\Bot_game\\Cookie_kakao\\pic\\blueStackIcon.png')
    game_pos = screen.find_bitmap(bs_icon)
    c_screen = autopy.bitmap.capture_screen()
    pos = []
    for row in range(0, 2):
        for column in range(0, 3):
            x, y = game_pos[0] + 440 + (column * 240), game_pos[1] + 270 + (row * 320)
            choice = c_screen.cropped(((x, y), (170, 250)))
            choice.save(f'{row}{column}.png')
            # screen = autopy.bitmap.capture_screen(((x, y), (170, 250)))
            # screen.save(f'{row}{column}.png')
            a = c_screen.count_of_bitmap(choice, rect=((game_pos[0]+409, game_pos[1]+246), (700, 630)), tolerance=0.3)
            print(a)


if __name__ == '__main__':
    access_token = 'U3AaIXQ7WKcTwDQBuYOCKJWe1E88gpmmK6cmJphVVPp'
    notify = LineNotify(access_token)

    notify.send("Text test")
    # main()
