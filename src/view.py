# src/view.py

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

# ダミーの View はテスト用に用意
class DummyView(View):
    def __init__(self):
        self.messages = []
    
    def display_message(self, message):
        self.messages.append(message)
        
    def display_cards(self, title, cards):
        msg = f"{title} " + ", ".join(str(card) for card in cards) if cards else title + " なし"
        self.messages.append(msg)
        
    def get_input(self, prompt):
        self.messages.append(prompt)
        return "0"
    
    def choose_from_list(self, prompt, items):
        self.display_cards(prompt, items)
        return 0

