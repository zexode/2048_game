import math
import pygame
from src.ui.hud import HUD


class Renderer:
    """
    Отвечает за визуализацию игры и анимации.
    Поддерживает темы: light и dark.
    """

    # ------- Цветовые схемы -------- #

    LIGHT_THEME = {
        "bg": (250, 248, 239),
        "board": (187, 173, 160),
        "cell": (205, 193, 180),
        "tile_colors": {
            0: (205, 193, 180),
            2: (238, 228, 218),
            4: (237, 224, 200),
            8: (242, 177, 121),
            16: (245, 149, 99),
            32: (246, 124, 95),
            64: (246, 94, 59),
            128: (237, 207, 114),
            256: (237, 204, 97),
            512: (237, 200, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 46),
        }
    }

    DARK_THEME = {
        "bg": (40, 40, 40),
        "board": (60, 60, 60),
        "cell": (90, 90, 90),
        "tile_colors": {
            0: (90, 90, 90),
            2: (120, 120, 140),
            4: (140, 120, 120),
            8: (150, 100, 100),
            16: (170, 80, 80),
            32: (200, 80, 80),
            64: (220, 70, 70),
            128: (200, 160, 80),
            256: (210, 180, 80),
            512: (220, 200, 80),
            1024: (230, 210, 80),
            2048: (240, 220, 80),
        }
    }

    def __init__(self, screen, board, theme="light"):
        self.screen = screen
        self.board = board

        self.theme_name = theme
        self.theme = Renderer.LIGHT_THEME if theme == "light" else Renderer.DARK_THEME

        self.width, self.height = screen.get_size()

        self.board_area = pygame.Rect(50, 150, 500, 500)
        self.tile_size = self.board_area.width // self.board.size

        self.font = pygame.font.SysFont("Arial", 40, bold=True)
        self.hud = HUD(self.screen, self.board)

        self.animating = False
        self.animation_time = 0.0
        self.animation_duration = 0.15

    # ---------- Themes ---------- #

    def set_theme(self, theme):
        self.theme_name = theme
        self.theme = Renderer.LIGHT_THEME if theme == "light" else Renderer.DARK_THEME

    # ---------- Animation ---------- #

    def start_move_animation(self):
        self.animating = True
        self.animation_time = 0.0

    def update(self, dt):
        if self.animating:
            self.animation_time += dt
            if self.animation_time >= self.animation_duration:
                self.animating = False

    def _scale(self):
        if not self.animating:
            return 1.0
        t = self.animation_time / self.animation_duration
        return 1.0 + 0.08 * math.sin(math.pi * t)

    # ---------- Draw Background ---------- #

    def draw_background(self):
        self.screen.fill(self.theme["bg"])

        pygame.draw.rect(self.screen, self.theme["board"],
                         self.board_area, border_radius=10)

        for r in range(self.board.size):
            for c in range(self.board.size):
                x = self.board_area.left + c * self.tile_size + 5
                y = self.board_area.top + r * self.tile_size + 5
                rect = pygame.Rect(x, y, self.tile_size - 10, self.tile_size - 10)
                pygame.draw.rect(self.screen, self.theme["cell"], rect, border_radius=8)

    # ---------- Draw Tiles ---------- #

    def draw_tiles(self):
        s = self._scale()

        for r in range(self.board.size):
            for c in range(self.board.size):
                val = self.board.grid[r][c]
                base = self.tile_size - 10
                tsize = int(base * s)
                dx = (base - tsize) // 2
                dy = (base - tsize) // 2

                x = self.board_area.left + c * self.tile_size + 5 + dx
                y = self.board_area.top + r * self.tile_size + 5 + dy

                rect = pygame.Rect(x, y, tsize, tsize)

                color = self.theme["tile_colors"].get(val, (100, 80, 50))
                pygame.draw.rect(self.screen, color, rect, border_radius=8)

                if val != 0:
                    text = self.font.render(str(val), True, (255, 255, 255))
                    self.screen.blit(text, text.get_rect(center=rect.center))

    # ---------- Full Draw ---------- #

    def draw(self):
        self.draw_background()
        self.draw_tiles()
        self.hud.draw()