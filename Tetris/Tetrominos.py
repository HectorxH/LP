try:
    import pygame
except:
    raise ImportError("No se a encontrado pygame en los modulos instalados.")
    
try:
    from abc import ABC
    from math import floor
    from constants import BLOCK_SIZE, COLS, SIDE
except ImportError as err:
    raise ImportError("Error al cargar modulos: {}".format(err))

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
        self.isI = False

    def get_color(self):
        return self.color

    def get_shape(self):
        return self.shape

    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos

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

    def draw_at(self, screen, cell_size, pos, scale):
        """
        Dibuja el tetromino en una posicion especifica de la pantalla.

        Argumentos:
            screen (superficie de pygame): Pantalla del juego.
            cell_size (entero): Ancho de un cuadrado de la pantalla en pixeles.
            pos (par): Posicion donde se quiere dibujar.
            scale (entero): Factor que escala el tamaño del tetromino mostrado en pantalla.

        Retorno:
            No retorna.
        """

        x, y = pos
        for off_y, row in enumerate(self.shape):
            for off_x, _ in filter(lambda x: x[1], enumerate(row)):
                correction = lambda x, off: x+off*cell_size*scale+(cell_size*scale*(1-BLOCK_SIZE))/2
                width = cell_size*scale*BLOCK_SIZE
                r = pygame.Rect(correction(x, off_x), correction(y, off_y), width, width)
                pygame.draw.rect(screen, self.color, r)

    def draw_ghost(self, screen, cell_size, pos):
        """
        Dibuja la sombra del tetromino, donde deberia caer.

        Argumentos:
            screen (superficie de pygame): Pantalla del juego.
            cell_size (entero): Ancho de un cuadrado de la pantalla en pixeles.
            pos (par): Posicion donde se quiere dibujar.

        Retorno:
            No retorna.
        """

        x, y = pos
        # x, y = ((SIDE+x-first_row)*CELL_SIZE,(y-first_col)*CELL_SIZE)
        color = tuple(map(lambda x: floor(x/3), self.color))
        for off_y, row in enumerate(self.shape):
            for off_x, _ in filter(lambda x: x[1], enumerate(row)):
                correction = lambda x, off_x: x+off_x*cell_size+(cell_size*(1-BLOCK_SIZE))/2
                width = cell_size*BLOCK_SIZE
                r = pygame.Rect(correction(x, off_x), correction(y, off_y), width, width)
                pygame.draw.rect(screen, color, r)

    def draw(self, screen, cell_size):
        """
        Dibuja el tetromino en la pantalla.

        Argumentos:
            screen (superficie de pygame): Pantalla del juego.
            cell_size (entero): Ancho de un cuadrado de la pantalla en pixeles.

        Retorno:
            No retorna.
        """

        first_row, first_col = 3, 5
        x, y = self.pos
        x, y = ((SIDE+x-first_row)*cell_size, (y-first_col)*cell_size)
        for off_y, row in enumerate(self.shape):
            for off_x, _ in filter(lambda x: x[1], enumerate(row)):
                correction = lambda x, off_x: x+off_x*cell_size+(cell_size*(1-BLOCK_SIZE))/2
                width = cell_size*BLOCK_SIZE
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
        self.name = 'O'

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
        self.name = 'L'
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
        self.name = 'J'
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
        self.name = 'T'

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
        self.name = 'I'

    def draw_at(self, screen, cell_size, pos, scale):
        """
        Dibuja el tetromino en una posicion especifica de la pantalla y la ajusta ya que su tamaño es distinto.

        Argumentos:
            screen (superficie de pygame): Pantalla del juego.
            cell_size (entero): Ancho de un cuadrado de la pantalla en pixeles.
            pos (par): Posicion donde se quiere dibujar.
            scale (entero): Factor que escala el tamaño del tetromino mostrado en pantalla.

        Retorno:
            No retorna.
        """

        scale = scale*0.9
        x, y = pos
        shape = self.shape[1:]
        for off_y, row in enumerate(shape):
            for off_x, _ in filter(lambda x: x[1], enumerate(row)):
                off_x, off_y = off_x-1.5, off_y
                correction = lambda x, off: x+off*cell_size*scale+(cell_size*(1-scale*BLOCK_SIZE))/2
                width = cell_size*scale*BLOCK_SIZE
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
        self.name = 'Z'

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
        self.name = 'S'

shapes = [O, L, J, T, I, Z, S]
