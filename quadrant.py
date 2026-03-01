from models import Bumper

class Quadrant:
    def __init__(self, color, variant, size=8, has_bumpers=False):
        self.color = color
        self.variant = variant
        self.size = size
        self.has_bumpers = has_bumpers
        self.walls = set()
        self.targets = []
        self.bumpers = []
        self.border_walls = set()

    def add_wall(self, cell1, cell2):
        self.walls.add(frozenset({cell1, cell2}))

    # Agrega paredes que están entre este cuadrante y otro
    def add_border_wall(self, cell, side):
        """
        side: "up", "down", "left", "right"
        """
        if side not in {"up", "down", "left", "right"}:
            raise ValueError("Side inválido")

        self.border_walls.add((cell, side))

    def add_target(self, color, symbol, position):
        self.targets.append((color, symbol, position))

    def add_bumper(self, position, diagonal, color):

        if diagonal not in {"/", "\\"}:
            raise ValueError("Diagonal inválida")

        self.bumpers.append(Bumper(position, diagonal, color))

    def rotate_90(self):

        new_q = Quadrant(
        color=self.color,
        variant=self.variant,
        size=self.size,
        has_bumpers=self.has_bumpers
    )

        size = self.size

        # Rotar walls
        for wall in self.walls:
            cell1, cell2 = tuple(wall)

            r1, c1 = cell1
            r2, c2 = cell2

            new_cell1 = (c1, size - 1 - r1)
            new_cell2 = (c2, size - 1 - r2)

            new_q.add_wall(new_cell1, new_cell2)

        # Rotar targets
        for color, symbol, position in self.targets:
            r, c = position
            new_position = (c, size - 1 - r)
            new_q.add_target(color, symbol, new_position)

                # Rotar border_walls
        for (r, c), side in self.border_walls:

            new_r = c
            new_c = size - 1 - r

            side_rotation = {
                "up": "right",
                "right": "down",
                "down": "left",
                "left": "up"
            }

            new_side = side_rotation[side]

            new_q.add_border_wall((new_r, new_c), new_side)

        # Rotar bumpers
        for bumper in self.bumpers:

            r, c = bumper.position

            new_r = c
            new_c = size - 1 - r

            if bumper.diagonal == "/":
                new_diagonal = "\\"
            else:
                new_diagonal = "/"

            new_q.add_bumper(
                (new_r, new_c),
                new_diagonal,
                bumper.color
            )

            # Al rotar 90°, las diagonales se invierten
            if bumper.diagonal == "/":
                new_diagonal = "\\"
            else:
                new_diagonal = "/"

            new_q.add_bumper((new_r, new_c), new_diagonal)

        return new_q
    
    def rotate(self, times=1):

        times = times % 4  # evitar rotaciones innecesarias

        result = self
        for _ in range(times):
            result = result.rotate_90()

        return result