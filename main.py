import json
import os
from PIL import Image, ImageDraw, ImageFont

def generate_video_frame():
    # ১. ডাটা ফাইল লোড
    if not os.path.exists('data.json'):
        print("Error: data.json not found!")
        return

    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # পেন্ডিং কন্টেন্ট নির্বাচন
    item = next((x for x in data if x.get('status') == 'pending'), None)

    if not item:
        print("No pending topics found in data.json!")
        return

    # ২. ক্যানভাস সাইজ (ইউটিউব শর্টস ১০৮০x১৯২০)
    width, height = 1080, 1920
    img = Image.new('RGB', (width, height), color='#0F172A')
    draw = ImageDraw.Draw(img)

    # ফন্ট সেটআপ (Montserrat/Poppins না থাকলে সিস্টেমের ডিফল্ট ফন্ট ব্যবহার করবে)
    try:
        font_hook = ImageFont.truetype("font.ttf", 52)
        font_card = ImageFont.truetype("font.ttf", 42)
    except:
        font_hook = font_card = ImageFont.load_default()

    # ৩. কার্ড ও টেক্সট রেন্ডারিং
    # মূল প্রশ্ন / হুক
    draw.text((width // 2, 350), item['hook'], fill="#F8FAFC", font=font_hook, anchor="mm")

    # কার্ড ১: GOOD (🥉 Bronze Border)
    draw.rounded_rectangle([90, 600, 990, 780], radius=24, fill="#1E293B", outline="#475569", width=3)
    draw.text((width // 2, 690), item['good'], fill="#CBD5E1", font=font_card, anchor="mm")

    # কার্ড ২: BETTER (🥈 Cyan Border)
    draw.rounded_rectangle([90, 850, 990, 1030], radius=24, fill="#1E293B", outline="#38BDF8", width=4)
    draw.text((width // 2, 940), item['better'], fill="#38BDF8", font=font_card, anchor="mm")

    # কার্ড ৩: BEST / WINNER (🥇 Golden Glow Border)
    draw.rounded_rectangle([80, 1100, 1000, 1340], radius=30, fill="#1E293B", outline="#FACC15", width=8)
    draw.text((width // 2, 1220), item['best'], fill="#FACC15", font=font_card, anchor="mm")

    # ৪. ইমেজ সেভ করা
    img.save("final_frame.png")
    print(f"Successfully generated frame for Topic ID: {item['id']}")

    # ৫. ডাটা আপডেট করা (pending -> done)
    item['status'] = 'done'
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    generate_video_frame()



