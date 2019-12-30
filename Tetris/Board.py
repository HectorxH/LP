from abc import ABC
from math import floor

import pygame

from constants import *
from Tetrominos import Tetromino


class Board:
    def __init__(self):
        self.margin = (3, 5)
        self.clock = 0
        self.active_tetromino = False
        self.matrix = [self.new_row() for j in range(ROWS+self.margin[1])]
        self.matrix += 2*[[BORDER_COLOR for i in range(COLS+2*self.margin[0])]]

    def new_row(self):
        x_border = [BORDER_COLOR for i in range(self.margin[0])]
        return list(x_border + [BACKGROUND for i in range(COLS)] + x_border)

    def new_tetromino(self, tetromino):
        self.tetromino = tetromino
        self.active_tetromino = True
        return self.willCollide(self.tetromino.get_pos())

    def willCollide(self, pos):
        x, y = pos
        shape = self.tetromino.get_shape()
        for off_y, row in enumerate(shape):
            for off_x, flag in enumerate(row):
                try:
                    if self.matrix[y+off_y][x+off_x] != BACKGROUND and flag:
                        return True
                except IndexError:
                    return True
        return False

    def move(self, direction):
        if not self.active_tetromino:
            return
        didMove = False
        x, y = self.tetromino.get_pos()
        x += direction
        if not self.willCollide((x, y)):
            self.tetromino.set_pos((x, y))
            didMove = True
        self.tetromino.last_rotate = False
        return didMove

    def draw_ghost(self, screen, cell_size):
        x, y = self.tetromino.get_pos()
        while not self.willCollide((x, y)):
            y += 1
        y -= 1

        first_row, first_col = 3, 5
        ghost_pos = ((x+SIDE-first_row)*cell_size, (y-first_col)*cell_size)
        self.tetromino.draw_ghost(screen, cell_size, ghost_pos)

    def isTspin(self):
        if self.tetromino.name is 'T':
            count = 0
            x, y = self.tetromino.get_pos()
            for off_x in [0, 2]:
                for off_y in [0, 2]:
                    if self.matrix[y+off_y][x+off_x] != BACKGROUND:
                        count += 1
            return count > 2 and not self.tetromino.wall_kick and self.tetromino.last_rotate
        return False

    def drop(self, delay, manual=False, hard=False):
        delay = max(delay, 1)
        Tetromino.DELAY = BASE_DALAY-floor((BASE_DALAY-delay)/2)
        self.clock += 1
        x, y = self.tetromino.get_pos()
        willCollide = self.willCollide((x, y+1))

        if willCollide:
            self.tetromino.lock_delay -= 1

        isTspin = False
        if self.clock % delay == 0 or manual:
            if not self.active_tetromino:
                return -2, isTspin
            if willCollide and (self.tetromino.lock_delay <= 0 or hard):
                shape = self.tetromino.get_shape()
                isTspin = self.isTspin()
                for off_y, row in enumerate(shape):
                    for off_x, _ in filter(lambda x: x[1], enumerate(row)):
                        self.matrix[y+off_y][x+off_x] = self.tetromino.get_color()
                        self.active_tetromino = False
                lines = 0
                for i, row in list(enumerate(self.matrix[:-2])):
                    if not BACKGROUND in row:
                        del self.matrix[i]
                        self.matrix = [self.new_row()] + self.matrix
                        lines += 1
                return lines, isTspin
            elif willCollide and self.tetromino.lock_delay >= 0:
                self.tetromino.set_pos((x, y))
                return -1, isTspin
            else:
                self.tetromino.lock_delay = Tetromino.DELAY
            y += 1
            self.tetromino.set_pos((x, y))
            self.tetromino.last_rotate = False
            return -1, isTspin
        return -10, isTspin

    def rotate(self, direction):
        if not self.active_tetromino:
            return
        kick_table = self.tetromino.rotation_cw
        x, y = self.tetromino.get_pos()
        state = self.tetromino.state
        if direction == 1:
            self.tetromino.rotate_cw()
            next_state = self.tetromino.state
        elif direction == -1:
            self.tetromino.rotate_ccw()
            next_state = self.tetromino.state
        for _, off1, off2 in zip(range(5), kick_table[state], kick_table[next_state]):
            off_x, off_y = off1[0]-off2[0], off1[1]-off2[1]
            if not self.willCollide((x+off_x, y+off_y)):
                self.tetromino.set_pos((x+off_x, y+off_y))
                self.tetromino.last_rotate = True
                return
        if direction:
            self.tetromino.rotate_ccw()
        else:
            self.tetromino.rotate_cw()

    def draw(self, screen, cell_size):
        for y, row in enumerate(self.matrix[5:-2]):
            for x, color in enumerate(row[3:-3]):
                correction = lambda x: cell_size*x+cell_size*(1-BLOCK_SIZE)/2
                width = cell_size*BLOCK_SIZE
                r = pygame.Rect(SIDE*cell_size+correction(x), correction(y), width, width)
                pygame.draw.rect(screen, color, r)
        if self.active_tetromino:
            self.draw_ghost(screen, cell_size)
            self.tetromino.draw(screen, cell_size)
