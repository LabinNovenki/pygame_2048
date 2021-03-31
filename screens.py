import pygame
import classes
from pygame.locals import *
import sys
import pygame.freetype
import game_cal

# 定义颜色
white = (255, 255, 255)
black = (0, 0, 0)
gray = (220, 213, 223)
transparent = (0, 0, 0, 0)

# 设置帧率
fps = 5000
flock = pygame.time.Clock()

num_location = [
    (56, 205), (129, 205), (203, 205), (277, 205),
    (56, 279), (129, 279), (203, 279), (277, 279),
    (56, 353), (129, 353), (203, 353), (277, 353),
    (56, 427), (129, 427), (203, 427), (277, 427)
]


# 开始界面
def init_menu(screen):
    # 绘制按钮
    start_btn = classes.Button \
        ((120, 250), 'images/start_btn.png', 'images/start_btn_pressed.png')
    end_btn = classes.Button \
        ((120, 350), 'images/quit_btn.png', 'images/quit_btn_pressed.png')

    btn_group = pygame.sprite.Group(start_btn, end_btn)
    btn_group.draw(screen)

    while True:
        for event in pygame.event.get():  # 循环获取事件
            if event.type == QUIT:  # 若检测到事件类型为退出，则退出系统
                pygame.quit()
                sys.exit()
            # 退出按钮
            if end_btn.is_press(event):
                end_btn.press()
            else:
                end_btn.unpress()
            if end_btn.is_mouse_up(event):
                end_btn.unpress()
                pygame.quit()
                sys.exit()
            # 开始按钮
            if start_btn.is_press(event):
                start_btn.press()
            else:
                start_btn.unpress()
            if start_btn.is_mouse_up(event):
                start_btn.unpress()
                return 2

        screen.fill(gray)
        f1 = pygame.freetype.Font('Fonts/comic.ttf', 36)
        f1_rect = f1.render_to(screen, (45, 100), "2 0 4 8", fgcolor=white, size=100)
        btn_group.draw(screen)
        pygame.display.update()  # 更新屏幕内容
        flock.tick(fps)


# 游戏界面
def game_scn(screen):
    # 绘制棋盘
    chess = classes.Board('images/board.png', (50, 200))

    # 退出按钮
    end_btn = classes.Button \
        ((200, 70), 'images/quit_btn.png', 'images/quit_btn_pressed.png')
    restart_btn = classes.Button \
        ((50, 40), 'images/restart_btn.png', 'images/restart_btn_pressed.png')
    group_btn = pygame.sprite.Group(end_btn, restart_btn)

    # 绘制数字
    board, num1_, loc_ = game_cal.init_board()
    num1 = classes.Number(num1_, loc_)

    group_num = pygame.sprite.Group(num1)  # 方块数字精灵组

    group_sttc = pygame.sprite.Group(chess)  # 静态对象的组

    res = []  # 储存游戏进程的结构体
    is_move = False  # 标识精灵们是否在移动中，移动中的游戏不会接受键盘输入
    is_move_complete = False  # 精灵是否移动完毕
    score = 0  # 玩家的分数
    while True:

        # 数字的移动
        if is_move:
            is_move = False
            is_move_complete = True
            for spt in group_num.sprites():
                # print('moving:', spt.loc, spt.num)
                if res[1][spt.loc] != -1:
                    if spt.move(res[1][spt.loc]):
                        # print(spt.loc, '->', res[1][spt.loc])
                        is_move = True
                        is_move_complete = False
                else:
                    continue
            '''flock.tick(fps)
            group_sttc.draw(screen)
            group_num.draw(screen)
            pygame.display.update()'''
        if is_move_complete:
            for spt in group_num.sprites():
                if res[1][spt.loc] != -1:
                    spt.loc = res[1][spt.loc]
        # 数字升级
        if is_move_complete:
            for i in range(0, 16):
                is_merge = res[2][i]
                num = 2
                if is_merge:
                    for each in group_num.sprites():
                        if each.loc == i:
                            # print('remove:', each.loc, ' ',each.num)
                            num = each.num
                            each.remove(group_num)
                    num_image = classes.Number(2 * num, i)
                    group_num.add(num_image)

        if is_move_complete:
            if res[3] >= 2048:
                # 胜利
                # print('you win!')
                return 4

        # 添加新数字并绘制
        if is_move_complete:
            new_num = game_cal.create_new_num(board)
            if new_num is None:
                # 失败
                return 3
            board[new_num[1]] = new_num[0]
            num_image = classes.Number(new_num[0], new_num[1])
            group_num.add(num_image)
            is_move_complete = False

        for event in pygame.event.get():  # 循环获取事件
            if event.type == QUIT:  # 若检测到事件类型为退出，则退出系统
                pygame.quit()
                sys.exit()

            # 退出按钮
            if end_btn.is_press(event):
                end_btn.press()
            else:
                end_btn.unpress()
            if end_btn.is_mouse_up(event):
                end_btn.unpress()
                pygame.quit()
                sys.exit()

            # 重玩按钮
            if restart_btn.is_press(event):
                restart_btn.press()
            else:
                restart_btn.unpress()
            if restart_btn.is_mouse_up(event):
                restart_btn.unpress()
                return 2

            if event.type == KEYDOWN and not is_move:
                if event.key == K_UP:
                    op = 1
                elif event.key == K_DOWN:
                    op = 2
                elif event.key == K_LEFT:
                    op = 3
                elif event.key == K_RIGHT:
                    op = 4
                else:
                    continue
                res = game_cal.player_move(op, board)
                board = res[0]
                # group_num.sprites().sort(key=lambda x:x.loc)
                is_move = True
                score = score + res[3]
                # print('res=', res)
        screen.fill(gray)
        group_sttc.draw(screen)
        group_num.draw(screen)
        group_btn.draw(screen)

        # 绘制文字
        f1 = pygame.freetype.Font('Fonts/comic.ttf', 12)
        f1_rect = f1.render_to(screen, (50, 160), "score:", fgcolor=black, size=35)

        red_rate = 255 * (min(score, 3000) / 3000)
        size_rate = 35 + 20 * (min(score, 3000) / 3000)
        f1 = pygame.freetype.Font('Fonts/comic.ttf', 12)
        f1_rect = f1.render_to(screen, (200, 145), str(score), fgcolor=(red_rate, 15, 15), size=size_rate)

        pygame.display.update()  # 更新屏幕内容
        flock.tick(fps)


