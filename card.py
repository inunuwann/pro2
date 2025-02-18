from collections import defaultdict
import random

class Card:
    def __init__(self, month, kind):
        self.month = month
        self.kind = kind

class Cardset:
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
        self.cards = [Card(month, kind) for month, kinds in kinds_by_month.items() for kind in kinds]

    def shuffle(self):
        random.shuffle(self.cards)

    def check_yaku(self):
        yaku = []

        #光役
        match len(self.kind_dict.get("光", [])):
            case 5:
                yaku.append("五光")
            case 4 if 11 in self.kind_dict["光"]:
                yaku.append("雨四光")
            case 4:
                yaku.append("四光")
            case 3:
                yaku.append("三光")

        #盃役
        match self.kind_dict:
            case hanami if 3 in hanami.get("光", []) and 9 in hanami.get("タネ", []):
                yaku.append("花見で一杯")
            case tsukimi if 8 in tsukimi.get("光", []) and 9 in tsukimi.get("タネ", []):
                yaku.append("月見で一杯")

        #たん役
        match len(self.kind_dict.get("短冊", [])):
            case tan if tan >= 5:
                yaku.append("たん")

        #青短赤短
        match self.kind_dict.get("短冊", []):
            case aotan if {6, 7, 9}.issubset(aotan):
                yaku.append("青短")
            case akatan if {1, 2, 3}.issubset(akatan):
                yaku.append("赤短")

        #たね役
        match len(self.kind_dict.get("タネ", [])):
            case tane if tane >= 5:
                yaku.append("タネ")

        #猪鹿蝶
        match self.kind_dict.get("タネ", []):
            case inosika if {6, 7, 10}.issubset(inosika):
                yaku.append("猪鹿蝶")

        #カス
        match len(self.kind_dict.get("カス", [])):
            case kasu if kasu >= 10:
                yaku.append("カス")

        return yaku

class Player:
    def __init__(self, name):
        self.name = name


class Board:
    MAX_ROUNDS = 12  # 最大ラウンド数を固定

    def __init__(self, players):
        self.players = players
        self.turn = 0  # 現在のターン
        self.round = 1  # 現在のラウンド
        self.max_rounds = self.MAX_ROUNDS  # 最大ラウンド数を固定
        self.current_player_index = 0  # 現在のプレイヤー

    def next_turn(self):
        """ターンを進める"""
        if self.round > self.max_rounds:
            print("ゲーム終了")
            return

        self.turn += 1
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

        # 1ラウンド終了 (全員のターンが終わったら次のラウンドへ)
        if self.current_player_index == 0:
            self.round += 1
            self.turn = 0  # 新ラウンドではターンをリセット

        # 最大ラウンドを超えたらゲーム終了
        if self.round > self.max_rounds:
            print("ゲーム終了")

    def get_current_player(self):
        """現在のプレイヤーを取得"""
        return self.players[self.current_player_index]

    def get_game_state(self):
        """現在のゲーム状態を取得"""
        return {
            "turn": self.turn,
            "round": self.round,
            "current_player": self.get_current_player(),
        }


class View:
    pass

class Controller:
    pass
