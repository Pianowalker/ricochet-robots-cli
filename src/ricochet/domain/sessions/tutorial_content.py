from pathlib import Path

from .tutorial_session import TutorialLevel, TutorialStep

_PUZZLE_DIR = (
    Path(__file__).parent.parent.parent / "backend" / "app" / "data" / "puzzles" / "tutorial"
)


def _parse_move(move_str: str) -> tuple[str, str]:
    """'YELLOW_LEFT' → ('yellow', 'left')"""
    color, direction = move_str.split("_", 1)
    return (color.lower(), direction.lower())


TUTORIAL_LEVELS = [
    TutorialLevel(
        puzzle_path=_PUZZLE_DIR / "nivel_1.json",
        steps=[
            TutorialStep(
                instruction="Mové el robot amarillo hacia la izquierda hasta el objetivo.",
                valid_moves=[_parse_move("YELLOW_LEFT")],
                feedback="Bien hecho.\n\nSolo el robot del mismo color que el objetivo puede alcanzarlo.",
            ),
        ],
    ),
    TutorialLevel(
        puzzle_path=_PUZZLE_DIR / "nivel_2.json",
        steps=[
            TutorialStep(
                instruction="Mové el robot azul hacia la derecha.",
                valid_moves=[_parse_move("BLUE_RIGHT")],
                feedback="Como habrás notado, el robot no se detiene cuando querés. Sigue moviéndose hasta chocar con una pared u otro robot.",
            ),
            TutorialStep(
                instruction="Ahora movelo hacia arriba para llegar al objetivo.",
                valid_moves=[_parse_move("BLUE_UP")],
                feedback="¡Bien!\n\nPodés usar las paredes para frenar los robots exactamente donde lo necesitás.",
            ),
        ],
    ),
    TutorialLevel(
        puzzle_path=_PUZZLE_DIR / "nivel_3.json",
        steps=[
            TutorialStep(
                instruction="Mové el robot rojo hacia la izquierda.",
                valid_moves=[_parse_move("RED_LEFT")],
                feedback="Perfecto.\n\nEse robot ahora quedó en una posición útil.",
            ),
            TutorialStep(
                instruction="Ahora mové el robot verde hacia arriba.",
                valid_moves=[_parse_move("GREEN_UP")],
                feedback="¿Notaste que el robot verde se detuvo al chocar con el rojo?",
            ),
            TutorialStep(
                instruction="Ahora movelo hacia la derecha para llegar al objetivo.",
                valid_moves=[_parse_move("GREEN_RIGHT")],
                feedback="¡Muy bien!\n\nLos robots pueden usarse como obstáculos para frenar a otros.",
            ),
        ],
    ),
    TutorialLevel(
        puzzle_path=_PUZZLE_DIR / "nivel_4.json",
        steps=[
            TutorialStep(
                instruction="Mové el robot amarillo para despejar el camino.",
                valid_moves=[_parse_move("YELLOW_LEFT"), _parse_move("YELLOW_RIGHT")],
                feedback="Bien.\n\nA veces hay que mover otros robots para abrir el paso.",
            ),
            TutorialStep(
                instruction="Ahora mové el robot rojo hacia abajo para llegar al objetivo.",
                valid_moves=[_parse_move("RED_DOWN")],
                feedback="¡Excelente!\n\nNo siempre el camino está libre. A veces hay que quitar obstáculos.",
            ),
        ],
    ),
    TutorialLevel(
        puzzle_path=_PUZZLE_DIR / "nivel_5.json",
        steps=[
            TutorialStep(
                instruction="Mové el robot azul hacia la izquierda.",
                valid_moves=[_parse_move("BLUE_LEFT")],
                feedback="¿Notaste lo que pasó?\n\nEl robot rebotó al tocar la barra verde y cambió de dirección.",
            ),
            TutorialStep(
                instruction="Las barras hacen rebotar a los robots cuando las tocan si no comparten color con el robot.\n\nAhora mové el robot azul hacia la derecha para llegar al objetivo.",
                valid_moves=[_parse_move("BLUE_RIGHT")],
                feedback="¡Muy bien!\n\nPodés usar los rebotes para alcanzar lugares que no están en línea recta.",
            ),
        ],
    ),
    TutorialLevel(
        puzzle_path=_PUZZLE_DIR / "nivel_6.json",
        steps=[
            TutorialStep(
                instruction="Mové el robot azul hacia arriba.",
                valid_moves=[_parse_move("BLUE_UP")],
                feedback="¿Notaste lo que pasó?\n\nEl robot atravesó la barra azul sin rebotar.\n\nCuando el robot y la barra tienen el mismo color, no hay rebote.",
            ),
            TutorialStep(
                instruction="Ahora movelo hacia la izquierda.",
                valid_moves=[_parse_move("BLUE_LEFT")],
                feedback="Bien.\n\nEl robot se detuvo al chocar con otro robot.",
            ),
            TutorialStep(
                instruction="Ahora movelo hacia abajo.",
                valid_moves=[_parse_move("BLUE_DOWN")],
                feedback="Perfecto.\n\nEl rebote cambió la dirección del movimiento.",
            ),
            TutorialStep(
                instruction="Ahora movelo hacia arriba para llegar al objetivo.",
                valid_moves=[_parse_move("BLUE_UP")],
                feedback="¡Excelente!\n\nAhora conocés todas las reglas del juego.\n\nPodés usar paredes, robots y rebotes para resolver cualquier puzzle.",
            ),
        ],
    ),
]
