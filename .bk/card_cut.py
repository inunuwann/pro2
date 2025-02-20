# Update the number of rows and columns based on the user's correction
rows = 6
cols = 8

# Recalculate individual card size
card_width = img_width // cols
card_height = img_height // rows

# Clear previous outputs and create a new directory
output_dir = "/mnt/data/hanahuda_cards_corrected"
os.makedirs(output_dir, exist_ok=True)

# Crop and save each card again
corrected_card_images = []
for row in range(rows):
    for col in range(cols):
        left = col * card_width
        upper = row * card_height
        right = left + card_width
        lower = upper + card_height
        card = image.crop((left, upper, right, lower))
        card_path = f"{output_dir}/card_{row}_{col}.png"
        card.save(card_path)
        corrected_card_images.append(card_path)

# Display one of the newly cropped images as a sample
corrected_card_images[:5]  # Showing first few card paths as output
