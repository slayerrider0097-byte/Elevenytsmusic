# ==========================================================
# Copyright (c) 2026 Arush
# All Rights Reserved.
#
# Project      : Arush API Telegram Music Bot
# Powered By   : Arush
# Type         : API Based Telegram Music Bot
#
# Bot          : @ArushApibot
# Channel      : https://t.me/innocentpapaboltee
# GitHub       : https://github.com/Arush
#
# Unauthorized copying, modification, or redistribution
# of this source code without permission is prohibited.
# ==========================================================
import os
import re
import asyncio
import aiohttp

from PIL import (
    Image,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageFont,
    ImageOps
)

from Elevenyts import config
from Elevenyts.helpers import Track


PANEL_W, PANEL_H = 1280, 720
PANEL_X = 0
PANEL_Y = 0

THUMB_W = 520
THUMB_H = 620
THUMB_X = 45
THUMB_Y = 50

TITLE_X = 650
TITLE_Y = 105

META_Y = 170

BAR_X = 650
BAR_Y = 250

BAR_RED_LEN = 250
BAR_TOTAL_LEN = 540

ICONS_W = 420
ICONS_H = 45
ICONS_X = 690
ICONS_Y = 355

MAX_TITLE_WIDTH = 500
_f = "QXJ0aXN0Ym90cw=="


def _decode_f():
    return "❤️ Powered By ARUSH ❤️"

def trim_to_width(text: str, font, max_w: int) -> str:

    ellipsis = "…"

    if font.getlength(text) <= max_w:
        return text

    for i in range(len(text) - 1, 0, -1):

        if font.getlength(text[:i] + ellipsis) <= max_w:
            return text[:i] + ellipsis

    return ellipsis


class Thumbnail:

    def __init__(self):

        try:

            self.title_font = ImageFont.truetype(
                "Elevenyts/helpers/Raleway-Bold.ttf",
                42
            )

            self.regular_font = ImageFont.truetype(
                "Elevenyts/helpers/Inter-Light.ttf",
                24
            )

            self.signature_font = ImageFont.truetype(
                "Elevenyts/helpers/Raleway-Bold.ttf",
                28
            )

        except OSError:

            self.title_font = ImageFont.load_default()
            self.regular_font = ImageFont.load_default()
            self.signature_font = ImageFont.load_default()

    async def save_thumb(self, output_path: str, url: str):

        async with aiohttp.ClientSession() as session:

            async with session.get(url) as resp:

                with open(output_path, "wb") as f:
                    f.write(await resp.read())

        return output_path

    async def generate(self, song: Track, size=(1280, 720)) -> str:

        try:

            temp = f"cache/temp_{song.id}.jpg"
            output = f"cache/{song.id}_ultra.png"

            if os.path.exists(output):
                return output

            await self.save_thumb(temp, song.thumbnail)

            return await asyncio.get_event_loop().run_in_executor(
                None,
                self._generate_sync,
                temp,
                output,
                song,
                size
            )

        except Exception:
            return config.DEFAULT_THUMB

    def _generate_sync(
        self,
        temp: str,
        output: str,
        song: Track,
        size=(1280, 720)
    ) -> str:

        try:

            with Image.open(temp) as temp_img:
                base = temp_img.resize(size).convert("RGBA")
                template = Image.open(
    "Elevenyts/helpers/music_template.png"
).convert("RGBA").resize(size)

            bg = template.copy()

            draw = ImageDraw.Draw(bg)

            draw.text(
                (45, 22),
                _decode_f(),
                fill=(255, 255, 255, 230),
                font=self.signature_font
            )

            thumb = ImageOps.fit(
    base,
    (THUMB_W, THUMB_H),
    method=Image.LANCZOS,
    centering=(0.5, 0.5)
)

            tmask = Image.new(
                "L",
                thumb.size,
                0
            )

            ImageDraw.Draw(tmask).rounded_rectangle(
    (0, 0, thumb.width, thumb.height),
    radius=35,
    fill=255
            )

            bg.paste(
    thumb,
    (THUMB_X, THUMB_Y),
    tmask
            )

            clean_title = re.sub(
                r"\W+",
                " ",
                song.title
            ).title()

            final_title = trim_to_width(
                clean_title,
                self.title_font,
                MAX_TITLE_WIDTH
            )

            draw.text(
                (TITLE_X + 2, TITLE_Y + 2),
                final_title,
                fill=(0, 0, 0),
                font=self.title_font
            )

            draw.text(
                (TITLE_X, TITLE_Y),
                final_title,
                fill=(255, 255, 255),
                font=self.title_font
            )

            meta_text = (
                f"Now Playing  •  YouTube  •  "
                f"{song.view_count or 'Unknown Views'}"
            )

            draw.text(
                (TITLE_X, META_Y),
                meta_text,
                fill=(180, 180, 180),
                font=self.regular_font
            )

            draw.rounded_rectangle(
                (
                    BAR_X,
                    BAR_Y - 5,
                    BAR_X + BAR_TOTAL_LEN,
                    BAR_Y + 5
                ),
                radius=12,
                fill=(60, 60, 60)
            )

            draw.rounded_rectangle(
                (
                    BAR_X,
                    BAR_Y - 5,
                    BAR_X + BAR_RED_LEN,
                    BAR_Y + 5
                ),
                radius=12,
                fill=(0, 255, 255)
            )

            draw.ellipse(
                (
                    BAR_X + BAR_RED_LEN - 12,
                    BAR_Y - 12,
                    BAR_X + BAR_RED_LEN + 12,
                    BAR_Y + 12
                ),
                fill=(0, 255, 255)
            )

            draw.text(
                (BAR_X, BAR_Y + 18),
                "00:00",
                fill="white",
                font=self.regular_font
            )

            is_live = getattr(song, "is_live", False)

            end_text = "LIVE" if is_live else song.duration

            draw.text(
                (BAR_X + BAR_TOTAL_LEN - 80, BAR_Y + 18),
                end_text,
                fill=(0, 255, 255) if is_live else "white",
                font=self.regular_font
            )

            icons_path = "Elevenyts/helpers/play_icons.png"

            if os.path.isfile(icons_path):

                with Image.open(icons_path) as icons_img:

                    ic = icons_img.resize(
                        (ICONS_W, ICONS_H)
                    ).convert("RGBA")

                    r, g, b, a = ic.split()

                    cyan_ic = Image.merge(
                        "RGBA",
                        (
                            r.point(lambda _: 0),
                            g.point(lambda _: 255),
                            b.point(lambda _: 255),
                            a
                        )
                    )

                    bg.paste(
                        cyan_ic,
                        (ICONS_X, ICONS_Y),
                        cyan_ic
                    )

            bg.save(output)

            try:
                os.remove(temp)

            except OSError:
                pass

            return output

        except Exception:
            return config.DEFAULT_THUMB
