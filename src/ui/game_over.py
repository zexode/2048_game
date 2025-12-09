import pygame


class GameOverScreen:
    """
    Экран поражения:
    - затемнение фона
    - текст 'Game Over'
    - кнопки Restart и Menu
    """

    def __init__(self, screen):
        self.screen = screen
        self.w, self.h = screen.get_size()

        # Шрифты
        self.font_title = pygame.font.SysFont("Arial", 60, bold=True)
        self.font_button = pygame.font.SysFont("Arial", 36)

        # Кнопки
        self.buttons = {
            "restart": pygame.Rect(self.w // 2 - 150, 350, 300, 70),
            "menu": pygame.Rect(self.w // 2 - 150, 450, 300, 70),
        }

    def draw(self):
        """Рисует затемнение + текст + кнопки"""

        # Тёмная прозрачная подложка
        overlay = pygame.Surface((self.w, self.h))
        overlay.set_alpha(180)  # прозрачность
        overlay.fill((50, 50, 50))
        self.screen.blit(overlay, (0, 0))

        # Текст "Game Over"
        title_surf = self.font_title.render("Game Over", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(self.w // 2, 200))
        self.screen.blit(title_surf, title_rect)

        # Кнопки
        for key, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (187, 173, 160), rect, border_radius=8)
            text_label = "Restart" if key == "restart" else "Menu"
            text_surf = self.font_button.render(text_label, True, (255, 255, 255))
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    def handle_mouse(self, pos):
        """Возвращает действие, если кнопка нажата"""
        if self.buttons["restart"].collidepoint(pos):
            return "restart"
        if self.buttons["menu"].collidepoint(pos):
            return "menu"
        return None