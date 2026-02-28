class Quadrant:
    def __init__(self, color, variant, size=8, has_bumpers=False):
        self.color = color
        self.variant = variant
        self.size = size
        self.has_bumpers = has_bumpers
        self.walls = set()
        self.targets = []
        self.bumpers = []

    def add_wall(self, cell1, cell2):
        self.walls.add(frozenset({cell1, cell2}))

    def add_target(self, color, symbol, position):
        self.targets.append((color, symbol, position))

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

        return new_q