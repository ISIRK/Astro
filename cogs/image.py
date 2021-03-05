import discord, numpy, textwrap
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from PIL import Image, ImageFilter, ImageDraw, ImageOps, ImageFont
from io import BytesIO

class image(commands.Cog, command_attrs={'cooldown': commands.Cooldown(1, 15, commands.BucketType.user)}):
    """Image manipulation commands"""
    def __init__(self, bot):
        self.bot = bot
        self.invis = 0x2F3136
        
    # Static Methods

    @staticmethod
    def do_ascii(image):
        image = Image.open(image)
        sc = 0.1
        gcf = 2
        bgcolor = (13, 2, 8)
        re_list = list(
            r" .'`^\,:;Il!i><~+_-?][}{1)(|\/tfjrxn"
            r"uvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
        )
        chars = numpy.asarray(re_list)
        font = ImageFont.load_default()
        letter_width = font.getsize("x")[0]
        letter_height = font.getsize("x")[1]
        wcf = letter_height / letter_width
        img = image.convert("RGB")

        width_by_letter = round(img.size[0] * sc * wcf)
        height_by_letter = round(img.size[1] * sc)
        s = (width_by_letter, height_by_letter)
        img = img.resize(s)
        img = numpy.sum(numpy.asarray(img), axis=2)
        img -= img.min()
        img = (1.0 - img / img.max()) ** gcf * (chars.size - 1)
        lines = ("\n".join(
            ("".join(r) for r in chars[img.astype(int)]))).split("\n")
        new_img_width = letter_width * width_by_letter
        new_img_height = letter_height * height_by_letter
        new_img = Image.new("RGBA", (new_img_width, new_img_height), bgcolor)
        draw = ImageDraw.Draw(new_img)
        y = 0
        line_idx = 0
        for line in lines:
            line_idx += 1
            draw.text((0, y), line, (0, 255, 65), font=font)
            y += letter_height
        buffer = BytesIO()
        new_img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    @staticmethod
    def do_quantize(img):
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
    def do_sketch(img):
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

    @staticmethod
    def do_invert(img):
        with Image.open(img).convert("RGB") as img:
            img = ImageOps.invert(img)
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            return buffer

    @staticmethod
    def do_emboss(img):
        with Image.open(img) as img:
            img = img.filter(ImageFilter.EMBOSS)
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            return buffer
        
    @staticmethod
    def do_solarize(img):
        with Image.open(img).convert("RGB") as img:
            img = ImageOps.solarize(img, threshold=64)
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            return buffer

    @staticmethod
    def do_pixel(img):
        with Image.open(img) as img:
            img = img.resize((36, 36), resample=Image.BILINEAR)
            img = img.resize(img.size, Image.NEAREST)
            img.save(buffer, format="PNG")
            buffer = BytesIO()
            buffer.seek(0)
            return buffer
        
    # Commands

    @commands.command()
    async def emboss(self, ctx, *, member: discord.Member = None):
        '''Embosses the avatar'''
        if not member:
            member = ctx.author
        url = member.avatar_url_as(size=512, format="png")
        async with ctx.typing():
            img = BytesIO(await url.read())
            img.seek(0)
            buffer = await self.bot.loop.run_in_executor(None, self.do_emboss, img)
        file=discord.File(buffer, filename="embossed.png")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Embossed Avatar", icon_url=member.avatar_url)
        e.set_image(url="attachment://embossed.png")
        await ctx.remove(file=file, embed=e)

    @commands.command()
    async def invert(self, ctx, *, member: discord.Member = None):
        '''Invert the avatar'''
        if not member:
            member = ctx.author
        url = member.avatar_url_as(size=512, format="png")
        async with ctx.typing():
            img = BytesIO(await url.read())
            img.seek(0)
            buffer = await self.bot.loop.run_in_executor(None, self.do_invert, img)
        file=discord.File(buffer, filename="invert.png")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Inverted Avatar", icon_url=member.avatar_url)
        e.set_image(url="attachment://invert.png")
        await ctx.remove(file=file, embed=e)

    @commands.command()
    async def solarize(self, ctx, member: discord.Member = None):
        '''Solarizes the avatar'''
        if not member:
            member = ctx.author
        url = member.avatar_url_as(size=512, format="png")
        async with ctx.typing():
            img = BytesIO(await url.read())
            img.seek(0)
            buffer = await self.bot.loop.run_in_executor(None, self.do_solarize, img)
        file=discord.File(buffer, filename="solarize.png")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Solarized Avatar", icon_url=member.avatar_url)
        e.set_image(url="attachment://solarize.png")
        await ctx.remove(file=file, embed=e)

    @commands.command()
    async def pixel(self, ctx, *, member: discord.Member = None):
        '''Pixelizes the avatar'''
        if not member:
            member = ctx.author
        url = member.avatar_url_as(size=512, format="png")
        async with ctx.typing():
            img = BytesIO(await url.read())
            img.seek(0)
            buffer = await self.bot.loop.run_in_executor(None, self.do_pixel, img)
        file=discord.File(buffer, filename="pixel.png")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Pixelated Avatar", icon_url=member.avatar_url)
        e.set_image(url="attachment://pixel.png")
        await ctx.remove(file=file, embed=e)

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
            buffer = await self.bot.loop.run_in_executor(None, self.do_sketch, img)
        file=discord.File(buffer, filename="sketch.png")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Sketched Avatar", icon_url=member.avatar_url)
        e.set_image(url="attachment://sketch.png")
        await ctx.remove(file=file, embed=e)

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
        await ctx.remove(file=file, embed=e)

    @commands.command()
    async def color(self, ctx, *, member: discord.Member = None):
        '''Colors the avatar'''
        if not member:
            member = ctx.author
        url = member.avatar_url_as(size=512, format="png")
        async with ctx.typing():
            img = BytesIO(await url.read())
            img.seek(0)
            buffer = await self.bot.loop.run_in_executor(None, self.do_quantize, img)
        file=discord.File(buffer, filename="quantize.gif")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Colored Avatar", icon_url=member.avatar_url)
        e.set_image(url="attachment://quantize.gif")
        await ctx.remove(file=file, embed=e)

    @commands.command()
    async def ascii(self, ctx, *, member: discord.Member = None):
        '''Ascii the avatar'''
        if not member:
            member = ctx.author
        url = member.avatar_url_as(size=512, format="png")
        async with ctx.typing():
            img = BytesIO(await url.read())
            img.seek(0)
            buffer = await self.bot.loop.run_in_executor(None, self.do_ascii, img)
        file=discord.File(buffer, filename="ascii.png")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Ascii Avatar", icon_url=member.avatar_url)
        e.set_image(url="attachment://ascii.png")
        await ctx.remove(file=file, embed=e)

def setup(bot):
    bot.add_cog(image(bot))
