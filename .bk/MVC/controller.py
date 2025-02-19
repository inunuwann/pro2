# controller.py
import random
from model import Player, Board
from view import ConsoleView

class GameController:
    TOTAL_ROUNDS = 12
    HAND_SIZE = 8
    TABLE_SIZE = 8

    def __init__(self, players, view: ConsoleView):
        self.players = players       # Model の Player オブジェクトのリスト
        self.view = view             # View の ConsoleView オブジェクト
        self.board = Board()         # Model の Board オブジェクト

    def run_game(self):
        self.view.display_game_start()
        for round_num in range(1, self.TOTAL_ROUNDS + 1):
            self.setup_round(round_num)
            self.run_round(round_num)
            self.finish_round(round_num)
        self.show_game_result()

    def setup_round(self, round_num):
        for p in self.players:
            p.decision_made = False
            p.decision = None
            p.hand = []
            # ※ captured のリセットはルールに合わせて判断してください
        self.board.setup_round(self.players, self.HAND_SIZE, self.TABLE_SIZE)
        self.view.display_round_setup(round_num, self.board.table)

    def run_round(self, round_num):
        round_over = False
        while not round_over:
            for p in self.players:
                if not p.hand:
                    self.view.display_round_end_condition(p.name, "手札切れ")
                    round_over = True
                    break
                decision = self.run_player_turn(p)
                if decision == "agari":
                    round_over = True
                    break

    def run_player_turn(self, player: Player) -> str:
        self.view.display_turn_start(player.name, player.captured, self.board.table)
        decision = self.execute_play_card_phase(player)
        if decision == "agari":
            return decision
        if not player.hand:
            self.view.display_turn_end(player.name, "手札切れ")
            return ""
        decision = self.execute_draw_card_phase(player)
        return decision

    def execute_play_card_phase(self, player: Player) -> str:
        if not player.hand:
            return ""
        played_card = self.get_player_card_choice(player, "手札からカードを選択")
        self.view.display_card_play(player.name, played_card)
        matches = [c for c in self.board.table if c.month == played_card.month]
        chosen_index = None
        if matches and not player.is_cpu:
            chosen_index = self.view.request_match_choice(matches)
        phase_result = self.board.process_play_phase(player, played_card, chosen_index)
        self.view.display_phase_result(player.name, played_card, phase_result)
        return self.handle_yaku_decision(player)

    def execute_draw_card_phase(self, player: Player) -> str:
        if self.board.is_deck_empty():
            self.view.display_deck_empty()
            return ""
        drawn_card = self.board.deck.cards.pop()
        self.view.display_card_draw(player.name, drawn_card)
        matches = [c for c in self.board.table if c.month == drawn_card.month]
        chosen_index = None
        if matches and not player.is_cpu:
            chosen_index = self.view.request_match_choice(matches)
        phase_result = self.board.process_draw_phase(player, drawn_card, chosen_index)
        self.view.display_phase_result(player.name, drawn_card, phase_result)
        return self.handle_yaku_decision(player)

    def get_player_card_choice(self, player: Player, prompt: str):
        if not player.is_cpu:
            index = self.view.request_card_choice(prompt, player.hand)
            return player.hand.pop(index)
        else:
            chosen = random.choice(player.hand)
            player.hand.remove(chosen)
            return chosen

    def handle_yaku_decision(self, player: Player) -> str:
        yaku = self.board.get_established_yaku(player)
        if yaku:
            decision = self.view.request_yaku_decision(player.name, yaku)
            player.decision_made = True
            player.decision = decision
            return decision  # "agari"ならラウンド終了、"koi"なら継続
        return ""

    def finish_round(self, round_num):
        players_summary = []
        for p in self.players:
            yaku = self.board.get_established_yaku(p)
            score = self.board.calculate_player_score(p)
            summary = {
                "name": p.name,
                "captured_count": len(p.captured),
                "yaku": yaku,
                "score": score,
                "decision": p.decision
            }
            players_summary.append(summary)
        self.view.display_round_summary(self.board.table, players_summary)

    def show_game_result(self):
        players_summary = []
        for p in self.players:
            yaku = self.board.get_established_yaku(p)
            score = self.board.calculate_player_score(p)
            summary = {
                "name": p.name,
                "captured_count": len(p.captured),
                "yaku": yaku,
                "score": score
            }
            players_summary.append(summary)
        self.view.display_game_summary(players_summary)
