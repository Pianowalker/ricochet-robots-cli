from dataclasses import dataclass, field
from pathlib import Path

from ricochet.domain.game import Game
from ricochet.domain.puzzle_loader import game_from_puzzle_file


@dataclass
class TutorialStep:
    instruction: str
    valid_moves: list[tuple[str, str]]  # list of (color, direction)
    feedback: str


@dataclass
class TutorialLevel:
    puzzle_path: Path
    steps: list[TutorialStep]


@dataclass
class TutorialMoveResult:
    accepted: bool
    message: str
    waypoints: list
    position: tuple
    level_complete: bool
    tutorial_complete: bool


class TutorialSession:
    def __init__(self, levels: list[TutorialLevel]):
        self.levels = levels
        self.current_level_index = 0
        self.current_step_index = 0
        self.game: Game | None = None
        self._load_level()

    def _load_level(self) -> None:
        level = self.levels[self.current_level_index]
        self.game = game_from_puzzle_file(level.puzzle_path)
        self.current_step_index = 0

    @property
    def current_level(self) -> TutorialLevel:
        return self.levels[self.current_level_index]

    @property
    def current_step(self) -> TutorialStep:
        return self.current_level.steps[self.current_step_index]

    @property
    def current_instruction(self) -> str:
        return self.current_step.instruction

    @property
    def level_number(self) -> int:
        return self.current_level_index + 1

    @property
    def total_levels(self) -> int:
        return len(self.levels)

    @property
    def is_last_level(self) -> bool:
        return self.current_level_index >= len(self.levels) - 1

    def move(self, color: str, direction: str) -> TutorialMoveResult:
        step = self.current_step

        if (color, direction) not in step.valid_moves:
            return TutorialMoveResult(
                accepted=False,
                message="Movimiento incorrecto. Intentalo de nuevo.",
                waypoints=[],
                position=self.game.robots[color].position,
                level_complete=False,
                tutorial_complete=False,
            )

        position, won, illegal, waypoints = self.game.move(color, direction)
        self.current_step_index += 1
        steps = self.current_level.steps

        if self.current_step_index >= len(steps):
            return TutorialMoveResult(
                accepted=True,
                message=step.feedback,
                waypoints=waypoints,
                position=position,
                level_complete=True,
                tutorial_complete=self.is_last_level,
            )

        return TutorialMoveResult(
            accepted=True,
            message=step.feedback,
            waypoints=waypoints,
            position=position,
            level_complete=False,
            tutorial_complete=False,
        )

    def advance_level(self) -> None:
        if not self.is_last_level:
            self.current_level_index += 1
            self._load_level()
