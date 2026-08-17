import json
import os
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, AudioFileClip

QUEUE_FILE = "data_queue.json"
IMAGE_OUTPUT = "current_frame.png"
VIDEO_OUTPUT = "youtube_short.mp4"
AUDIO_FILE = "bg_music_01.mp3"  # আপনার রিপোজিটরির মিউজিক ফাইল

# ১. ডাটা ক্যু থেকে রিড করা
def get_pending_item():
    if not os.path.exists(QUEUE_FILE):
        raise FileNotFoundError(f"{QUEUE_FILE} ফাইলটি পাওয়া যায়নি!")
    
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        data_list = json.load(f)

    for item in data_list:
        if item.get("status") == "pending":
            return item, data_list
    return None, data_list

# ২. ৩টি ক্যারোসেল ডটসহ ইনফোগ্রাফিক ইমেজ তৈরি
def generate_image(data):
    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), color=(248, 250, 252))
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arial.ttf", 55)
        card_font = ImageFont.truetype("arial.ttf", 45)
        text_font = ImageFont.truetype("arial.ttf", 32)
    except IOError:
        title_font = card_font = text_font = ImageFont.load_default()

    # Category Title
    draw.text((width // 2, 220), data["category"], fill=(15, 23, 42), font=title_font, anchor="mm")

    # 3 Good/Better/Best Cards
    ranks = [data["good"], data["better"], data["best"]]
    card_colors = [(241, 245, 249), (226, 232, 240), (254, 240, 138)]
    start_y, card_height, card_width, gap = 400, 360, 920, 50

    for i, rank_data in enumerate(ranks):
        y1 = start_y + i * (card_height + gap)
        y2 = y1 + card_height
        x1 = (width - card_width) // 2
        x2 = x1 + card_width

        draw.rounded_rectangle([x1, y1, x2, y2], radius=28, fill=card_colors[i], outline=(203, 213, 225), width=2)
        draw.text((x1 + 45, y1 + 75), f"{rank_data['rank']} - {rank_data['name']}", fill=(15, 23, 42), font=card_font)
        draw.text((x1 + 45, y1 + 175), rank_data["highlight"], fill=(51, 65, 85), font=text_font)

    # 3 Carousel Dots (1st Active)
    dot_y, dot_radius, dot_gap = height - 180, 14, 35
    total_dots_width = (3 * dot_radius * 2) + (2 * dot_gap)
    dot_start_x = (width - total_dots_width) // 2

    for i in range(3):
        cx = dot_start_x + i * (dot_radius * 2 + dot_gap) + dot_radius
        color = (37, 99, 235) if i == 0 else (203, 213, 225)
        draw.ellipse([cx - dot_radius, dot_y - dot_radius, cx + dot_radius, dot_y + dot_radius], fill=color)

    img.save(IMAGE_OUTPUT)

# ৩. ইমেজ + bg_music_01.mp3 দিয়ে ৬ সেকেন্ডের ভিডিও তৈরি
def generate_video():
    video_clip = ImageClip(IMAGE_OUTPUT).set_duration(6)
    
    # Audio integration
    if os.path.exists(AUDIO_FILE):
        audio_clip = AudioFileClip(AUDIO_FILE).subclip(0, 6)  # প্রথম ৬ সেকেন্ডের ব্যাকগ্রাউন্ড মিউজিক
        video_clip = video_clip.set_audio(audio_clip)
    
    video_clip.write_videofile(VIDEO_OUTPUT, fps=24, codec="libx264", audio_codec="aac")

# ৪. ডাটা স্ট্যাটাস আপডেট
def update_queue(used_item, data_list):
    for item in data_list:
        if item["id"] == used_item["id"]:
            item["status"] = "uploaded"
            break
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(data_list, f, indent=2)

if __name__ == "__main__":
    current_item, full_data = get_pending_item()
    if current_item:
        print(f"Processing ID {current_item['id']}: {current_item['category']}")
        generate_image(current_item)
        generate_video()
        update_queue(current_item, full_data)
        print("Success: Video generated with audio!")



