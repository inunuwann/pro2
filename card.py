from collections import defaultdict

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

    def check_yaku(self):
        yaku = []

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
