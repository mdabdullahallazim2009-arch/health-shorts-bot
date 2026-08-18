import os
import requests
import json
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
from moviepy.video.fx.all import fadein

# ১. টেলিগ্রাম বোট সেটিংস
BOT_TOKEN = "8919388077:AAEbXtcd_4FE6VNrp-N9HgKpe_niRrW3tqM"
CHAT_ID = "-1004368928162"

# ২. ভিডিও সেটিংস (2K Resolution)
WIDTH, HEIGHT = 1440, 2560
FPS = 30
DURATION = 6.0

def send_to_telegram(video_path, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
    with open(video_path, 'rb') as video:
        payload = {'chat_id': CHAT_ID, 'caption': caption}
        files = {'video': video}
        response = requests.post(url, data=payload, files=files)
        return response

def create_short(quote_text, output_name):
    bg = ColorClip(size=(WIDTH, HEIGHT), color=(10, 10, 10), duration=DURATION)
    bg = bg.resize(lambda t: 1 + 0.02 * t)

    words = quote_text.split()
    time_per_word = (DURATION - 1.5) / max(len(words), 1)
    text_clips = []
    accumulated_text = ""

    for i, word in enumerate(words):
        accumulated_text += word + " "
        start_time = i * time_per_word
        txt_clip = TextClip(
            accumulated_text.strip(),
            fontsize=75,
            color='white',
            font='font.ttf', 
            method='caption',
            size=(WIDTH - 200, None),
            align='center'
        ).set_start(start_time).set_duration(DURATION - start_time).set_position('center').fx(fadein, 0.15)
        text_clips.append(txt_clip)

    dots = TextClip("•  •  •", fontsize=50, color='gray', font='font.ttf')\
           .set_position((WIDTH // 2 - 50, HEIGHT - 250))\
           .set_duration(DURATION)\
           .set_opacity(0.6)

    final_video = CompositeVideoClip([bg] + text_clips + [dots], size=(WIDTH, HEIGHT)).set_duration(DURATION)
    final_video.write_videofile(output_name, fps=FPS, codec='libx264', audio=False, preset='ultrafast')

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
