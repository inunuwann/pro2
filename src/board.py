from .models import Cardset
import random

# =====================
# Board
# =====================

class Board:
    HAND_SIZE = 8
    TABLE_SIZE = 8

    def __init__(self, players, view):
        self.players = players
        self.view = view  # ユーザー選択用にViewを保持
        self.deck = None
        self.table = []

    def setup_round(self, round_num):
        """ラウンドの初期化"""
        for p in self.players:
            p.decision_made = False
            p.decision = None
            p.hand = []
            p.captured = []

        self.deck = Cardset()
        self.deck.generate_cards()
        self.deck.shuffle()

        for _ in range(self.HAND_SIZE):
            for p in self.players:
                if self.deck.cards:
                    p.hand.append(self.deck.cards.pop())

        self.table = [self.deck.cards.pop() for _ in range(self.TABLE_SIZE)]

        return round_num, self.table

    def play_turn(self, player):
        """プレイヤーのターン処理"""
        if not player.hand:
            return False, []

        played_card = self.choose_card(player)
        result1 = self.match_card(player, played_card, source="hand")

        if not player.decision_made and self.check_yaku_and_decide(player):
            return True, result1  # あがりを選択した場合、即 True を返す

        if not self.deck.cards:
            return False, result1

        drawn_card = self.deck.cards.pop()
        result2 = self.match_card(player, drawn_card, source="deck")

        if not player.decision_made and self.check_yaku_and_decide(player):
            return True, result1 + result2  # あがりを選択した場合、即 True を返す

        return False, result1 + result2

    def choose_card(self, player):
        """手札からカードを選択（出力せずにデータを返す）"""
        if player.is_cpu:
            played_card = random.choice(player.hand)
            player.hand.remove(played_card)
            return played_card
        else:
            # 人間の場合、選択前に場札と自分の出来札を表示する
            self.view.display_cards("【場札】", self.table)
            self.view.display_cards(f"【{player.name}の出来札】", player.captured)
            index = self.view.choose_from_list(f"{player.name}の手札を選んでください:", player.hand)
            played_card = player.hand.pop(index)
            return played_card

    def match_card(self, player, card, source="hand"):
        """カードのマッチング処理
           source は "hand"（手札から出した場合）または "deck"（山札から引いた場合）を示す
        """
        matching_cards = [c for c in self.table if c.month == card.month]
        if matching_cards:
            chosen_match = random.choice(matching_cards)
            self.table.remove(chosen_match)
            player.captured.extend([card, chosen_match])
            # タプル: ("match", player, 出したカード, マッチした場札, source)
            return [("match", player, card, chosen_match, source)]
        else:
            self.table.append(card)
            # タプル: ("no_match", 出したカード, source)
            return [("no_match", card, source)]

    def check_yaku_and_decide(self, player):
        """役の判定。役があれば、CPUはランダム、人間は選択"""
        captured_set = Cardset(player.captured)
        yaku = captured_set.check_yaku()

        if yaku:
            self.view.display_message(f"{player.name} の役: {', '.join(yaku)}")

            if player.is_cpu:
                # CPUの場合、ランダムに決定
                decision = random.choice(["agari", "koi"])
                self.view.display_message(f"CPUは {decision} を選択しました。")
            else:
                # 人間プレイヤーの場合、選択肢を表示
                decision = self.view.choose_from_list("こいこいするか、あがるか選んでください (0: あがる, 1: こいこい)", ["あがる", "こいこい"])
                decision = "agari" if decision == 0 else "koi"

            player.decision_made = True
            player.decision = decision

            # "agari" ならゲーム終了
            return decision == "agari"

        return False

