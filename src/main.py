# src/main.py

from src.model import Player
from src.view import View
from src.controller import Controller

def main():
    # 人間プレイヤーと CPU を生成
    human = Player("あなた")
    cpu = Player("CPU", is_cpu=True)
    players = [human, cpu]
    view = View()
    controller = Controller(players, view)
    controller.run_game()

if __name__ == "__main__":
    main()

