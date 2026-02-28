from models import Robot, Target
import random


class Game:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.walls = set()
        self.robots = {}
        self.targets = []
        self.active_target = None

    def load_quadrant(self, quadrant, offset=(0,0)):

        row_offset, col_offset = offset

        # Walls
        for wall in quadrant.walls:
            cell1, cell2 = tuple(wall)

            r1, c1 = cell1
            r2, c2 = cell2

            self.add_wall(
                (r1 + row_offset, c1 + col_offset),
                (r2 + row_offset, c2 + col_offset)
            )

        # Targets
        for color, symbol, position in quadrant.targets:
            r, c = position
            self.add_target(
                color,
                symbol,
                (r + row_offset, c + col_offset)
            )

    def add_robot(self, color, position):
        self.robots[color] = Robot(color, position)

    def add_wall(self, cell1, cell2):
        # Validar que sean contiguas ortogonalmente
        r1, c1 = cell1
        r2, c2 = cell2

        if not (0 <= r1 < self.height and 0 <= c1 < self.width):
            raise ValueError("cell1 fuera del tablero")

        if not (0 <= r2 < self.height and 0 <= c2 < self.width):
            raise ValueError("cell2 fuera del tablero")

        if abs(r1 - r2) + abs(c1 - c2) != 1:
            raise ValueError("Las celdas no son contiguas")

        self.walls.add(frozenset({cell1, cell2}))

    def add_target(self, color, symbol, position):
        self.targets.append(Target(color, symbol, position))

    def activate_target(self, index):
        self.active_target = self.targets[index]

    def place_robots_randomly(self, colors):

        occupied = set()

        # No pueden empezar sobre targets
        target_positions = {t.position for t in self.targets}

        for color in colors:

            while True:
                r = random.randint(0, self.height - 1)
                c = random.randint(0, self.width - 1)

                position = (r, c)

                # Condiciones de validez
                if (
                    position not in occupied and
                    position not in target_positions
                ):
                    break

            self.add_robot(color, position)
            occupied.add(position)

    def move(self, color, direction):
        robot = self.robots[color]
        r, c = robot.position

        directions = {
            "right": (0, 1),
            "left":  (0, -1),
            "up":    (-1, 0),
            "down":  (1, 0)
        }

        dr, dc = directions[direction]

        while True:
            nr = r + dr
            nc = c + dc

            # 1) borde
            if not (0 <= nr < self.height and 0 <= nc < self.width):
                break

            # 2) pared
            if frozenset({(r, c), (nr, nc)}) in self.walls:
                break

            # 3) otro robot
            if any(other.position == (nr, nc)
                   for other in self.robots.values()
                   if other.color != color):
                break

            # avanzar
            r, c = nr, nc

        robot.position = (r, c)

        won = False

        if self.active_target is not None:
            if robot.position == self.active_target.position:
                if (self.active_target.color is None or
                    robot.color == self.active_target.color):
                    won = True

        return robot.position, won
            
