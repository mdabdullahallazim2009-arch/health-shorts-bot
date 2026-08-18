import os
import requests
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip

BOT_TOKEN = "8919388077:AAEbXtcd_4FE6VNrp-N9HgKpe_niRrW3tqM"
CHAT_ID = "-1004368928162"

WIDTH, HEIGHT = 1080, 1920
FPS = 30
DURATION = 6.0

def send_to_telegram(video_path, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
    with open(video_path, 'rb') as video:
        payload = {'chat_id': CHAT_ID, 'caption': caption}
        files = {'video': video}
        return requests.post(url, data=payload, files=files)

def create_text_image(text):
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(10, 10, 10))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype('font.ttf', 55)
    except:
        font = ImageFont.load_default()

    words = text.split()
    lines, current_line = [], []
    for word in words:
        current_line.append(word)
        bbox = draw.textbbox((0, 0), " ".join(current_line), font=font)
        if bbox[2] > WIDTH - 160:
            current_line.pop()
            lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    
    full_text = "\n".join(lines)
    bbox = draw.multiline_textbbox((0, 0), full_text, font=font, align="center")
    x = (WIDTH - (bbox[2] - bbox[0])) // 2
    y = (HEIGHT - (bbox[3] - bbox[1])) // 2
    
    draw.multiline_text((x, y), full_text, fill=(255, 255, 255), font=font, align="center")
    
    dots = "•  •  •"
    d_bbox = draw.textbbox((0, 0), dots, font=font)
    draw.text(((WIDTH - (d_bbox[2] - d_bbox[0])) // 2, HEIGHT - 220), dots, fill=(130, 130, 130), font=font)

    return np.array(img)

def create_short(quote_text, output_name):
    frame_np = create_text_image(quote_text)
    clip = ImageClip(frame_np).set_duration(DURATION)
    clip.write_videofile(output_name, fps=FPS, codec='libx264', audio=False, preset='ultrafast')

def main():
    if os.path.exists('data.json'):
        with open('data.json', 'r', encoding='utf-8') as f:
            quotes = json.load(f)
            
        for i, quote in enumerate(quotes[:12]):
            video_name = f"short_{i+1}.mp4"
            print(f"ভিডিও {i+1} তৈরি হচ্ছে...")
            create_short(quote, video_name)
            
            caption = f"{quote}\n\n#Attitude #Quotes #Motivation #Shorts"
            print(f"ভিডিও {i+1} টেলিগ্রামে পাঠানো হচ্ছে...")
            send_to_telegram(video_name, caption)
            print(f"✅ ভিডিও {i+1} সফলভাবে সেন্ড হয়েছে!")

if __name__ == "__main__":
    main()
