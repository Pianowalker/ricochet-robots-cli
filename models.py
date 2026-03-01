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
        self.diagonal = diagonal
        self.color = color

    def reflect(self, direction, robot_color):

        # Si el robot es del mismo color → no rebota
        if robot_color == self.color:
            return direction

        if self.diagonal == "/":
            mapping = {
                "right": "up",
                "up": "right",
                "left": "down",
                "down": "left"
            }
        else:  # "\"
            mapping = {
                "right": "down",
                "down": "right",
                "left": "up",
                "up": "left"
            }

        return mapping[direction]
    
    def __str__(self):
        return self.diagonal