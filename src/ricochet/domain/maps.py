import random
from .quadrant import Quadrant
from .game import Game

def assemble_board(q1, q2, q3, q4):

    # Validación de colores únicos
    colors = [q1.color, q2.color, q3.color, q4.color]
    if len(set(colors)) != 4:
        raise ValueError("Los cuadrantes deben ser de colores distintos.")

    game = Game(16, 16)

    # Offsets
    game.load_quadrant(q1, offset=(0, 0))
    game.load_quadrant(q2, offset=(0, 8))
    game.load_quadrant(q3, offset=(8, 0))
    game.load_quadrant(q4, offset=(8, 8))

    # Bloque central 2x2
    center_cells = [(7,7), (7,8), (8,7), (8,8)]

    for cell in center_cells:
        game.blocked_cells.add(cell)

    # Paredes alrededor del bloque central
    central_walls = [
        ((7,6),(7,7)),
        ((6,7),(7,7)),
        ((7,8),(7,9)),
        ((6,8),(7,8)),
        ((8,6),(8,7)),
        ((8,7),(9,7)),
        ((8,8),(8,9)),
        ((8,8),(9,8)),
    ]

    for c1, c2 in central_walls:
        game.add_wall(c1, c2)

    return game


def create_green_quadrant_v1():

    q = Quadrant("green", 1)

    # Targets
    q.add_target("Y", "cross",  (1,3))
    q.add_target("R", "moon",   (3,1))
    q.add_target("B", "planet", (4,6))
    q.add_target("G", "sun",    (6,3))

    # Amarillo
    q.add_wall((0,3),(1,3))
    q.add_wall((1,3),(1,4))

    # Rojo
    q.add_wall((3,1),(4,1))
    q.add_wall((3,0),(3,1))

    # Azul
    q.add_wall((4,6),(5,6))
    q.add_wall((4,6),(4,7))

    # Verde
    q.add_wall((6,2),(6,3))
    q.add_wall((5,3),(6,3))

    # Extra walls
    q.add_wall((5,0),(6,0))
    q.add_wall((7,5),(7,6))

    # Hueco central
    q.add_wall((0,6),(0,7))
    q.add_wall((0,7),(1,7))

    return q

def create_green_quadrant_v2():

    q = Quadrant("green", 2)

    # --------------------
    # ENCASTRE
    # --------------------
    q.add_wall((0, 6), (0, 7))  # izquierda
    q.add_wall((0, 7), (1, 7))  # abajo

    # --------------------
    # TARGET AMARILLO (1,1)
    q.add_target("Y", "sun", (1,1))
    q.add_wall((0,1),(1,1))
    q.add_wall((1,1),(1,2))

    # TARGET AZUL (1,5)
    q.add_target("B", "moon", (1,5))
    q.add_wall((0,5),(1,5))
    q.add_wall((1,4),(1,5))

    # TARGET ROJO (4,6)
    q.add_target("R", "planet", (4,6))
    q.add_wall((4,6),(5,6))
    q.add_wall((4,6),(4,7))

    # TARGET VERDE (6,2)
    q.add_target("G", "cross", (6,2))
    q.add_wall((6,2),(7,2))
    q.add_wall((6,1),(6,2))

    # --------------------
    # PAREDES EXTRA
    # --------------------
    q.add_wall((2, 0), (3, 0))
    q.add_wall((7, 5), (7, 6))

    return q

def create_green_quadrant_v3():

    q = Quadrant("green", 3)

    # -----------------
    # TARGETS
    # -----------------

    # Amarillo - cruz (1,3)
    q.add_target("Y", "cross", (1, 3))
    q.add_wall((1, 3), (1, 4))  # derecha
    q.add_wall((0, 3), (1, 3))  # arriba

    # Verde - sol (4,1)
    q.add_target("G", "sun", (4, 1))
    q.add_wall((4, 0), (4, 1))  # izquierda
    q.add_wall((4, 1), (5, 1))  # abajo

    # Azul - planeta (3,6)
    q.add_target("B", "planet", (3, 6))
    q.add_wall((2, 6), (3, 6))  # arriba
    q.add_wall((3, 5), (3, 6))  # izquierda

    # Rojo - luna (6,4)
    q.add_target("R", "moon", (6, 4))
    q.add_wall((6, 4), (7, 4))  # abajo
    q.add_wall((6, 4), (6, 5))  # derecha

    # -----------------
    # PAREDES EXTRA
    # -----------------

    q.add_wall((5, 0), (6, 0))
    q.add_wall((7, 6), (7, 7))

    # -----------------
    # ENCASTRE (0,7)
    # -----------------

    q.add_wall((0, 6), (0, 7))  # izquierda
    q.add_wall((0, 7), (1, 7))  # abajo

    return q

