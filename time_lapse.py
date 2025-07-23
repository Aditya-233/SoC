import imageio
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

# List your NDVI change image filenames with year labels
image_files = [
    ('NDVI_Change_2010-2011.png', '2010-2011'),
    ('NDVI_Change_2011-2013.png', '2011-2013'),
    ('NDVI_Change_2013-2014.png', '2013-2014'),
    ('NDVI_Change_2014-2015.png', '2014-2015'),
    ('NDVI_Change_2015-2016.png', '2015-2016'),
    ('NDVI_Change_2016-2017.png', '2016-2017'),
    ('NDVI_Change_2017-2018.png', '2017-2018'),
    ('NDVI_Change_2018-2019.png', '2018-2019'),
    ('NDVI_Change_2019-2020.png', '2019-2020'),
    ('NDVI_Change_2020-2021.png', '2020-2021'),
    ('NDVI_Change_2021-2022.png', '2021-2022'),
    ('NDVI_Change_2022-2023.png', '2022-2023'),
    ('NDVI_Change_2023-2024.png', '2023-2024')
]

# Enhance contrast and color
def enhance_image(img):
    img = ImageEnhance.Contrast(img).enhance(1.3)
    img = ImageEnhance.Color(img).enhance(1.2)
    return img

# Create a legend image
def create_legend():
    legend_width, legend_height = 200, 60
    legend_img = Image.new('RGBA', (legend_width, legend_height), (255, 255, 255, 200))
    draw = ImageDraw.Draw(legend_img)
    colors = [(255, 0, 0), (0, 128, 0)]
    labels = ['NDVI Loss', 'NDVI Gain']
    for i, (color, label) in enumerate(zip(colors, labels)):
        draw.rectangle([10, 10 + i*25, 30, 30 + i*25], fill=color)
        draw.text((40, 10 + i*25), label, fill='black')
    return legend_img

# Load a font
try:
    font = ImageFont.truetype("arial.ttf", 20)
except:
    font = ImageFont.load_default()

legend_img = create_legend()
images = []

for filename, year_label in image_files:
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        continue
    img = Image.open(filename).convert('RGBA')
    img = enhance_image(img)
    draw = ImageDraw.Draw(img)

    # Add year label
    draw.rectangle([5, 5, 150, 35], fill=(255, 255, 255, 180))
    draw.text((10, 8), year_label, fill='black', font=font)

    # Add title
    title = "NDVI Change Map"
    bbox = draw.textbbox((0, 0), title, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.rectangle([(img.width//2 - w//2 - 10), 5, (img.width//2 + w//2 + 10), 35], fill=(255, 255, 255, 180))
    draw.text((img.width//2 - w//2, 8), title, fill='black', font=font)

    # Add legend
    img.paste(legend_img, (img.width - legend_img.width - 10, img.height - legend_img.height - 10), legend_img)

    images.append(img)

# Save as GIF if images are loaded
if images:
    images[0].save(
        'NDVI_Change_2010-2024_Enhanced.gif',
        save_all=True,
        append_images=images[1:],
        duration=800,
        loop=0
    )
    print("GIF created: NDVI_Change_2010-2024_Enhanced.gif")
else:
    print("No images loaded, GIF not created.")
