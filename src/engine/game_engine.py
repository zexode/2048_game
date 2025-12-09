import pygame

from src.config.config_manager import ConfigManager
from src.config.settings_manager import SettingsManager

from src.game.board import Board

from src.engine.renderer import Renderer

from src.ui.menu import Menu
from src.ui.settings_screen import SettingsScreen
from src.ui.game_over import GameOverScreen


class GameEngine:
    """
    Главное ядро игры.
    Состояния:
    - MENU (главное меню)
    - SETTINGS (экран настроек)
    - GAME (игра)
    - GAME_OVER (проигрыш)
    """

    def __init__(self, config_path="src/config/game_config.json"):
        pygame.init()

        # Конфиги
        self.config = ConfigManager(config_path)
        self.settings_manager = SettingsManager()

        # Окно
        self.window_size = (600, 700)
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("2048")

        # Сцены
        self.menu = Menu(self.screen)
        self.settings_screen = SettingsScreen(self.screen, self.settings_manager)
        self.game_over_screen = GameOverScreen(self.screen)

        # Логика Board + Renderer будут заменяться при apply_settings()
        self.board = None
        self.renderer = None
        self.apply_settings()

        # Состояние
        self.state = "MENU"
        self.running = True

    # ======================================================
    # Применение настроек (board size, theme)
    # ======================================================

    def apply_settings(self):
        """Пересоздаёт Board и Renderer при изменении настроек."""
        size = self.settings_manager.board_size
        theme = self.settings_manager.theme  # пока не используем, позже добавим цветовые темы

        # Создаём новую логику игры
        self.board = Board(
            size=size,
            target_value=self.config.target_value,
            new_tile_values=self.config.new_tile_values,
            new_tile_probabilities=self.config.new_tile_probabilities,
        )

        # Создаём новый Renderer
        self.renderer = Renderer(
            self.screen,
            self.board,
            theme=self.settings_manager.theme
        )

    # ======================================================
    # Обработка событий
    # ======================================================

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            # ------------------- MENU -------------------
            if self.state == "MENU":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    action = self.menu.handle_mouse(event.pos)

                    if action == "start":
                        self.apply_settings()
                        self.start_game()

                    elif action == "settings":
                        self.state = "SETTINGS"

                    elif action == "quit":
                        self.running = False

            # ------------------- SETTINGS -------------------
            elif self.state == "SETTINGS":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    action = self.settings_screen.handle_mouse(event.pos)

                    if action == "menu":
                        self.state = "MENU"

                    elif action in ("refresh_game", "refresh_theme"):
                        self.apply_settings()

            # ------------------- GAME -------------------
            elif self.state == "GAME":

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "MENU"

                    moves = {
                        pygame.K_LEFT: "left",
                        pygame.K_RIGHT: "right",
                        pygame.K_UP: "up",
                        pygame.K_DOWN: "down",
                    }

                    if event.key in moves:
                        moved, gained, won, lost = self.board.move(moves[event.key])

                        if moved:
                            # Запускаем анимацию "поп" плиток
                            self.renderer.start_move_animation()

                        if lost:
                            self.state = "GAME_OVER"

            # ------------------- GAME OVER -------------------
            elif self.state == "GAME_OVER":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    action = self.game_over_screen.handle_mouse(event.pos)

                    if action == "restart":
                        self.start_game()

                    elif action == "menu":
                        self.state = "MENU"

    # ======================================================
    # Управление состояниями
    # ======================================================

    def start_game(self):
        """Начать новую игру."""
        self.board.reset(initial_tiles=self.config.initial_tiles)
        self.state = "GAME"

    # ======================================================
    # Главный цикл
    # ======================================================

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            dt = clock.tick(60) / 1000.0  # дельта времени (секунды)

            self.handle_events()

            # Анимации
            self.renderer.update(dt)

            # Рендер экранов
            if self.state == "MENU":
                self.menu.draw()

            elif self.state == "SETTINGS":
                self.settings_screen.draw()

            elif self.state == "GAME":
                self.renderer.draw()

            elif self.state == "GAME_OVER":
                self.renderer.draw()
                self.game_over_screen.draw()

            pygame.display.flip()

        pygame.quit()