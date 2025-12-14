from telethon import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import pytz

api_id = 36928371
api_hash = "f9a57924aa8167c3dea10a40ae9fcdff"

tz = pytz.timezone("Asia/Tashkent")
client = TelegramClient("session", api_id, api_hash)

def generate_avatar():
    img = Image.new("RGB", (1024, 1024), "black")
    draw = ImageDraw.Draw(img)

    time_str = datetime.now(tz).strftime("%H:%M")

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 300)
    except:
        font = ImageFont.load_default()

    layer = Image.new("RGBA", img.size)
    d = ImageDraw.Draw(layer)

    w, h = d.textsize(time_str, font=font)
    x = (1024 - w) // 2
    y = (1024 - h) // 2

    d.text((x, y), time_str, font=font, fill=(0, 255, 255, 255))
    glow = layer.filter(ImageFilter.GaussianBlur(30))

    img = Image.alpha_composite(img.convert("RGBA"), glow)
    img = Image.alpha_composite(img, layer)

    img.convert("RGB").save("avatar.jpg", quality=95)

def update_avatar():
    generate_avatar()
    with client:
        client(UploadProfilePhotoRequest(
            file=client.upload_file("avatar.jpg")
        ))
        print("Avatar updated")

scheduler = BlockingScheduler()
scheduler.add_job(update_avatar, "interval", minutes=1)

with client:
    update_avatar()
    scheduler.start()