def create_green_quadrant_v4():

    q = Quadrant("green", 4, has_bumpers=True)

    # -----------------
    # TARGETS
    # -----------------

    # Amarillo - cruz (1,4)
    q.add_target("Y", "cross", (1, 4))
    q.add_wall((1, 4), (1, 5))  # derecha
    q.add_wall((0, 4), (1, 4))  # arriba

    # Verde - sol (5,6)
    q.add_target("G", "sun", (5, 6))
    q.add_wall((5, 5), (5, 6))  # izquierda

    # Azul - planeta (4,6)
    q.add_target("B", "planet", (4, 6))
    q.add_wall((4, 6), (5, 6))  # abajo
    q.add_wall((4, 6), (4, 7))  # derecha

    # Rojo - luna (6,3)
    q.add_target("R", "moon", (6, 3))
    q.add_wall((6, 3), (7, 3))  # abajo
    q.add_wall((6, 2), (6, 3))  # izquierda

    # -----------------
    # PAREDES EXTRA
    # -----------------

    q.add_wall((2, 0), (1, 0))
    q.add_wall((7, 5), (7, 6))

    # -----------------
    # BUMPERS
    # -----------------

    q.add_bumper((2, 7), "/", "yellow")
    q.add_bumper((3, 1), "\\", "green")

    # -----------------
    # ENCASTRE (0,7)
    # -----------------

    q.add_wall((0, 6), (0, 7))  # izquierda
    q.add_wall((0, 7), (1, 7))  # abajo

    return q

def create_blue_quadrant_v1():

    q = Quadrant("blue", 1)

    # -----------------
    # TARGETS
    # -----------------

    q.add_target("B", "sun",    (2,3))
    q.add_target("G", "cross",  (3,5))
    q.add_target("Y", "moon",   (4,2))
    q.add_target("R", "planet", (5,4))

    # -----------------
    # WALLS targets
    # -----------------

    # Azul
    q.add_wall((2,3),(2,4))
    q.add_wall((2,3),(3,3))

    # Verde
    q.add_wall((3,5),(2,5))
    q.add_wall((3,5),(3,6))

    # Amarillo
    q.add_wall((4,2),(5,2))
    q.add_wall((4,1),(4,2))

    # Rojo
    q.add_wall((4,4),(5,4))
    q.add_wall((5,3),(5,4))

    # -----------------
    # Walls extra
    # -----------------

    q.add_wall((1,0),(2,0))
    q.add_wall((7,3),(7,4))

    # -----------------
    # Encastre (0,7)
    # -----------------

    q.add_wall((0,6),(0,7))
    q.add_wall((0,7),(1,7))

    return q

def create_blue_quadrant_v2():

    q = Quadrant("blue", 2)

    # --------------------
    # ENCASTRE (0,7)
    # --------------------
    q.add_wall((0, 6), (0, 7))  # izquierda
    q.add_wall((0, 7), (1, 7))  # abajo

    # --------------------
    # TARGET AMARILLO (1,4)
    # paredes: abajo / izquierda
    # --------------------
    q.add_target("Y", "sun", (1, 4))
    q.add_wall((1, 4), (2, 4))  # abajo
    q.add_wall((1, 3), (1, 4))  # izquierda

    # --------------------
    # TARGET VERDE (2,1)
    # paredes: arriba / derecha
    # --------------------
    q.add_target("G", "cross", (2, 1))
    q.add_wall((1, 1), (2, 1))  # arriba
    q.add_wall((2, 1), (2, 2))  # derecha

    # --------------------
    # TARGET AZUL (5,6)
    # paredes: arriba / izquierda
    # --------------------
    q.add_target("B", "moon", (5, 6))
    q.add_wall((4, 6), (5, 6))  # arriba
    q.add_wall((5, 5), (5, 6))  # izquierda

    # --------------------
    # TARGET ROJO (6,2)
    # paredes: abajo / derecha
    # --------------------
    q.add_target("R", "planet", (6, 2))
    q.add_wall((6, 2), (7, 2))  # abajo
    q.add_wall((6, 2), (6, 3))  # derecha

    # --------------------
    # PAREDES EXTRA
    # --------------------
    q.add_wall((3, 0), (4, 0))
    q.add_wall((7, 3), (7, 4))

    return q

