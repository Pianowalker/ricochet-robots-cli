"""
Punto de entrada de la GUI de Ricochet Robots.
Inicializa pygame, ventana y game loop.
"""
import pygame
import sys

# Tamaño de ventana: espacio para tablero 800x800 + panel lateral
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 820

from .game_window import GameWindow


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Ricochet Robots")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    try:
        font = pygame.font.SysFont("Segoe UI", 22)
    except Exception:
        pass
    gw = GameWindow(screen, font)
    running = True
    while running:
        events = pygame.event.get()
        running = gw.handle_events(events)
        dt = clock.tick(60) / 1000.0
        gw.update(dt)
        gw.draw()
        pygame.display.flip()
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
