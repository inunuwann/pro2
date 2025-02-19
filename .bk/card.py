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
        """プレイヤーのターン処理
           1. 手札からカードを選んで出す（source="hand"）
           2. マッチング処理を行う
           3. 山札からカードを引き、同様にマッチング処理を行う
        """
        # 手札からカードを出す
        played_card = self.choose_card(player)
        result1 = self.match_card(player, played_card, source="hand")
        if not player.decision_made and self.check_yaku_and_decide(player):
            return True, result1

        # 山札が空でなければ、カードを引いて処理
        if not self.deck.cards:
            return False, result1

        drawn_card = self.deck.cards.pop()
        result2 = self.match_card(player, drawn_card, source="deck")
        if not player.decision_made and self.check_yaku_and_decide(player):
            return True, result1 + result2

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
        """役の判定。役があれば CPU はランダム、または人間は（ここでは仮に）あがりとする"""
        captured_set = Cardset(player.captured)
        yaku = captured_set.check_yaku()
        if yaku:
            if player.is_cpu:
                decision = random.choice(['agari', 'koi'])
            else:
                # 人間の場合、実際には役を表示して選択させることも可能
                decision = 'agari'
            player.decision_made = True
            player.decision = decision
            return decision == "agari"
        return False

# =====================
# View
# =====================
class View:
    def display_game_start(self):
        self.display_message("=== ゲーム開始 ===\n")

    def display_game_end(self):
        self.display_message("\n=== ゲーム終了 ===")

    def display_round_start(self, round_num, table):
        self.display_message(f"\n===== ラウンド {round_num} 開始 =====")
        self.display_cards("【初期場札】", table)

    def display_turn_result(self, player, match_result):
        """ターン結果を表示（source に応じたメッセージを出力）"""
        for result in match_result:
            if result[0] == "match":
                # result: ("match", player, card, matched_card, source)
                card = result[2]
                matched_card = result[3]
                source = result[4] if len(result) > 4 else "hand"
                if source == "hand":
                    self.display_message(f"{player.name} は手札から {card} を出し、場の {matched_card} とマッチし、獲得しました！")
                elif source == "deck":
                    self.display_message(f"{player.name} は山札から引いた {card} が、場の {matched_card} とマッチし、獲得しました！")
            elif result[0] == "no_match":
                # result: ("no_match", card, source)
                card = result[1]
                source = result[2] if len(result) > 2 else "hand"
                if source == "hand":
                    self.display_message(f"手札から出した {card} は、マッチするカードがなかったので場に置きました。")
                elif source == "deck":
                    self.display_message(f"山札から引いた {card} は、マッチするカードがなかったので場に置きました。")

    def display_final_score(self, player, score, yaku):
        yaku_text = ", ".join(yaku) if yaku else "役なし"
        self.display_message(f"{player.name} の得点: {score}点 ({yaku_text})")

    def display_message(self, message):
        print(message)

    def display_cards(self, title, cards):
        print(title)
        if cards:
            for idx, card in enumerate(cards):
                print(f"  {idx}: {card}")
        else:
            print("  なし")

    def get_input(self, prompt):
        return input(prompt)

    def choose_from_list(self, prompt, items):
        self.display_cards(prompt, items)
        while True:
            try:
                choice = int(self.get_input("選択番号: "))
                if 0 <= choice < len(items):
                    return choice
                else:
                    self.display_message("正しい番号を入力してください。")
            except ValueError:
                self.display_message("数字を入力してください。")

# =====================
# Controller
# =====================
class Controller:
    TOTAL_ROUNDS = 12

    def __init__(self, players, view):
        self.view = view
        self.board = Board(players, view)

    def run_game(self):
        self.view.display_game_start()
        for round_num in range(1, self.TOTAL_ROUNDS + 1):
            round_num, table = self.board.setup_round(round_num)
            self.view.display_round_start(round_num, table)

            round_over = False
            while not round_over:
                for player in self.board.players:
                    if not player.hand:
                        round_over = True
                        break

                    round_over, match_result = self.board.play_turn(player)
                    self.view.display_turn_result(player, match_result)

        self.show_game_result()

    def show_game_result(self):
        self.view.display_game_end()
        for p in self.board.players:
            captured_set = Cardset(p.captured)
            yaku = captured_set.check_yaku()
            score = captured_set.calculate_score()
            self.view.display_final_score(p, score, yaku)

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
