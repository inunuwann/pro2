from PIL import Image
import os

# 画像を開く
image_path = "img/hanahuda.png"
image = Image.open(image_path)

# 画像のサイズを取得
img_width, img_height = image.size

# カードの行と列の数（予想）
rows = 6  # 縦のカード数
cols = 9  # 横のカード数

# カードのサイズを計算
card_width = img_width // cols
card_height = img_height // rows

# 保存ディレクトリの作成
output_dir = "iamge/"
os.makedirs(output_dir, exist_ok=True)

# カードごとに分割して保存
card_paths = []
for row in range(rows):
    for col in range(cols):
        left = col * card_width
        upper = row * card_height
        right = left + card_width
        lower = upper + card_height

        card = image.crop((left, upper, right, lower))
        card_filename = f"card_{row}_{col}.png"
        card_path = os.path.join(output_dir, card_filename)
        card.save(card_path)
        card_paths.append(card_path)

# 分割したカードのパスを表示
card_paths
