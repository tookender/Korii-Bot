from __future__ import annotations
from PIL import Image, ImageChops, ImageDraw, ImageFont
from jishaku.functools import executor_function
import discord
from io import BytesIO

FONT_BOLD_48 = ImageFont.truetype("./bot/utilities/FiraCode-Bold.ttf", 48)
FONT_BOLD_36 = ImageFont.truetype("./bot/utilities/FiraCode-Bold.ttf", 36)
FONT_BOLD_28 = ImageFont.truetype("./bot/utilities/FiraCode-Bold.ttf", 28)
FONT_BOLD_22 = ImageFont.truetype("./bot/utilities/FiraCode-Bold.ttf", 22)
FONT_MEDIUM_32 = ImageFont.truetype("./bot/utilities/FiraCode-Medium.ttf", 32)
FONT_MEDIUM_28 = ImageFont.truetype("./bot/utilities/FiraCode-Medium.ttf", 28)
FONT_MEDIUM_24 = ImageFont.truetype("./bot/utilities/FiraCode-Medium.ttf", 24)
FONT_MEDIUM_20 = ImageFont.truetype("./bot/utilities/FiraCode-Medium.ttf", 20)


def get_accent_color(image: Image.Image, palette_size=16) -> tuple[int, int, int]:
    img = image.copy()
    img.thumbnail((100, 100))

    paletted = img.convert("P", palette=Image.ADAPTIVE, colors=palette_size)

    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    palette_index = color_counts[0][1]
    accent_color = palette[palette_index * 3 : palette_index * 3 + 3] # type: ignore

    return tuple(accent_color)


def get_color_alpha(
    foreground: tuple[int, int, int], alpha: float, background: tuple[int, int, int] = (34, 40, 49)
) -> tuple[int, int, int]:
    color = []
    for f, b in zip(foreground, background):
        color.append(int(f * alpha + b * (1 - alpha)))

    return tuple(color)


async def render(user: discord.Member, level: int, current_xp: int, required_xp: int, messages: int) -> discord.File:
    template = Image.new("RGBA", (1154, 360), (36, 36, 36))
    avatar = Image.open(BytesIO(await user.avatar.read()))
    color = get_accent_color(avatar)
    mask = Image.new("L", (avatar.size[0] * 3, avatar.size[1] * 3), 0)
    mask = mask.resize(avatar.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, avatar.split()[-1])

    avatar, avatar_mask = create_outlined_rounded_rectangle(
        (192, 192), 44, 44, (57, 62, 70), get_color_alpha(color, 0.6)
    )
    template.paste(avatar, (38, 38), avatar_mask)

    buffer =  BytesIO()
    template.save(buffer, "png")
    buffer.seek(0)

    return discord.File(buffer, filename="rank.png")