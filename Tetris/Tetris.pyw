import sys
from abc import ABC
from math import floor
from random import shuffle

import pygame

CELL_SIZE = 36
SIDE = 6
COLS = 10
ROWS = 22
MAX_FPS = 30
BASE_DALAY = 40
BLOCK_SIZE = 0.7
BACKGROUND = (0, 0, 0)
DETAIL = (30, 30, 30)
BORDER_COLOR = (255, 255, 255)
TEXT_DURATION = 20

VOLUME = 0.3

SCORE = [0, 100, 300, 500, 800, 1200, 1600]
LINES_PER_LINE = [0, 1, 3, 5, 8]

class TetrisGame:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        self.dimensions = (CELL_SIZE*(COLS+2*SIDE), CELL_SIZE*ROWS)
        self.side = CELL_SIZE*(COLS+SIDE)

        self.make_fonts()

        icon_surf = pygame.image.load("Tetris.png")
        pygame.display.set_icon(icon_surf)
        self.screen = pygame.surface.Surface(self.dimensions)
        self.window = pygame.display.set_mode(self.dimensions, pygame.RESIZABLE)
        self.window.fill(DETAIL)
        pygame.display.set_caption("Tetris!")

        pygame.mixer.music.load("Tetris.ogg")

        self.sounds = {}
        self.sounds["lock"] = pygame.mixer.Sound("sfx/lock.wav")
        self.sounds["hard drop"] = pygame.mixer.Sound("sfx/hard_drop.wav")
        self.sounds["swap"] = pygame.mixer.Sound("sfx/swap.wav")
        self.sounds["move"] = pygame.mixer.Sound("sfx/move.wav")
        self.sounds["rotate"] = pygame.mixer.Sound("sfx/rotate.wav")
        self.sounds["single"] = pygame.mixer.Sound("sfx/single.wav")
        self.sounds["double"] = pygame.mixer.Sound("sfx/double.wav")
        self.sounds["triple"] = pygame.mixer.Sound("sfx/triple.wav")
        self.sounds["tetris"] = pygame.mixer.Sound("sfx/tetris.wav")
        self.sounds["b2b tetris"] = pygame.mixer.Sound("sfx/b2b_tetris.wav")

        self.init_game()


    def make_fonts(self):
        font = "ComicSansMS3.ttf"
        create_font = lambda size: pygame.font.Font(
            font, floor(CELL_SIZE*size),
            bold=False,
            italic=False)

        base = 0.8

        self.small_font = create_font(base-0.2)
        self.default_font = create_font(base)
        self.big_font = create_font(base+0.3)

    def new_bag(self):
        shapes = [O, L, J, T, I, Z, S]
        bag = [shape() for shape in shapes]
        shuffle(bag)
        return bag

    def new_tetromino(self):
        if len(self.bag) == 7:
            self.bag = self.bag+self.new_bag()
        self.tetromino = self.bag.pop(0)

        self.gameover = self.board.new_tetromino(self.tetromino)


    def init_game(self):
        self.board = Board()

        self.bag = self.new_bag() + self.new_bag()
        self.new_tetromino()
        self.text = []

        self.gameover = False
        self.paused = False

        self.delay = BASE_DALAY

        self.isMovingLeft = False
        self.isMovingRight = False
        self.isSoftDroping = False

        self.holding = False
        self.did_swap = False

        self.b2b_tetris = False
        self.b2b_tspin = False

        self.stats = {}
        self.stats["Level"] = 1
        self.stats["Score"] = 0
        self.stats["Lines"] = 0
        self.stats["Combo"] = 0

        pygame.mixer.music.rewind()
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(VOLUME)

    def draw_next(self):
        offset = floor(CELL_SIZE/2)
        self.display_text("Next:", (self.side+CELL_SIZE, 0))

        next_tetromino = self.bag[0]
        next_tetromino.draw_at(self.screen, (self.side+offset, 3*offset), 0.9)

        for i, tetromino in enumerate(self.bag[1:7]):
            if isinstance(tetromino, I):
                tetromino.draw_at(self.screen, (self.side+9*offset, 3*(i+0.2)*offset), 0.4)
            else:
                tetromino.draw_at(self.screen, (self.side+9*offset, 3*(i+0.5)*offset), 0.4)

    def draw_hold(self):
        self.display_text("Hold:", (CELL_SIZE*0.1, CELL_SIZE*0.1))
        if self.holding:
            self.hold.draw_at(self.screen, (CELL_SIZE*1, CELL_SIZE*2), 1.1)

    def draw_stats(self):
        x, y = 0.1, 5
        print_stat = lambda offset, k: self.display_smoll_text(
            "{}: {}".format(k, self.stats[k]),
            (1+self.side+CELL_SIZE*x, CELL_SIZE*(y+offset)))
        for i, k in enumerate(self.stats):
            print_stat(i, k)

    def draw_splash_text(self):
        for i, info in enumerate(self.text):
            f, time_left = info
            if time_left == 0:
                del self.text[i]
            else:
                self.text[i] = (f, time_left-1)
            f()

    def display_text(self, string, pos):
        self.screen.blit(self.default_font.render(string, False, (255, 255, 255), DETAIL), pos)

    def display_smoll_text(self, string, pos):
        self.screen.blit(self.small_font.render(string, False, (255, 255, 255), DETAIL), pos)

    def display_big_text(self, string, y):
        text = self.big_font.render(string, False, (255, 255, 255), (0, 0, 0, 255))
        text_rect = text.get_rect(center=(self.dimensions[0]/2, y))
        self.screen.blit(text, text_rect)

    def add_splash_text(self, string, pos_y):
        self.text.append((lambda: self.display_big_text(string, pos_y), TEXT_DURATION))

    def tspin(self, x, b2b=False):
        if x == 0:
            string = "T-Spin"
        elif x == 1:
            string = "T-Spin Single!"
        elif x == 2:
            string = "T-Spin Double!!"
        elif x == 3:
            string = "T-Spin Triple!!!"

        if b2b:
            self.add_splash_text("Back 2 Back!", CELL_SIZE*2)
        self.add_splash_text(string, CELL_SIZE*4)


    def combo_count(self, combo):
        self.add_splash_text("x{}!".format(combo), CELL_SIZE*6)

    def tetris(self, b2b=False):
        if b2b:
            self.add_splash_text("Back 2 Back!", CELL_SIZE*2)
        self.add_splash_text("Tetris!", CELL_SIZE*4)

    def score_lines(self, lines, isTspin):
        if lines == 0:
            self.stats["Combo"] = 0
        else:
            self.stats["Combo"] += 1

        if lines >= 4 and self.b2b_tetris:
            self.stats["Score"] += floor(SCORE[lines]*self.stats["Level"]*0.5)
            self.tetris(b2b=True)
        elif isTspin and self.b2b_tspin:
            self.stats["Score"] += floor(SCORE[lines+3]*self.stats["Level"]*0.5)
            self.tspin(lines, b2b=True)
        elif isTspin:
            self.stats["Score"] += SCORE[lines+3]*self.stats["Level"]
            self.tspin(lines)
        else:
            self.stats["Score"] += SCORE[lines]*self.stats["Level"]
            if lines == 4:
                self.tetris()

        self.stats["Score"] += 50*self.stats["Combo"]*self.stats["Level"]
        if self.stats["Combo"] >= 5:
            self.combo_count(self.stats["Combo"])

        self.stats["Lines"] += LINES_PER_LINE[lines]
        if self.stats["Lines"] >= self.stats["Level"]*5:
            self.stats["Level"] += 1
            self.delay = max(0, BASE_DALAY-2*self.stats["Level"])

        if lines > 0:
            self.b2b_tetris = lines >= 4
            self.b2b_tspin = isTspin

    def move(self, direction):
        if not self.gameover and not self.paused:
            if self.board.move(direction):
                pygame.mixer.Sound.play(self.sounds["move"])

    def resize(self, w, h):
        global CELL_SIZE
        w, h = w-w%COLS, h-h%ROWS
        w, h = max(w, h), min(w, h)
        self.dimensions = (w, h)
        self.window = pygame.display.set_mode(self.dimensions, pygame.RESIZABLE)
        CELL_SIZE = floor(h/22)
        self.side = CELL_SIZE*(COLS+SIDE)
        self.screen = pygame.surface.Surface((h, h))
        self.make_fonts()

    def quit(self):
        sys.exit()

    def swap_hold(self):
        if not self.gameover and not self.paused and not self.did_swap:
            pygame.mixer.Sound.play(self.sounds["swap"])
            if not self.holding:
                self.hold = self.tetromino
                self.new_tetromino()
                self.hold, self.tetromino = self.tetromino, self.hold
                self.holding = True
            self.board.new_tetromino(self.hold)
            self.hold, self.tetromino = self.tetromino, self.hold
            self.hold.reset()
            self.did_swap = True

    def update_piece(self, lines, isTspin):
        if lines == 4:
            if self.b2b_tetris:
                pygame.mixer.Sound.play(self.sounds["b2b tetris"])
            else:
                pygame.mixer.Sound.play(self.sounds["tetris"])
        else:
            lock_type = ["lock", "single", "double", "triple"]
            pygame.mixer.Sound.play(self.sounds[lock_type[lines]])
        self.score_lines(lines, isTspin)
        self.new_tetromino()
        self.did_swap = False

    def drop(self, soft=False):
        if not self.gameover and not self.paused:
            if soft and self.tetromino.score < 20:
                self.stats["Score"] += 1
                self.tetromino.score += 1
            lines, isTspin = self.board.drop(self.delay, soft)
            if lines >= 0:
                self.update_piece(lines, isTspin)

    def hard_drop(self):
        if not self.gameover and not self.paused:
            pygame.mixer.Sound.play(self.sounds["hard drop"])
            self.stats["Score"] += 40
            lines, isTspin = self.board.drop(self.delay, manual=True)
            while lines < 0:
                lines, isTspin = self.board.drop(self.delay, manual=True, hard=True)
            self.update_piece(lines, isTspin)

    def rotate(self, direction):
        if not self.gameover and not self.paused:
            pygame.mixer.Sound.play(self.sounds["rotate"])
            self.board.rotate(direction)

    def pause(self):
        pass

    def restart(self):
        self.init_game()

    def loop(self):
        clock = pygame.time.Clock()
        moveTick = 0
        moveAccel = 0
        dropTick = 0

        w, h = self.dimensions

        verticalLine = lambda x: pygame.draw.line(self.screen, BORDER_COLOR, (x, 0), (x, h))

        while True:
            self.window.fill(DETAIL)
            self.screen.fill(DETAIL)
            if self.gameover:
                self.restart()
            elif self.paused:
                pass #Draw Pause screen?
            else:
                verticalLine(SIDE*CELL_SIZE)
                verticalLine(self.side+1)
                self.board.draw(self.screen)
                self.draw_next()
                self.draw_hold()
                self.draw_stats()
                self.draw_splash_text()
            self.window.blit(self.screen, (floor(w/2 - CELL_SIZE*11), 0))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                    elif event.key in (pygame.K_UP, pygame.K_x):
                        self.rotate(1)
                    elif event.key in (pygame.K_LSHIFT, pygame.K_c):
                        self.swap_hold()
                    elif event.key in (pygame.K_LCTRL, pygame.K_z):
                        self.rotate(-1)
                    elif event.key == pygame.K_SPACE:
                        self.hard_drop()
                    elif event.key == pygame.K_q:
                        self.quit()
                    elif event.key == pygame.K_r:
                        self.restart()
                    elif event.key == pygame.K_LEFT:
                        self.isMovingLeft = True
                        moveTick = 0
                        moveAccel = 7
                    elif event.key == pygame.K_RIGHT:
                        self.isMovingRight = True
                        moveTick = 0
                        moveAccel = 7
                    elif event.key == pygame.K_DOWN:
                        self.isSoftDroping = True
                        dropTick = 0

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.isMovingLeft = False
                    elif event.key == pygame.K_RIGHT:
                        self.isMovingRight = False
                    elif event.key == pygame.K_DOWN:
                        self.isSoftDroping = False
                elif event.type == pygame.VIDEORESIZE:
                    self.resize(event.w, event.h)

            self.drop()
            if moveTick == 0:
                if self.isMovingLeft:
                    self.move(-1)
                elif self.isMovingRight:
                    self.move(1)
                moveAccel = max(moveAccel-1, 4)
            if dropTick == 0 and self.isSoftDroping:
                self.drop(soft=True)
            moveTick = (moveTick+1)%floor(moveAccel*MAX_FPS/60)
            dropTick = (dropTick+1)%floor(5*MAX_FPS/60)

            clock.tick(MAX_FPS)

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

    def draw_ghost(self, screen):
        x, y = self.tetromino.get_pos()
        while not self.willCollide((x, y)):
            y += 1
        y -= 1

        first_row, first_col = 3, 5
        self.tetromino.draw_ghost(screen, ((x+SIDE-first_row)*CELL_SIZE, (y-first_col)*CELL_SIZE))

    def isTspin(self):
        if isinstance(self.tetromino, T):
            count = 0
            x, y = self.tetromino.get_pos()
            for off_x in [0, 2]:
                for off_y in [0, 2]:
                    if self.matrix[y+off_y][x+off_x] != BACKGROUND:
                        count += 1
            return count > 2 and not self.tetromino.wall_kick and self.tetromino.last_rotate
        return False

    def drop(self, delay, manual=False, hard=False):
        Tetromino.DELAY = BASE_DALAY-floor((BASE_DALAY-delay)/2)
        self.clock += 1
        self.tetromino.lock_delay -= 1
        if delay <= 0:
            delay = 1
            lines, isTspin = self.drop(delay+1)
            if lines >= 0:
                return lines, isTspin
        isTspin = False
        if self.clock % delay == 0 or manual:
            if not self.active_tetromino:
                return -2, isTspin
            x, y = self.tetromino.get_pos()
            if self.willCollide((x, y+1)) and (self.tetromino.lock_delay <= 0 or hard):
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
            elif self.willCollide((x, y+1)) and self.tetromino.lock_delay >= 0:
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
                # self.tetromino.wall_kick = i>0
                self.tetromino.last_rotate = True
                return
        if direction:
            self.tetromino.rotate_ccw()
        else:
            self.tetromino.rotate_cw()

    def draw(self, screen):
        for y, row in enumerate(self.matrix[5:-2]):
            for x, color in enumerate(row[3:-3]):
                correction = lambda x: CELL_SIZE*x+CELL_SIZE*(1-BLOCK_SIZE)/2
                width = CELL_SIZE*BLOCK_SIZE
                r = pygame.Rect(SIDE*CELL_SIZE+correction(x), correction(y), width, width)
                pygame.draw.rect(screen, color, r)
        if self.active_tetromino:
            self.draw_ghost(screen)
            self.tetromino.draw(screen)

