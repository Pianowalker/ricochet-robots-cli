from quadrant import Quadrant

def create_green_quadrant():

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