# 失败界面
def end_menu(screen):
    # 绘制按钮
    end_btn = classes.Button \
        ((120, 400), 'images/quit_btn.png', 'images/quit_btn_pressed.png')
    restart_btn = classes.Button \
        ((150, 280), 'images/restart_btn.png', 'images/restart_btn_pressed.png')

    btn_group = pygame.sprite.Group(restart_btn, end_btn)

    # 绘制静态对象
    image_fail = classes.Board('images/fail.png', (110, 150))

    group_sttc = pygame.sprite.Group(image_fail)

    while True:
        for event in pygame.event.get():  # 循环获取事件
            if event.type == QUIT:  # 若检测到事件类型为退出，则退出系统
                pygame.quit()
                sys.exit()
            # 退出按钮
            if end_btn.is_press(event):
                end_btn.press()
            else:
                end_btn.unpress()
            if end_btn.is_mouse_up(event):
                end_btn.unpress()
                pygame.quit()
                sys.exit()
            # 重玩按钮
            if restart_btn.is_press(event):
                restart_btn.press()
            else:
                restart_btn.unpress()
            if restart_btn.is_mouse_up(event):
                restart_btn.unpress()
                return 2
        screen.fill(gray)
        btn_group.draw(screen)
        group_sttc.draw(screen)
        pygame.display.update()  # 更新屏幕内容
        flock.tick(fps)


def win_menu(screen):
    # 绘制按钮
    end_btn = classes.Button \
        ((120, 400), 'images/quit_btn.png', 'images/quit_btn_pressed.png')
    restart_btn = classes.Button \
        ((150, 280), 'images/restart_btn.png', 'images/restart_btn_pressed.png')

    btn_group = pygame.sprite.Group(restart_btn, end_btn)

    # 绘制静态对象
    image_win = classes.Board('images/win.png', (70, 120))

    group_sttc = pygame.sprite.Group(image_win)

    while True:
        for event in pygame.event.get():  # 循环获取事件
            if event.type == QUIT:  # 若检测到事件类型为退出，则退出系统
                pygame.quit()
                sys.exit()
            # 退出按钮
            if end_btn.is_press(event):
                end_btn.press()
            else:
                end_btn.unpress()
            if end_btn.is_mouse_up(event):
                end_btn.unpress()
                pygame.quit()
                sys.exit()
            # 重玩按钮
            if restart_btn.is_press(event):
                restart_btn.press()
            else:
                restart_btn.unpress()
            if restart_btn.is_mouse_up(event):
                restart_btn.unpress()
                return 2
        screen.fill(gray)
        btn_group.draw(screen)
        group_sttc.draw(screen)
        pygame.display.update()  # 更新屏幕内容
        flock.tick(fps)

