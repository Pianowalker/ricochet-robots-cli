"""
Renderizado del tablero y elementos del juego.
Diseñado para poder reemplazar shapes por sprites en el futuro.
Cada elemento tiene su propia función de dibujo.
"""
import pygame
import math

# Dimensiones del tablero
CELL_SIZE = 50
BOARD_ROWS = 16
BOARD_COLS = 16
BOARD_PIXEL_WIDTH = BOARD_COLS * CELL_SIZE   # 800
BOARD_PIXEL_HEIGHT = BOARD_ROWS * CELL_SIZE  # 800

# Colores (RGB)
COLOR_GRID = (60, 60, 70)
COLOR_GRID_LINE = (80, 80, 90)
COLOR_WALL = (200, 200, 210)  # Gris claro para contrastar con el fondo
COLOR_BG_BOARD = (35, 35, 45)

# Robots: colores sólidos
COLOR_ROBOT = {
    "red": (220, 60, 60),
    "green": (60, 180, 80),
    "blue": (60, 100, 220),
    "yellow": (220, 200, 60),
    "gray": (150, 155, 165),
}

# Targets: mismos colores pero más tenues
COLOR_TARGET = {
    "red": (180, 90, 90),
    "green": (90, 160, 110),
    "blue": (90, 130, 200),
    "yellow": (200, 190, 100),
}
COLOR_TARGET_WILDCARD = (200, 100, 180)  # magenta tenue

# Bumpers
COLOR_BUMPER = (120, 120, 140)
COLOR_BUMPER_LINE = (180, 180, 200)

# Centro de una celda en píxeles (desde esquina superior izquierda del tablero)
def cell_to_pixel(row: int, col: int) -> tuple[int, int]:
    """Devuelve (x, y) del centro de la celda en coordenadas de pantalla del tablero."""
    x = col * CELL_SIZE + CELL_SIZE // 2
    y = row * CELL_SIZE + CELL_SIZE // 2
    return (x, y)


def draw_board(
    surface: pygame.Surface,
    offset_x: int = 0,
    offset_y: int = 0,
    rows: int = BOARD_ROWS,
    cols: int = BOARD_COLS,
    cell_size: int = CELL_SIZE,
) -> None:
    """Dibuja el fondo del tablero y la grilla."""
    pw = cols * cell_size
    ph = rows * cell_size
    rect = pygame.Rect(offset_x, offset_y, pw, ph)
    surface.fill(COLOR_BG_BOARD, rect)
    for r in range(rows + 1):
        y = offset_y + r * cell_size
        pygame.draw.line(surface, COLOR_GRID_LINE, (offset_x, y), (offset_x + pw, y), 1)
    for c in range(cols + 1):
        x = offset_x + c * cell_size
        pygame.draw.line(surface, COLOR_GRID_LINE, (x, offset_y), (x, offset_y + ph), 1)


