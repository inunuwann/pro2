# model.py
from collections import defaultdict
import random

class Card:
    """カードを表すクラス"""
    def __init__(self, month, kind):
        self.month = month  # 1～12月
        self.kind = kind    # 例："光", "短冊", "タネ", "カス"

    def __str__(self):
        return f"{self.month}月の{self.kind}"

    def __repr__(self):
        return self.__str__()

class Cardset:
    """
    複数のカードを管理し、役判定や得点計算を行うクラス
    """
    def __init__(self, cards=None):
        self.cards = cards if cards else []
        self.card_dict = defaultdict(list)
        self.kind_dict = defaultdict(list)
        for card in self.cards:
            self.card_dict[card.month].append(card.kind)
            self.kind_dict[card.kind].append(card.month)

    def add_card(self, card):
        self.cards.append(card)
        self.card_dict[card.month].append(card.kind)
        self.kind_dict[card.kind].append(card.month)

    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)
            self.card_dict[card.month].remove(card.kind)
            self.kind_dict[card.kind].remove(card.month)

    def generate_cards(self):
        kinds_by_month = {
            1: ["光", "短冊", "カス", "カス"],
            2: ["短冊", "タネ", "カス", "カス"],
            3: ["光", "短冊", "カス", "カス"],
            4: ["短冊", "タネ", "カス", "カス"],
            5: ["短冊", "タネ", "カス", "カス"],
            6: ["短冊", "タネ", "カス", "カス"],
            7: ["短冊", "タネ", "カス", "カス"],
            8: ["光", "タネ", "カス", "カス"],
            9: ["短冊", "タネ", "カス", "カス"],
            10: ["短冊", "タネ", "カス", "カス"],
            11: ["光", "タネ", "カス", "カス"],
            12: ["光", "カス", "カス", "カス"],
        }
        self.cards = [Card(month, kind)
                      for month, kinds in kinds_by_month.items()
                      for kind in kinds]

    def shuffle(self):
        random.shuffle(self.cards)

    def check_yaku(self):
        """
        獲得したカードから成立した役（yaku）のリストを返す。
        判定は match-case とガード節を用いて行う。
        """
        yaku = []
        # 光の枚数による判定
        match len(self.kind_dict.get("光", [])):
            case 5:
                yaku.append("五光")
            case 4 if 11 in self.kind_dict["光"]:
                yaku.append("雨四光")
            case 4:
                yaku.append("四光")
            case 3:
                yaku.append("三光")
            case _:
                pass

        # 花見・月見の例（タネの存在で判定）
        match (3 in self.kind_dict.get("光", []), 9 in self.kind_dict.get("タネ", [])):
            case (True, True):
                yaku.append("花見で一杯")
            case _:
                pass
        match (8 in self.kind_dict.get("光", []), 9 in self.kind_dict.get("タネ", [])):
            case (True, True):
                yaku.append("月見で一杯")
            case _:
                pass

        # 短冊による判定
        match len(self.kind_dict.get("短冊", [])):
            case n if n >= 5:
                yaku.append("たん")
            case _:
                pass
        match set(self.kind_dict.get("短冊", [])):
            case s if {6, 7, 9}.issubset(s):
                yaku.append("青短")
            case s if {1, 2, 3}.issubset(s):
                yaku.append("赤短")
            case _:
                pass

        # タネ・猪鹿蝶
        match len(self.kind_dict.get("タネ", [])):
            case n if n >= 5:
                yaku.append("タネ")
            case _:
                pass
        match set(self.kind_dict.get("タネ", [])):
            case s if {6, 7, 10}.issubset(s):
                yaku.append("猪鹿蝶")
            case _:
                pass

        # カス
        match len(self.kind_dict.get("カス", [])):
            case n if n >= 10:
                yaku.append("カス")
            case _:
                pass

        return yaku

    def calculate_score(self):
        """チェック済みの役リストから総得点を計算する"""
        yaku_list = self.check_yaku()
        return ScoreCalculator.calculate_score(yaku_list)

    @staticmethod
    def find_match(card, table):
        """
        与えられたカードとテーブル上のカードリストから、
        同じ月のカード（マッチするカード）をリストとして返します。
        """
        return [c for c in table if c.month == card.month]

