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
