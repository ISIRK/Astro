import discord, numpy, textwrap
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from PIL import Image, ImageFilter, ImageDraw, ImageChops
from io import BytesIO

class image(commands.Cog, command_attrs={'cooldown': commands.Cooldown(1, 15, commands.BucketType.user)}):
    """Image manipulation commands"""
    def __init__(self, bot):
        self.bot = bot
        self.invis = 0x2F3136

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

    @staticmethod
    async def do_sketch(img):
        ele = numpy.pi/2.2
        azi = numpy.pi/4.
        dep = 10.

        with Image.open(img).convert('L') as img:
            a = numpy.asarray(img).astype('float')
            grad = numpy.gradient(a)
            grad_x, grad_y = grad
            gd = numpy.cos(ele)
            dx = gd*numpy.cos(azi)
            dy = gd*numpy.sin(azi)
            dz = numpy.sin(ele)
            grad_x = grad_x*dep/100.
            grad_y = grad_y*dep/100.
            leng = numpy.sqrt(grad_x**2 + grad_y**2 + 1.)
            uni_x = grad_x/leng
            uni_y = grad_y/leng
            uni_z = 1./leng
            a2 = 255*(dx*uni_x + dy*uni_y + dz*uni_z)
            a2 = a2.clip(0,255)
            img2 = Image.fromarray(a2.astype('uint8')) 
            buffer = BytesIO()
            img2.save(buffer, format="PNG")
            buffer.seek(0)
            return buffer

    @commands.command()
    async def sharpen(self, ctx, *, member: discord.Member = None):
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
        file=discord.File(buffer, filename="sharpen.png")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Sharpened Avatar", icon_url=member.avatar_url)
        e.set_image(url="attachment://sharpen.png")
        await ctx.send(file=file, embed=e)

    @commands.command()
    async def emboss(self, ctx, *, member: discord.Member = None):
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
        file=discord.File(buffer, filename="emboss.png")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Embossed Avatar", icon_url=member.avatar_url)
        e.set_image(url="attachment://emboss.png")
        await ctx.send(file=file, embed=e)

    @commands.command()
    async def invert(self, ctx, *, member: discord.Member = None):
        '''Inverts the avatar'''
        if not member:
            member = ctx.author
        avatarUrl = member.avatar_url_as(size=512, format="png")
        avatar = BytesIO(await avatarUrl.read())
        image = Image.open(avatar)
        async with ctx.typing():
            image = ImageChops.invert(image)
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)
        file=discord.File(buffer, filename="invert.png")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Inverted Avatar", icon_url=member.avatar_url)
        e.set_image(url="attachment://invert.png")
        await ctx.send(file=file, embed=e)

    @commands.command()
    async def edge(self, ctx, *, member: discord.Member = None):
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
        file=discord.File(buffer, filename="edge.png")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Edges Enhanced Avatar", icon_url=member.avatar_url)
        e.set_image(url="attachment://edge.png")
        await ctx.send(file=file, embed=e)

    @commands.command()
    async def pixel(self, ctx, *, member: discord.Member = None):
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
        file=discord.File(buffer, filename="pixel.png")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Pixelated Avatar", icon_url=member.avatar_url)
        e.set_image(url="attachment://pixel.png")
        await ctx.send(file=file, embed=e)

    @commands.command()
    async def text(self, ctx, *, text: str):
        '''Display text on an image'''
        async with ctx.typing():
            img = Image.new('RGB', (200, 100), color = (114, 137, 218))
            d = ImageDraw.Draw(img)
            text = '\n'.join(textwrap.wrap(text, width=50))
            d.text((10,10), text, fill='white')
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
        await ctx.send(file=discord.File(buffer, filename="text.png"))

    @commands.command()
    async def sketch(self, ctx, *, member: discord.Member = None):
        '''Sketches the avatar'''
        if not member:
            member = ctx.author
        url = member.avatar_url_as(size=512, format="png")
        async with ctx.typing():
            img = BytesIO(await url.read())
            img.seek(0)
            buffer = await self.do_sketch(img)
        file=discord.File(buffer, filename="sketch.png")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Sketched Avatar", icon_url=member.avatar_url)
        e.set_image(url="attachment://sketch.png")
        await ctx.send(file=file, embed=e)

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
            img1 = img1.resize((512, 512))
            img1 = img1.convert("RGBA")
            img2 = img2.resize((512, 512))
            img2 = img2.convert("RGBA")
            out = Image.blend(img1, img2, 0.5)
            buffer = BytesIO()
            out.save(buffer, format="PNG")
            buffer.seek(0)
        file=discord.File(buffer, filename="merge.png")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Merged Avatars", icon_url=m1.avatar_url)
        e.set_image(url="attachment://merge.png")
        await ctx.send(file=file, embed=e)

    @commands.command()
    async def color(self, ctx, *, member: discord.Member = None):
        '''Colors the avatar'''
        if not member:
            member = ctx.author
        url = member.avatar_url_as(size=512, format="png")
        async with ctx.typing():
            img = BytesIO(await url.read())
            img.seek(0)
            buffer = await self.quantize(img)
        file=discord.File(buffer, filename="quantize.gif")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Colored Avatar", icon_url=member.avatar_url)
        e.set_image(url="attachment://quantize.gif")
        await ctx.send(file=file, embed=e)

def setup(bot):
    bot.add_cog(image(bot))
