"""
Elementos de interfaz: botones, etiquetas, paneles.
Muestra: Round, Score, Moves declared, Moves used, Current target.
Botones: Start game, Select mode, Declare moves, Next round.
"""
import pygame

# Identificadores de botones
BTN_PLAY = "play"
BTN_RULES = "rules"
BTN_CONTROLS = "controls"
BTN_EXIT = "exit"
BTN_MODE_RANDOM = "mode_random"
BTN_MODE_NO_BUMPERS = "mode_no_bumpers"
BTN_MODE_AT_LEAST_ONE = "mode_at_least_one"
BTN_DECLARE_MOVES = "declare_moves"
BTN_NEXT_ROUND = "next_round"
BTN_BACK = "back"
BTN_GAME_MODE_MATCH = "game_mode_match"
BTN_GAME_MODE_PRACTICE = "game_mode_practice"
BTN_NEXT_PUZZLE = "next_puzzle"
BTN_RESET_PUZZLE = "reset_puzzle"
BTN_TOGGLE_EASY = "toggle_easy"
BTN_ABANDON = "abandon"
BTN_TUTORIAL = "tutorial"
BTN_TUTORIAL_CONTINUE = "tutorial_continue"
BTN_TUTORIAL_MENU = "tutorial_menu"

# Colores
COLOR_BTN = (80, 90, 120)
COLOR_BTN_HOVER = (100, 110, 150)
COLOR_BTN_TEXT = (240, 240, 250)
COLOR_LABEL = (200, 200, 220)
COLOR_BG_PANEL = (45, 48, 60)


def draw_button(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    rect: pygame.Rect,
    hover: bool = False,
) -> None:
    """Dibuja un botón con texto."""
    color = COLOR_BTN_HOVER if hover else COLOR_BTN
    pygame.draw.rect(surface, color, rect, border_radius=6)
    pygame.draw.rect(surface, (120, 130, 160), rect, 2, border_radius=6)
    txt = font.render(text, True, COLOR_BTN_TEXT)
    tx = rect.centerx - txt.get_width() // 2
    ty = rect.centery - txt.get_height() // 2
    surface.blit(txt, (tx, ty))


def draw_menu_buttons(
    surface: pygame.Surface,
    font: pygame.font.Font,
    mouse_pos: tuple[int, int],
) -> dict[str, pygame.Rect]:
    """Dibuja botones del menú principal. Devuelve {id: Rect} para detectar clics."""
    w, h = surface.get_size()
    cx = w // 2
    start_y = 200
    step = 48
    buttons = {}
    labels = [
        (BTN_PLAY, "Jugar"),
        (BTN_TUTORIAL, "Tutorial"),
        (BTN_CONTROLS, "Controles"),
        (BTN_RULES, "Reglas"),
        (BTN_EXIT, "Salir"),
    ]
    for i, (bid, label) in enumerate(labels):
        rect = pygame.Rect(cx - 100, start_y + i * step, 200, 40)
        buttons[bid] = rect
        draw_button(surface, font, label, rect, rect.collidepoint(mouse_pos))
    return buttons


