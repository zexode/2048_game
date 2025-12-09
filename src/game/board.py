import random
from typing import List, Tuple


class Board:
    """
    Класс Board инкапсулирует всю "математику" игры 2048:
    - состояние поля (матрица чисел);
    - генерация новых плиток;
    - обработка сдвигов и слияний;
    - вычисление очков;
    - проверка победы/поражения.

    Важный момент: здесь НЕТ графики, только логика.
    Это удобно для тестирования и хорошо ложится под требования методички
    про разделение логики и визуализации.
    """

    def __init__(
        self,
        size: int = 4,
        target_value: int = 2048,
        new_tile_values=None,
        new_tile_probabilities=None,
    ):
        self.size = size
        self.target_value = target_value

        # Значения новых плиток и их вероятности появления
        self.new_tile_values = new_tile_values or [2, 4]
        self.new_tile_probabilities = (
            new_tile_probabilities or [0.9, 0.1]
        )

        # Внутреннее представление поля
        self.grid: List[List[int]] = [
            [0 for _ in range(self.size)] for _ in range(self.size)
        ]

        # Текущее количество очков
        self.score: int = 0

    # ==========================
    # Инициализация и сброс игры
    # ==========================

    def reset(self, initial_tiles: int = 2) -> None:
        """
        Очищает поле и создаёт заданное количество стартовых плиток.
        """
        self.grid = [
            [0 for _ in range(self.size)] for _ in range(self.size)
        ]
        self.score = 0

        for _ in range(initial_tiles):
            self.add_random_tile()

    # =====================
    # Работа с плитками
    # =====================

    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """
        Возвращает список координат пустых клеток (r, c).
        """
        empty = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == 0:
                    empty.append((r, c))
        return empty

    def add_random_tile(self) -> bool:
        """
        Добавляет новую плитку в случайную пустую клетку.
        Возвращает True, если плитка добавлена, False, если пустых клеток нет.
        """
        empty_cells = self.get_empty_cells()
        if not empty_cells:
            return False

        r, c = random.choice(empty_cells)

        # Выбираем значение новой плитки согласно вероятностям
        value = random.choices(
            self.new_tile_values, weights=self.new_tile_probabilities
        )[0]

        self.grid[r][c] = value
        return True

    # =====================
    # Проверка состояния
    # =====================

    def has_won(self) -> bool:
        """
        Возвращает True, если на поле есть плитка с target_value.
        """
        return any(
            cell >= self.target_value
            for row in self.grid
            for cell in row
        )

    def can_move(self) -> bool:
        """
        Проверяет, возможно ли ещё сделать ход:
        - есть хотя бы одна пустая клетка
        ИЛИ
        - есть две соседние по вертикали/горизонтали одинаковые плитки.
        """
        # Пустые клетки
        if self.get_empty_cells():
            return True

        # Проверка по горизонтали и вертикали
        for r in range(self.size):
            for c in range(self.size):
                value = self.grid[r][c]

                # сосед справа
                if c + 1 < self.size and self.grid[r][c + 1] == value:
                    return True

                # сосед снизу
                if r + 1 < self.size and self.grid[r + 1][c] == value:
                    return True

        return False

    # =====================
    # Основная логика хода
    # =====================

    def move(self, direction: str) -> Tuple[bool, int, bool, bool]:
        """
        Выполняет ход в одну из сторон: "up", "down", "left", "right".

        Возвращает кортеж:
        - moved: bool        -- изменилось ли поле (был ли реальный ход)
        - gained_score: int  -- количество очков, полученных за этот ход
        - won: bool          -- достигнут ли target_value
        - lost: bool         -- нет возможных ходов после этого хода
        """
        valid_directions = {"up", "down", "left", "right"}
        if direction not in valid_directions:
            raise ValueError(f"Invalid direction: {direction}")

        # Сохраняем копию поля перед ходом
        old_grid = [row[:] for row in self.grid]

        # Накопленный за ход прирост очков
        gained_score = 0

        # Для удобства обрабатываем сдвиги в терминах "сдвиг влево" на строках.
        # Для up/down/right преобразуем поле, делаем move_left, и обратно.
        if direction == "left":
            gained_score = self._move_left_on_grid(self.grid)
        elif direction == "right":
            # Разворачиваем строки, двигаем "влево", разворачиваем обратно
            self._reverse_rows()
            gained_score = self._move_left_on_grid(self.grid)
            self._reverse_rows()
        elif direction == "up":
            # Транспонируем, двигаем "влево", транспонируем обратно
            self._transpose()
            gained_score = self._move_left_on_grid(self.grid)
            self._transpose()
        elif direction == "down":
            # Транспонируем, разворачиваем строки, двигаем "влево", разворачиваем, транспонируем
            self._transpose()
            self._reverse_rows()
            gained_score = self._move_left_on_grid(self.grid)
            self._reverse_rows()
            self._transpose()

        # Проверяем, изменилось ли поле
        moved = old_grid != self.grid

        if moved:
            # Если ход что-то изменил, добавляем новую плитку
            self.add_random_tile()
            # Обновляем общий счёт
            self.score += gained_score

        # Проверяем победу и поражение
        won = self.has_won()
        lost = not self.can_move()

        return moved, gained_score, won, lost

    # =====================
    # Вспомогательные методы для move
    # =====================

    def _move_left_on_grid(self, grid: List[List[int]]) -> int:
        """
        Применяет ход "влево" ко всем строкам.
        Возвращает суммарный прирост очков за слияния.
        """
        total_gained = 0

        for r in range(self.size):
            row = grid[r]
            new_row, gained = self._compress_and_merge_row_left(row)
            grid[r] = new_row
            total_gained += gained

        return total_gained

    def _compress_and_merge_row_left(
        self, row: List[int]
    ) -> Tuple[List[int], int]:
        """
        Для одной строки:
        - сдвигает все ненулевые элементы влево;
        - объединяет соседние одинаковые плитки;
        - снова сдвигает влево после слияния.

        Возвращает:
        - новую строку;
        - очки, полученные за все слияния.
        """
        # Удаляем все нули
        filtered = [value for value in row if value != 0]

        merged_row: List[int] = []
        gained_score = 0

        skip_next = False
        for i in range(len(filtered)):
            if skip_next:
                skip_next = False
                continue

            current = filtered[i]

            # Проверяем, можем ли слить текущую и следующую плитку
            if i + 1 < len(filtered) and filtered[i + 1] == current:
                merged_value = current * 2
                merged_row.append(merged_value)
                gained_score += merged_value
                skip_next = True  # пропускаем следующую, т.к. уже слили
            else:
                merged_row.append(current)

        # Дополняем строку нулями справа
        while len(merged_row) < self.size:
            merged_row.append(0)

        return merged_row, gained_score

    def _reverse_rows(self) -> None:
        """
        Разворачивает каждый ряд (для реализации "right" и "down").
        """
        for r in range(self.size):
            self.grid[r].reverse()

    def _transpose(self) -> None:
        """
        Транспонирует матрицу (для реализации "up" и "down").
        """
        self.grid = [list(row) for row in zip(*self.grid)]