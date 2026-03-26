"""
Animación del movimiento de robots.
El robot se desliza celda por celda hasta la posición final.
"""
import pygame
from .renderer import CELL_SIZE, cell_to_pixel

# Tiempo por celda (segundos)
DURATION_PER_CELL = 0.06


class RobotAnimation:
    """Animación de un robot moviéndose desde una celda inicial hasta la final."""

    def __init__(
        self,
        color: str,
        from_cell: tuple[int, int],
        to_cell: tuple[int, int],
        waypoints: list[tuple[int, int]] | None = None,
    ):
        self.color = color
        self.from_cell = from_cell
        self.to_cell = to_cell
        if waypoints and len(waypoints) >= 2:
            self.trajectory = waypoints
        else:
            self.trajectory = _build_trajectory(from_cell, to_cell)
        self.duration_total = DURATION_PER_CELL * max(1, len(self.trajectory) - 1)
        self.elapsed = 0.0

    def update(self, dt: float) -> bool:
        """Actualiza la animación. Devuelve True si ya terminó."""
        self.elapsed += dt
        return self.elapsed >= self.duration_total

    def get_current_pixel_position(self) -> tuple[float, float]:
        """Devuelve (px, py) en coordenadas del tablero (0..800) para dibujar el robot."""
        if not self.trajectory:
            return cell_to_pixel(self.to_cell[0], self.to_cell[1])
        if self.elapsed >= self.duration_total:
            r, c = self.trajectory[-1]
            return cell_to_pixel(r, c)
        t = self.elapsed / self.duration_total if self.duration_total > 0 else 1.0
        n = len(self.trajectory) - 1
        segment = min(int(t * n), n - 1) if n > 0 else 0
        local_t = (t * n - segment) if n > 0 else 1.0
        r0, c0 = self.trajectory[segment]
        r1, c1 = self.trajectory[segment + 1]
        x0, y0 = cell_to_pixel(r0, c0)
        x1, y1 = cell_to_pixel(r1, c1)
        px = x0 + (x1 - x0) * local_t
        py = y0 + (y1 - y0) * local_t
        return (px, py)


def _build_trajectory(from_cell: tuple[int, int], to_cell: tuple[int, int]) -> list[tuple[int, int]]:
    """Construye la lista de celdas desde from_cell hasta to_cell (incluida)."""
    r0, c0 = from_cell
    r1, c1 = to_cell
    if (r0, c0) == (r1, c1):
        return [from_cell]
    dr = 1 if r1 > r0 else (-1 if r1 < r0 else 0)
    dc = 1 if c1 > c0 else (-1 if c1 < c0 else 0)
    path = []
    r, c = r0, c0
    while (r, c) != (r1, c1):
        path.append((r, c))
        r += dr
        c += dc
    path.append((r1, c1))
    return path
