import sys
import os

# Добавляем путь к корневой директории проекта,
# чтобы Python видел папки config/, engine/ и game/
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
sys.path.append(ROOT_DIR)

from engine.game_engine import GameEngine


def main():
    game = GameEngine()
    game.run()


if __name__ == "__main__":
    main()