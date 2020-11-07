import random


def random_i():
    i = random.randint(0, 2)
    chip_Locator = i
    chip_list = ["剪刀", "布", "石头"]
    chip = chip_list[chip_Locator]
    return chip


def player_chip_choose():
    # print(chip)

    print(
        """         ---------------------------
        三局两胜制
        下方输入你的筹码：0代表剪刀，1代表布，2代表石头
        -----------------------
        """)

    player_chip = int(input("在此输入你的筹码:"))
    if player_chip == 0:
        player_chip = '剪刀'
    elif player_chip == 1:
        player_chip = '布'
    elif player_chip == 2:
        player_chip = '石头'
    print(f"你选择的筹码为【{player_chip}】")
    return player_chip


def play_ready(Counter_num):
    player_chip = player_chip_choose()
    ai_chip = random_i()
    if player_chip == ai_chip:
        print(f"双方都出了{player_chip}，平局嗷")
        Counter_num += 0
    else:
        if player_chip == '剪刀':
            if ai_chip == '石头':
                print(f"AI出了{ai_chip}，player出{player_chip}，本回合你输了嗷！")
                Counter_num = Counter_num - 1

            elif ai_chip == '步':
                print(f"AI出了{ai_chip}，player出{player_chip}，本回合你赢了嗷！")
                Counter_num = Counter_num + 1

        elif player_chip == '石头':
            if ai_chip == '布':
                print(f"AI出了{ai_chip}，player出{player_chip}，本回合你输了嗷！")
                Counter_num = Counter_num - 1

            elif ai_chip == '剪刀':
                print(f"AI出了{ai_chip}，player出{player_chip}，本回合你赢了嗷！")
                Counter_num = Counter_num + 1

        elif player_chip == '布':
            if ai_chip == '剪刀':
                print(f"AI出了{ai_chip}，player出{player_chip}，本回合你输了嗷！")
                Counter_num = Counter_num - 1

            elif ai_chip == '石头':
                print(f"AI出了{ai_chip}，player出{player_chip}，本回合你赢了嗷！")
                Counter_num = Counter_num + 1
    return Counter_num


def play():
    Counter_num = 0
    for i in range(3):
        Counter_num = play_ready(Counter_num)
        print(Counter_num)
        if Counter_num == 2:
            print("恭喜你赢得比赛了呢")
            break
        else:
            pass
    if Counter_num != 2:
        print("都没赢过电脑？")


play()
# print("Hello!")
