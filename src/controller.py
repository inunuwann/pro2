from src.board import Board
from src.models import Cardset

# =====================
# Controller
# =====================

class Controller:
    TOTAL_ROUNDS = 12

    def __init__(self, players, view):
        self.view = view
        self.board = Board(players, view)

    def run_game(self):
        """ゲームのメインループ"""
        self.view.display_message("=== ゲーム開始 ===\n")

        for round_num in range(1, self.TOTAL_ROUNDS + 1):
            round_num, table = self.board.setup_round(round_num)
            self.view.display_message(f"\n===== ラウンド {round_num} 開始 =====")

            round_over = False
            while not round_over:
                for player in self.board.players:
                    if not player.hand:
                        round_over = True
                        break

                    agari, match_result = self.board.play_turn(player)
                    self.view.display_turn_result(player, match_result)

                    if agari:  # あがりを選択した場合、ラウンドを終了し、次のラウンドへ
                        self.view.display_message(f"\n{player.name} があがりを選択しました！")
                        round_over = True  # ラウンド終了
                        break

            self.show_round_result(round_num)  # ← ラウンド終了時の得点表示を追加

        self.show_game_result()  # 全ラウンド終了後にスコア表示

    def show_game_result(self):
        self.view.display_game_end()
        for p in self.board.players:
            captured_set = Cardset(p.captured)
            yaku = captured_set.check_yaku()
            score = captured_set.calculate_score()
            self.view.display_final_score(p, score, yaku)

    def show_round_result(self, round_num):
        """ラウンド終了時に得点を表示"""
        self.view.display_message(f"\n===== ラウンド {round_num} 終了 =====")

        for p in self.board.players:
            captured_set = Cardset(p.captured)
            yaku = captured_set.check_yaku()
            score = captured_set.calculate_score()
            self.view.display_final_score(p, score, yaku)
