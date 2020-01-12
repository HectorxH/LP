import sys
from math import floor
from random import shuffle
import heapq as pq

import pygame

from Board import Board
from constants import *
from Tetrominos import Tetromino, shapes

class InputBox:
    abc = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

    def __init__(self):
        self.text = [0, 0, 0]
        self.curr = 0

    def move_left(self):
        self.curr = (self.curr-1)%3

    def move_right(self):
        self.curr = (self.curr+1)%3

    def up(self):
        self.text[self.curr] = (self.text[self.curr]+1)%len(InputBox.abc)

    def down(self):
        self.text[self.curr] = (self.text[self.curr]-1)%len(InputBox.abc)

    def get_text(self):
        return "".join(list(map(lambda x: InputBox.abc[x], self.text)))

    def get_pos(self):
        pos = [' ', ' ', ' ']
        pos[self.curr] = '^'
        return "".join(pos)

class TetrisGame:
    SCORE = [0, 100, 300, 500, 800, 1200, 1600]
    LINES = [0, 1, 3, 5, 8]

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()

        self.cell_size = 36
        self.volume = 0.3

        self.dimensions = (self.cell_size*(COLS+2*SIDE), self.cell_size*ROWS)
        self.side = self.cell_size*(COLS+SIDE)

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
        """
        Crea los distintos tipos de fuentes para el tamaño de la pantalla actual.

        Retorno:
            No retorna.
        """

        font = "joystix monospace.ttf"

        create_font = lambda size: pygame.font.Font(
            font, floor(self.cell_size*size),
            bold=False,
            italic=False)

        base = 0.8

        self.small_font = create_font(base-0.2)
        self.default_font = create_font(base)
        self.big_font = create_font(base+0.3)

    def new_bag(self):
        """
        Ordena de manera aleatoria los siguientes 7 tetrominos que el jugador obtendra.

        Retorno:
            Retorna la bolsa.
        """

        bag = [shape() for shape in shapes]
        shuffle(bag)
        return bag

    def new_tetromino(self):
        """
        Crea un nuevo tetromino, lo a;ade al tablero y si se vacia la bolsa, crea una nueva.

        Retorno:
            No retorna.
        """

        if len(self.bag) == 7:
            self.bag = self.bag+self.new_bag()
        self.tetromino = self.bag.pop(0)

        self.gameover = self.board.new_tetromino(self.tetromino)


    def init_game(self):
        """
        Inicia un nuevo juego.

        Retorno:
            No retorna.
        """

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

        scores = []
        self.top10 = []
        with open("scores.txt", 'r+') as file:
            for line in file:
                score, name = line.strip().split(', ')
                scores.append((int(score), name))
            pq.heapify(scores)
            self.top10 = pq.nlargest(10, scores)

        pygame.mixer.music.rewind()
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(self.volume)

    def draw_next(self):
        """
        Dibuja los siguientes tetrominos.

        Retorno:
            No retorna.
        """

        offset = floor(self.cell_size/2)
        self.display_text("Next:", (self.side+self.cell_size, 0))

        next_tetromino = self.bag[0]
        next_tetromino.draw_at(self.screen, self.cell_size, (self.side+offset, 3*offset), 0.9)

        for i, tetromino in enumerate(self.bag[1:7]):
            tetromino.draw_at(
                self.screen,
                self.cell_size,
                (self.side+9*offset, 3*(i+0.2 if tetromino.name is 'I' else i+0.3)*offset),
                0.4)

    def draw_hold(self):
        """
        Dibuja el tetrimonio que esta en hold.

        Retorno:
            No retorna.
        """

        self.display_text("Hold:", (self.cell_size*0.1, self.cell_size*0.1))
        if self.holding:
            self.hold.draw_at(self.screen, self.cell_size, (self.cell_size, self.cell_size*2), 1.1)

    def draw_stats(self):
        """
        Muestra la informacion de las estadisticas.

        Retorno:
            No retorna.
        """

        x, y = 0.1, 10
        print_stat = lambda offset, k: self.display_smoll_text(
            "{}: {}".format(k, self.stats[k]),
            (1+self.side+self.cell_size*x, self.cell_size*(y+offset)))
        for i, k in enumerate(self.stats):
            print_stat(i, k)

    def draw_splash_text(self):
        """
        Se asegura de que los mensajes de bonificacion aparezcan en pantalla por un tiempo.

        Retorno:
            No retorna.
        """

        for i, info in enumerate(self.text):
            f, time_left = info
            if time_left <= 0:
                del self.text[i]
            else:
                self.text[i] = (f, time_left-1)
            f()

    def display_text(self, string, pos):
        """
        Muestra en pantalla el texto string en la posicion pos con la fuente por defecto.
        
        Argumentos:
            string (string): Texto que se quiere mostrar.
            pos (par): Posicion donde se mostrara el texto.

        Retorno:
            No retorna.
        """

        self.screen.blit(self.default_font.render(string, False, (255, 255, 255), DETAIL), pos)

    def display_smoll_text(self, string, pos):
        """
        Muestra en pantalla el texto string en la posicion pos con la fuente por defecto pero en tamaño pequeño.
        
        Argumentos:
            string (string): Texto que se quiere mostrar.
            pos (par): Posicion donde se mostrara el texto.

        Retorno:
            No retorna.
        """

        self.screen.blit(self.small_font.render(string, False, (255, 255, 255), DETAIL), pos)

    def display_big_text(self, string, pos):
        """
        Muestra en pantalla el texto string en la posicion pos con la fuente por defecto pero en tamaño grande.

        Argumentos:
            string (string): Texto que se quiere mostrar.
            pos (par): Posicion donde se mostrara el texto.

        Retorno:
            No retorna.
        """
        self.screen.blit(self.big_font.render(string, False, (255, 255, 255), DETAIL), pos)

    def splash_text(self, string, y):
        """
        Crea los splash text.

        Argumentos:
            string (string): Texto que se quiere mostrar.
            y (int): Funcion que imprime el texto entregado a la funcion.

        Retorno:
            Retorna una funcion.
        """

        text = self.big_font.render(string, False, (255, 255, 255), (0, 0, 0, 255))
        text_rect = text.get_rect(center=((self.cell_size/2)*(COLS+2*SIDE), y*self.cell_size))
        return lambda:self.screen.blit(text, text_rect)

    def tspin(self, x, b2b=False):
        """
        Muestra los mensajes de T-Spin.

        Argumentos:
            x (int): Cantidad de lineas que se limpiaron con el T-Spin.
            b2b (boolean): Es True si las ultimas lineas se limpiaron con un T-Spin y False en caso contrario.

        Retorno:
            No retorna.
        """

        if x == 0:
            string = "T-Spin"
        elif x == 1:
            string = "T-Spin Single!"
        elif x == 2:
            string = "T-Spin Double!!"
        elif x == 3:
            string = "T-Spin Triple!!!"

        if b2b:
            self.text.append((self.splash_text("Back 2 Back!", 2), TEXT_DURATION))
        self.text.append((self.splash_text(string, 4), TEXT_DURATION))

    def combo_count(self, combo):
        """
        Muestra el combo actual.

        Argumentos:
            combo (int): Cantidad de combos que ha realizado el jugador hasta el momento

        Retorno:
            No retorna.
        """

        self.text.append((self.splash_text("x{}!".format(combo), 6), TEXT_DURATION))

    def tetris(self, b2b=False):
        """
        Muestra los mensajes de Tetris.

        Argumentos:
            b2b (boolean): 

        Retorno:
            No retorna.
        """

        if b2b:
            self.text.append((self.splash_text("Back 2 Back!", 2), TEXT_DURATION))
        self.text.append((self.splash_text("Tetris!", 4), TEXT_DURATION))

    def score_lines(self, lines, isTspin):
        """
        Actualiza el puntaje actual y muestra en pantalla los textos de jugadas especiales.

        Dada la cantidad de lineas que se limpiaron y si la jugada fue un T-Spin o Tetris, actualiza
        el puntaje actual y muestra en pantalla los textos de jugadas especiales si es necesario.

        Argumentos:
            lines (int): Cantidad de lineas que se limpiaron.
            isTspin (boolean): Es True si la jugada fue un T-Spin y False si es que no.

        Retorno:
            No retorna.
        """

        if lines == 0:
            self.stats["Combo"] = 0
        else:
            self.stats["Combo"] += 1

        if lines >= 4 and self.b2b_tetris:
            self.stats["Score"] += floor(TetrisGame.SCORE[lines]*self.stats["Level"]*0.5)
            self.tetris(b2b=True)
        elif isTspin and self.b2b_tspin:
            self.stats["Score"] += floor(TetrisGame.SCORE[lines+3]*self.stats["Level"]*0.5)
            self.tspin(lines, b2b=True)
        elif isTspin:
            self.stats["Score"] += TetrisGame.SCORE[lines+3]*self.stats["Level"]
            self.tspin(lines)
        else:
            self.stats["Score"] += TetrisGame.SCORE[lines]*self.stats["Level"]
            if lines == 4:
                self.tetris()

        self.stats["Score"] += 50*self.stats["Combo"]*self.stats["Level"]
        if self.stats["Combo"] >= 5:
            self.combo_count(self.stats["Combo"])

        self.stats["Lines"] += TetrisGame.LINES[lines]
        if self.stats["Lines"] >= self.stats["Level"]*5:
            self.stats["Level"] += 1
            self.delay = max(0, BASE_DALAY-2*self.stats["Level"])

        if lines > 0:
            self.b2b_tetris = lines >= 4
            self.b2b_tspin = isTspin

    def move(self, direction):
        """
        Se encarga del movimiento horizontal del tetromino.

        Argumentos:
            direction (int): Direccion en la que se movera el tetromino.

        Retorno:
            No retorna.
        """

        if not self.gameover and not self.paused:
            if self.board.move(direction):
                pygame.mixer.Sound.play(self.sounds["move"])

    def resize(self, w, h):
        """
        Modifica el tamaño de la pantalla.

        Argumentos:
            w (int): Cantidad de pixeles para el ancho.
            h (int): Cantidad de pixeles para el alto.

        Retorno:
            No retorna.
        """

        w, h = w-w%COLS, h-h%ROWS
        w, h = max(w, h), min(w, h)
        self.dimensions = (w, h)
        self.window = pygame.display.set_mode(self.dimensions, pygame.RESIZABLE)
        self.cell_size = floor(h/22)
        self.side = self.cell_size*(COLS+SIDE)
        self.screen = pygame.surface.Surface((h, h))
        self.make_fonts()

    def quit(self):
        """
        Permite salir del juego.

        Retorno:
            No retorna.
        """

        sys.exit()

    def swap_hold(self):
        """
        Intercambia el tetromino actual con el guardado en hold.

        Retorno:
            No retorna.
        """

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
        """
        Cuando un tetromino choca con una pieza, saca un nuevo tetromino de la bolsa y calcula el puntaje.

        Argumentos:
            lines (int): Cantidad de lineas que se limpiaron.
            isTspin (boolean): Es True si la jugada fue un T-Spin y False si es que no.

        Retorno:
            No retorna.
        """

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
        """
        Hace que el tetromino caiga.

        Argumentos:
            soft (boolean): Si es True el tetromino baja mas rapido.

        Retorno:
            No retorna.
        """

        if not self.gameover and not self.paused:
            if soft and self.tetromino.score < 20:
                self.stats["Score"] += 1
                self.tetromino.score += 1
            lines, isTspin = self.board.drop(self.delay, soft)
            if lines >= 0:
                self.update_piece(lines, isTspin)

    def hard_drop(self):
        """
        Hace que el tetromino caiga de una vez.

        Retorno:
            No retorna.
        """

        if not self.gameover and not self.paused:
            pygame.mixer.Sound.play(self.sounds["hard drop"])
            self.stats["Score"] += 40
            lines, isTspin = self.board.drop(self.delay, manual=True)
            while lines < 0:
                lines, isTspin = self.board.drop(self.delay, manual=True, hard=True)
            self.update_piece(lines, isTspin)

    def rotate(self, direction):
        """
        Rota el tetromino actual en 90°.

        Argumentos:
            direction (int): Direccion en la que se rotara el tetromino.

        Retorno:
            No retorna.
        """

        if not self.gameover and not self.paused:
            pygame.mixer.Sound.play(self.sounds["rotate"])
            self.board.rotate(direction)

    def pause(self):
        """
        Detiene el juego momentaneamente.

        Retorno:
            No retorna.
        """

        self.display_big_text("HIGH SCORES:", (self.cell_size*(SIDE+1), self.cell_size*(2)))
        
        for i, info in enumerate(self.top10):
            score, name = info
            score = -score
            self.display_text(
                "{place}.- {name}: {score}".format(place=i+1, name=name, score=-score),
                 (self.cell_size*(SIDE+1), self.cell_size*(4+i)))
        
    def restart(self):
        """
        Comienza un nuevo juego y actualiza High Scores.

        Retorno:
            No retorna.
        """

        no_name = True
        input_field = InputBox()
        while no_name:
            w, h = self.dimensions

            self.window.fill(DETAIL)
            self.screen.fill(DETAIL)

            self.pause()

            self.display_big_text("NEW SCORE:", (self.cell_size*(SIDE+1), self.cell_size*(16)))
            self.display_text(
                "{name}: {score}".format(name=input_field.get_text(), score=self.stats["Score"]),
                 (self.cell_size*(SIDE+1), self.cell_size*(18)))
            self.display_text(
                input_field.get_pos(),
                 (self.cell_size*(SIDE+1), self.cell_size*(19)))

            self.window.blit(self.screen, (floor(w/2 - self.cell_size*ROWS/2), 0))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        input_field.up()
                        pygame.mixer.Sound.play(self.sounds["move"])
                    elif event.key == pygame.K_DOWN:
                        input_field.down()
                        pygame.mixer.Sound.play(self.sounds["move"])
                    elif event.key == pygame.K_LEFT:
                        input_field.move_left()
                        pygame.mixer.Sound.play(self.sounds["move"])
                    elif event.key == pygame.K_RIGHT:
                        input_field.move_right()
                        pygame.mixer.Sound.play(self.sounds["move"])
                    elif event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE):
                        pygame.mixer.Sound.play(self.sounds["triple"])
                        no_name = False
            
        with open('scores.txt', 'a') as file:
            file.write("{score}, {name}".format(score=self.stats["Score"], name=input_field.get_text()) + '\n')
        self.init_game()

    def loop(self):
        """
        Loop principal del juego.

        Retorno:
            No retorna.
        """

        clock = pygame.time.Clock()
        moveTick = 0
        moveAccel = 0
        dropTick = 0

        w, h = self.dimensions

        verticalLine = lambda x: pygame.draw.line(self.screen, BORDER_COLOR, (x, 0), (x, h))

        while True:
            w, h = self.dimensions
            self.window.fill(DETAIL)
            self.screen.fill(DETAIL)
            if self.gameover:
                self.restart()
            elif self.paused:
                self.pause()
            else:
                verticalLine(SIDE*self.cell_size)
                verticalLine(self.side+1)
                self.board.draw(self.screen, self.cell_size)
                self.draw_next()
                self.draw_hold()
                self.draw_stats()
                self.draw_splash_text()
            self.window.blit(self.screen, (floor(w/2 - self.cell_size*ROWS/2), 0))
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

if __name__ == '__main__':
    App = TetrisGame()
    App.loop()
