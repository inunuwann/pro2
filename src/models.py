from collections import defaultdict
import random

# =====================
# Model
# =====================

class Card:
    def __init__(self, month, kind):
        self.month = month  # 1～12月
        self.kind = kind    # 例："光", "短冊", "タネ", "カス"

    def __str__(self):
        return f"{self.month}月の{self.kind}"

    def __repr__(self):
        return self.__str__()

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
        self.cards = [Card(month, kind)
                      for month, kinds in kinds_by_month.items()
                      for kind in kinds]

    def shuffle(self):
        random.shuffle(self.cards)

    def check_yaku(self):
        yaku = []
        # ※ 役判定はシンプルな例です
        match len(self.kind_dict.get("光", [])):
            case 5:
                yaku.append("五光")
            case 4 if 11 in self.kind_dict["光"]:
                yaku.append("雨四光")
            case 4:
                yaku.append("四光")
            case 3:
                yaku.append("三光")
        match self.kind_dict:
            case hanami if 3 in hanami.get("光", []) and 9 in hanami.get("タネ", []):
                yaku.append("花見で一杯")
            case tsukimi if 8 in tsukimi.get("光", []) and 9 in tsukimi.get("タネ", []):
                yaku.append("月見で一杯")
        match len(self.kind_dict.get("短冊", [])):
            case tan if tan >= 5:
                yaku.append("たん")
        match self.kind_dict.get("短冊", []):
            case aotan if {6, 7, 9}.issubset(aotan):
                yaku.append("青短")
            case akatan if {1, 2, 3}.issubset(akatan):
                yaku.append("赤短")
        match len(self.kind_dict.get("タネ", [])):
            case tane if tane >= 5:
                yaku.append("タネ")
        match self.kind_dict.get("タネ", []):
            case inosika if {6, 7, 10}.issubset(inosika):
                yaku.append("猪鹿蝶")
        match len(self.kind_dict.get("カス", [])):
            case kasu if kasu >= 10:
                yaku.append("カス")
        return yaku

    def calculate_score(self):
        """
        各役に対して以下の点数を加算する:
          三光：5点
          四光：8点
          雨四光：7点
          五光：10点
          花見で一杯：5点
          月見で一杯：5点
          青短：5点
          赤短：5点
          たん：1点
          猪鹿蝶：5点
          タネ：1点
          カス：1点
        """
        yaku_list = self.check_yaku()
        score_mapping = {
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
        score = sum(score_mapping.get(y, 0) for y in yaku_list)
        return score

class Player:
    def __init__(self, name, is_cpu=False):
        self.name = name
        self.is_cpu = is_cpu
        self.hand = []      # 各ラウンド開始時に配られる手札
        self.captured = []  # ゲーム全体で獲得したカード（出来札）
        # ラウンド毎の役宣言状態（こいこいかあがりかの選択済みか）
        self.decision_made = False
        self.decision = None

    def __str__(self):
        return self.name
