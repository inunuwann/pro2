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

    def show_game_result(self):
        """ゲーム終了後にスコアを表示"""
        self.view.display_message("\n=== ゲーム終了 ===")

        for p in self.board.players:
            captured_set = Cardset(p.captured)
            yaku = captured_set.check_yaku()
            score = captured_set.calculate_score()
            self.view.display_final_score(p, score, yaku)