class ScoreCalculator:
    """
    役と得点のマッピングに基づいて得点を計算するクラス
    """
    SCORE_MAPPING = {
        "三光": 5,
        "四光": 8,
        "雨四光": 7,
        "五光": 10,
        "花見で一杯": 5,
        "月見で一杯": 5,
        "青短": 5,
        "赤短": 5,
        "たん": 1,
        "猪鹿蝶": 5,
        "タネ": 1,
        "カス": 1
    }

    @classmethod
    def calculate_score(cls, yaku_list):
        return sum(cls.SCORE_MAPPING.get(yaku, 0) for yaku in yaku_list)

class Player:
    """プレイヤーを表すクラス（人間・CPU）"""
    def __init__(self, name, is_cpu=False):
        self.name = name
        self.is_cpu = is_cpu
        self.hand = []      # 各ラウンド開始時に配られる手札
        self.captured = []  # 獲得したカード（出来札）
        self.decision_made = False  # このラウンドであがり／こいこいの宣言済みか
        self.decision = None        # 'agari'（あがり） or 'koi'（こいこい）

    def __str__(self):
        return self.name

class Board:
    """
    Board クラスは、デッキや場札、ターン／ラウンドの進行状態を管理します。
    Controller はこの Board クラスのメソッドを呼び出して、ゲーム進行のロジックを利用します。
    """
    def __init__(self):
        self.deck = Cardset()
        self.table = []

    def setup_round(self, players, hand_size, table_size):
        """ラウンド開始時のデッキ生成、シャッフル、手札および場札の配布を行う"""
        self.deck.generate_cards()
        self.deck.shuffle()
        for p in players:
            p.hand = []
        for _ in range(hand_size):
            for p in players:
                if self.deck.cards:
                    p.hand.append(self.deck.cards.pop())
        self.table = []
        for _ in range(table_size):
            if self.deck.cards:
                self.table.append(self.deck.cards.pop())

    def process_play_phase(self, player, card, chosen_match_index=None):
        """
        プレイヤーが手札からカードを出す際の処理。
        マッチ判定は Cardset.find_match() を用いて行います。
        マッチがあれば、指定された（またはデフォルトの）カードとマッチさせ、
        マッチしなければカードをそのまま場札に追加します。
        戻り値は { "match": bool, "matched_card": matched_card } の辞書です。
        """
        matches = Cardset.find_match(card, self.table)
        if matches:
            if chosen_match_index is not None:
                chosen_match = matches[chosen_match_index]
            else:
                chosen_match = matches[0]
            self.table.remove(chosen_match)
            player.captured.extend([card, chosen_match])
            return {"match": True, "matched_card": chosen_match}
        else:
            self.table.append(card)
            return {"match": False, "matched_card": None}

    def process_draw_phase(self, player, card, chosen_match_index=None):
        """
        山札から引いたカードに対する処理。
        基本的には process_play_phase と同様のロジックです。
        """
        return self.process_play_phase(player, card, chosen_match_index)

    def get_established_yaku(self, player) -> list:
        """
        プレイヤーの獲得カードから Cardset を作成し、check_yaku() を呼び出して
        成立している役の一覧を返します。
        """
        cardset = Cardset(player.captured)
        return cardset.check_yaku()

    def calculate_player_score(self, player) -> int:
        """プレイヤーの獲得カードから総得点を計算して返す"""
        cardset = Cardset(player.captured)
        return cardset.calculate_score()

    def is_deck_empty(self) -> bool:
        return len(self.deck.cards) == 0
