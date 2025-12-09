import json
import os
import pygame


class HUD:
    """
    Класс HUD отвечает за отображение:
    - текущего счёта
    - лучшего результата (Best Score)
    """

    def __init__(self, screen, board, highscore_file="highscore.json"):
        self.screen = screen
        self.board = board
        self.highscore_file = highscore_file

        # Шрифты
        self.font_title = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_score = pygame.font.SysFont("Arial", 28, bold=True)

        # Загружаем best score
        self.best_score = self.load_best_score()

    # =====================================================
    # Работа с high score (сохранение JSON файла)
    # =====================================================

    def load_best_score(self) -> int:
        """
        Загружает лучший результат из JSON файла.
        Если файла нет — создаёт пустой.
        """
        if not os.path.exists(self.highscore_file):
            with open(self.highscore_file, "w", encoding="utf-8") as f:
                json.dump({"best_score": 0}, f, indent=4)
            return 0

        try:
            with open(self.highscore_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("best_score", 0)
        except Exception:
            return 0

    def save_best_score(self):
        """
        Если текущий счёт превысил рекорд — обновляем его.
        """
        if self.board.score > self.best_score:
            self.best_score = self.board.score
            with open(self.highscore_file, "w", encoding="utf-8") as f:
                json.dump({"best_score": self.best_score}, f, indent=4)

    # =====================================================
    # Отрисовка HUD
    # =====================================================

    def draw(self):
        """
        Рисует Score и Best Score сверху.
        """

        # Score
        score_text = self.font_score.render(
            f"Score: {self.board.score}",
            True,
            (0, 0, 0)
        )
        self.screen.blit(score_text, (50, 40))

        # Best Score
        best_text = self.font_score.render(
            f"Best: {self.best_score}",
            True,
            (0, 0, 0)
        )
        self.screen.blit(best_text, (350, 40))

        # После каждого кадра проверяем рекорд
        self.save_best_score()