def draw_mode_buttons(
    surface: pygame.Surface,
    font: pygame.font.Font,
    mouse_pos: tuple[int, int],
    rounds_input_str: str = "",
    show_rounds: bool = True,
    easy_mode: bool = False,
) -> dict[str, pygame.Rect]:
    """Dibuja botones de selección de modo de mapa y campo para escribir cantidad de rondas."""
    w, h = surface.get_size()
    cx = w // 2
    start_y = 180
    step = 44
    labels = [
        (BTN_MODE_RANDOM, "Aleatorio"),
        (BTN_MODE_NO_BUMPERS, "Sin bumpers"),
        (BTN_MODE_AT_LEAST_ONE, "Al menos un bumper"),
    ]
    buttons = {}
    for i, (bid, label) in enumerate(labels):
        rect = pygame.Rect(cx - 140, start_y + i * step, 280, 38)
        buttons[bid] = rect
        draw_button(surface, font, label, rect, rect.collidepoint(mouse_pos))
    if show_rounds:
        rnd_y = start_y + 3 * step + 16
        label1 = font.render("Rondas a jugar (mín 1, máx 10):", True, COLOR_LABEL)
        surface.blit(label1, (cx - 200, rnd_y))
        input_rect = pygame.Rect(cx - 140, rnd_y + 28, 120, 32)
        pygame.draw.rect(surface, (55, 58, 72), input_rect, border_radius=6)
        pygame.draw.rect(surface, (140, 150, 180), input_rect, 2, border_radius=6)
        txt = font.render(rounds_input_str + "_", True, (240, 240, 250))
        surface.blit(txt, (input_rect.x + 8, input_rect.centery - txt.get_height() // 2))
    # Toggle modo fácil (5 robots con gris)
    easy_y = start_y + 3 * step + (80 if show_rounds else 16)
    easy_label = "Modo facil (5 robots): ON" if easy_mode else "Modo facil (5 robots): OFF"
    easy_color = (80, 140, 80) if easy_mode else COLOR_BTN
    easy_rect = pygame.Rect(cx - 140, easy_y, 280, 38)
    pygame.draw.rect(surface, easy_color, easy_rect, border_radius=6)
    pygame.draw.rect(surface, (120, 130, 160), easy_rect, 2, border_radius=6)
    easy_txt = font.render(easy_label, True, COLOR_BTN_TEXT)
    surface.blit(easy_txt, (easy_rect.centerx - easy_txt.get_width() // 2,
                             easy_rect.centery - easy_txt.get_height() // 2))
    buttons[BTN_TOGGLE_EASY] = easy_rect
    return buttons


def draw_game_mode_select_buttons(
    surface: pygame.Surface,
    font: pygame.font.Font,
    mouse_pos: tuple[int, int],
) -> dict[str, pygame.Rect]:
    """Pantalla intermedia: elegir entre Partida y Práctica."""
    w, h = surface.get_size()
    cx = w // 2
    start_y = 200
    step = 48
    buttons = {}
    labels = [
        (BTN_GAME_MODE_MATCH, "Partida"),
        (BTN_GAME_MODE_PRACTICE, "Practica"),
        (BTN_BACK, "Volver"),
    ]
    for i, (bid, label) in enumerate(labels):
        rect = pygame.Rect(cx - 100, start_y + i * step, 200, 40)
        buttons[bid] = rect
        draw_button(surface, font, label, rect, rect.collidepoint(mouse_pos))
    return buttons


def draw_practice_buttons(
    surface: pygame.Surface,
    font: pygame.font.Font,
    mouse_pos: tuple[int, int],
    ui_x: int,
    ui_y: int,
) -> dict[str, pygame.Rect]:
    """Botones del panel lateral en modo práctica."""
    buttons = {}
    by = ui_y + 180
    labels = [
        (BTN_RESET_PUZZLE, "Reiniciar"),
        (BTN_NEXT_PUZZLE, "Siguiente puzzle"),
    ]
    for bid, label in labels:
        rect = pygame.Rect(ui_x, by, 180, 36)
        buttons[bid] = rect
        draw_button(surface, font, label, rect, rect.collidepoint(mouse_pos))
        by += 50
    rect_abandon = pygame.Rect(ui_x, by + 10, 180, 36)
    buttons[BTN_ABANDON] = rect_abandon
    hover_abandon = rect_abandon.collidepoint(mouse_pos)
    pygame.draw.rect(surface, (130, 50, 50) if hover_abandon else (100, 40, 40), rect_abandon, border_radius=6)
    pygame.draw.rect(surface, (180, 80, 80), rect_abandon, 2, border_radius=6)
    txt = font.render("Abandonar", True, (240, 200, 200))
    surface.blit(txt, (rect_abandon.centerx - txt.get_width() // 2, rect_abandon.centery - txt.get_height() // 2))
    return buttons


def draw_playing_buttons(
    surface: pygame.Surface,
    font: pygame.font.Font,
    mouse_pos: tuple[int, int],
    can_declare: bool,
    can_next_round: bool,
    ui_x: int,
    ui_y: int,
    show_declare_button: bool = True,
    highlight_declare: bool = False,
) -> dict[str, pygame.Rect]:
    """Botones durante la partida. show_declare_button=False oculta el botón Declarar (ya declarado).
    highlight_declare=True destaca el botón Declarar movidas al comienzo de ronda."""
    buttons = {}
    by = ui_y + 180
    if show_declare_button:
        rect_declare = pygame.Rect(ui_x, by, 180, 36)
        buttons[BTN_DECLARE_MOVES] = rect_declare
        if highlight_declare:
            highlight_rect = rect_declare.inflate(8, 8)
            pygame.draw.rect(surface, (90, 120, 160), highlight_rect, border_radius=8)
            pygame.draw.rect(surface, (160, 200, 255), highlight_rect, 2, border_radius=8)
        draw_button(surface, font, "Declarar movidas", rect_declare, rect_declare.collidepoint(mouse_pos) and can_declare)
        by += 50
    rect_next = pygame.Rect(ui_x, by, 180, 36)
    buttons[BTN_NEXT_ROUND] = rect_next
    draw_button(surface, font, "Siguiente ronda", rect_next, rect_next.collidepoint(mouse_pos) and can_next_round)
    by += 60
    rect_abandon = pygame.Rect(ui_x, by, 180, 36)
    buttons[BTN_ABANDON] = rect_abandon
    hover_abandon = rect_abandon.collidepoint(mouse_pos)
    pygame.draw.rect(surface, (130, 50, 50) if hover_abandon else (100, 40, 40), rect_abandon, border_radius=6)
    pygame.draw.rect(surface, (180, 80, 80), rect_abandon, 2, border_radius=6)
    txt = font.render("Abandonar", True, (240, 200, 200))
    surface.blit(txt, (rect_abandon.centerx - txt.get_width() // 2, rect_abandon.centery - txt.get_height() // 2))
    return buttons


def draw_rules_screen(surface: pygame.Surface, font: pygame.font.Font, mouse_pos: tuple[int, int]) -> dict[str, pygame.Rect]:
    """Pantalla de reglas con botón Volver."""
    rules = [
        "Robots: R (rojo), B (azul), G (verde), Y (amarillo).",
        "Modo facil: agrega el robot gris (W), solo sirve de apoyo, nunca es objetivo.",
        "Objetivo: Llevar un robot al simbolo de su mismo color",
        "en la cantidad de movidas que declaras previamente.",
        "Comodin (forma de espiral): cualquier robot de color puede alcanzarlo (no el gris).",
        "Los robots se deslizan hasta una pared, un robot o un borde.",
        "Los resortes (bumpers) (/ \\) reflejan el movimiento.",
        "Puntaje: +1 si acertas exacto; -1 si no.",
    ]
    y = 120
    for line in rules:
        surf = font.render(line, True, COLOR_LABEL)
        surface.blit(surf, (80, y))
        y += 32
    rect = pygame.Rect(surface.get_width() // 2 - 70, y + 20, 140, 40)
    draw_button(surface, font, "Volver", rect, rect.collidepoint(mouse_pos))
    return {BTN_BACK: rect}


def draw_controls_screen(surface: pygame.Surface, font: pygame.font.Font, mouse_pos: tuple[int, int]) -> dict[str, pygame.Rect]:
    """Pantalla de controles (mouse y teclado) con botón Volver."""
    lines = [
        "Controles para mover robots:",
        "",
        "Con el mouse:",
        "  1. Clic en el robot que querés mover.",
        "  2. Flechas del teclado (↑↓←→) para la dirección,",
        "     o un clic en una celda adyacente.",
        "  El robot queda seleccionado hasta que elijas otro.",
        "",
        "Con el teclado:",
        "  R (rojo), B (azul), G (verde), Y (amarillo), W (gris, modo facil)",
        "  para elegir robot, luego flechas (↑↓←→).",
    ]
    y = 100
    for line in lines:
        surf = font.render(line, True, COLOR_LABEL)
        surface.blit(surf, (80, y))
        y += 28
    rect = pygame.Rect(surface.get_width() // 2 - 70, y + 24, 140, 40)
    draw_button(surface, font, "Volver", rect, rect.collidepoint(mouse_pos))
    return {BTN_BACK: rect}


def _draw_wrapped_text(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    x: int,
    y: int,
    max_width: int,
    color: tuple,
) -> int:
    """Dibuja texto con word-wrap respetando \\n. Devuelve el y final."""
    line_h = font.get_height() + 4
    for paragraph in text.split("\n"):
        if paragraph == "":
            y += line_h // 2
            continue
        words = paragraph.split(" ")
        line = ""
        for word in words:
            test = (line + " " + word).strip()
            if font.size(test)[0] <= max_width:
                line = test
            else:
                if line:
                    surface.blit(font.render(line, True, color), (x, y))
                    y += line_h
                line = word
        if line:
            surface.blit(font.render(line, True, color), (x, y))
            y += line_h
    return y


def draw_tutorial_panel(
    surface: pygame.Surface,
    font: pygame.font.Font,
    mouse_pos: tuple[int, int],
    ui_x: int,
    ui_y: int,
    level_num: int,
    total_levels: int,
    instruction: str,
    message: str,
    level_complete: bool,
    tutorial_complete: bool,
) -> dict[str, pygame.Rect]:
    """Panel lateral del tutorial: nivel, instrucción, feedback y botones."""
    buttons = {}
    panel_w = surface.get_width() - ui_x - 10
    text_max_w = panel_w - 4

    y = ui_y

    # Indicador de nivel
    level_surf = font.render(f"Nivel {level_num} / {total_levels}", True, (200, 200, 220))
    surface.blit(level_surf, (ui_x, y))
    y += level_surf.get_height() + 6

    # Separador
    pygame.draw.line(surface, (80, 85, 110), (ui_x, y), (ui_x + panel_w, y), 1)
    y += 10

    if not level_complete:
        # Instrucción activa
        if instruction:
            y = _draw_wrapped_text(surface, font, instruction, ui_x, y, text_max_w, (220, 230, 255))
            y += 8

        # Feedback o error tras un movimiento
        if message:
            is_error = "incorrecto" in message.lower()
            msg_color = (255, 110, 110) if is_error else (160, 230, 160)
            y = _draw_wrapped_text(surface, font, message, ui_x, y, text_max_w, msg_color)
    else:
        # Nivel completado: mostrar feedback
        if message:
            y = _draw_wrapped_text(surface, font, message, ui_x, y, text_max_w, (160, 230, 160))
            y += 16

        # Botón Continuar o Menú principal
        btn_rect = pygame.Rect(ui_x, y, panel_w, 38)
        if tutorial_complete:
            buttons[BTN_TUTORIAL_MENU] = btn_rect
            draw_button(surface, font, "Menu principal", btn_rect, btn_rect.collidepoint(mouse_pos))
        else:
            buttons[BTN_TUTORIAL_CONTINUE] = btn_rect
            draw_button(surface, font, "Continuar", btn_rect, btn_rect.collidepoint(mouse_pos))

    # Botón Abandonar anclado al fondo del panel
    y_abandon = surface.get_height() - 56
    rect_abandon = pygame.Rect(ui_x, y_abandon, panel_w, 36)
    buttons[BTN_ABANDON] = rect_abandon
    hover_abandon = rect_abandon.collidepoint(mouse_pos)
    pygame.draw.rect(
        surface,
        (130, 50, 50) if hover_abandon else (100, 40, 40),
        rect_abandon,
        border_radius=6,
    )
    pygame.draw.rect(surface, (180, 80, 80), rect_abandon, 2, border_radius=6)
    txt = font.render("Abandonar", True, (240, 200, 200))
    surface.blit(txt, (rect_abandon.centerx - txt.get_width() // 2, rect_abandon.centery - txt.get_height() // 2))

    return buttons


def get_button_at(buttons: dict[str, pygame.Rect], pos: tuple[int, int]) -> str | None:
    """Devuelve el id del botón bajo pos, o None."""
    for bid, rect in buttons.items():
        if rect.collidepoint(pos):
            return bid
    return None
