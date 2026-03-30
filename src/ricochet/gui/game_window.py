"""
Ventana principal del juego: estados y flujo.
Pantallas: MENU, MODE_SELECT, PLAYING, ROUND_END, GAME_END.
Usa el dominio sin modificarlo: Game, SinglePlayerSession, build_random_board.
"""
import pygame
from ricochet.domain.game import Game
from ricochet.domain.sessions.single_player_session import SinglePlayerSession
from ricochet.domain.sessions.practice_session import PracticeSession
from ricochet.domain.maps import build_random_board

from .renderer import (
    draw_board,
    draw_walls,
    draw_targets,
    draw_robots,
    draw_bumpers,
    draw_ui,
    BOARD_PIXEL_WIDTH,
    BOARD_PIXEL_HEIGHT,
    CELL_SIZE,
)
from .input_handler import InputHandler
from .animation import RobotAnimation
from . import sounds
from . import ui

# Estados de pantalla
MENU = "menu"
GAME_MODE_SELECT = "game_mode_select"
MODE_SELECT = "mode_select"
PLAYING = "playing"
ROUND_END = "round_end"
GAME_END = "game_end"
RULES = "rules"
CONTROLS = "controls"
PRACTICE = "practice"

# Modos para build_random_board
MODE_MAP = {
    "random": "random",
    "no_bumpers": "no_bumpers",
    "at_least_one_bumper": "at_least_one_bumper",
}


