from random import  shuffle
from math import floor
import pygame, sys

CELL_SIZE = 36
SIDE = 6
COLS = 10
ROWS = 22
MAX_FPS = 30
BASE_DALAY = 40
BLOCK_SIZE = 0.7
BACKGROUND = (0,0,0)
DETAIL = (30,30,30)
TEXT_DURATION = 20

VOLUME = 0.3

score = [0, 100, 300, 500, 800, 1200, 1600]
linelines = [0, 1, 3, 5, 8]

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
        font = pygame.font.get_default_font()
        create_font = lambda size: pygame.font.Font(font, floor(CELL_SIZE*size))

        self.small_font = create_font(0.5)
        self.default_font =  create_font(0.7)
        self.big_font = create_font(1)

    def new_bag(self):
        shapes = [O, L, J, T, I, Z, S]
        list = [shapes[i]() for i in range(7)]
        shuffle(list)
        return list

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
        self.bag[0].draw(self.screen, (self.side+offset,CELL_SIZE), 0.9)
        for i, tetromino in enumerate(self.bag[1:7]):
            tetromino.draw(self.screen, (self.side+8*offset, 4*i*offset), 0.4)

    def draw_hold(self):
        x,y = 1,1
        self.display_text("Hold:", (CELL_SIZE*x, CELL_SIZE*y))
        if self.holding:
            self.hold.draw(self.screen, (CELL_SIZE*x,CELL_SIZE*(y+1)), 1.1, False)

    def draw_stats(self):
        x,y = 0.1,5
        print_stat = lambda offset, k: self.display_smoll_text("{}: {}".format(k, self.stats[k]), (1+self.side+CELL_SIZE*x, CELL_SIZE*(y+offset)))
        for i, k in enumerate(self.stats):
            print_stat(i,k)

    def draw_splash_text(self):
        for i, info in enumerate(self.text):
            f, time_left = info
            if time_left == 0:
                del self.text[i]
            else:
                self.text[i] = (f, time_left-1)
            f()

    def display_text(self, string, pos):
        self.screen.blit(self.default_font.render(string,False,(255,255,255), DETAIL), pos)

    def display_smoll_text(self, string, pos):
        self.screen.blit(self.small_font.render(string,False,(255,255,255), DETAIL), pos)

    def display_big_text(self, string, pos):
        self.screen.blit(self.big_font.render(string,False,(255,255,255), (0,0,0,255)), pos)

    def tspin(self, x):
        if x==0:
            str = "T-Spin"
        elif x==1:
            str = "T-Spin Single!"
        elif x==2:
            str = "T-Spin Double!!"
        elif x==3:
            str = "T-Spin Triple!!!"
        self.text.append((lambda:self.display_big_text(str, (SIDE*CELL_SIZE+CELL_SIZE*2,CELL_SIZE*3)), TEXT_DURATION))


    def combo_count(self, combo):
        self.text.append((lambda:self.display_big_text("x{}!".format(combo), (SIDE*CELL_SIZE+CELL_SIZE*4,CELL_SIZE*4)), TEXT_DURATION))

    def tetris(self):
        self.text.append((lambda:self.display_big_text("Tetris!", (SIDE*CELL_SIZE+CELL_SIZE*4,CELL_SIZE*3)), TEXT_DURATION))

    def b2b(self):
        self.text.append((lambda:self.display_big_text("Back to Back", (SIDE*CELL_SIZE+CELL_SIZE*2,CELL_SIZE*2)), TEXT_DURATION))

    def score_lines(self, lines, isTspin):
        if lines == 0:
            self.stats["Combo"] = 0
        else:
            self.stats["Combo"]+=1

        if isTspin:
            self.stats["Score"] += score[lines+3]*self.stats["Level"]
            self.tspin(lines)
        else:
            self.stats["Score"] += score[lines]*self.stats["Level"]
            if lines == 4:
                self.tetris()

        if lines>=4 and self.b2b_tetris:
            self.stats["Score"] += floor(score[lines]*self.stats["Level"]*0.5)
            self.b2b()
        if isTspin and self.b2b_tspin:
            self.stats["Score"] += floor(score[lines+3]*self.stats["Level"]*0.5)
            self.b2b()

        self.stats["Score"] += 50*self.stats["Combo"]*self.stats["Level"]
        if self.stats["Combo"] >= 5:
            self.combo_count(self.stats["Combo"])

        self.stats["Lines"] += linelines[lines]
        if self.stats["Lines"] >= self.stats["Level"]*5:
            self.stats["Level"] += 1
            self.delay = max(1, BASE_DALAY-2*self.stats["Level"])

        if lines > 0:
            self.b2b_tetris = lines>=4
            self.b2b_tspin = isTspin

    def move(self, dir):
        if not self.gameover and not self.paused:
            if self.board.move(dir):
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
        self.default_font =  pygame.font.Font(pygame.font.get_default_font(), floor(CELL_SIZE*0.7))
        self.small_font = pygame.font.Font(pygame.font.get_default_font(), floor(CELL_SIZE*0.5))
        self.big_font = pygame.font.Font(pygame.font.get_default_font(), floor(CELL_SIZE))

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
            type = ["lock", "single", "double", "triple"]
            pygame.mixer.Sound.play(self.sounds[type[lines]])
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

    def rotate(self, dir):
        if not self.gameover and not self.paused:
            pygame.mixer.Sound.play(self.sounds["rotate"])
            self.board.rotate(dir)

    def pause(self):
        pass

    def restart(self):
        self.init_game()

    def loop(self):
        clock = pygame.time.Clock()
        moveTick = 0
        moveAccel = 0
        dropTick = 0

        while True:
            self.window.fill(DETAIL)
            self.screen.fill(DETAIL)
            if self.gameover:
                self.restart()
            elif self.paused:
                pass #Draw Pause screen?
            else:
                pygame.draw.line(self.screen,(255,255,255),(SIDE*CELL_SIZE, 0),(SIDE*CELL_SIZE, self.dimensions[1]))
                pygame.draw.line(self.screen,(255,255,255),(self.side+1, 0),(self.side+1, self.dimensions[1]))
                self.board.draw(self.screen)
                self.draw_next()
                self.draw_hold()
                self.draw_stats()
                self.draw_splash_text()
            self.window.blit(self.screen, (floor(self.dimensions[0]/2 - CELL_SIZE*11), 0))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: self.paused = not self.paused
                    elif event.key in (pygame.K_UP, pygame.K_x): self.rotate(1)
                    elif event.key in (pygame.K_LSHIFT, pygame.K_c): self.swap_hold()
                    elif event.key in (pygame.K_LCTRL, pygame.K_z):  self.rotate(-1)
                    elif event.key == pygame.K_SPACE: self.hard_drop()
                    elif event.key == pygame.K_q: self.quit()
                    elif event.key == pygame.K_r: self.restart()
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
                    if event.key == pygame.K_LEFT: self.isMovingLeft = False
                    elif event.key == pygame.K_RIGHT: self.isMovingRight = False
                    elif event.key == pygame.K_DOWN: self.isSoftDroping = False
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
        didMove = False
        x, y = self.tetromino.get_pos()
        x += dir
        if not self.willCollide((x,y)):
            self.tetromino.set_pos((x,y))
            didMove = True
        self.tetromino.last_rotate = False
        return didMove

    def draw_ghost(self, screen):
        x, y = self.tetromino.get_pos()
        while not self.willCollide((x, y)):
            y += 1
        y -= 1
        self.tetromino.draw(screen, ((x+SIDE-3)*CELL_SIZE, (y-5)*CELL_SIZE), ghost=True)

    def drop(self, delay, manual=False, hard=False):
        Tetromino.DELAY = BASE_DALAY-floor((BASE_DALAY-delay)/2)
        isTspin = False
        self.clock += 1
        self.tetromino.lock_delay -= 1
        if self.clock % delay == 0 or manual:
            if not self.active_tetromino:
                return -2, isTspin
            x, y = self.tetromino.get_pos()
            if self.willCollide((x,y+1)) and (self.tetromino.lock_delay <= 0 or hard):
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
            elif self.willCollide((x,y+1)) and self.tetromino.lock_delay >= 0:
                self.tetromino.set_pos((x,y))
                return -1, isTspin
            else:
                self.tetromino.lock_delay = Tetromino.DELAY
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
        for y, row in enumerate(self.matrix[5:-2]):
            for x, color in enumerate(row[3:-3]):
                r = pygame.Rect(SIDE*CELL_SIZE+CELL_SIZE*x+CELL_SIZE*(1-BLOCK_SIZE)/2, CELL_SIZE*y+CELL_SIZE*(1-BLOCK_SIZE)/2, CELL_SIZE*BLOCK_SIZE, CELL_SIZE*BLOCK_SIZE)
                pygame.draw.rect(screen, color, r)
        if self.active_tetromino:
            self.draw_ghost(screen)
            self.tetromino.draw(screen)

