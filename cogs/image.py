import discord, numpy, textwrap
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from PIL import Image, ImageFilter, ImageDraw, ImageOps, ImageFont
from io import BytesIO

class image(commands.Cog, command_attrs={'cooldown': commands.Cooldown(1, 10, commands.BucketType.user)}):
    """Image manipulation commands"""
    def __init__(self, bot):
        self.bot = bot
        self.invis = 0x2F3136
        
    # Static Methods

    @staticmethod
    def do_meme(img, text: str):
        with Image.open(img) as tv:
            wid = tv.size[0]
            hei = tv.size[0]
            if 0 < wid < 200:
                sfm = [25, 15, 10, 5]
                mplier = 0.1
                hply = 0.1
            elif 400 > wid >= 200:
                sfm = [30, 20, 10, 5]
                mplier = 0.075
                hply = 0.2
            elif 400 <= wid < 600:
                sfm = [50, 30, 20, 10]
                mplier = 0.05
                hply = 0.3
            elif 800 > wid >= 600:
                sfm = [70, 50, 30, 20]
                mplier = 0.025
                hply = 0.4
            elif 1000 > wid >= 800:
                sfm = [80, 60, 40, 30]
                mplier = 0.01
                hply = 0.5
            elif 1500 > wid >= 1000:
                sfm = [100, 80, 60, 40]
                mplier = 0.01
                hply = 0.6
            elif 2000 > wid >= 1400:
                sfm = [120, 100, 80, 60]
                mplier = 0.01
                hply = 0.6
            elif 2000 <= wid < 3000:
                sfm = [140, 120, 100, 80]
                mplier = 0.01
                hply = 0.6
            elif wid >= 3000:
                sfm = [180, 160, 140, 120]
                mplier = 0.01
                hply = 0.6
            else:
                raise ParameterError("Image is too large")
            x_pos = int(mplier * wid)
            y_pos = int(-1 * (mplier * hply * 10) * hei)
            print(y_pos)
            if 50 > len(text) > 0:
                size = sfm[1]
            elif 100 > len(text) > 50:
                size = sfm[1]
            elif 100 < len(text) < 250:
                size = sfm[2]
            elif len(text) > 250 and len(text) > 500:
                size = sfm[3]
            elif 500 < len(text) < 1000:
                size = sfm[4]
            else:
                raise ParameterError("text is too long")
            y = Image.new("RGBA", (tv.size[0], 800), (256, 256, 256))
            wra = WriteText(y)
            f = wra.write_text_box(
                x_pos, -10, text, tv.size[0] - 40,
                "app/image/assets/whitney-medium.ttf",
                size, color=(0, 0, 0)
            )
            t = f
            im = wra.ret_img()
            # im = Image.open(bt)
            ima = im.crop((0, 0, tv.size[0], t))
            bcan = Image.new("RGBA", (tv.size[0], tv.size[1] + t), (0, 0, 0, 0))
            bcan.paste(ima)
            bcan.paste(tv, (0, t))
            buffer = BytesIO()
            bcan.save(buffer, format="PNG")
            buffer.seek(0)
            return buffer

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
    def do_merge(img1, img2):
        img1 = Image.open(img1).convert("RGBA").resize((512, 512))
        img2 = Image.open(img2).convert("RGBA").resize((512, 512))
        img = Image.blend(img1, img2, 0.5)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
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
            buffer = BytesIO()
            img.save(buffer, format="PNG")
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
            img1 = BytesIO(await url1.read())
            img1.seek(0)
            img2 = BytesIO(await url2.read())
            img2.seek(0)
            buffer = await self.bot.loop.run_in_executor(None, self.do_merge, img1, img2)
        file=discord.File(buffer, filename="merge.png")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Merged Avatar", icon_url=m1.avatar_url)
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

    @commands.command()
    async def memegen(self, ctx, image, *, text):
        '''Memegen'''
        if "-u" in image:
            url = member.avatar_url_as(size=512, format="png")
        elif ctx.message.attachments:
            url = ctx.message.attachments[0]
        else:
            url = image
        async with ctx.typing():
            img = BytesIO(await url.read())
            img.seek(0)
            buffer = await self.bot.loop.run_in_executor(None, self.do_meme, img, text)
        file=discord.File(buffer, filename="meme.png")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Meme", icon_url=member.avatar_url)
        e.set_image(url="attachment://meme.png")
        await ctx.remove(file=file, embed=e)

def setup(bot):
    bot.add_cog(image(bot))
