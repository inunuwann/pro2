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

class Player:
    def __init__(self, name, is_cpu=False):
        self.name = name
        self.is_cpu = is_cpu
        self.hand = []      # 各ラウンド開始時に配られる手札
        self.captured = []  # ゲーム全体で獲得したカード（出来札）

    def __str__(self):
        return self.name

# =====================
# View
# =====================

class View:
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

    # ユーザーにリストからの選択を促し、選ばれたインデックスを返す
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
    HAND_SIZE = 8
    TABLE_SIZE = 8

    def __init__(self, players, view):
        self.players = players  # Model の Player オブジェクトのリスト
        self.view = view        # View オブジェクト

    def run_game(self):
        self.view.display_message("=== ゲーム開始 ===\n")
        for round_num in range(1, self.TOTAL_ROUNDS + 1):
            self.setup_round(round_num)
            self.play_round(round_num)
            self.finish_round(round_num)
        self.show_game_result()

    # ラウンドのセットアップ：デッキ生成・シャッフル、手札・初期場札の配布
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

    # ラウンド内のターンを進める
    def play_round(self, round_num):
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

    # 1プレイヤーのターンの処理（手札出し＋山札引き）
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

    # 手札からカードを出すフェーズ（View の選択機能を利用）
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

    # 山札からカードを引くフェーズ
    def draw_card_phase(self, player):
        if self.deck.cards:
            drawn_card = self.deck.cards.pop()
            self.view.display_message(f"\n{player.name} は山札から {drawn_card} を引きました。")
            self.match_phase(player, drawn_card)
            return True
        else:
            self.view.display_message("山札はもうありません。")
            return False

    # カードのマッチング処理：View の選択機能を利用してマッチ対象を決定
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

    # ラウンド終了時の表示処理
    def finish_round(self, round_num):
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

    # ゲーム終了時の結果表示
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
