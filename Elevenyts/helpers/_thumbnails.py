# Static Background Thumbnail Generator (Arush Edition)
# Replace your existing _thumbnails.py with this version's logic.

from PIL import Image, ImageDraw, ImageFont
import os

BACKGROUND = "Elevenyts/helpers/background.png"  # <-- Your fixed background image


class Thumbnail:
    def __init__(self):
        try:
            self.title_font = ImageFont.truetype("Elevenyts/helpers/Raleway-Bold.ttf", 44)
            self.meta_font = ImageFont.truetype("Elevenyts/helpers/Inter-Light.ttf", 28)
        except Exception:
            self.title_font = ImageFont.load_default()
            self.meta_font = ImageFont.load_default()

    async def generate(self, song, size=(1280, 720)):
        bg = Image.open(BACKGROUND).convert("RGBA").resize(size)
        draw = ImageDraw.Draw(bg)

        title = getattr(song, "title", "Unknown Song")
        duration = getattr(song, "duration", "00:00")
        requester = getattr(song, "requested_by", None)
        if requester:
            requester = getattr(requester, "first_name", str(requester))
        else:
            requester = "Unknown"

        draw.text((70, 470), title, fill="white", font=self.title_font)
        draw.text((70, 540), f"Requested By : {requester}", fill="white", font=self.meta_font)
        draw.text((70, 580), f"Duration : {duration}", fill="white", font=self.meta_font)

        # Progress bar
        x1, y1 = 70, 640
        width = 1140
        draw.rounded_rectangle((x1, y1, x1 + width, y1 + 12), radius=8, fill=(70, 70, 70))
        progress = int(width * 0.35)
        draw.rounded_rectangle((x1, y1, x1 + progress, y1 + 12), radius=8, fill=(220, 40, 40))
        draw.ellipse((x1 + progress - 10, y1 - 10, x1 + progress + 10, y1 + 22), fill=(220, 40, 40))
        draw.text((70, 660), "00:00", fill="white", font=self.meta_font)
        draw.text((1120, 660), duration, fill="white", font=self.meta_font)

        os.makedirs("cache", exist_ok=True)
        out = f"cache/{getattr(song,'id','thumb')}_static.png"
        bg.save(out)
        return out
