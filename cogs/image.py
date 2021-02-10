import discord
from discord.ext import commands
from PIL import Image, ImageFilter
from io import BytesIO

class image(commands.Cog):
    """Image manipulation commands"""

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def Quantize(url:str):
        img = BytesIO(await url.read())
        with Image.open(img) as image:
            siz = 300
            newsize = (siz,siz)

            w, h = image.size
            if w > h:
                the_key = w / siz
                image = image.resize((siz,int(h / the_key))).convert("RGBA")
            elif h > w:
                the_key = h / siz
                image = image.resize((int(w / the_key),siz)).convert("RGBA")
            else:
                image = image.resize(newsize).convert("RGBA")

            images1 = []
            for i in range(60):
                try:
                    im = image.copy()
                    im = im.quantize(colors=i + 1, method=2)
                    images1.append(im)
                except:
                    break

            images2 = list(reversed(images1))
            images = images1 + images2

            buffer = BytesIO()
            images[0].save(buffer,
                           format='gif',
                           save_all=True,
                           append_images=images[1:],
                           duration=1,
                           loop=0)
            buffer.seek(0)
            return buffer

    @commands.command()
    async def flip(self, ctx, member: discord.Member = None):
        """Flips the avatar"""
        if not member:
            member = ctx.author
        avatarUrl = member.avatar_url_as(size=512, format="png")
        avatar = BytesIO(await avatarUrl.read())
        image = Image.open(avatar)
        async with ctx.typing():
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
        async with ctx.typing():
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
        async with ctx.typing():
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

    @commands.command()
    async def color(self, ctx, member: discord.Member = None):
        """Colors the avatar"""
        if not member:
            member = ctx.author
        url = member.avatar_url_as(size=512, format="png")
        async with ctx.typing():
            buffer = self.Quantize(str(url))
        await ctx.send(file=discord.File(buffer, filename="quantize.gif"))

def setup(bot):
    bot.add_cog(image(bot))
