import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from PIL import Image, ImageFilter, ImageDraw
from io import BytesIO

class image(commands.Cog, command_attrs={'cooldown': commands.Cooldown(1, 15, commands.BucketType.user)}):
    """Image manipulation commands"""
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def quantize(img):
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
    async def sharpen(self, ctx, member: discord.Member = None):
        '''Sharpens the avatar'''
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
        '''Embosses the avatar'''
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
    async def edge(self, ctx, member: discord.Member = None):
        '''Enhance the edges of the avatar'''
        if not member:
            member = ctx.author
        avatarUrl = member.avatar_url_as(size=512, format="png")
        avatar = BytesIO(await avatarUrl.read())
        image = Image.open(avatar)
        async with ctx.typing():
            image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)
        await ctx.send(file=discord.File(buffer, filename="edge.png"))

    @commands.command()
    async def pixel(self, ctx, member: discord.Member = None):
        '''Pixelizes the avatar'''
        if not member:
            member = ctx.author
        avatarUrl = member.avatar_url_as(size=512, format="png")
        avatar = BytesIO(await avatarUrl.read())
        img = Image.open(avatar)
        async with ctx.typing():
            imgSmall = img.resize((36, 36), resample=Image.BILINEAR)
            image = imgSmall.resize(img.size, Image.NEAREST)
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)
        await ctx.send(file=discord.File(buffer, filename="pixel.png"))

    @commands.command()
    async def text(self, ctx, *, text: str):
        '''Display text on an image'''
        async with ctx.typing():
            img = Image.new('RGB', (100, 50), color = (114, 137, 218))
            d = ImageDraw.Draw(img)
            d.text((10,10), text, fill=(255,255,255))
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
        await ctx.send(file=discord.File(buffer, filename="text.png"))

    @commands.command()
    async def merge(self, ctx, m1: discord.Member, m2: discord.Member = None):
        '''Merge two avatars together'''
        if not m2:
            m2 = ctx.author
        url1 = m1.avatar_url_as(size=512, format="png")
        url2 = m2.avatar_url_as(size=512, format="png")
        async with ctx.typing():
            img1 = Image.open(BytesIO(await url1.read()))
            img2 = Image.open(BytesIO(await url2.read()))
            img1.resize((512, 512))
            img1 = im1.convert("RGBA")
            img2.resize((512, 512))
            img2 = img2.convert("RGBA")
            out = Image.blend(img1, img2, 0.5)
            buffer = BytesIO()
            out.save(buffer, format="PNG")
            buffer.seek(0)
        await ctx.send(file=discord.File(buffer, filename="merge.png"))

    @commands.command()
    async def color(self, ctx, member: discord.Member = None):
        '''Colors the avatar'''
        if not member:
            member = ctx.author
        url = member.avatar_url_as(size=512, format="png")
        async with ctx.typing():
            img = BytesIO(await url.read())
            img.seek(0)
            buffer = await self.quantize(img)
        await ctx.send(file=discord.File(buffer, filename="quantize.gif"))

def setup(bot):
    bot.add_cog(image(bot))