def create_blue_quadrant_v3():

    q = Quadrant("blue", 3, has_bumpers=False)

    # -----------------
    # TARGETS
    # -----------------

    # Azul - sol (1,3)
    q.add_target("B", "sun", (1, 3))
    q.add_wall((1, 3), (1, 4))  # derecha
    q.add_wall((1, 3), (2, 3))  # abajo

    # Rojo - planeta (3,5)
    q.add_target("R", "planet", (3, 5))
    q.add_wall((3, 4), (3, 5))  # izquierda
    q.add_wall((2, 5), (3, 5))  # arriba

    # Amarillo - luna (5,1)
    q.add_target("Y", "moon", (5, 1))
    q.add_wall((5, 1), (6, 1))  # abajo
    q.add_wall((5, 0), (5, 1))  # izquierda

    # Verde - cruz (6,6)
    q.add_target("G", "cross", (6, 6))
    q.add_wall((5, 6), (6, 6))  # arriba
    q.add_wall((6, 6), (6, 7))  # derecha

    # -----------------
    # PAREDES EXTRA
    # -----------------

    q.add_wall((2, 0), (3, 0))
    q.add_wall((7, 4), (7, 5))

    # -----------------
    # ENCASTRE (0,7)
    # -----------------

    q.add_wall((0, 6), (0, 7))  # izquierda
    q.add_wall((0, 7), (1, 7))  # abajo

    return q

def create_blue_quadrant_v4():

    q = Quadrant("blue", 4, has_bumpers=True)

    # -----------------
    # TARGETS
    # -----------------

    # Amarillo - luna (1,2)
    q.add_target("Y", "moon", (1, 2))
    q.add_wall((1, 1), (1, 2))  # izquierda
    q.add_wall((1, 2), (2, 2))  # abajo

    # Verde - cruz (2,2)
    q.add_target("G", "cross", (2, 2))
    q.add_wall((2, 2), (2, 3))  # derecha

    # Azul - sol (3,7)
    q.add_target("B", "sun", (3, 7))
    q.add_wall((2, 7), (3, 7))  # arriba
    q.add_wall((3, 6), (3, 7))  # izquierda

    # Rojo - planeta (6,5)
    q.add_target("R", "planet", (6, 5))
    q.add_wall((6, 5), (7, 5))  # abajo
    q.add_wall((6, 5), (6, 6))  # derecha

    # -----------------
    # PAREDES EXTRA
    # -----------------

    q.add_wall((4, 0), (5, 0))
    q.add_wall((7, 6), (7, 7))

    # -----------------
    # BUMPERS
    # -----------------

    q.add_bumper((0, 4), "/", "red")
    q.add_bumper((5, 1), "\\", "blue")

    # -----------------
    # ENCASTRE (0,7)
    # -----------------

    q.add_wall((0, 6), (0, 7))  # izquierda
    q.add_wall((0, 7), (1, 7))  # abajo

    return q

def create_yellow_quadrant_v1():

    q = Quadrant("yellow", 1)

    # -----------------
    # TARGETS
    # -----------------

    q.add_target(None, "spiral", (0,2))   # comodín
    q.add_target("B", "moon",    (2,1))
    q.add_target("G", "planet",  (1,5))
    q.add_target("R", "cross",   (4,4))
    q.add_target("Y", "sun",     (6,6))

    # -----------------
    # WALLS targets
    # -----------------

    # Comodín
    q.add_wall((0,2),(0,3))
    q.add_border_wall((0,2), "up")

    # Azul
    q.add_wall((2,1),(2,2))
    q.add_wall((2,1),(3,1))

    # Verde
    q.add_wall((1,5),(1,4))
    q.add_wall((1,5),(2,5))

    # Rojo
    q.add_wall((4,4),(4,5))
    q.add_wall((4,4),(3,4))

    # Amarillo
    q.add_wall((6,6),(6,5))
    q.add_wall((6,6),(5,6))

    # -----------------
    # Walls extra
    # -----------------

    q.add_wall((4,0),(5,0))
    q.add_wall((7,3),(7,4))

    # -----------------
    # Encastre
    # -----------------

    q.add_wall((0,6),(0,7))
    q.add_wall((0,7),(1,7))

    return q

