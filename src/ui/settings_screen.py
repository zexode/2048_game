import pygame


class SettingsScreen:
    """
    Экран настроек.
    - выбор размера поля
    - выбор темы
    """

    def __init__(self, screen, settings_manager):
        self.screen = screen
        self.settings = settings_manager
        self.w, self.h = screen.get_size()

        self.font_title = pygame.font.SysFont("Arial", 48, bold=True)
        self.font_option = pygame.font.SysFont("Arial", 32)
        self.font_back = pygame.font.SysFont("Arial", 28)

        # Кнопки выбора размера поля (3, 4, 5)
        self.buttons_board = {
            3: pygame.Rect(self.w // 2 - 150, 230, 90, 60),
            4: pygame.Rect(self.w // 2 - 45, 230, 90, 60),
            5: pygame.Rect(self.w // 2 + 60, 230, 90, 60),
        }

        # Кнопки выбора темы
        self.buttons_theme = {
            "light": pygame.Rect(self.w // 2 - 150, 330, 150, 60),
            "dark": pygame.Rect(self.w // 2 + 10, 330, 150, 60),
        }

        # Back Button
        self.back_button = pygame.Rect(20, 20, 100, 40)

    def draw(self):
        self.screen.fill((240, 235, 225))

        # Заголовок
        title = self.font_title.render("Settings", True, (60, 58, 50))
        self.screen.blit(title, (self.w // 2 - title.get_width() // 2, 120))

        # --- Board size label ---
        board_label = self.font_option.render("Board Size:", True, (50, 50, 50))
        self.screen.blit(board_label, (self.w // 2 - 110, 190))

        # Board buttons
        for size, rect in self.buttons_board.items():
            color = (187, 173, 160)
            if self.settings.board_size == size:
                color = (246, 124, 95)  # highlight
            pygame.draw.rect(self.screen, color, rect, border_radius=8)

            text = self.font_option.render(str(size), True, (255, 255, 255))
            self.screen.blit(text, text.get_rect(center=rect.center))

        # --- Theme label ---
        theme_label = self.font_option.render("Theme:", True, (50, 50, 50))
        self.screen.blit(theme_label, (self.w // 2 - 60, 300))

        # Theme buttons
        for theme, rect in self.buttons_theme.items():
            color = (187, 173, 160)
            if self.settings.theme == theme:
                color = (246, 124, 95)
            pygame.draw.rect(self.screen, color, rect, border_radius=8)

            text = self.font_option.render(theme.capitalize(), True, (255, 255, 255))
            self.screen.blit(text, text.get_rect(center=rect.center))

        # Back
        pygame.draw.rect(self.screen, (120, 110, 100), self.back_button, border_radius=8)
        text = self.font_back.render("Back", True, (255, 255, 255))
        self.screen.blit(text, text.get_rect(center=self.back_button.center))

    def handle_mouse(self, pos):
        # change board size
        for size, rect in self.buttons_board.items():
            if rect.collidepoint(pos):
                self.settings.set_board_size(size)
                return "refresh_game"

        # change theme
        for theme, rect in self.buttons_theme.items():
            if rect.collidepoint(pos):
                self.settings.set_theme(theme)
                return "refresh_theme"

        # go back
        if self.back_button.collidepoint(pos):
            return "menu"

        return None