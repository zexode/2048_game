import json
import os


class SettingsManager:
    """
    Управляет пользовательскими настройками:
    - размер поля (3x3, 4x4, 5x5)
    - тема оформления (light / dark)
    """

    def __init__(self, path="src/config/settings.json"):
        self.path = path
        self.settings = {}

        self.load()

    def load(self):
        """Загрузить настройки из файла или создать новый."""
        if not os.path.exists(self.path):
            self.settings = {
                "board_size": 4,
                "theme": "light"
            }
            self.save()
            return

        with open(self.path, "r", encoding="utf-8") as f:
            self.settings = json.load(f)

    def save(self):
        """Сохранить текущие настройки."""
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)

    # =============== GETTERS ==================
    @property
    def board_size(self):
        return self.settings.get("board_size", 4)

    @property
    def theme(self):
        return self.settings.get("theme", "light")

    # =============== SETTERS ==================
    def set_board_size(self, size):
        self.settings["board_size"] = size
        self.save()

    def set_theme(self, theme):
        self.settings["theme"] = theme
        self.save()