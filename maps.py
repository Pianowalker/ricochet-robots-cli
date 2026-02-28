def load_quadrant_A(game):

    # Targets
    game.add_target("Y", "cross",  (1,3))
    game.add_target("R", "moon",   (3,1))
    game.add_target("B", "planet", (4,6))
    game.add_target("G", "sun",    (6,3))

    # Amarillo
    game.add_wall((0,3),(1,3))
    game.add_wall((1,3),(1,4))

    # Rojo
    game.add_wall((3,1),(4,1))
    game.add_wall((3,0),(3,1))

    # Azul
    game.add_wall((4,6),(5,6))
    game.add_wall((4,6),(4,7))

    # Verde
    game.add_wall((6,2),(6,3))
    game.add_wall((5,3),(6,3))

    # Pared adicional izquierda inferior
    game.add_wall((5,0),(6,0))

    # Pared inferior derecha
    game.add_wall((7,5),(7,6))

    # Hueco central
    game.add_wall((0,6),(0,7))
    game.add_wall((0,7),(1,7))