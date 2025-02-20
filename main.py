from src.models import Cardset, Card, Player
from src.view import View
from src.controller import Controller

# =====================
# メイン処理
# =====================
def main():
    human = Player("あなた")
    cpu = Player("CPU", is_cpu=True)
    players = [human, cpu]
    view = View()
    controller = Controller(players, view)
    controller.run_game()

if __name__ == "__main__":
    main()
