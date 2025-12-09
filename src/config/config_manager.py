import json
import os


class ConfigManager:
    """
    Класс отвечает за загрузку и предоставление настроек игры из JSON-файла.
    В методичке это важный пункт: управление настройками через конфигурационные файлы.
    """

    def __init__(self, config_path: str):
        self.config_path = config_path
        self._config_data = {}
        self.load_config()

    def load_config(self) -> None:
        """Загружает настройки из JSON-файла."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as f:
            self._config_data = json.load(f)

    @property
    def data(self) -> dict:
        """Возвращает полный словарь конфигурации."""
        return self._config_data

    # Удобные геттеры для основных параметров

    @property
    def board_size(self) -> int:
        return int(self._config_data["game"]["board_size"])

    @property
    def target_value(self) -> int:
        return int(self._config_data["game"]["target_value"])

    @property
    def initial_tiles(self) -> int:
        return int(self._config_data["game"]["initial_tiles"])

    @property
    def new_tile_values(self) -> list:
        return list(self._config_data["game"]["new_tile_values"])

    @property
    def new_tile_probabilities(self) -> list:
        return list(self._config_data["game"]["new_tile_probabilities"])

    @property
    def highscore_file(self) -> str:
        return self._config_data["score"]["highscore_file"]