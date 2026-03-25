"""
Manejo de entrada: teclado y mouse.
Soporta tres sistemas de control:
1) Click en robot + flechas
2) Tecla R/B/G/Y + flechas
3) Click en robot + click en dirección (celda adyacente)
"""
import pygame
from .renderer import CELL_SIZE, BOARD_PIXEL_WIDTH, BOARD_PIXEL_HEIGHT

# Mapeo tecla letra -> color del dominio
KEY_TO_COLOR = {
    pygame.K_r: "red",
    pygame.K_b: "blue",
    pygame.K_g: "green",
    pygame.K_y: "yellow",
}

ARROW_TO_DIRECTION = {
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right",
}


def pixel_to_cell(px: int, py: int, offset_x: int = 0, offset_y: int = 0) -> tuple[int, int] | None:
    """Convierte coordenadas de pantalla a (row, col). None si fuera del tablero."""
    x = px - offset_x
    y = py - offset_y
    if not (0 <= x < BOARD_PIXEL_WIDTH and 0 <= y < BOARD_PIXEL_HEIGHT):
        return None
    col = x // CELL_SIZE
    row = y // CELL_SIZE
    return (row, col)


def get_direction_from_cells(from_cell: tuple[int, int], to_cell: tuple[int, int]) -> str | None:
    """Si to_cell está en una dirección cardinal respecto a from_cell, devuelve 'up'/'down'/'left'/'right'. Si no, None."""
    r0, c0 = from_cell
    r1, c1 = to_cell
    dr = r1 - r0
    dc = c1 - c0
    if dr == 0 and dc == 0:
        return None
    if abs(dr) >= abs(dc):
        return "down" if dr > 0 else "up"
    return "right" if dc > 0 else "left"


class InputHandler:
    """Agrupa estado de entrada y procesa eventos."""

    def __init__(self, board_offset_x: int = 0, board_offset_y: int = 0):
        self.board_offset_x = board_offset_x
        self.board_offset_y = board_offset_y
        self.selected_robot_color: str | None = None
        self.pending_click_for_direction = False
        self._pending_key_robot: str | None = None

    def set_board_offset(self, x: int, y: int):
        self.board_offset_x = x
        self.board_offset_y = y

    def process_events(
        self,
        events: list[pygame.event.Event],
        robots: dict,
    ) -> list[tuple]:
        """
        Procesa eventos y devuelve lista de acciones.
        Acciones: ("move", color, direction), ("select_robot", color), ("deselect",).
        """
        actions = []
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Control 2: R/B/G/Y + flecha (tecla letra guarda color para la siguiente flecha)
                if event.key in KEY_TO_COLOR:
                    self._pending_key_robot = KEY_TO_COLOR[event.key]
                    self.selected_robot_color = self._pending_key_robot
                    continue
                if event.key in ARROW_TO_DIRECTION:
                    direction = ARROW_TO_DIRECTION[event.key]
                    # Si hay robot seleccionado (Control 1) o pendiente de tecla (Control 2)
                    color = self._pending_key_robot or self.selected_robot_color
                    if color and color in robots:
                        actions.append(("move", color, direction))
                        self.selected_robot_color = color  # mantener selección para movidas siguientes
                    self._pending_key_robot = None
                    continue
                self._pending_key_robot = None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cell = pixel_to_cell(
                    event.pos[0], event.pos[1],
                    self.board_offset_x, self.board_offset_y,
                )
                if cell is None:
                    # No deseleccionar: la selección se mantiene hasta elegir otro robot
                    continue
                row, col = cell
                robot_here = None
                for color, robot in robots.items():
                    if robot.position == (row, col):
                        robot_here = color
                        break
                if robot_here and robot_here != self.selected_robot_color:
                    # Click sobre otro robot: cambiar selección
                    self.selected_robot_color = robot_here
                    self.pending_click_for_direction = True
                elif self.pending_click_for_direction and self.selected_robot_color and self.selected_robot_color in robots:
                    # Click en celda vacía con robot seleccionado: mover en esa dirección
                    from_cell = robots[self.selected_robot_color].position
                    direction = get_direction_from_cells(from_cell, (row, col))
                    if direction:
                        actions.append(("move", self.selected_robot_color, direction))
                    # Mantener pending para poder seguir moviendo sin re-seleccionar
                elif robot_here:
                    # Primer click sobre un robot sin selección previa
                    self.selected_robot_color = robot_here
                    self.pending_click_for_direction = True
                # Clic en celda vacía sin selección: no hacer nada

        return actions

    def get_selected_robot(self) -> str | None:
        return self.selected_robot_color

    def clear_selection(self):
        self.selected_robot_color = None
        self.pending_click_for_direction = False