def create_yellow_quadrant_v2():

    q = Quadrant("yellow", 2)

    # --------------------
    # ENCASTRE (0,7)
    # --------------------
    q.add_wall((0, 6), (0, 7))  # izquierda
    q.add_wall((0, 7), (1, 7))  # abajo

    # --------------------
    # TARGET COMODÍN (0,5)
    q.add_target(None, "spiral", (0, 5))
    q.add_border_wall((0, 5), "up")
    q.add_wall((0, 5), (0, 6))  # derecha

    # --------------------
    # TARGET AZUL (1,1)
    # paredes abajo / derecha
    # --------------------
    q.add_target("B", "moon", (1, 1))
    q.add_wall((1, 1), (2, 1))  # abajo
    q.add_wall((1, 1), (1, 2))  # derecha

    # --------------------
    # TARGET VERDE (2,4)
    # paredes izquierda / abajo
    # --------------------
    q.add_target("G", "planet", (2, 4))
    q.add_wall((2, 3), (2, 4))  # izquierda
    q.add_wall((2, 4), (3, 4))  # abajo

    # --------------------
    # TARGET ROJO (5,5)
    # paredes arriba / derecha
    # --------------------
    q.add_target("R", "cross", (5, 5))
    q.add_wall((4, 5), (5, 5))  # arriba
    q.add_wall((5, 5), (5, 6))  # derecha

    # --------------------
    # TARGET AMARILLO (6,3)
    # paredes arriba / izquierda
    # --------------------
    q.add_target("Y", "sun", (6, 3))
    q.add_wall((5, 3), (6, 3))  # arriba
    q.add_wall((6, 2), (6, 3))  # izquierda

    # --------------------
    # PAREDES EXTRA
    # --------------------
    q.add_wall((3,0), (4,0))
    q.add_wall((7, 6), (7, 7))

    return q

def create_yellow_quadrant_v3():

    q = Quadrant("yellow", 3)

    # -----------------
    # TARGETS
    # -----------------

    # Amarillo - sol (1,4)
    q.add_target("Y", "sun", (1, 4))
    q.add_wall((1, 3), (1, 4))  # izquierda
    q.add_wall((1, 4), (2, 4))  # abajo

    # Verde - planeta (6,3)
    q.add_target("G", "planet", (6, 3))
    q.add_wall((6, 3), (6, 4))  # derecha
    q.add_wall((6, 3), (7, 3))  # abajo

    # Azul - luna (2,6)
    q.add_target("B", "moon", (2, 6))
    q.add_wall((1, 6), (2, 6))  # arriba
    q.add_wall((2, 5), (2, 6))  # izquierda

    # Rojo - cruz (5,1)
    q.add_target("R", "cross", (5, 1))
    q.add_wall((4, 1), (5, 1))  # arriba
    q.add_wall((5, 1), (5, 2))  # derecha

    # Comodín - espiral (4,7)
    q.add_target(None, "spiral", (4, 7))
    q.add_wall((3, 7), (4, 7))          # arriba
    q.add_border_wall((4, 7), "right")  # derecha (borde)

    # -----------------
    # PAREDES EXTRA
    # -----------------

    q.add_wall((2, 0), (3, 0))
    q.add_wall((7, 4), (7, 5))

    # -----------------
    # ENCASTRE (0,7)
    # -----------------

    q.add_wall((0, 6), (0, 7))  # izquierda
    q.add_wall((0, 7), (1, 7))  # abajo

    return q