def draw_walls(
    surface: pygame.Surface,
    walls: set,
    offset_x: int = 0,
    offset_y: int = 0,
    cell_size: int = CELL_SIZE,
) -> None:
    """Dibuja las paredes del juego. walls: set de frozenset({(r1,c1), (r2,c2)}).

    Se usa un rectángulo sólido en lugar de líneas gruesas para que las paredes
    queden perfectamente alineadas a píxeles y se vean nítidas.
    """
    thick = 4
    for wall in walls:
        (r1, c1), (r2, c2) = tuple(wall)
        if r1 == r2:
            # pared vertical entre dos columnas
            col = max(c1, c2)
            x = offset_x + col * cell_size
            y = offset_y + r1 * cell_size
            rect = pygame.Rect(x - thick // 2, y, thick, cell_size)
            surface.fill(COLOR_WALL, rect)
        else:
            # pared horizontal entre dos filas
            row = max(r1, r2)
            x = offset_x + c1 * cell_size
            y = offset_y + row * cell_size
            rect = pygame.Rect(x, y - thick // 2, cell_size, thick)
            surface.fill(COLOR_WALL, rect)


def _draw_spiral(
    surface: pygame.Surface,
    px: int,
    py: int,
    radius: int,
    color: tuple[int, int, int],
    width: int = 0,
) -> None:
    """Dibuja una espiral (comodín)."""
    points = []
    turns = 2.5
    steps = 60
    line_w = width if width > 0 else 2
    for i in range(steps + 1):
        t = (i / steps) * turns * 2 * math.pi
        r = (radius * 0.15) + (radius * 0.85 * i / steps)
        x = px + int(r * math.cos(t))
        y = py + int(r * math.sin(t))
        points.append((x, y))
    if len(points) >= 2:
        pygame.draw.lines(surface, color, False, points, line_w)


def _draw_target_shape(
    surface: pygame.Surface,
    px: int,
    py: int,
    symbol: str,
    color: tuple[int, int, int],
    radius: int,
    width: int = 0,
) -> None:
    """Dibuja un «símbolo» en la posición dada.

    - cross: cruz de líneas.
    - sun: círculo con rayos.
    - planet: círculo con anillo.
    - moon: creciente.
    Cualquier otro valor se dibuja como círculo normal (comodín).
    El parámetro *width* sirve para dibujar sólo el contorno si es mayor que 0.
    """
    if symbol == "cross":
        half = radius
        pygame.draw.line(surface, color, (px - half, py), (px + half, py), width or 3)
        pygame.draw.line(surface, color, (px, py - half), (px, py + half), width or 3)
    elif symbol == "sun":
        # Estrella con puntas tipo sierra (muchas puntas afiladas, bien distinta de los robots)
        points = []
        n_points = 8
        for i in range(n_points * 2):
            angle = (i * (180 / n_points) - 90) * math.pi / 180
            r = radius if i % 2 == 0 else radius * 0.35
            points.append((px + int(r * math.cos(angle)), py + int(r * math.sin(angle))))
        if width == 0:
            pygame.draw.polygon(surface, color, points)
        else:
            pygame.draw.polygon(surface, color, points, width or 2)
    elif symbol == "planet":
        pygame.draw.circle(surface, color, (px, py), radius, width)
        if width == 0:
            ring_rect = pygame.Rect(px - radius * 1.4, py - radius // 3, radius * 2.8, radius * 2 // 3)
            pygame.draw.ellipse(surface, color, ring_rect, 2)
    elif symbol == "moon":
        pygame.draw.circle(surface, color, (px, py), radius, width)
        if width == 0:
            # dibujar un círculo de fondo desplazado para crear un creciente
            offset = radius // 2
            pygame.draw.circle(surface, COLOR_BG_BOARD, (px + offset, py - offset), radius)
    else:
        # Comodín: espiral (2.5 vueltas desde el centro)
        _draw_spiral(surface, px, py, radius, color, width)


def draw_targets(
    surface: pygame.Surface,
    targets: list,
    active_target,
    offset_x: int = 0,
    offset_y: int = 0,
    cell_size: int = CELL_SIZE,
) -> None:
    """Dibuja solo el objetivo activo en el tablero (resaltado con contorno blanco)."""
    if active_target is None:
        return
    target = active_target
    r, c = target.position
    px = offset_x + c * cell_size + cell_size // 2
    py = offset_y + r * cell_size + cell_size // 2
    if target.color is None:
        color = COLOR_TARGET_WILDCARD
    else:
        color = COLOR_TARGET.get(target.color, COLOR_TARGET_WILDCARD)
    radius = cell_size // 3
    _draw_target_shape(surface, px, py, target.symbol, (255, 255, 255), radius + 2, width=2)
    _draw_target_shape(surface, px, py, target.symbol, color, radius)


def _draw_robot_shape(
    surface: pygame.Surface,
    px: float,
    py: float,
    fill: tuple[int, int, int],
    selected: bool,
) -> None:
    """Dibuja un robot con forma humanoide simple usando primitivas de pygame."""
    px, py = int(px), int(py)

    # Versión oscura del color para el cuerpo
    dark = tuple(max(0, ch - 55) for ch in fill)

    # Antena
    pygame.draw.line(surface, (190, 190, 205), (px, py - 17), (px, py - 23), 2)
    pygame.draw.circle(surface, (220, 225, 240), (px, py - 23), 3)

    # Cuerpo (rectángulo redondeado, color oscuro)
    body_rect = pygame.Rect(px - 10, py + 1, 20, 11)
    pygame.draw.rect(surface, dark, body_rect, border_radius=3)
    pygame.draw.rect(surface, (170, 175, 190), body_rect, 1, border_radius=3)

    # Cabeza (rectángulo redondeado, color principal)
    head_rect = pygame.Rect(px - 12, py - 16, 24, 17)
    pygame.draw.rect(surface, fill, head_rect, border_radius=5)

    # Borde de cabeza: blanco grueso si seleccionado, gris fino si no
    border_color = (255, 255, 255) if selected else (190, 195, 210)
    border_w = 3 if selected else 1
    pygame.draw.rect(surface, border_color, head_rect, border_w, border_radius=5)

    # Ojos (blancos con pupila oscura)
    for ex in (px - 5, px + 5):
        ey = py - 10
        pygame.draw.circle(surface, (235, 240, 255), (ex, ey), 3)
        pygame.draw.circle(surface, (15, 15, 25), (ex, ey), 1)

    # Boca (línea fina)
    pygame.draw.line(surface, (190, 195, 210), (px - 5, py - 3), (px + 5, py - 3), 1)


def draw_robots(
    surface: pygame.Surface,
    robots: dict,
    offset_x: int = 0,
    offset_y: int = 0,
    robot_override: dict | None = None,
    robot_pixel_override: dict | None = None,
    selected_color: str | None = None,
    cell_size: int = CELL_SIZE,
) -> None:
    """
    Dibuja los robots con forma de robot simple.
    robot_override: opcional {color: (row, col)} para posición en celdas.
    robot_pixel_override: opcional {color: (px, py)} posición en píxeles (para animación).
    selected_color: si se proporciona, ese robot recibe un borde más grueso.
    """
    for color, robot in robots.items():
        if robot_pixel_override and color in robot_pixel_override:
            px, py = robot_pixel_override[color]
            px, py = offset_x + px, offset_y + py
        elif robot_override and color in robot_override:
            r, c = robot_override[color]
            px = offset_x + c * cell_size + cell_size // 2
            py = offset_y + r * cell_size + cell_size // 2
        else:
            r, c = robot.position
            px = offset_x + c * cell_size + cell_size // 2
            py = offset_y + r * cell_size + cell_size // 2
        fill = COLOR_ROBOT.get(color, (150, 150, 150))
        _draw_robot_shape(surface, px, py, fill, selected=(color == selected_color))


def draw_bumpers(
    surface: pygame.Surface,
    bumpers: dict,
    offset_x: int = 0,
    offset_y: int = 0,
    cell_size: int = CELL_SIZE,
) -> None:
    """Dibuja los bumpers como diagonales en la celda, con el color del bumper."""
    for (r, c), bumper in bumpers.items():
        px = offset_x + c * cell_size + cell_size // 2
        py = offset_y + r * cell_size + cell_size // 2
        color = COLOR_ROBOT.get(bumper.color, COLOR_BUMPER_LINE)
        half = cell_size // 2 - 2
        if bumper.diagonal == "/":
            pygame.draw.line(surface, color, (px - half, py + half), (px + half, py - half), 4)
        else:
            pygame.draw.line(surface, color, (px - half, py - half), (px + half, py + half), 4)


def draw_ui(
    surface: pygame.Surface,
    font: pygame.font.Font,
    round_num: int,
    total_rounds: int,
    score: int,
    declared_moves: int | None,
    moves_used: int,
    active_target=None,
    offset_x: int = 0,
    offset_y: int = 0,
) -> None:
    """Dibuja el panel lateral de UI (ronda, puntuación, movidas, objetivo actual).
    Si active_target está definido, se dibuja el objetivo igual que en el tablero."""
    y = offset_y
    line_height = 28
    color_text = (220, 220, 230)
    labels = [
        f"Ronda: {round_num}/{total_rounds}",
        f"Score: {score}",
        f"Declaradas: {declared_moves if declared_moves is not None else '-'}",
        f"Usadas: {moves_used}",
        "Objetivo:",
    ]
    for text in labels:
        surf = font.render(text, True, color_text)
        surface.blit(surf, (offset_x, y))
        y += line_height
    # Objetivo: icono más pequeño y a la derecha; texto indicando qué robot debe llegar
    obj_label_y = y - line_height
    obj_center_x = offset_x + 125
    obj_center_y = obj_label_y + line_height // 2
    if active_target is not None:
        if active_target.color is None:
            color = COLOR_TARGET_WILDCARD
            robot_text = "Cualquier robot"
        else:
            color = COLOR_TARGET.get(active_target.color, COLOR_TARGET_WILDCARD)
            robot_text = {"red": "Rojo", "green": "Verde", "blue": "Azul", "yellow": "Amarillo"}.get(
                active_target.color, active_target.color.capitalize()
            )
            robot_text = f"Llevar: {robot_text}"
        radius_ui = 8
        _draw_target_shape(
            surface, obj_center_x, obj_center_y,
            active_target.symbol, color, radius_ui,
        )
        _draw_target_shape(
            surface, obj_center_x, obj_center_y,
            active_target.symbol, (255, 255, 255), radius_ui + 1, width=2,
        )
        robot_surf = font.render(robot_text, True, (200, 210, 230))
        surface.blit(robot_surf, (offset_x, obj_label_y + line_height + 2))
