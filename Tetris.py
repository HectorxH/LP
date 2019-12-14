from random import  shuffle
import pygame, sys

CELL_SIZE = 36
SIDE = 6
COLS = 10
ROWS = 22
MAX_FPS = 30
BASE_DALAY = 40
VANITY = 0.7
BACKGROUND = (0,0,0)
DETAIL = (30,30,30)
TEXT_DURATION = 20

VOLUME = 0.3

score = [0, 100, 300, 500, 800, 1200, 1600]
linelines = [0, 1, 3, 5, 8]

class TetrisGame:
    def __init__(self):
        pygame.init()
        self.dimensions = (CELL_SIZE*(COLS+SIDE), CELL_SIZE*ROWS)
        self.side = CELL_SIZE*COLS

        self.default_font =  pygame.font.Font(pygame.font.get_default_font(), int(CELL_SIZE*0.7))
        self.small_font = pygame.font.Font(pygame.font.get_default_font(), int(CELL_SIZE*0.5))
        self.big_font = pygame.font.Font(pygame.font.get_default_font(), int(CELL_SIZE))

        self.screen = pygame.display.set_mode(self.dimensions)

        pygame.mixer.music.load("Tetris.ogg")

        self.init_game()

    #Genera una nueva instancia de cada pieza y las desordena
    def new_bag(self):
        shapes = [O, L, J, T, I, Z, S]
        list = [shapes[i]() for i in range(7)]
        shuffle(list)
        return list

    def new_tetromino(self):
        if len(self.bag) == 7:
            self.bag = self.new_bag() + self.bag
        self.tetromino = self.bag.pop()

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

        self.level = 1
        self.score = 0
        self.lines = 0
        self.combo = 0

        self.count = 0

        pygame.mixer.music.rewind()
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(VOLUME)

    def draw_next(self):
        self.display_text("Next:", (self.side+CELL_SIZE, 0))
        self.bag[-1].draw(self.screen, (self.side+CELL_SIZE,CELL_SIZE), 0.7)
        self.bag[-2].draw(self.screen, (self.side+CELL_SIZE*4,CELL_SIZE*0.5), 0.4)
        self.bag[-3].draw(self.screen, (self.side+CELL_SIZE*4,CELL_SIZE*2), 0.4)
        self.bag[-4].draw(self.screen, (self.side+CELL_SIZE*4,CELL_SIZE*3.5), 0.4)
        self.bag[-5].draw(self.screen, (self.side+CELL_SIZE*4,CELL_SIZE*5), 0.4)
        self.bag[-6].draw(self.screen, (self.side+CELL_SIZE*4,CELL_SIZE*6.5), 0.4)
        self.bag[-7].draw(self.screen, (self.side+CELL_SIZE*4,CELL_SIZE*8), 0.4)

    def draw_hold(self):
        x,y = 1,15
        self.display_text("Hold:", (self.side+CELL_SIZE*x, CELL_SIZE*y))
        if self.holding:
            self.hold.draw(self.screen, (self.side+CELL_SIZE*(x+1),CELL_SIZE*(y+1)), 0.7)

    def draw_stats(self):
        x,y = 0.1,5
        self.display_smoll_text("Level: {}".format(self.level), (self.side+CELL_SIZE*x, CELL_SIZE*y))
        self.display_smoll_text("Lines: {}".format(self.lines), (self.side+CELL_SIZE*x, CELL_SIZE*(y+1)))
        self.display_smoll_text("Score: {}".format(self.score), (self.side+CELL_SIZE*x, CELL_SIZE*(y+2)))
        self.display_smoll_text("Combo: {}".format(self.combo), (self.side+CELL_SIZE*x, CELL_SIZE*(y+3)))

    def draw_splash_text(self):
        for i, info in enumerate(self.text):
            f, time_left = info
            if time_left == 0:
                del self.text[i]
            else:
                self.text[i] = (f, time_left-1)
            f()

    def display_text(self, string, pos):
        self.screen.blit(self.default_font.render(string,False,(255,255,255), BACKGROUND), pos)

    def display_smoll_text(self, string, pos):
        self.screen.blit(self.small_font.render(string,False,(255,255,255), BACKGROUND), pos)

    def display_big_text(self, string, pos):
        self.screen.blit(self.big_font.render(string,False,(255,255,255), (0,0,0,255)), pos)


    def tspin(self, x):
        if x==0:
            self.text.append((lambda:self.display_big_text("T-Spin", (CELL_SIZE*4,CELL_SIZE*3)), TEXT_DURATION))
        elif x==1:
            self.text.append((lambda:self.display_big_text("T-Spin Single!", (CELL_SIZE*2,CELL_SIZE*3)), TEXT_DURATION))
        elif x==2:
            self.text.append((lambda:self.display_big_text("T-Spin Double!!", (CELL_SIZE*2,CELL_SIZE*3)), TEXT_DURATION))
        elif x==3:
            self.text.append((lambda:self.display_big_text("T-Spin Triple!!!", (CELL_SIZE*2,CELL_SIZE*3)), TEXT_DURATION))
        print("Tspin")


    def combo_count(self, combo):
        self.text.append((lambda:self.display_big_text("x{}!".format(combo), (CELL_SIZE*4,CELL_SIZE*4)), TEXT_DURATION))

    def tetris(self):
        self.text.append((lambda:self.display_big_text("Tetris!", (CELL_SIZE*4,CELL_SIZE*3)), TEXT_DURATION))

    def b2b(self):
        self.text.append((lambda:self.display_big_text("Back to Back", (CELL_SIZE*2,CELL_SIZE*2)), TEXT_DURATION))

    def score_lines(self, lines, isTspin):
        if lines == 0:
            self.combo = 0
        else:
            self.combo+=1

        if isTspin:
            self.score += score[lines+3]*self.level
            self.tspin(lines)
        else:
            self.score += score[lines]*self.level
            if lines == 4:
                self.tetris()

        if lines>=4 and self.b2b_tetris:
            self.score += int(score[lines]*self.level*0.5)
            self.b2b()
        if isTspin and self.b2b_tspin:
            self.score += int(score[lines+3]*self.level*0.5)
            self.b2b()

        self.score += 50*self.combo*self.level
        if self.combo >= 5:
            self.combo_count(self.combo)

        self.lines += linelines[lines]
        if self.lines >= self.level*5:
            self.level += 1
            self.delay = max(1, BASE_DALAY-2*self.level)

        self.b2b_tetris = lines>=4
        self.b2b_tspin_double = lines==2 and isTspin
        self.b2b_tspin_triple = isTspin

    def move(self, dir):
        if not self.gameover and not self.paused:
            self.board.move(dir)



    def quit(self):
        sys.exit()

    def swap_hold(self):
        if not self.gameover and not self.paused and not self.did_swap:
            if not self.holding:
                self.hold = self.tetromino
                self.new_tetromino()
                self.hold, self.tetromino = self.tetromino, self.hold
                self.holding = True
            self.board.new_tetromino(self.hold)
            self.hold, self.tetromino = self.tetromino, self.hold
            self.hold.reset()
            self.did_swap = True
            self.count = 0

    def drop(self):
        if not self.gameover and not self.paused:
            lines, isTspin = self.board.drop(self.delay)
            if lines >= 0:
                self.score_lines(lines, isTspin)
                self.new_tetromino()
                self.count = 0
                self.did_swap = False

    def soft_drop(self):
        if not self.gameover and not self.paused:
            if self.count < 20:
                self.score += 1
            lines, isTspin = self.board.drop(self.delay, manual=True)
            if lines >= 0:
                self.score_lines(lines, isTspin)
                self.new_tetromino()
                self.count = 0
                self.did_swap = False


    def hard_drop(self):
        if not self.gameover and not self.paused:
            self.score += 40
            lines, isTspin = self.board.drop(self.delay, manual=True)
            while lines < 0:
                lines, isTspin = self.board.drop(self.delay, manual=True, hard=True)
            self.score_lines(lines, isTspin)
            self.new_tetromino()
            self.count = 0
            self.did_swap = False

    def rotate(self, dir):
        if not self.gameover and not self.paused:
            self.board.rotate(dir)

    def pause(self):
        pass

    def restart(self):
        self.init_game()

    def loop(self):

        clock = pygame.time.Clock()
        tick = 0

        while True:
            self.screen.fill(DETAIL)
            if self.gameover:
                self.restart()
            elif self.paused:
                pass #Draw Pause screen?
            else:
                pygame.draw.line(self.screen,(255,255,255),(0, 0),(0, self.dimensions[1]))
                pygame.draw.line(self.screen,(255,255,255),(self.side+1, 0),(self.side+1, self.dimensions[1]))
                self.board.draw(self.screen)
                self.draw_next()
                self.draw_hold()
                self.draw_stats()
                self.draw_splash_text()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: self.paused = not self.paused
                    elif event.key == pygame.K_LEFT: self.isMovingLeft = True
                    elif event.key == pygame.K_RIGHT: self.isMovingRight = True
                    elif event.key == pygame.K_DOWN: self.isSoftDroping = True
                    elif event.key in (pygame.K_UP, pygame.K_x): self.rotate(1)
                    elif event.key in (pygame.K_LSHIFT, pygame.K_c): self.swap_hold()
                    elif event.key in (pygame.K_LCTRL, pygame.K_z):  self.rotate(-1)
                    elif event.key == pygame.K_SPACE: self.hard_drop()
                    elif event.key == pygame.K_q: self.quit()
                    elif event.key == pygame.K_r: self.restart()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT: self.isMovingLeft = False
                    elif event.key == pygame.K_RIGHT: self.isMovingRight = False
                    elif event.key == pygame.K_DOWN: self.isSoftDroping = False
            # print(clock.get_fps())
            self.drop()
            if tick == 0:
                if self.isMovingLeft:
                    self.move(-1)
                elif self.isMovingRight:
                    self.move(1)
                elif self.isSoftDroping:
                    self.soft_drop()

            tick = (tick+1)%int(5*MAX_FPS/60)

            clock.tick(MAX_FPS)

