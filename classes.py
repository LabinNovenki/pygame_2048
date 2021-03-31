import pygame
import math

num_location = [
        (56, 205), (129, 205), (203, 205), (277, 205),
        (56, 279), (129, 279), (203, 279), (277, 279),
        (56, 353), (129, 353), (203, 353), (277, 353),
        (56, 427), (129, 427), (203, 427), (277, 427)
    ]

class Button(pygame.sprite.Sprite):
    def __init__(self, pos, image_unpressed, image_pressed):
        # 调用父类的初始化方法
        super(Button, self).__init__()
        # 定义对象属性
        self.image = pygame.image.load(image_unpressed)  # 未按下的按钮图片
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos)
        self.image_pressed = image_pressed
        self.image_unpressed = image_unpressed

    def press(self):
        self.image = pygame.image.load(self.image_pressed)

    def unpress(self):
        self.image = pygame.image.load(self.image_unpressed)

    def is_press(self, event):  # 检测按钮是否被按下
        x, y = pygame.mouse.get_pos()
        if self.rect.left < x < self.rect.right and self.rect.top < y < self.rect.bottom:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.press()
                return 1
            else:
                return 0

    def is_mouse_up(self, event):  # 检测鼠标左键是否抬起
        x, y = pygame.mouse.get_pos()
        if self.rect.left < x < self.rect.right and self.rect.top < y < self.rect.bottom:
            if event.type == pygame.MOUSEBUTTONUP:
                return 1
            else:
                return 0


class Board(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super(Board, self).__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos)


class GameScreen(pygame.sprite.Sprite):

    def __init__(self, screen):
        # 调用父类的构造方法
        super().__init__()
        # 初始化属性
        gray = (220, 213, 223)
        screen.fill(gray)


class Number(pygame.sprite.Sprite):
    def __init__(self, num, loc):
        super(Number, self).__init__()

        self.image = pygame.image.load('images/' + str(num) + '.jpg')
        self.num = num
        self.rect = self.image.get_rect()
        self.pos = num_location[loc]
        self.rect = self.rect.move(self.pos)
        self.loc = loc
        self.speed = [0, 0]
        self.is_stop = False

    def move(self, new_loc):
        if not self.is_stop:
            self.speed = [num_location[new_loc][0] - self.pos[0], num_location[new_loc][1] - self.pos[1]]
            i = 0
            for i in range(0, 2):
                if self.speed[i] < 0:
                    self.speed[i] = -1
                elif self.speed[i] > 0:
                    self.speed[i] = 1
            self.rect = self.rect.move(self.speed)
            self.pos = self.rect.left, self.rect.top
            if self.speed == [0, 0]:
                return 0  # 已经移动到指定位置
            else:
                return 1  # 未移动到指定位置
        else:
            return 0

    def update(self):
        self.is_stop = False

