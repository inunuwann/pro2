# src/controller.py

import random
from src.model import Card, Cardset, Player
from src.view import View

class Controller:
    TOTAL_ROUNDS = 12
    HAND_SIZE = 8
    TABLE_SIZE = 8

    def __init__(self, players, view):
        self.players = players  # Model の Player オブジェクトのリスト
        self.view = view        # View オブジェクト

    def run_game(self):
        self.view.display_message("=== ゲーム開始 ===\n")
        for round_num in range(1, self.TOTAL_ROUNDS + 1):
            self.setup_round(round_num)
            self.play_round()
            self.finish_round()
        self.show_game_result()

    def setup_round(self, round_num):
        self.view.display_message(f"\n===== ラウンド {round_num} 開始 =====")
        self.deck = Cardset()
        self.deck.generate_cards()
        self.deck.shuffle()
        for p in self.players:
            p.hand = []
        for _ in range(self.HAND_SIZE):
            for p in self.players:
                if self.deck.cards:
                    p.hand.append(self.deck.cards.pop())
        self.table = []
        for _ in range(self.TABLE_SIZE):
            if self.deck.cards:
                self.table.append(self.deck.cards.pop())
        self.view.display_message("初期場札:")
        self.view.display_cards("", self.table)

    def play_round(self):
        round_over = False
        while not round_over:
            for p in self.players:
                if not p.hand:
                    self.view.display_message(f"\n【{p.name} の手札がなくなりました】 ラウンド終了！")
                    round_over = True
                    break
                if self.process_turn(p):
                    round_over = True
                    break

    def process_turn(self, player):
        self.view.display_message(f"\n【{player.name} のターン】")
        if not player.is_cpu:
            self.view.display_cards("あなたの出来札:", player.captured)
        self.view.display_cards("現在の場札:", self.table)
        if not self.play_card_phase(player):
            return True
        if not player.hand:
            self.view.display_message(f"\n【{player.name} の手札がなくなりました】 ラウンド終了！")
            return True
        if not self.draw_card_phase(player):
            return True
        if not player.hand:
            self.view.display_message(f"\n【{player.name} の手札がなくなりました】 ラウンド終了！")
            return True
        return False

    def play_card_phase(self, player):
        if player.hand:
            if not player.is_cpu:
                choice = self.view.choose_from_list("あなたの手札:", player.hand)
                played_card = player.hand.pop(choice)
            else:
                played_card = random.choice(player.hand)
                player.hand.remove(played_card)
            self.view.display_message(f"{player.name} は手札から {played_card} を出しました。")
            self.match_phase(player, played_card)
            return True
        return False

    def draw_card_phase(self, player):
        if self.deck.cards:
            drawn_card = self.deck.cards.pop()
            self.view.display_message(f"\n{player.name} は山札から {drawn_card} を引きました。")
            self.match_phase(player, drawn_card)
            return True
        else:
            self.view.display_message("山札はもうありません。")
            return False

    def match_phase(self, player, card):
        matching_cards = [c for c in self.table if c.month == card.month]
        if matching_cards:
            if not player.is_cpu:
                choice = self.view.choose_from_list("該当するカード:", matching_cards)
                chosen_match = matching_cards[choice]
            else:
                chosen_match = random.choice(matching_cards)
            self.table.remove(chosen_match)
            player.captured.extend([card, chosen_match])
            self.view.display_message(f"{player.name} は {chosen_match} とマッチ！ 両カードを獲得。")
        else:
            self.table.append(card)
            self.view.display_message("マッチするカードがなかったので、場札に置きました。")

    def finish_round(self):
        self.view.display_message("\n===== ラウンド終了 =====")
        self.view.display_cards("残った場札:", self.table)
        for p in self.players:
            self.view.display_message(f"\n{p.name} のラウンド獲得カード枚数: {len(p.captured)}")
            captured_set = Cardset(p.captured)
            yaku = captured_set.check_yaku()
            if yaku:
                self.view.display_message("　→ 役: " + ", ".join(yaku))
            else:
                self.view.display_message("　→ 役: なし")

    def show_game_result(self):
        self.view.display_message("\n=== ゲーム終了 ===")
        for p in self.players:
            self.view.display_message(f"\n{p.name} の総獲得カード枚数: {len(p.captured)}")
            captured_set = Cardset(p.captured)
            yaku = captured_set.check_yaku()
            if yaku:
                self.view.display_message("　→ 役: " + ", ".join(yaku))
            else:
                self.view.display_message("　→ 役: なし")