class Board:
    def __init__(self):
        self.clock = 0
        self.active_tetromino = False
        empty_row = [(255,255,255)]*3+[BACKGROUND]*COLS+[(255,255,255)]*3
        self.matrix = [list(empty_row) for j in range(ROWS+5)] + [[(255,255,255)]*(COLS+6)]*2

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
                    if self.matrix[y+off_y][x+off_x] != BACKGROUND and flag == True:
                        return True
                except IndexError:
                    return True
        return False

    def move(self, dir):
        if self.active_tetromino == False:
            return
        x, y = self.tetromino.get_pos()
        x += dir
        if not self.willCollide((x,y)):
            self.tetromino.set_pos((x,y))
        # self.tetromino.wall_kick = False
        self.tetromino.last_rotate = False

    def drop(self, delay, manual=False, hard=False):
        isTspin = False
        self.clock += 1
        if self.clock % delay == 0 or manual:
            if self.active_tetromino == False:
                return -2, isTspin
            x, y = self.tetromino.get_pos()
            if self.willCollide((x,y+1)) and (self.tetromino.lock_delay == 0 or hard):
                shape = self.tetromino.get_shape()
                if isinstance(self.tetromino, T):
                    count = 0
                    for off_x in [0, 2]:
                        for off_y in [0, 2]:
                            if self.matrix[y+off_y][x+off_x] != (0,0,0):
                                count+=1
                    isTspin = count > 2 and not self.tetromino.wall_kick and self.tetromino.last_rotate
                for off_y, row in enumerate(shape):
                    for off_x, flag in filter(lambda c: c[1] != 0, enumerate(row)):
                        self.matrix[y+off_y][x+off_x] = self.tetromino.get_color()
                        self.active_tetromino = False
                lines = 0
                for i, row in list(enumerate(self.matrix[:-2])):
                    if not BACKGROUND in row:
                        del self.matrix[i]
                        self.matrix = [[(255,255,255)]*3+[BACKGROUND]*COLS+[(255,255,255)]*3] + self.matrix
                        lines += 1
                return lines, isTspin
            elif self.willCollide((x,y+1)):
                self.tetromino.lock_delay-= 1
                self.tetromino.set_pos((x,y))
                return -1, isTspin
            y += 1
            self.tetromino.set_pos((x,y))
            # self.tetromino.wall_kick = False
            self.tetromino.last_rotate = False
            return -1, isTspin
        return -10, isTspin

    def rotate(self, dir):
        if self.active_tetromino == False:
            return
        kick_table = self.tetromino.rotation_cw
        x,y = self.tetromino.get_pos()
        state = self.tetromino.state
        if dir == 1:
            self.tetromino.rotate_cw()
            next_state = self.tetromino.state
        elif dir == -1:
            self.tetromino.rotate_ccw()
            next_state = self.tetromino.state
        for i, off1, off2 in zip(range(5), kick_table[state], kick_table[next_state]):
            off_x, off_y = off1[0]-off2[0], off1[1]-off2[1]
            if not self.willCollide((x+off_x,y+off_y)):
                self.tetromino.set_pos((x+off_x,y+off_y))
                # self.tetromino.wall_kick = i>0
                self.tetromino.last_rotate = True
                return
        self.tetromino.rotate_ccw() if dir == 1 else self.tetromino.rotate_cw()

    def draw(self, screen):
        for y, row in enumerate(self.matrix[5:]):
            for x, color in enumerate(row[3:-3]):
                r = pygame.Rect(CELL_SIZE*x+CELL_SIZE*(1-VANITY)/2, CELL_SIZE*y+CELL_SIZE*(1-VANITY)/2, CELL_SIZE*VANITY, CELL_SIZE*VANITY)
                pygame.draw.rect(screen, color, r)
        if self.active_tetromino:
            self.tetromino.draw(screen)

