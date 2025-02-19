import os
import tkinter as tk
from PIL import Image, ImageTk

class HanafudaGameGUI:
    def __init__(self, root, img_folder):
        self.root = root
        self.root.title("Hanafuda Game")

        self.img_folder = img_folder
        self.card_back = ImageTk.PhotoImage(Image.open(os.path.join(img_folder, "black.png")).resize((50, 80), Image.LANCZOS))

        self.sample_cards = []
        card_indices = [(0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (0,7), (1,0), (2,1), (3,2), (4,3), (5,4), (3,5), (2,6), (1,7)]
        for i, j in card_indices:
            try:
                img = ImageTk.PhotoImage(Image.open(os.path.join(img_folder, f"card_{i}_{j}.png")).resize((50, 80), Image.LANCZOS))
                self.sample_cards.append(img)
            except FileNotFoundError:
                print(f"Warning: Missing image card_{i}_{j}.png")
                self.sample_cards.append(self.card_back)  # Fallback to card back if missing

        # CPUの手札 (裏向き 8枚)
        self.cpu_hand = tk.Frame(root)
        self.cpu_hand.pack()
        for _ in range(8):
            tk.Label(self.cpu_hand, image=self.card_back).pack(side=tk.LEFT, padx=5)

        # CPUの出来札 (4枚)
        self.cpu_pile = tk.Frame(root)
        self.cpu_pile.pack()
        for i in range(4):
            tk.Label(self.cpu_pile, image=self.sample_cards[i]).pack(side=tk.LEFT, padx=5)

        # スペース
        tk.Label(root, text="\n").pack()

        # 場札 (6枚)
        self.field = tk.Frame(root)
        self.field.pack()
        for i in range(4, 10):
            tk.Label(self.field, image=self.sample_cards[i]).pack(side=tk.LEFT, padx=5)

        # スペース
        tk.Label(root, text="\n").pack()

        # ユーザーの出来札 (4枚)
        self.user_pile = tk.Frame(root)
        self.user_pile.pack()
        for i in range(10, 14):
            tk.Label(self.user_pile, image=self.sample_cards[i]).pack(side=tk.LEFT, padx=5)

        # 自分の手札 (7枚)
        self.user_hand = tk.Frame(root)
        self.user_hand.pack()
        for i in range(14, 15):
            tk.Label(self.user_hand, image=self.sample_cards[i]).pack(side=tk.LEFT, padx=5)

if __name__ == "__main__":
    img_folder = "iamge"  # 画像フォルダのパスを指定
    if not os.path.exists(img_folder):
        print("Image folder not found! Please place images in 'img' folder.")
    else:
        root = tk.Tk()
        game_gui = HanafudaGameGUI(root, img_folder)
        root.mainloop()
