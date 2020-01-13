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
        """
        Cuando se limpia una fila crea una nueva.

        Retorno:
            Retorna la nueva fila.
        """

        x_border = [BORDER_COLOR for i in range(self.margin[0])]
        return list(x_border + [BACKGROUND for i in range(COLS)] + x_border)

    def new_tetromino(self, tetromino):
        """
        Recibe un tetromino que pasa a ser el tetromino activo.

        Argumentos:
            tetromino (tetromino): Tetromino activo.

        Retorno:
            Retorna True si el tetromino puede aparecer o False en caso contrario.
        """

        self.tetromino = tetromino
        self.active_tetromino = True
        return self.willCollide(self.tetromino.get_pos())

    def willCollide(self, pos):
        """
        Revisa si el tetromino choca con un objeto.

        Argumentos:
            pos (par): Posicion del tetromino.

        Retorno:
            Retorna True si choca con un objeto o False en caso contrario.
        """

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
        """
        Se encarga del movimiento horizontal del tetromino y retorna si fue posible moverlo.

        Argumentos:
            direction (int): Direccion en la que se movera el tetromino.

        Retorno:
            Retorna True si logro mover el tetromino o False si no se pudo mover.
        """
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
        """
        Dibuja la sombra del tetromino.

        Argumentos:
            screen (superficie de pygame): Pantalla del juego.
            cell_size (entero): Ancho de un cuadrado de la pantalla en pixeles.

        Retorno:
            No retorna
        """

        x, y = self.tetromino.get_pos()
        while not self.willCollide((x, y)):
            y += 1
        y -= 1

        first_row, first_col = 3, 5
        ghost_pos = ((x+SIDE-first_row)*cell_size, (y-first_col)*cell_size)
        self.tetromino.draw_ghost(screen, cell_size, ghost_pos)

    def isTspin(self):
        """
        Revisa si esta en un estado de T-Spin.

        Retorno:
            Retorna True si esta en un estado de T-Spin o False si es que no.
        """

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
        """
        Baja el tetromino activo una casilla.

        Baja el tetrmino activo una casilla y lo bloquea despues de intentar bajarlo antes de que colisione.
        Si se bloquea, revisa si se tienen que limpiar lineas.

        Argumentos:
            delay (int): Tiempo que espera antes de volver a bajar la pieza.
            soft (boolean): Es True si el jugador baja manualmente la pieza y es False si no.
            hard (boolean): Es True si el jugador realiza un hard drop y es False si no.

        Retorno:
            Retorna el numero de lineas limpiadas, -1 si no se bloqueo y si fue un T-Spin.
        """

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
        """
        Rota el tetromino activo en 90°.

        Argumentos:
            direction (int): Direccion en la que se rotara el tetromino.

        Retorno:
            No retorna.
        """

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
        """
        Dibuja la cuadricula y los objetos bloqueados en el piso.

        Argumentos:
            screen (superficie de pygame): Pantalla del juego.
            cell_size (entero): Ancho de un cuadrado de la pantalla en pixeles.

        Retorno:
            No retorna.
        """

        for y, row in enumerate(self.matrix[5:-2]):
            for x, color in enumerate(row[3:-3]):
                correction = lambda x: cell_size*x+cell_size*(1-BLOCK_SIZE)/2
                width = cell_size*BLOCK_SIZE
                r = pygame.Rect(SIDE*cell_size+correction(x), correction(y), width, width)
                pygame.draw.rect(screen, color, r)
        if self.active_tetromino:
            self.draw_ghost(screen, cell_size)
            self.tetromino.draw(screen, cell_size)
