import random
from quadrant import Quadrant
from game import Game

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
]

BLUE_QUADRANTS = [
    create_blue_quadrant_v1,
]

RED_QUADRANTS = [
    create_red_quadrant_v4,
]

YELLOW_QUADRANTS = [
    create_yellow_quadrant_v1,
    create_yellow_quadrant_v2
]

def build_random_board():

    q_green = random.choice(GREEN_QUADRANTS)()
    q_blue = random.choice(BLUE_QUADRANTS)()
    q_red = random.choice(RED_QUADRANTS)()
    q_yellow = random.choice(YELLOW_QUADRANTS)()

    quadrants = [q_green, q_blue, q_red, q_yellow]

    random.shuffle(quadrants)

    q_tl = quadrants[0].rotate(1)
    q_tr = quadrants[1].rotate(2)
    q_bl = quadrants[2].rotate(0)
    q_br = quadrants[3].rotate(3)

    return assemble_board(q_tl, q_tr, q_bl, q_br)