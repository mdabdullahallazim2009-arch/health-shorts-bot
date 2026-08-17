
import json
import os
from PIL import Image, ImageDraw

# ১. ডাটা লোড করা
with open('data.json', 'r') as f:
    data = json.load(f)

item = data[0]

# ২. ১০৮০x১৯২০ ফুল এইচডি শর্টস ক্যানভাস তৈরি
target_w, target_h = 1080, 1920
bg_img = Image.open('protein_01.png').convert('RGB')
bg_img = bg_img.resize((target_w, target_h))

draw = ImageDraw.Draw(bg_img)

# ৩. সাইন্টিফিক টেক্সট লেআউট বসানো
# বোল্ড ক্যাটাগরি হেডার
draw.text((target_w // 2, 250), item['category'], fill='#FFD700', anchor="mm")

# টাইটেল ও নিউট্রিয়েন্ট তথ্য
draw.text((target_w // 2, 450), item['title'], fill='#FFFFFF', anchor="mm")
draw.text((target_w // 2, 850), f"{item['item_a_label']} : {item['item_a_val']}", fill='#00FF66', anchor="mm")
draw.text((target_w // 2, 1050), f"{item['item_b_label']} : {item['item_b_val']}", fill='#FF4444', anchor="mm")

# ৪. ক্যারোসেল ডটস (Bottom Growth Hack)
dot_y, dot_r, spacing = 1750, 12, 40
start_x = (target_w // 2) - (1.5 * spacing)

for i in range(4):
    x = start_x + (i * spacing)
    color = '#FFD700' if i == 0 else '#777777' # প্রথম ডটটি একটিভ থাকবে
    draw.ellipse([x - dot_r, dot_y - dot_r, x + dot_r, dot_y + dot_r], fill=color)

# ৫. ফ্রেম ও ৭ সেকেন্ডের HD MP4 ভিডিও তৈরি
os.makedirs('output', exist_ok=True)
bg_img.save('output/final_frame.png')

os.system("ffmpeg -y -loop 1 -i output/final_frame.png -i bg_music_01.mp3 -c:v libx264 -t 7 -pix_fmt yuv420p -shortest output/final_video.mp4")
print("Scientific Shorts Video Created Successfully!")
