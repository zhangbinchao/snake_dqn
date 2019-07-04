# -------------------------
# Project: Deep Q-Learning on Snake
# Author: bc_zhang
# Date: 2019.7.4
# -------------------------

import random
import sys
import time
import pygame
from pygame.locals import *
from collections import deque
import math

SCREEN_WIDTH = 260      # 屏幕宽度
SCREEN_HEIGHT = 260     # 屏幕高度
SIZE = 20               # 小方格大小
LINE_WIDTH = 1          # 网格线宽度

# 游戏区域的坐标范围
SCOPE_X = (0, SCREEN_WIDTH // SIZE - 1)
SCOPE_Y = (0, SCREEN_HEIGHT // SIZE - 1)

# 食物的分值及颜色
FOOD_STYLE_LIST = [(1, (255, 255, 255)), (20, (100, 255, 100)), (30, (100, 100, 255))]  #都用绿色，得分1分

LIGHT = (100, 100, 100)
DARK = (200, 200, 200)      # 蛇的颜色
BLACK = (0, 0, 0)           # 网格线颜色
RED = (255, 255, 255)         # 红色，GAME OVER 的字体颜色
BGCOLOR = (40, 40, 60)      # 背景色



def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))


# 初始化蛇
def init_snake():
    snake = deque()
    snake.append((7, SCOPE_Y[0]+6))
    snake.append((6, SCOPE_Y[0]+6))
    snake.append((5, SCOPE_Y[0]+6))
    return snake


def create_food(snake):
    food_x = random.randint(SCOPE_X[0], SCOPE_X[1])
    food_y = random.randint(SCOPE_Y[0], SCOPE_Y[1])
    while (food_x, food_y) in snake:
        # 如果食物出现在蛇身上，则重来
        food_x = random.randint(SCOPE_X[0], SCOPE_X[1])
        food_y = random.randint(SCOPE_Y[0], SCOPE_Y[1])
    return food_x, food_y


def get_food_style():
    return FOOD_STYLE_LIST[0]


class GameState:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('GluttonousSnake')
        # 蛇
        self.snake = init_snake()
        # 食物
        self.food = create_food(self.snake)
        self.food_style = get_food_style()
        # 方向
        self.pos = (1, 0)
        self.game_over = False
        self.score = 0  # 得分
        # self.speed = 0.1


    def frame_step(self,input_actions):
        terminal = False
        reward = 0.1

        # 检测输入正确性
        if input_actions[0] == 1 or input_actions[1]== 1 or input_actions[2]== 1 or input_actions[3] == 1:  # 检查输入正常
            if input_actions[0] == 1 and input_actions[1] == 0 and input_actions[2] == 0 and input_actions[3] == 0 and self.pos != (0,1):
                # 这个判断是为了防止蛇向上移时按了向下键，导致直接 GAME OVER  向上
                self.pos = (0, -1)

            elif input_actions[0] == 0 and input_actions[1] == 1 and input_actions[2] == 0 and input_actions[3] == 0 and self.pos != (0,-1):
                #向下
                self.pos = (0, 1)
            elif input_actions[0] == 0 and input_actions[1] == 0 and input_actions[2] == 1 and input_actions[3] == 0 and self.pos != (1,0):
                #向左
                self.pos = (-1, 0)
            elif input_actions[0] == 0 and input_actions[1] == 0 and input_actions[2] == 0 and input_actions[3] == 1 and self.pos != (-1,0):
                #向右
                self.pos = (1, 0)
            else:
                pass

        else:
            raise ValueError('Multiple input actions!')

        # 填充背景色
        self.screen.fill(BGCOLOR)
        # 画网格线 竖线
        for x in range(SIZE, SCREEN_WIDTH, SIZE):
            pygame.draw.line(self.screen, BLACK, (x, SCOPE_Y[0] * SIZE), (x, SCREEN_HEIGHT), LINE_WIDTH)
        # 画网格线 横线
        for y in range(SCOPE_Y[0] * SIZE, SCREEN_HEIGHT, SIZE):
            pygame.draw.line(self.screen, BLACK, (0, y), (SCREEN_WIDTH, y), LINE_WIDTH)

        next_s = (self.snake[0][0] + self.pos[0], self.snake[0][1] + self.pos[1])
        if next_s == self.food:
            # 吃到了食物
            self.snake.appendleft(next_s)
            self.score += self.food_style[0]
            self.food = create_food(self.snake)
            self.food_style = get_food_style()
            reward = 1
            # self.score += 1
        else:
            if SCOPE_X[0] <= next_s[0] <= SCOPE_X[1] and SCOPE_Y[0] <= next_s[1] <= SCOPE_Y[1] \
                    and next_s not in self.snake:
                self.snake.appendleft(next_s)
                self.snake.pop()

                # dis = (math.sqrt(pow((self.food[0]-next_s[0]),2)+pow((self.food[1]-next_s[1]),2)))
                # reward = (1/dis)*0.5

            else:
                reward = -1  #死亡惩罚
                terminal = True

                # print('failure')
                self.__init__()


        print('score:%u' % self.score)



        if terminal ==True:
            font2 = pygame.font.Font(None,50 )# GAME OVER 的字体
            fwidth, fheight = font2.size('GAME OVER')
            print_text(self.screen, font2, (SCREEN_WIDTH - fwidth) // 2, (SCREEN_HEIGHT - fheight) // 2, 'GAME OVER', RED)
        else:
            # 画食物
            if reward != 1:
                pygame.draw.circle(self.screen, DARK,
                                   (self.food[0] * SIZE + LINE_WIDTH + 10, self.food[1] * SIZE + LINE_WIDTH + 10), 10,
                                   0)
            # 画蛇
            flag = 0
            for s in self.snake:
                if flag == 0:
                    pygame.draw.circle(self.screen, DARK, (s[0] * SIZE + LINE_WIDTH+10, s[1] * SIZE + LINE_WIDTH+10),10, 0)
                    flag = 1
                else:
                    pygame.draw.rect(self.screen, DARK, (s[0] * SIZE + LINE_WIDTH, s[1] * SIZE + LINE_WIDTH,
                                                SIZE - LINE_WIDTH * 2, SIZE - LINE_WIDTH * 2), 0)


        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(90)
        return image_data, reward, terminal,self.score



