import pygame
from pygame.locals import *
import game_cal
import screens

# pygame之前必须初始化
pygame.init()
# 设置用于显示的窗口，单位为像素
size = width, height = 400, 600
screen = pygame.display.set_mode(size)
# 设置标题
pygame.display.set_caption("2048")
# 缩放图片大小
# ball1.ball_sur = pygame.transform.scale(ball1.ball_sur, (50, 50))
# 绘制菜单界面
flag = 1
while True:
    if flag == 1:
        flag = screens.init_menu(screen)
    if flag == 2:
        flag = screens.game_scn(screen)
    if flag == 3:
        flag = screens.end_menu(screen)
    if flag == 4:
        flag = screens.win_menu(screen)
