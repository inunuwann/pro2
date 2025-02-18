# src/model.py

from collections import defaultdict
import random

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
        # 例として光の枚数に応じた役を判定
        if len(self.kind_dict.get("光", [])) == 5:
            yaku.append("五光")
        # 他の役判定も必要に応じて実装
        return yaku

class Player:
    def __init__(self, name, is_cpu=False):
        self.name = name
        self.is_cpu = is_cpu
        self.hand = []      # 各ラウンドの手札
        self.captured = []  # ゲーム全体で獲得したカード（出来札）
        
    def __str__(self):
        return self.name