class Tetromino(ABC):
    DELAY = 4
    rotation_cw = [
        [( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0)],
        [( 0, 0), ( 1, 0), ( 1, 1), ( 0,-2), ( 1,-2)],
        [( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0)],
        [( 0, 0), (-1, 0), (-1, 1), ( 0,-2), (-1,-2)]
    ]
    def __init__(self):
        self.state = 0
        self.lock_delay = Tetromino.DELAY
        self.score = 0

    def get_color(self):
        return self.color

    def get_shape(self):
        return self.shape

    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos

    def get_width(self):
        return self.width

    def rotate_cw(self):
        self.shape = list(map(list, list(zip(*self.shape[::-1]))))
        self.width, self.hight = self.hight, self.width
        self.state = (self.state+1)%4

    def rotate_ccw(self):
        self.shape = list(map(list, list(zip(*self.shape))[::-1]))
        self.width, self.hight = self.hight, self.width
        self.state = (self.state-1)%4


    def reset(self):
        self.__init__()

    def draw_at(self, screen, pos, scale):
        x, y = pos
        for off_y, row in enumerate(self.shape):
            for off_x, _ in filter(lambda x: x[1], enumerate(row)):
                correction = lambda x, off: x+off*CELL_SIZE*scale+(CELL_SIZE*scale*(1-BLOCK_SIZE))/2
                width = CELL_SIZE*scale*BLOCK_SIZE
                r = pygame.Rect(correction(x, off_x), correction(y, off_y), width, width)
                pygame.draw.rect(screen, self.color, r)

    def draw_ghost(self, screen, pos):
        x, y = pos
        # x, y = ((SIDE+x-first_row)*CELL_SIZE,(y-first_col)*CELL_SIZE)
        color = tuple(map(lambda x: floor(x/3), self.color))
        for off_y, row in enumerate(self.shape):
            for off_x, _ in filter(lambda x: x[1], enumerate(row)):
                correction = lambda x, off_x: x+off_x*CELL_SIZE+(CELL_SIZE*(1-BLOCK_SIZE))/2
                width = CELL_SIZE*BLOCK_SIZE
                r = pygame.Rect(correction(x, off_x), correction(y, off_y), width, width)
                pygame.draw.rect(screen, color, r)

    def draw(self, screen):
        first_row, first_col = 3, 5
        x, y = self.pos
        x, y = ((SIDE+x-first_row)*CELL_SIZE, (y-first_col)*CELL_SIZE)
        for off_y, row in enumerate(self.shape):
            for off_x, _ in filter(lambda x: x[1], enumerate(row)):
                correction = lambda x, off_x: x+off_x*CELL_SIZE+(CELL_SIZE*(1-BLOCK_SIZE))/2
                width = CELL_SIZE*BLOCK_SIZE
                r = pygame.Rect(correction(x, off_x), correction(y, off_y), width, width)
                pygame.draw.rect(screen, self.color, r)