def create_yellow_quadrant_v4():

    q = Quadrant("yellow", 4, has_bumpers=True)

    # -----------------
    # TARGETS
    # -----------------

    # Amarillo - sol (1,2)
    q.add_target("Y", "sun", (1, 2))
    q.add_wall((1, 1), (1, 2))  # izquierda
    q.add_wall((1, 2), (2, 2))  # abajo

    # Verde - planeta (4,3)
    q.add_target("G", "planet", (4, 3))
    q.add_wall((4, 3), (4, 4))  # derecha

    # Azul - luna (5,3)
    q.add_target("B", "moon", (5, 3))
    q.add_wall((4, 3), (5, 3))  # arriba
    q.add_wall((5, 2), (5, 3))  # izquierda

    # Rojo - cruz (6,5)
    q.add_target("R", "cross", (6, 5))
    q.add_wall((5, 5), (6, 5))  # arriba
    q.add_wall((6, 5), (6, 6))  # derecha

    # Comodín - espiral (2,7)
    q.add_target(None, "spiral", (2, 7))
    q.add_wall((1, 7), (2, 7))           # arriba
    q.add_border_wall((2, 7), "right")   # derecha (borde)

    # -----------------
    # PAREDES EXTRA
    # -----------------

    q.add_wall((2, 0), (3, 0))
    q.add_wall((7, 6), (7, 7))

    # -----------------
    # BUMPERS
    # -----------------

    q.add_bumper((5, 1), "/", "red")
    q.add_bumper((4, 6), "/", "green")

    # -----------------
    # ENCASTRE (0,7)
    # -----------------

    q.add_wall((0, 6), (0, 7))  # izquierda
    q.add_wall((0, 7), (1, 7))  # abajo

    return q

def create_red_quadrant_v1():

    q = Quadrant("red", 1, has_bumpers=False)

    # -----------------
    # TARGETS
    # -----------------

    q.add_target("R", "sun",     (0,5))
    q.add_target("B", "cross",   (2,2))
    q.add_target("G", "moon",    (5,4))
    q.add_target("Y", "planet",  (6,6))

    # -----------------
    # Walls targets
    # -----------------

    # Rojo
    q.add_wall((0,5),(1,5))
    q.add_wall((0,5),(0,6))

    # Azul
    q.add_wall((2,2),(1,2))
    q.add_wall((2,2),(2,3))

    # Verde
    q.add_wall((5,4),(4,4))
    q.add_wall((5,4),(5,3))

    # Amarillo
    q.add_wall((6,6),(6,5))
    q.add_wall((6,6),(7,6))

    # -----------------
    # Walls extra
    # -----------------

    q.add_wall((3,0),(4,0))
    q.add_wall((7,4),(7,5))

    # -----------------
    # Encastre
    # -----------------

    q.add_wall((0,7),(0,6))
    q.add_wall((0,7),(1,7))

    return q

def create_red_quadrant_v2():

    q = Quadrant("red", 2, has_bumpers=False)

    # -----------------
    # TARGETS
    # -----------------

    # Amarillo - planeta (0,5)
    q.add_target("Y", "planet", (0, 5))
    q.add_wall((0, 4), (0, 5))  # izquierda
    q.add_wall((0, 5), (1, 5))  # abajo

    # Verde - luna (1,2)
    q.add_target("G", "moon", (1, 2))
    q.add_wall((0, 2), (1, 2))  # arriba
    q.add_wall((1, 1), (1, 2))  # izquierda

    # Azul - cruz (5,4)
    q.add_target("B", "cross", (5, 4))
    q.add_wall((4, 4), (5, 4))  # arriba
    q.add_wall((5, 4), (5, 5))  # derecha

    # Rojo - sol (6,1)
    q.add_target("R", "sun", (6, 1))
    q.add_wall((6, 1), (7, 1))  # abajo
    q.add_wall((6, 1), (6, 2))  # derecha

    # -----------------
    # PAREDES EXTRA
    # -----------------

    q.add_wall((3, 0), (4, 0))
    q.add_wall((7, 5), (7, 6))

    # -----------------
    # ENCASTRE (0,7)
    # -----------------

    q.add_wall((0, 6), (0, 7))  # izquierda
    q.add_wall((0, 7), (1, 7))  # abajo

    return q

def create_red_quadrant_v3():

    q = Quadrant("red", 3, has_bumpers=False)

    # -----------------
    # TARGETS
    # -----------------

    # Amarillo - planeta (2,5)
    q.add_target("Y", "planet", (2, 5))
    q.add_wall((2, 4), (2, 5))  # izquierda
    q.add_wall((2, 5), (3, 5))  # abajo

    # Verde - luna (3,1)
    q.add_target("G", "moon", (3, 1))
    q.add_wall((3, 0), (3, 1))  # izquierda
    q.add_wall((2, 1), (3, 1))  # arriba

    # Azul - cruz (4,6)
    q.add_target("B", "cross", (4, 6))
    q.add_wall((3, 6), (4, 6))  # arriba
    q.add_wall((4, 6), (4, 7))  # derecha

    # Rojo - sol (6,3)
    q.add_target("R", "sun", (6, 3))
    q.add_wall((6, 3), (7, 3))  # abajo
    q.add_wall((6, 3), (6, 4))  # derecha

    # -----------------
    # PAREDES EXTRA
    # -----------------

    q.add_wall((5, 0), (6, 0))
    q.add_wall((7, 5), (7, 6))

    # -----------------
    # ENCASTRE (0,7)
    # -----------------

    q.add_wall((0, 6), (0, 7))  # izquierda
    q.add_wall((0, 7), (1, 7))  # abajo

    return q

