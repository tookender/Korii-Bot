import aggdraw
from PIL import Image, ImageFont, ImageDraw
from dataclasses import dataclass
import discord
from io import BytesIO


def generate_rounded_corners(image: Image.Image, radius):
    """generate round corner for image"""
    mask = Image.new('L', image.size) # filled with black by default
    draw = aggdraw.Draw(mask)
    brush = aggdraw.Brush('white')
    width, height = mask.size
    #upper-left corner
    draw.pieslice((0,0,radius*2, radius*2), 90, 180, None, brush)
    #upper-right corner
    draw.pieslice((width - radius*2, 0, width, radius*2), 0, 90, None, brush)
    #bottom-left corner
    draw.pieslice((0, height - radius * 2, radius*2, height),180, 270, None, brush)
    #bottom-right corner
    draw.pieslice((width - radius * 2, height - radius * 2, width, height), 270, 360, None, brush)
    #center rectangle
    draw.rectangle((radius, radius, width - radius, height - radius), brush)
    #four edge rectangle
    draw.rectangle((radius, 0, width - radius, radius), brush)
    draw.rectangle((0, radius, radius, height-radius), brush)
    draw.rectangle((radius, height-radius, width-radius, height), brush)
    draw.rectangle((width-radius, radius, width, height-radius), brush)
    draw.flush()
    image = image.convert('RGBA')
    image.putalpha(mask)
    return image



class GoKillYourself:
    def __init__(self, member: discord.Member):
        # User
        self.member = member
        self.display_name = member.display_name[:8] + ("..." if len(member.display_name) > 8 else "")
        self.name = str(member)[:16] + ("..." if len(str(member)) > 16 else "")

        # Colors
        self.WHITE = (230, 230, 230)
        self.GRAY = (140, 140, 140)

        # Fonts
        self.SMALL = ImageFont.truetype("./bot/assets/fonts/Roboto-Bold.ttf", 34)
        self.MEDIUM = ImageFont.truetype("./bot/assets/fonts/Roboto-Bold.ttf", 42)
        self.BIG = ImageFont.truetype("./bot/assets/fonts/Roboto-Black.ttf")
        self.VERY_BIG = ImageFont.truetype("./bot/assets/fonts/Roboto-Black.ttf", 56)

        # PIL
        self.image = Image.new("RGBA", (1200, 400), (36, 36, 36))
        self.draw = ImageDraw.Draw(self.image)
        

    async def paste_avatar(self, coordinates: tuple[int, int]) -> None:
        avatar = Image.open(BytesIO(await self.member.avatar.read()))
        avatar = generate_rounded_corners(image=avatar, radius=avatar.width // 6)
        avatar.resize((290, 290))

        self.image.paste(avatar, coordinates, avatar)
    
    def generate_text(self):
        box = (350, 25, 700, 75)
        font_size = 52

        size = None
        font = None
        while (size is None or size[0] > box[2] or size[1] > box[3] - box[1]) and font_size > 0:
            font = ImageFont.truetype("./bot/assets/fonts/Roboto-Black.ttf", font_size)
            size = font.getsize_multiline(self.member.display_name)
            font_size -= 1
        
        self.draw.multiline_text((box[0], box[1]), self.member.display_name, self.WHITE, font)

    async def generate(self) -> discord.File:
        await self.paste_avatar((25, 25))
        self.generate_text()
        
        self.image.save("card.png")
        return discord.File("card.png")



def go_kill_yourself(image: Image.Image, draw: ImageDraw.ImageDraw):
    top_text = f"Rank #0000"
    bottom_text = f"out of 0000 users"

    # Top text (tt)
    ttfont = ImageFont.truetype('./bot/assets/fonts/Roboto-Bold.ttf', 60)
    _, _, ttx, tty = draw.textbbox((0, 0), top_text, font=ttfont)

    # Bottom Text (bt) needs font calculation
    btfont = ImageFont.truetype('./bot/assets/fonts/Roboto-Bold.ttf', 60)
    btx = 0
    bty = 0
    for i in range(59, 25, -1):
        _, _, btx, bty = draw.textbbox((0, 0), bottom_text, font=btfont)
        if btx <= ttx:
            break
        btfont = ImageFont.truetype('./bot/assets/fonts/Roboto-Bold.ttf', i)

    padl = 10 + 50 + 25
    baseh = 10 + 50

    draw.text((padl, baseh - tty - bty), top_text, 'white', font=ttfont)
    draw.text((padl, baseh - bty), bottom_text, font=btfont, fill=(140, 140, 140))

    # Left side text stack
    height = baseh
    to_rm = bty
    width = 1200 - 50

    text = f"0000 messages deleted"
    _, _, msx, _ = draw.textbbox((0, 0), text, font=btfont)
    height -= to_rm
    draw.text((width - msx, height), text, font=btfont, fill=(140, 140, 140))

    text = f"0000 messages edited"
    _, _, msx, _ = draw.textbbox((0, 0), text, font=btfont)
    height -= to_rm
    draw.text((width - msx, height), text, font=btfont, fill=(140, 140, 140))

    text = f"0000 messages sent"
    _, _, msx, _ =draw.textbbox((0, 0), text, font=btfont)
    height -= to_rm
    draw.text((width - msx, height), text, font=btfont, fill=(140, 140, 140))