class O(Tetromino):
    rotation_cw = [
        [( 0, 0)],
        [( 0, 1)],
        [(-1, 1)],
        [(-1, 0)]
    ]
    def __init__(self):
        super().__init__()
        self.width = 2
        self.hight = 2
        self.pos = (floor(COLS/2) - 2 + 3, 5)
        self.shape = [[0, 1, 1],
    	              [0, 1, 1],
                      [0, 0, 0]]
        self.color = (255, 255, 0)

class L(Tetromino):
    def __init__(self):
        super().__init__()
        self.width = 3
        self.hight = 2
        self.pos = (floor(COLS/2) - 2 + 3, 5)
        self.shape = [[0, 0, 1],
    	              [1, 1, 1],
                      [0, 0, 0]]
        self.color = (255, 165, 0)
class J(Tetromino):
    def __init__(self):
        super().__init__()
        self.width = 3
        self.hight = 2
        self.pos = (floor(COLS/2) - 2 + 3, 5)
        self.shape = [[1, 0, 0],
    	              [1, 1, 1],
                      [0, 0, 0]]
        self.color = (0, 0, 255)
class T(Tetromino):
    def __init__(self):
        super().__init__()
        self.width = 3
        self.hight = 2
        self.pos = (floor(COLS/2) - 2 + 3, 5)
        self.shape = [[0, 1, 0],
    	              [1, 1, 1],
                      [0, 0, 0]]
        self.color = (160, 32, 240)
        self.wall_kick = False
        self.last_rotate = False

