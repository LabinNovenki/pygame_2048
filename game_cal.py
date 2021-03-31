import random
import math


def init_board():
    """
    初始化棋盘
    :return:新建棋盘，长度为16的一维列表(棋盘， 数字， 位置)
    """
    count = 0
    board = 16 * [0]
    loc = random.randint(0, 15)
    rdm2 = random.random()
    if rdm2 <= 0.5:
        board[loc] = 2
    else:
        board[loc] = 4
    return board, board[loc], loc


def create_new_num(board):
    """
    随机地在棋盘上加入一个数字
    :return: 新生成的数字与其所在位置(数字， 位置)
    """
    count = 0
    list = []
    res = [2, 0]
    for i in range(0, 16):
        if board[i] == 0:
            count = count + 1
            list.append(i)
    if count == 0:
        return None
    rdm1 = random.randint(0, count - 1)
    res[1] = list[rdm1]
    rdm2 = random.random()
    if rdm2 < 0.5:
        res[0] = 2
    else:
        res[0] = 4
    return res


def player_move(op, board):
    """
    描述用户的操作
    :param op: 描述用户的操作，包括上下左右(1, 2, 3, 4)四个方向
    :param board: 一维列表，储存游戏棋盘
    :return: (棋盘，每个数字更新后的位置，发生合并的位置，此次行动增加的分数)
    new_loc[i] = k表示位置i的数组更新到了位置k，当k = -1时， 位置未发生更新，当k = -2， 数字从游戏中删除
    merge_loc[i] = k表示位置i的数字发生了合并，将原来的sprite删除，生成更高级的sprites,当k = 0时，数字未发生合并
    score为增加的分数
    """
    new_loc = 16 * [-1]  # new_loc[i] = k表示原本在位置i的数字移动到了位置k
    merge_loc = 16 * [0]  # merge_loc[i] = k表示位置i的数字需要升级
    score = 0
    if op == 1:  # 向上移动
        for i in range(4, 16):
            k = i
            if board[k] != 0:
                while board[k - 4] == 0:
                    board[k - 4] = board[k]
                    board[k] = 0
                    k = k - 4
                    if k - 4 < 0:
                        break
                new_loc[i] = k
                if k - 4 < 0:
                    continue
                if board[k - 4] == board[k] and not merge_loc[k - 4]:
                    board[k] = 0
                    board[k - 4] = board[k - 4] * 2
                    new_loc[i] = k - 4
                    score = board[k - 4]
                    merge_loc[k - 4] = 1
            else:
                new_loc[i] = -1
    elif op == 2:  # 向下移动
        for i in range(11, -1, -1):
            k = i
            if board[k] != 0:
                while board[k + 4] == 0:
                    board[k + 4] = board[k]
                    board[k] = 0
                    k = k + 4
                    if k + 4 > 15:
                        break
                new_loc[i] = k
                if k + 4 > 15:
                    continue
                if board[k + 4] == board[k] and not merge_loc[k + 4]:
                    board[k] = 0
                    board[k + 4] = board[k + 4] * 2
                    new_loc[i] = k + 4
                    score = board[k + 4]
                    merge_loc[k + 4] = 1
            else:
                new_loc[i] = -1
    elif op == 3:  # 向左移动
        for i in range(1, 16):
            if i == 4 or i == 8 or i == 12:
                continue
            k = i
            if board[k] != 0:
                while board[k - 1] == 0:
                    board[k - 1] = board[k]
                    board[k] = 0
                    k = k - 1
                    if k == 0 or k == 4 or k == 8 or k == 12:
                        break
                new_loc[i] = k
                if k == 0 or k == 4 or k == 8 or k == 12:
                    continue
                if board[k - 1] == board[k] and not merge_loc[k - 1]:
                    board[k] = 0
                    board[k - 1] = board[k - 1] * 2
                    new_loc[i] = k - 1
                    score = board[k - 1]
                    merge_loc[k - 1] = 1
            else:
                new_loc[i] = -1
    elif op == 4:  # 向右移动
        for i in range(15, -1, -1):
            if i == 3 or i == 7 or i == 11 or i == 15:
                continue
            k = i
            if board[k] != 0:
                while board[k + 1] == 0:
                    board[k + 1] = board[k]
                    board[k] = 0
                    k = k + 1
                    if k == 3 or k == 7 or k == 11 or k == 15:
                        break
                new_loc[i] = k
                if k == 3 or k == 7 or k == 11 or k == 15:
                    continue
                if board[k + 1] == board[k] and not merge_loc[k + 1]:
                    board[k] = 0
                    board[k + 1] = board[k + 1] * 2
                    new_loc[i] = k + 1
                    score = board[k + 1]
                    merge_loc[k + 1] = 1
            else:
                new_loc[i] = -1
    return board, new_loc, merge_loc, score


def game_2048():
    board = init_board()
    while True:
        player_move()

