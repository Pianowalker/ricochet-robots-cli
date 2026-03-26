import random


class PracticeSession:
    def __init__(self, game):
        self.game = game
        self.move_count = 0
        self.round_active = False
        self.round_start_positions = {}
        self.remaining_targets = []

    def start_puzzle(self):
        if not self.remaining_targets:
            self.remaining_targets = list(self.game.targets)
        target = random.choice(self.remaining_targets)
        self.game.active_target = target
        self.remaining_targets.remove(target)
        self._save_round_start_positions()
        self.move_count = 0
        self.round_active = True
        return True

    def _save_round_start_positions(self):
        self.round_start_positions = {
            color: robot.position
            for color, robot in self.game.robots.items()
        }

    def reset_puzzle(self):
        for color, position in self.round_start_positions.items():
            self.game.robots[color].position = position
        self.move_count = 0
        self.round_active = True

    def move(self, color, direction):
        if not self.round_active:
            return None, False, "No hay puzzle activo", []
        position, won, illegal, waypoints = self.game.move(color, direction)
        if illegal:
            return position, False, "Movimiento ilegal: no se puede terminar en un bumper", []
        self.move_count += 1
        if won:
            self.round_active = False
            return position, True, "Objetivo alcanzado!", waypoints
        return position, False, "", waypoints