class I(Tetromino):
    rotation_cw = [
        [( 0, 0), (-1, 0), ( 2, 0), (-1, 0), ( 2, 0)],
        [(-1, 0), ( 0, 0), ( 0, 0), ( 0,-1), ( 0, 2)],
        [(-1,-1), ( 1,-1), (-2,-1), ( 1, 0), (-2, 0)],
        [( 0,-1), ( 0,-1), ( 0,-1), ( 0, 1), ( 0,-2)]
    ]
    def __init__(self):
        super().__init__()
        self.width = 4
        self.hight = 1
        self.pos = (floor(COLS/2) -3 + 3, 3)
        self.shape = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 1, 1, 1, 1],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
        self.color = (0, 255, 255)

    def draw_at(self, screen, pos, scale):
        scale = scale*0.9
        x, y = pos
        shape = self.shape[1:]
        for off_y, row in enumerate(shape):
            for off_x, _ in filter(lambda x: x[1], enumerate(row)):
                off_x, off_y = off_x-1.5, off_y
                correction = lambda x, off: x+off*CELL_SIZE*scale+(CELL_SIZE*(1-scale*BLOCK_SIZE))/2
                width = CELL_SIZE*scale*BLOCK_SIZE
                r = pygame.Rect(correction(x, off_x), correction(y, off_y), width, width)
                pygame.draw.rect(screen, self.color, r)


class Z(Tetromino):
    def __init__(self):
        super().__init__()
        self.width = 3
        self.hight = 2
        self.pos = (floor(COLS/2) - 2 + 3, 5)
        self.shape = [[1, 1, 0],
    	              [0, 1, 1],
                      [0, 0, 0]]
        self.color = (255, 0, 0)
class S(Tetromino):
    def __init__(self):
        super().__init__()
        self.width = 3
        self.hight = 2
        self.pos = (floor(COLS/2) - 2 + 3, 5)
        self.shape = [[0, 1, 1],
    	              [1, 1, 0],
                      [0, 0, 0]]
        self.color = (0, 255, 0)

if __name__ == '__main__':
    App = TetrisGame()
    App.loop()