class Tetromino():
    DELAY = 4
    rotation_cw = [
        [( 0, 0),( 0, 0),( 0, 0),( 0, 0),( 0, 0)],
        [( 0, 0),( 1, 0),( 1, 1),( 0,-2),( 1,-2)],
        [( 0, 0),( 0, 0),( 0, 0),( 0, 0),( 0, 0)],
        [( 0, 0),(-1, 0),(-1, 1),( 0,-2),(-1,-2)]
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

    def draw(self, screen, pos=(-1,-1), scale=1, ghost=False):
        x, y = ((SIDE+self.pos[0]-3)*CELL_SIZE,(self.pos[1]-5)*CELL_SIZE) if pos==(-1,-1) else pos
        shape = self.shape[1:] if scale != 1 and isinstance(self, I) else self.shape
        color = tuple(map(lambda x: floor(x/3), self.color)) if ghost else self.color
        for off_y, row in enumerate(shape):
            for off_x, block in enumerate(row):
                if scale != 1 and isinstance(self, I):
                    off_x = off_x-1
                if block != 0:
                    r = pygame.Rect(x+off_x*CELL_SIZE*scale+(CELL_SIZE*(1-scale*BLOCK_SIZE))/2, y+off_y*CELL_SIZE*scale+(CELL_SIZE*(1-scale*BLOCK_SIZE))/2, CELL_SIZE*scale*BLOCK_SIZE, CELL_SIZE*scale*BLOCK_SIZE)
                    pygame.draw.rect(screen, color, r)

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
        self.color = (255,255,0)

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
        self.color = (0,0,255)
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
        [( 0, 0),(-1, 0),( 2, 0),(-1, 0),( 2, 0)],
        [(-1, 0),( 0, 0),( 0, 0),( 0,-1),( 0, 2)],
        [(-1,-1),( 1,-1),(-2,-1),( 1, 0),(-2, 0)],
        [( 0,-1),( 0,-1),( 0,-1),( 0, 1),( 0,-2)]
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


class Z(Tetromino):
    def __init__(self):
        super().__init__()
        self.width = 3
        self.hight = 2
        self.pos = (floor(COLS/2) - 2 + 3, 5)
        self.shape = [[1, 1, 0],
    	              [0, 1, 1],
                      [0, 0, 0]]
        self.color = (255,0,0)
class S(Tetromino):
    def __init__(self):
        super().__init__()
        self.width = 3
        self.hight = 2
        self.pos = (floor(COLS/2) - 2 + 3, 5)
        self.shape = [[0, 1, 1],
    	              [1, 1, 0],
                      [0, 0, 0]]
        self.color = (0,255,0)

if __name__ == '__main__':
	App = TetrisGame()
	App.loop()
