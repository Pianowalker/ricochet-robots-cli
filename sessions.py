import random

class SinglePlayerSession:
    def __init__(self, game, total_rounds=5):
        self.game = game
        self.total_rounds = total_rounds

        self.current_round = 0
        self.score = 0

        self.declared_moves = None
        self.move_count = 0
        self.round_active = False

        self.round_start_positions = {}

        self.remaining_targets = []

    # ----------------------------
    # RONDAS
    # ----------------------------

    def start_new_round(self):
        if self.current_round == 0:
            if len(self.game.targets) < self.total_rounds:
                raise ValueError(
                    "Cantidad de targets menor que cantidad de rondas."
                )
            self.remaining_targets = list(self.game.targets)
        if self.current_round >= self.total_rounds:
            return False  # no más rondas

        self.current_round += 1
        self.declared_moves = None
        self.move_count = 0
        self.round_active = True

        if not self.remaining_targets:
            self.remaining_targets = list(self.game.targets)
        target = random.choice(self.remaining_targets)
        self.game.active_target = target
        self.remaining_targets.remove(target)

        self._save_round_start_positions()

        return True

    def _save_round_start_positions(self):
        self.round_start_positions = {
            color: robot.position
            for color, robot in self.game.robots.items()
        }

    def _reset_to_round_start(self):
        for color, position in self.round_start_positions.items():
            self.game.robots[color].position = position

    # ----------------------------
    # DECLARACIÓN
    # ----------------------------

    def declare_solution(self, moves):
        self.declared_moves = moves

    # ----------------------------
    # MOVIMIENTO
    # ----------------------------

    def move(self, color, direction):
        if not self.round_active:
            return None, False, "La ronda no está activa"

        if self.declared_moves is None:
            return None, False, "Primero declarás la cantidad de movidas"

        self.move_count += 1

        position, won = self.game.move(color, direction)

        # Excedió lo declarado
        if self.move_count > self.declared_moves:
            self.score -= 1
            self._reset_to_round_start()
            self.round_active = False
            return position, False, "Excediste la cantidad declarada. Punto -1"

        # Ganó
        if won:
            if self.move_count == self.declared_moves:
                self.score += 1
                result = "✔ Exacto. Punto +1"
            else:
                self.score -= 1
                result = "Llegaste pero no en la cantidad exacta. Punto -1"

            self.round_active = False
            return position, True, result

        return position, False, "Movimiento realizado"