def create_red_quadrant_v4():

    q = Quadrant("red", 4, has_bumpers=True)

    # -----------------
    # TARGETS
    # -----------------

    q.add_target("B", "cross",  (1,2))
    q.add_target("Y", "planet", (2,6))
    q.add_target("R", "sun", (4,4))
    q.add_target("G", "moon",   (5,4))

    # -----------------
    # BUMPERS
    # -----------------

    q.add_bumper((1,3), "/", "yellow")
    q.add_bumper((3,1), "/", "blue")

    # -----------------
    # WALLS targets
    # -----------------

    # Azul
    q.add_wall((1,2),(0,2))
    q.add_wall((1,2),(1,3))

    # Amarillo
    q.add_wall((2,6),(2,5))
    q.add_wall((2,6),(3,6))

    # Rojo
    q.add_wall((4,4),(4,5))
    q.add_wall((4,4),(5,4))

    # Verde
    q.add_wall((5,4),(5,3))

    # -----------------
    # Walls extra
    # -----------------

    q.add_wall((2,0),(3,0))
    q.add_wall((7,2),(7,3))

    # -----------------
    # Encastre
    # -----------------

    q.add_wall((0,6),(0,7))
    q.add_wall((0,7),(1,7))

    return q

GREEN_QUADRANTS = [
    create_green_quadrant_v1,
    create_green_quadrant_v2,
    create_green_quadrant_v3,
    create_green_quadrant_v4
]

BLUE_QUADRANTS = [
    create_blue_quadrant_v1,
    create_blue_quadrant_v2,
    create_blue_quadrant_v3,
    create_blue_quadrant_v4
]

RED_QUADRANTS = [
    create_red_quadrant_v1,
    create_red_quadrant_v2,
    create_red_quadrant_v3,
    create_red_quadrant_v4,
]

YELLOW_QUADRANTS = [
    create_yellow_quadrant_v1,
    create_yellow_quadrant_v2,
    create_yellow_quadrant_v3,
    create_yellow_quadrant_v4
]

def choose_quadrant(quadrant_factories, mode):

    # Crear todas las variantes posibles
    quadrants = [factory() for factory in quadrant_factories]

    if mode == "random":
        return random.choice(quadrants)

    if mode == "no_bumpers":
        candidates = [q for q in quadrants if not q.has_bumpers]
        return random.choice(candidates)

    if mode == "at_least_one_bumper":
        return random.choice(quadrants)

    raise ValueError("Modo inválido")

def build_random_board(mode="random", seed=None):

    if seed is not None:
        random.seed(seed)

    q_green = choose_quadrant(GREEN_QUADRANTS, mode)
    q_blue = choose_quadrant(BLUE_QUADRANTS, mode)
    q_red = choose_quadrant(RED_QUADRANTS, mode)
    q_yellow = choose_quadrant(YELLOW_QUADRANTS, mode)

    quadrants = [q_green, q_blue, q_red, q_yellow]

    if mode == "at_least_one_bumper":
        if not any(q.has_bumpers for q in quadrants):

            # elegir uno al azar
            index = random.randint(0, 3)

            color_lists = [
                GREEN_QUADRANTS,
                BLUE_QUADRANTS,
                RED_QUADRANTS,
                YELLOW_QUADRANTS
            ]

            factories = color_lists[index]

            bumper_quadrants = [
                f() for f in factories if f().has_bumpers
            ]

            quadrants[index] = random.choice(bumper_quadrants)

    random.shuffle(quadrants)

    q_tl = quadrants[0].rotate(1)
    q_tr = quadrants[1].rotate(2)
    q_bl = quadrants[2].rotate(0)
    q_br = quadrants[3].rotate(3)

    return assemble_board(q_tl, q_tr, q_bl, q_br)