class Tetromino():
    rotation_cw = [
        [( 0, 0),( 0, 0),( 0, 0),( 0, 0),( 0, 0)],
        [( 0, 0),( 1, 0),( 1, 1),( 0,-2),( 1,-2)],
        [( 0, 0),( 0, 0),( 0, 0),( 0, 0),( 0, 0)],
        [( 0, 0),(-1, 0),(-1, 1),( 0,-2),(-1,-2)]
    ]
    def __init__(self):
        self.state = 0
        self.lock_delay = 2

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

    def draw(self, screen, pos=(-1,-1), scale=1):
        x, y = ((self.pos[0]-3)*CELL_SIZE,(self.pos[1]-5)*CELL_SIZE) if pos==(-1,-1) else pos
        shape = self.shape[1:] if scale != 1 and isinstance(self, I) else self.shape
        for off_y, row in enumerate(shape):
            for off_x, block in enumerate(row):
                if scale != 1 and isinstance(self, I):
                    off_x = off_x-1
                if block != 0:
                    r = pygame.Rect(x+off_x*CELL_SIZE*scale+(CELL_SIZE*(1-scale*VANITY))/2, y+off_y*CELL_SIZE*scale+(CELL_SIZE*(1-scale*VANITY))/2, CELL_SIZE*scale*VANITY, CELL_SIZE*scale*VANITY)
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
        self.pos = (int(COLS/2) - 2 + 3, 5)
        self.shape = [[0, 1, 1],
    	              [0, 1, 1],
                      [0, 0, 0]]
        self.color = (255,255,0)

