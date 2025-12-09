import pygame


class Menu:
    """
    Главное меню игры 2048:
    - Start Game
    - Settings
    - Quit
    """

    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()

        # Шрифты
        self.font_title = pygame.font.SysFont("Arial", 60, bold=True)
        self.font_button = pygame.font.SysFont("Arial", 36)

        # Кнопки меню
        self.buttons = {
            "start": pygame.Rect(self.width // 2 - 150, 280, 300, 70),
            "settings": pygame.Rect(self.width // 2 - 150, 380, 300, 70),
            "quit": pygame.Rect(self.width // 2 - 150, 480, 300, 70)
        }

    def draw(self):
        """Отрисовка экрана меню."""
        self.screen.fill((250, 248, 239))

        # Заголовок
        title_surf = self.font_title.render("2048", True, (60, 58, 50))
        title_rect = title_surf.get_rect(center=(self.width // 2, 150))
        self.screen.blit(title_surf, title_rect)

        # Отрисовка кнопок
        for key, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (187, 173, 160), rect, border_radius=8)

            # Названия кнопок
            if key == "start":
                label = "Start Game"
            elif key == "settings":
                label = "Settings"
            else:
                label = "Quit"

            text_surf = self.font_button.render(label, True, (255, 255, 255))
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    def handle_mouse(self, pos):
        """Проверка нажатий мыши по кнопкам."""
        if self.buttons["start"].collidepoint(pos):
            return "start"
        elif self.buttons["settings"].collidepoint(pos):
            return "settings"
        elif self.buttons["quit"].collidepoint(pos):
            return "quit"
        return None