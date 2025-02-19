# controller.py
import random

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

# model.py
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

# view.py
class ConsoleView:
    """
    ConsoleView は、ユーザーへの各種出力や入力要求を担当します。
    Controller から渡されたデータ（状態や選択肢など）を画面に表示し、
    ユーザーの入力値を Controller に返します。
    """

    # 出力関連メソッド
    def display_game_start(self):
        print("=== ゲーム開始 ===\n")

    def display_round_setup(self, round_num, table_cards):
        print(f"\n===== ラウンド {round_num} 開始 =====")
        print("初期場札:")
        self.render_cards("", table_cards)

    def display_round_end_condition(self, player_name, condition):
        print(f"\n【{player_name} の{condition}】 ラウンド終了！")

    def display_turn_start(self, player_name, captured, table_cards):
        print(f"\n【{player_name} のターン】")
        print("獲得カード:")
        self.render_cards("", captured)
        print("現在の場札:")
        self.render_cards("", table_cards)

    def display_card_play(self, player_name, card):
        print(f"{player_name} は手札から {card} を出しました。")

    def display_card_draw(self, player_name, card):
        print(f"{player_name} は山札から {card} を引きました。")

    def display_phase_result(self, player_name, card, result):
        if result["match"]:
            print(f"{player_name} は {result['matched_card']} とマッチ！")
        else:
            print("マッチするカードはありませんでした。")

    def display_deck_empty(self):
        print("山札はもうありません。")

    def display_turn_end(self, player_name, condition):
        print(f"\n【{player_name} の{condition}】 ターン終了！")

    def display_round_summary(self, table_cards, players_summary):
        print("\n===== ラウンド終了 =====")
        print("残り場札:")
        self.render_cards("", table_cards)
        for summary in players_summary:
            print(f"\n{summary['name']} の獲得枚数: {summary['captured_count']}")
            if summary.get("yaku"):
                print("　→ 役: " + ", ".join(summary["yaku"]))
                print(f"　→ 得点: {summary['score']}点")
                print(f"　→ 宣言: {summary.get('decision')}")
            else:
                print("　→ 役: なし")

    def display_game_summary(self, players_summary):
        print("\n=== ゲーム終了 ===")
        for summary in players_summary:
            print(f"\n{summary['name']} の総獲得枚数: {summary['captured_count']}")
            if summary.get("yaku"):
                print("　→ 役: " + ", ".join(summary["yaku"]))
                print(f"　→ 得点: {summary['score']}点")
            else:
                print("　→ 役: なし")

    # 入力・選択要求関連メソッド
    def request_card_choice(self, prompt, cards):
        self.render_cards(prompt, cards)
        while True:
            try:
                choice = int(input("選択番号: "))
                if 0 <= choice < len(cards):
                    return choice
                else:
                    print("正しい番号を入力してください。")
            except ValueError:
                print("数字を入力してください。")

    def request_match_choice(self, matches):
        self.render_cards("該当するカード:", matches)
        while True:
            try:
                choice = int(input("選択番号: "))
                if 0 <= choice < len(matches):
                    return choice
                else:
                    print("正しい番号を入力してください。")
            except ValueError:
                print("数字を入力してください。")

    def request_yaku_decision(self, player_name, yaku_list):
        print(f"\n{player_name}：役完成！({', '.join(yaku_list)})")
        decision = input("あがりを宣言しますか？ それともこいこいですか？ (agari/koi): ")
        return decision.strip().lower()

    # 補助的な描画メソッド
    def render_cards(self, title, cards):
        if title:
            print(title)
        if cards:
            for idx, card in enumerate(cards):
                print(f"  {idx}: {card}")
        else:
            print("  なし")
