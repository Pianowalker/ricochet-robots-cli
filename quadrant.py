class Quadrant:
    def __init__(self, color, variant, has_bumpers=False):
        self.color = color
        self.variant = variant
        self.has_bumpers = has_bumpers
        self.walls = set()
        self.targets = []
        self.bumpers = []

    def add_wall(self, cell1, cell2):
        self.walls.add(frozenset({cell1, cell2}))

    def add_target(self, color, symbol, position):
        self.targets.append((color, symbol, position))