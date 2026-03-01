class Robot:
    def __init__(self, color, position):
        self.color = color
        self.position = position


class Target:
    def __init__(self, color, symbol, position):
        self.color = color        # "R", "B", etc o None para comodín
        self.symbol = symbol      # "planet", "moon", etc
        self.position = position

class Bumper:
    def __init__(self, position, diagonal, color):
        self.position = position
        self.diagonal = diagonal   # "/" o "\\"
        self.color = color         # "R", "G", "B", "Y"