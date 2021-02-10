import discord
from discord.ext import commands
from PIL import Image, ImageFilter
from io import BytesIO

class image(commands.Cog):
    """Image manipulation commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def flip(self, ctx, member: discord.Member = None):
        """Flips the avatar"""
        if not member:
            member = ctx.author
        avatarUrl = member.avatar_url_as(size=512, format="png")
        avatar = BytesIO(await avatarUrl.read())
        image = Image.open(avatar)

        image = image.rotate(180)
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        await ctx.send(file=discord.File(buffer, filename="flip.png"))

    @commands.command()
    async def blur(self, ctx, member: discord.Member = None):
        """Blurs the avatar"""
        if not member:
            member = ctx.author
        avatarUrl = member.avatar_url_as(size=512, format="png")
        avatar = BytesIO(await avatarUrl.read())
        image = Image.open(avatar)

        image = image.filter(ImageFilter.BLUR)
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        await ctx.send(file=discord.File(buffer, filename="blur.png"))

    @commands.command()
    async def sharpen(self, ctx, member: discord.Member = None):
        """Sharpens the avatar"""
        if not member:
            member = ctx.author
        avatarUrl = member.avatar_url_as(size=512, format="png")
        avatar = BytesIO(await avatarUrl.read())
        image = Image.open(avatar)

        image = image.filter(ImageFilter.SHARPEN)
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        await ctx.send(file=discord.File(buffer, filename="sharpen.png"))

    @commands.command()
    async def emboss(self, ctx, member: discord.Member = None):
        """Embosses the avatar"""
        if not member:
            member = ctx.author
        avatarUrl = member.avatar_url_as(size=512, format="png")
        avatar = BytesIO(await avatarUrl.read())
        image = Image.open(avatar)
        async with ctx.typing():
            image = image.filter(ImageFilter.EMBOSS)
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)
        await ctx.send(file=discord.File(buffer, filename="emboss.png"))

def setup(bot):
    bot.add_cog(image(bot))
