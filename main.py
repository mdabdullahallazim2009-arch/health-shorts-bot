
import os
import requests
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
from moviepy.video.fx.all import fadein

# ১. ভিডিও সেটিংস (2K / 30 FPS)
WIDTH, HEIGHT = 1440, 2560
FPS = 30
DURATION = 6.0

# ২. টেলিগ্রাম বোট সেটিংস (আপনার বোটের তথ্য দিন)
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

def send_to_telegram(video_path, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
    with open(video_path, 'rb') as video:
        payload = {'chat_id': CHAT_ID, 'caption': caption}
        files = {'video': video}
        requests.post(url, data=payload, files=files)

def create_short(quote_text, output_name):
    # ডার্ক ব্যাকগ্রাউন্ড + স্লাইট জুম
    bg = ColorClip(size=(WIDTH, HEIGHT), color=(10, 10, 10), duration=DURATION)
    bg = bg.resize(lambda t: 1 + 0.02 * t)

    # ওয়ার্ড-বাই-ওয়ার্ড টেক্সট অ্যানিমেশন
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
            font='font.ttf',  # আপনার গিটহাবের ফন্ট
            method='caption',
            size=(WIDTH - 200, None),
            align='center'
        ).set_start(start_time).set_duration(DURATION - start_time).set_position('center').fx(fadein, 0.15)
        
        text_clips.append(txt_clip)

    # বটম থ্রি-ডট (...)
    dots = TextClip("•  •  •", fontsize=50, color='gray', font='font.ttf')\
           .set_position((WIDTH // 2 - 50, HEIGHT - 250))\
           .set_duration(DURATION)\
           .set_opacity(0.6)

    # রেন্ডার
    final_video = CompositeVideoClip([bg] + text_clips + [dots], size=(WIDTH, HEIGHT)).set_duration(DURATION)
    final_video.write_videofile(output_name, fps=FPS, codec='libx264', audio=False, preset='ultrafast')

# ১২টি ভিডিও তৈরি ও টেলিগ্রামে পাঠানো
def main():
    if os.path.exists('data.json'):
        # JSON বা TXT থেকে কোট পড়া
        import json
        with open('data.json', 'r', encoding='utf-8') as f:
            quotes = json.load(f)  # লিস্ট আকারে থাকবে
            
        for i, quote in enumerate(quotes[:12]):
            video_name = f"short_{i+1}.mp4"
            create_short(quote, video_name)
            
            # টেলিগ্রামে অটো-সেন্ড
            caption = f"{quote}\n\n#Attitude #Quotes #Motivation #Shorts"
            send_to_telegram(video_name, caption)
            print(f"Video {i+1} sent to Telegram!")

if __name__ == "__main__":
    main()



