import json
from PIL import Image, ImageDraw

# ১. ডাটা রিড করা
with open('data.json', 'r') as f:
    data = json.load(f)

item = data[0]

# ২. ছবি লোড করা
image = Image.open('protein_01.png')
draw = ImageDraw.Draw(image)

# ৩. ছবির ওপর টেক্সট বসানো
draw.text((50, 50), item['category'], fill="white")
draw.text((50, 120), item['title'], fill="yellow")

# ৪. আউটপুট সেভ করা
image.save('output_frame.png')
print("Frame created successfully!")