class L(Tetromino):
    def __init__(self):
        super().__init__()
        self.width = 3
        self.hight = 2
        self.pos = (int(COLS/2) - 2 + 3, 5)
        self.shape = [[0, 0, 1],
    	              [1, 1, 1],
                      [0, 0, 0]]
        self.color = (255, 165, 0)
class J(Tetromino):
    def __init__(self):
        super().__init__()
        self.width = 3
        self.hight = 2
        self.pos = (int(COLS/2) - 2 + 3, 5)
        self.shape = [[1, 0, 0],
    	              [1, 1, 1],
                      [0, 0, 0]]
        self.color = (0,0,255)
class T(Tetromino):
    def __init__(self):
        super().__init__()
        self.width = 3
        self.hight = 2
        self.pos = (int(COLS/2) - 2 + 3, 5)
        self.shape = [[0, 1, 0],
    	              [1, 1, 1],
                      [0, 0, 0]]
        self.color = (160, 32, 240)
        self.wall_kick = False
        self.last_rotate = False

class I(Tetromino):
    rotation_cw = [
        [( 0, 0),(-1, 0),( 2, 0),(-1, 0),( 2, 0)],
        [(-1, 0),( 0, 0),( 0, 0),( 0,-1),( 0, 2)],
        [(-1,-1),( 1,-1),(-2,-1),( 1, 0),(-2, 0)],
        [( 0,-1),( 0,-1),( 0,-1),( 0, 1),( 0,-2)]
    ]
    def __init__(self):
        super().__init__()
        self.width = 4
        self.hight = 1
        self.pos = (int(COLS/2) -3 + 3, 3)
        self.shape = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 1, 1, 1, 1],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
        self.color = (0, 255, 255)


class Z(Tetromino):
    def __init__(self):
        super().__init__()
        self.width = 3
        self.hight = 2
        self.pos = (int(COLS/2) - 2 + 3, 5)
        self.shape = [[1, 1, 0],
    	              [0, 1, 1],
                      [0, 0, 0]]
        self.color = (255,0,0)
class S(Tetromino):
    def __init__(self):
        super().__init__()
        self.width = 3
        self.hight = 2
        self.pos = (int(COLS/2) - 2 + 3, 5)
        self.shape = [[0, 1, 1],
    	              [1, 1, 0],
                      [0, 0, 0]]
        self.color = (0,255,0)

if __name__ == '__main__':
	App = TetrisGame()
	App.loop()