class GameWindow:
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font):
        self.screen = screen
        self.font = font
        self.state = MENU
        self.game: Game | None = None
        self.session: SinglePlayerSession | None = None
        self.mode: str = "random"
        self.board_offset_x = 0
        self.board_offset_y = 0
        self.input_handler = InputHandler(0, 0)
        self.active_animation: RobotAnimation | None = None
        self.round_end_message: str = ""
        self.buttons: dict = {}
        self.declaring_moves = False
        self.declare_input_str = ""
        self.total_rounds = 5
        self.rounds_input_str = ""
        self.round_end_timer: float = 0.0
        self.practice_session: PracticeSession | None = None
        self._is_practice_mode: bool = False
        self.practice_message: str = ""
        self.easy_mode: bool = False

    def _start_game(self):
        """Crea Game y Session según el modo elegido."""
        self.game = build_random_board(mode=self.mode)
        colors = ["red", "green", "blue", "yellow"]
        if self.easy_mode:
            colors = colors + ["gray"]
        self.game.place_robots_randomly(colors)
        max_rounds = min(10, len(self.game.targets) if self.game.targets else 10)
        try:
            n = max(1, min(10, int(self.rounds_input_str.strip() or "1")))
        except ValueError:
            n = 5
        self.total_rounds = min(n, max_rounds)
        self.session = SinglePlayerSession(self.game, total_rounds=self.total_rounds)
        self.state = PLAYING
        self.declaring_moves = False
        self.declare_input_str = ""
        started = self.session.start_new_round()
        if not started:
            self.state = GAME_END
        self.input_handler.clear_selection()

    def _start_practice(self):
        """Crea Game y PracticeSession para el modo práctica."""
        self.game = build_random_board(mode=self.mode)
        colors = ["red", "green", "blue", "yellow"]
        if self.easy_mode:
            colors = colors + ["gray"]
        self.game.place_robots_randomly(colors)
        self.session = None
        self.practice_session = PracticeSession(self.game)
        self.practice_session.start_puzzle()
        self.state = PRACTICE
        self.practice_message = ""
        self.input_handler.clear_selection()

    def _abandon_to_menu(self):
        """Abandona la partida o práctica activa y vuelve al menú."""
        self.session = None
        self.practice_session = None
        self.practice_message = ""
        self.active_animation = None
        self.input_handler.clear_selection()
        self.state = MENU

    def _get_target_text(self) -> str:
        if not self.session or not self.session.game.active_target:
            return "-"
        t = self.session.game.active_target
        if t.color is None:
            return "Comodín (*)"
        return t.color.capitalize()

    def handle_events(self, events: list) -> bool:
        """Procesa eventos. Devuelve False si hay que salir (Exit)."""
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.state in (RULES, CONTROLS, GAME_MODE_SELECT):
                    self.state = MENU
                elif self.state in (PLAYING, PRACTICE, ROUND_END):
                    if self.declaring_moves:
                        self.declaring_moves = False
                    else:
                        self._abandon_to_menu()
                else:
                    return False

        if self.state == MENU:
            for e in events:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    bid = ui.get_button_at(self.buttons, e.pos)
                    if bid == ui.BTN_EXIT:
                        return False
                    if bid == ui.BTN_PLAY:
                        self.state = GAME_MODE_SELECT
                        sounds.play(sounds.SOUND_BUTTON_CLICK)
                    if bid == ui.BTN_RULES:
                        self.state = RULES
                        sounds.play(sounds.SOUND_BUTTON_CLICK)
                    if bid == ui.BTN_CONTROLS:
                        self.state = CONTROLS
                        sounds.play(sounds.SOUND_BUTTON_CLICK)

        elif self.state == GAME_MODE_SELECT:
            for e in events:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    bid = ui.get_button_at(self.buttons, e.pos)
                    if bid == ui.BTN_GAME_MODE_MATCH:
                        self._is_practice_mode = False
                        self.state = MODE_SELECT
                        sounds.play(sounds.SOUND_BUTTON_CLICK)
                    elif bid == ui.BTN_GAME_MODE_PRACTICE:
                        self._is_practice_mode = True
                        self.state = MODE_SELECT
                        sounds.play(sounds.SOUND_BUTTON_CLICK)
                    elif bid == ui.BTN_BACK:
                        self.state = MENU
                        sounds.play(sounds.SOUND_BUTTON_CLICK)

        elif self.state == RULES:
            for e in events:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if ui.get_button_at(self.buttons, e.pos) == ui.BTN_BACK:
                        self.state = MENU
                        sounds.play(sounds.SOUND_BUTTON_CLICK)

        elif self.state == CONTROLS:
            for e in events:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if ui.get_button_at(self.buttons, e.pos) == ui.BTN_BACK:
                        self.state = MENU
                        sounds.play(sounds.SOUND_BUTTON_CLICK)

        elif self.state == MODE_SELECT:
            for e in events:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_BACKSPACE:
                        self.rounds_input_str = self.rounds_input_str[:-1]
                    elif e.unicode.isdigit() and len(self.rounds_input_str) < 3:
                        self.rounds_input_str += e.unicode
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    bid = ui.get_button_at(self.buttons, e.pos)
                    if bid == ui.BTN_MODE_RANDOM:
                        self.mode = "random"
                        self._start_practice() if self._is_practice_mode else self._start_game()
                        sounds.play(sounds.SOUND_BUTTON_CLICK)
                    elif bid == ui.BTN_MODE_NO_BUMPERS:
                        self.mode = "no_bumpers"
                        self._start_practice() if self._is_practice_mode else self._start_game()
                        sounds.play(sounds.SOUND_BUTTON_CLICK)
                    elif bid == ui.BTN_MODE_AT_LEAST_ONE:
                        self.mode = "at_least_one_bumper"
                        self._start_practice() if self._is_practice_mode else self._start_game()
                        sounds.play(sounds.SOUND_BUTTON_CLICK)
                    elif bid == ui.BTN_TOGGLE_EASY:
                        self.easy_mode = not self.easy_mode
                        sounds.play(sounds.SOUND_BUTTON_CLICK)

        elif self.state == PLAYING and self.session and self.game:
            if self.declaring_moves:
                for e in events:
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER:
                            try:
                                n = int(self.declare_input_str or "0")
                                if n > 0:
                                    self.session.declare_solution(n)
                                    self.declaring_moves = False
                                    sounds.play(sounds.SOUND_BUTTON_CLICK)
                            except ValueError:
                                pass
                        elif e.key == pygame.K_BACKSPACE:
                            self.declare_input_str = self.declare_input_str[:-1]
                        elif e.unicode.isdigit():
                            self.declare_input_str += e.unicode
                            if len(self.declare_input_str) > 3:
                                self.declare_input_str = self.declare_input_str[:3]
            else:
                actions = self.input_handler.process_events(events, self.game.robots)
                for action in actions:
                    if action[0] == "move" and len(action) == 3:
                        _, color, direction = action
                        if not self.session.round_active or self.session.declared_moves is None:
                            continue
                        if self.active_animation:
                            continue
                        from_pos = self.game.robots[color].position
                        position, won, message, waypoints = self.session.move(color, direction)
                        to_pos = position
                        illegal = "ilegal" in message.lower() or "bumper" in message.lower()
                        if illegal:
                            sounds.play(sounds.SOUND_BUMPER_HIT)
                        elif from_pos != to_pos:
                            self.active_animation = RobotAnimation(color, from_pos, to_pos, waypoints)
                            sounds.play(sounds.SOUND_ROBOT_MOVE)
                        if not self.session.round_active:
                            self.round_end_message = message
                            self.round_end_timer = 0.0
                            if "Exacto" in message or "Punto +1" in message:
                                sounds.play(sounds.SOUND_WIN_ROUND)
                            else:
                                sounds.play(sounds.SOUND_LOSE_ROUND)
                            self.state = ROUND_END
                for e in events:
                    if e.type == pygame.KEYDOWN:
                        if (e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER) and self.session.declared_moves is None and self.session.round_active:
                            self.declaring_moves = True
                            self.declare_input_str = ""
                            sounds.play(sounds.SOUND_BUTTON_CLICK)
                    if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                        bid = ui.get_button_at(self.buttons, e.pos)
                        if bid == ui.BTN_DECLARE_MOVES and self.session.declared_moves is None and self.session.round_active:
                            self.declaring_moves = True
                            self.declare_input_str = ""
                            sounds.play(sounds.SOUND_BUTTON_CLICK)
                        elif bid == ui.BTN_ABANDON:
                            self._abandon_to_menu()

        elif self.state == PRACTICE and self.practice_session and self.game:
            actions = self.input_handler.process_events(events, self.game.robots)
            for action in actions:
                if action[0] == "move" and len(action) == 3:
                    _, color, direction = action
                    if not self.practice_session.round_active or self.active_animation:
                        continue
                    from_pos = self.game.robots[color].position
                    position, won, message, waypoints = self.practice_session.move(color, direction)
                    to_pos = position
                    if "ilegal" in message.lower() or "bumper" in message.lower():
                        sounds.play(sounds.SOUND_BUMPER_HIT)
                    elif from_pos != to_pos:
                        self.active_animation = RobotAnimation(color, from_pos, to_pos, waypoints)
                        sounds.play(sounds.SOUND_ROBOT_MOVE)
                    if won:
                        self.practice_message = "Objetivo alcanzado!"
                        sounds.play(sounds.SOUND_WIN_ROUND)
            for e in events:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    bid = ui.get_button_at(self.buttons, e.pos)
                    if bid == ui.BTN_NEXT_PUZZLE:
                        self.practice_session.start_puzzle()
                        self.practice_message = ""
                        self.input_handler.clear_selection()
                        sounds.play(sounds.SOUND_BUTTON_CLICK)
                    elif bid == ui.BTN_RESET_PUZZLE:
                        self.practice_session.reset_puzzle()
                        self.practice_message = ""
                        self.input_handler.clear_selection()
                        sounds.play(sounds.SOUND_BUTTON_CLICK)
                    elif bid == ui.BTN_ABANDON:
                        self._abandon_to_menu()

        elif self.state == ROUND_END:
            for e in events:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    bid = ui.get_button_at(self.buttons, e.pos)
                    if bid == ui.BTN_NEXT_ROUND:
                        self._advance_from_round_end()
                        sounds.play(sounds.SOUND_BUTTON_CLICK)

        elif self.state == GAME_END:
            for e in events:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    self.state = MENU
                    self.game = None
                    self.session = None

        return True

    def _advance_from_round_end(self):
        """Pasa a la siguiente ronda o a fin de partida."""
        started = self.session.start_new_round()
        self.round_end_message = ""
        self.round_end_timer = 0.0
        if started:
            self.state = PLAYING
        else:
            self.state = GAME_END

    def update(self, dt: float):
        """Actualiza animaciones y avance automático de ronda."""
        if self.active_animation:
            if self.active_animation.update(dt):
                self.active_animation = None
        if self.state == ROUND_END and self.session:
            self.round_end_timer += dt
            if self.round_end_timer >= 2.0:
                self._advance_from_round_end()

    def draw(self):
        """Dibuja la pantalla actual."""
        self.screen.fill((30, 32, 42))
        mouse_pos = pygame.mouse.get_pos()

        if self.state == MENU:
            title = self.font.render("Ricochet Robots", True, (240, 240, 250))
            r = title.get_rect(center=(self.screen.get_width() // 2, 120))
            self.screen.blit(title, r)
            self.buttons = ui.draw_menu_buttons(self.screen, self.font, mouse_pos)

        elif self.state == GAME_MODE_SELECT:
            title = self.font.render("Elegir tipo de juego", True, (240, 240, 250))
            r = title.get_rect(center=(self.screen.get_width() // 2, 120))
            self.screen.blit(title, r)
            self.buttons = ui.draw_game_mode_select_buttons(self.screen, self.font, mouse_pos)

        elif self.state == RULES:
            title = self.font.render("Reglas", True, (240, 240, 250))
            self.screen.blit(title, (80, 60))
            self.buttons = ui.draw_rules_screen(self.screen, self.font, mouse_pos)

        elif self.state == CONTROLS:
            title = self.font.render("Controles", True, (240, 240, 250))
            self.screen.blit(title, (80, 60))
            self.buttons = ui.draw_controls_screen(self.screen, self.font, mouse_pos)

        elif self.state == MODE_SELECT:
            title = self.font.render("Elegir modo de mapa", True, (240, 240, 250))
            r = title.get_rect(center=(self.screen.get_width() // 2, 120))
            self.screen.blit(title, r)
            self.buttons = ui.draw_mode_buttons(
                self.screen, self.font, mouse_pos,
                rounds_input_str=self.rounds_input_str,
                show_rounds=not self._is_practice_mode,
                easy_mode=self.easy_mode,
            )

        elif self.state == PLAYING and self.game and self.session:
            self.board_offset_x = 0
            self.board_offset_y = 0
            self.input_handler.set_board_offset(self.board_offset_x, self.board_offset_y)
            draw_board(self.screen, self.board_offset_x, self.board_offset_y)
            draw_walls(self.screen, self.game.walls, self.board_offset_x, self.board_offset_y)
            draw_targets(
                self.screen, self.game.targets, self.game.active_target,
                self.board_offset_x, self.board_offset_y,
            )
            draw_bumpers(self.screen, self.game.bumpers, self.board_offset_x, self.board_offset_y)
            robot_pixel_override = None
            if self.active_animation:
                px, py = self.active_animation.get_current_pixel_position()
                robot_pixel_override = {self.active_animation.color: (px, py)}
            draw_robots(
                self.screen, self.game.robots,
                self.board_offset_x, self.board_offset_y,
                robot_pixel_override=robot_pixel_override,
                selected_color=self.input_handler.get_selected_robot(),
            )
            ui_x = self.board_offset_x + BOARD_PIXEL_WIDTH + 20
            ui_y = 20
            draw_ui(
                self.screen, self.font,
                self.session.current_round, self.session.total_rounds,
                self.session.score,
                self.session.declared_moves, self.session.move_count,
                active_target=self.game.active_target,
                offset_x=ui_x, offset_y=ui_y,
            )
            if self.declaring_moves:
                self.buttons = {}
                # Destacar la consulta de movidas (fondo y texto)
                prompt_rect = pygame.Rect(ui_x - 8, ui_y + 192, 220, 52)
                pygame.draw.rect(self.screen, (70, 75, 95), prompt_rect, border_radius=8)
                pygame.draw.rect(self.screen, (140, 180, 220), prompt_rect, 2, border_radius=8)
                prompt = self.font.render("¿Cuántas movidas? (Enter para confirmar)", True, (255, 255, 255))
                self.screen.blit(prompt, (ui_x, ui_y + 200))
                inp = self.font.render(self.declare_input_str + "_", True, (255, 255, 255))
                self.screen.blit(inp, (ui_x, ui_y + 235))
            else:
                show_declare = self.session.declared_moves is None
                need_highlight = show_declare and self.session.round_active
                self.buttons = ui.draw_playing_buttons(
                    self.screen, self.font, mouse_pos,
                    can_declare=self.session.round_active and show_declare,
                    can_next_round=False,
                    ui_x=ui_x, ui_y=120,
                    show_declare_button=show_declare,
                    highlight_declare=need_highlight,
                )

        elif self.state == ROUND_END and self.session:
            draw_board(self.screen, self.board_offset_x, self.board_offset_y)
            draw_walls(self.screen, self.game.walls, self.board_offset_x, self.board_offset_y)
            draw_targets(
                self.screen, self.game.targets, self.game.active_target,
                self.board_offset_x, self.board_offset_y,
            )
            draw_bumpers(self.screen, self.game.bumpers, self.board_offset_x, self.board_offset_y)
            ro = None
            if self.active_animation:
                px, py = self.active_animation.get_current_pixel_position()
                ro = {self.active_animation.color: (px, py)}
            draw_robots(
                self.screen, self.game.robots,
                self.board_offset_x, self.board_offset_y,
                robot_pixel_override=ro,
                selected_color=self.input_handler.get_selected_robot(),
            )
            ui_x = self.board_offset_x + BOARD_PIXEL_WIDTH + 20
            draw_ui(
                self.screen, self.font,
                self.session.current_round, self.session.total_rounds,
                self.session.score,
                self.session.declared_moves, self.session.move_count,
                active_target=self.game.active_target,
                offset_x=ui_x, offset_y=20,
            )
            self.buttons = ui.draw_playing_buttons(
                self.screen, self.font, mouse_pos,
                can_declare=False, can_next_round=True,
                ui_x=ui_x, ui_y=120,
                show_declare_button=False,
            )
            # Panel flotante centrado sobre el tablero
            panel_w, panel_h = 460, 110
            panel_x = self.board_offset_x + (BOARD_PIXEL_WIDTH - panel_w) // 2
            panel_y = self.board_offset_y + (BOARD_PIXEL_HEIGHT - panel_h) // 2
            panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
            panel_surf.fill((20, 22, 32, 210))
            self.screen.blit(panel_surf, (panel_x, panel_y))
            pygame.draw.rect(self.screen, (140, 160, 200), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=8)
            msg = self.font.render(self.round_end_message[:60], True, (255, 240, 200))
            msg_r = msg.get_rect(centerx=panel_x + panel_w // 2, top=panel_y + 20)
            self.screen.blit(msg, msg_r)
            remaining = max(0, 2.0 - self.round_end_timer)
            auto_msg = self.font.render(f"Siguiente ronda en {remaining:.1f}s  (o clic en botón)", True, (160, 175, 200))
            auto_r = auto_msg.get_rect(centerx=panel_x + panel_w // 2, top=panel_y + 62)
            self.screen.blit(auto_msg, auto_r)

        elif self.state == PRACTICE and self.practice_session and self.game:
            self.board_offset_x = 0
            self.board_offset_y = 0
            self.input_handler.set_board_offset(self.board_offset_x, self.board_offset_y)
            draw_board(self.screen, self.board_offset_x, self.board_offset_y)
            draw_walls(self.screen, self.game.walls, self.board_offset_x, self.board_offset_y)
            draw_targets(
                self.screen, self.game.targets, self.game.active_target,
                self.board_offset_x, self.board_offset_y,
            )
            draw_bumpers(self.screen, self.game.bumpers, self.board_offset_x, self.board_offset_y)
            robot_pixel_override = None
            if self.active_animation:
                px, py = self.active_animation.get_current_pixel_position()
                robot_pixel_override = {self.active_animation.color: (px, py)}
            draw_robots(
                self.screen, self.game.robots,
                self.board_offset_x, self.board_offset_y,
                robot_pixel_override=robot_pixel_override,
                selected_color=self.input_handler.get_selected_robot(),
            )
            ui_x = self.board_offset_x + BOARD_PIXEL_WIDTH + 20
            ui_y = 20
            color_text = (220, 220, 230)
            move_surf = self.font.render(f"Movidas: {self.practice_session.move_count}", True, color_text)
            self.screen.blit(move_surf, (ui_x, ui_y))
            if self.game.active_target:
                if self.game.active_target.color is None:
                    target_label = "Objetivo: Comodin"
                else:
                    target_label = f"Objetivo: {self.game.active_target.color.capitalize()}"
                t_surf = self.font.render(target_label, True, color_text)
                self.screen.blit(t_surf, (ui_x, ui_y + 30))
            self.buttons = ui.draw_practice_buttons(
                self.screen, self.font, mouse_pos, ui_x=ui_x, ui_y=ui_y,
            )
            if self.practice_message:
                panel_w, panel_h = 360, 70
                panel_x = self.board_offset_x + (BOARD_PIXEL_WIDTH - panel_w) // 2
                panel_y = self.board_offset_y + (BOARD_PIXEL_HEIGHT - panel_h) // 2
                panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
                panel_surf.fill((20, 22, 32, 210))
                self.screen.blit(panel_surf, (panel_x, panel_y))
                pygame.draw.rect(self.screen, (100, 210, 100), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=8)
                msg = self.font.render(self.practice_message, True, (120, 240, 120))
                msg_r = msg.get_rect(centerx=panel_x + panel_w // 2, centery=panel_y + panel_h // 2)
                self.screen.blit(msg, msg_r)

        elif self.state == GAME_END and self.session:
            title = self.font.render("Partida terminada", True, (240, 240, 250))
            r = title.get_rect(center=(self.screen.get_width() // 2, 200))
            self.screen.blit(title, r)
            score_txt = self.font.render(f"Score final: {self.session.score}", True, (200, 200, 220))
            r2 = score_txt.get_rect(center=(self.screen.get_width() // 2, 260))
            self.screen.blit(score_txt, r2)
            if self.session.score > 0:
                result_text, result_color = "Resultado: Victoria", (120, 220, 120)
            elif self.session.score < 0:
                result_text, result_color = "Resultado: Derrota", (220, 100, 100)
            else:
                result_text, result_color = "Resultado: Empate", (200, 200, 150)
            result_surf = self.font.render(result_text, True, result_color)
            r_res = result_surf.get_rect(center=(self.screen.get_width() // 2, 300))
            self.screen.blit(result_surf, r_res)
            click = self.font.render("Clic para volver al menú", True, (180, 180, 200))
            r3 = click.get_rect(center=(self.screen.get_width() // 2, 360))
            self.screen.blit(click, r3)
