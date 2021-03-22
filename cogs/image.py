import discord, numpy, requests, wand, datetime, humanize, textwrap, asyncio
from io import BytesIO
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from wand.image import Image as WandImage
from PIL import Image, ImageFilter, ImageDraw, ImageOps, ImageFont, ImageSequence

class image(commands.Cog, command_attrs={'cooldown': commands.Cooldown(1, 10, commands.BucketType.user)}):
    """Image manipulation commands"""
    def __init__(self, bot):
        self.bot = bot
        self.invis = 0x2F3136
        
    # Pillow Image Manipulation

    @staticmethod
    def do_mc(txt) -> BytesIO:
        image = Image.open(requests.get('https://i.imgur.com/JtNJFZy.png', stream=True).raw).convert("RGBA")
        draw = ImageDraw.Draw(image)
        font_path = "cogs/assets/minecraft.ttf"
        font = ImageFont.truetype(font_path, 17)
        draw.text((60, 30), txt, (255, 255, 255), font=font)
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    @staticmethod
    def do_ascii(image) -> BytesIO:
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
    def do_quantize(img) -> BytesIO:
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
    def do_wash(img) -> BytesIO:
        with Image.open(img) as img:
            images = []
            for i in range(30):
                im = img.copy()
                im = im.rotate(12 * i)
                images.append(im)
            gif = BytesIO()
            images[0].save(gif,
                           format='gif',
                           save_all=True,
                           append_images=images,
                           duration=1,
                           loop=0)
            gif.seek(0)
            gif = Image.open(gif)
            wash = Image.open("cogs/assets/wash.png")
            frames = []
            for frame in ImageSequence.Iterator(gif):
                frame = frame.copy()
                frame.paste(wash) #, mask=wash
                frames.append(frame)
            buffer = BytesIO()
            frames[0].save(buffer,
                           format='gif',
                           save_all=True,
                           append_images=images,
                           duration=1,
                           loop=0)
            buffer.seek(0)
            return buffer

    @staticmethod
    def do_sketch(img) -> BytesIO:
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
    def do_tr(text: str) -> BytesIO:
        #text = '\n'.join(textwrap.wrap(text, width=15))
        font = ImageFont.truetype("cogs/assets/Ubuntu.ttf", 30)
        width, height = font.getsize(text)
        width += 20
        height += 20

        image = Image.new("RGBA", (width, height), color=0)
        draw = ImageDraw.Draw(image)

        w, h = draw.textsize(text, font=font)
        draw.text(
            ((width - w) / 2, (height - h) / 2),
            text=text,
            fill="white",
            font=font,
            stroke_width=1,
            stroke_color=(255, 255, 255),
        )

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer, text

    @staticmethod
    def do_merge(img1, img2) -> BytesIO:
        img1 = Image.open(img1).convert("RGBA").resize((512, 512))
        img2 = Image.open(img2).convert("RGBA").resize((512, 512))
        img = Image.blend(img1, img2, 0.5)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    @staticmethod
    def do_invert(img) -> BytesIO:
        with Image.open(img).convert("RGB") as img:
            img = ImageOps.invert(img)
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            return buffer

    @staticmethod
    def do_emboss(img) -> BytesIO:
        with Image.open(img) as img:
            img = img.filter(ImageFilter.EMBOSS)
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            return buffer
        
    @staticmethod
    def do_solarize(img) -> BytesIO:
        with Image.open(img).convert("RGB") as img:
            img = ImageOps.solarize(img, threshold=64)
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            return buffer

    @staticmethod
    def do_pixel(img) -> BytesIO:
        with Image.open(img) as img:
            img1 = img.resize((36, 36), resample=Image.BILINEAR)
            img = img1.resize(img1.size, Image.NEAREST)
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            return buffer

    # Wand Image Manipulation

    @staticmethod
    def do_swirl(img) -> BytesIO:
        with WandImage(blob=img) as img:
            img.swirl(degree=-90)
            buffer = BytesIO()
            img.save(buffer)
            buffer.seek(0)
            return buffer

    @staticmethod
    def do_polaroid(img) -> BytesIO:
        with WandImage(blob=img) as img:
            img.polaroid()
            buffer = BytesIO()
            img.save(buffer)
            buffer.seek(0)
            return buffer

    @staticmethod
    def do_floor(img) -> BytesIO:
        with WandImage(blob=img) as img:
            img.virtual_pixel = "tile"
            img.resize(300, 300)
            x, y = img.width, img.height
            arguments = (0, 0, 77, 153, x, 0, 179, 153, 0, y, 51, 255, x, y, 204, 255)
            img.distort("perspective", arguments)
            buffer = BytesIO()
            img.save(buffer)
            buffer.seek(0)
            return buffer

    @staticmethod
    def do_cube(img) -> BytesIO:
        with WandImage(blob=img) as image:
            def s(x):
                return int(x / 3)

            image.resize(s(1000), s(860))
            image.format = "png"
            image.alpha_channel = 'opaque'

            image1 = image
            image2 = WandImage(image1)

            out = WandImage(width=s(3000 - 450), height=s(860 - 100) * 3)
            out.format = "png"

            image1.shear(background=wand.color.Color("none"), x=-30)
            image1.rotate(-30)
            out.composite(image1, left=s(500 - 250), top=s(0 - 230) + s(118))
            image1.close()

            image2.shear(background=wand.color.Color("rgba(0,0,0,0)"), x=30)
            image2.rotate(-30)
            image3 = WandImage(image2)
            out.composite(image2, left=s(1000 - 250) - s(72), top=s(860 - 230))
            image2.close()

            image3.flip()
            out.composite(image3, left=s(0 - 250) + s(68), top=s(860 - 230))
            image3.close()

            out.crop(left=80, top=40, right=665, bottom=710)

            buffer = BytesIO()
            out.save(buffer)
            buffer.seek(0)
            return buffer

    @staticmethod
    def do_spread(img) -> BytesIO:
        with WandImage(blob=img) as img:
            img.resize(256, 256)
            img.alpha_channel = False

            output = WandImage(width=img.width, height=img.height)
            output.format = "GIF"

            output.sequence[0] = img
            output.sequence.extend(img for _ in range(0, 2))

            for radius in range(0, 13):
                with img.clone() as frame:
                    frame.spread(radius=radius ** 2)
                    output.sequence.append(frame)

            output.sequence.extend(reversed(output.sequence))

            img.close()

            output.optimize_layers()
            output.optimize_transparency()
            buffer = BytesIO()
            output.save(buffer)
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

    @commands.max_concurrency(1, per=BucketType.channel, wait=False)
    @commands.command(aliases=['tr'])
    async def typeracer(self, ctx):
        '''See who can type the fastest'''
        r = await self.bot.session.get("https://api.quotable.io/random?maxLength=100")
        resp = await r.json()
        buffer, text = await self.bot.loop.run_in_executor(None, self.do_tr, resp['content'])
        file=discord.File(buffer, filename="typeracer.png")
        e=discord.Embed(title='Type this quote', color=self.invis).set_footer(text=resp['author'])
        e.set_image(url="attachment://typeracer.png")
        await ctx.send(file=file, embed=e)
        start = datetime.datetime.now()
        going = True
        while going:
            try:
                m = await self.bot.wait_for('message', timeout=60, check=lambda m:(ctx.channel == m.channel))
            except asyncio.TimeoutError:
                await ctx.send('Took too long')
                going = False
            else:
                if m.content == resp['content']:
                    end = datetime.datetime.now()
                    await ctx.send(f'{m.author.mention} typed it correct in **`{humanize.precisedelta((end - start).total_seconds())}`**')
                    going = False

    @commands.command()
    async def swirl(self, ctx, *, member: discord.Member = None):
        '''Swirls the avatar'''
        if not member:
            member = ctx.author
        url = member.avatar_url_as(size=512, format="png")
        async with ctx.typing():
            img = BytesIO(await url.read())
            img.seek(0)
            buffer = await self.bot.loop.run_in_executor(None, self.do_swirl, img)
        file=discord.File(buffer, filename="swirl.png")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Swirled Avatar", icon_url=member.avatar_url)
        e.set_image(url="attachment://swirl.png")
        await ctx.remove(file=file, embed=e)

    @commands.command()
    async def polaroid(self, ctx, *, member: discord.Member = None):
        '''Polaroid the avatar'''
        if not member:
            member = ctx.author
        url = member.avatar_url_as(size=512, format="png")
        async with ctx.typing():
            img = BytesIO(await url.read())
            img.seek(0)
            buffer = await self.bot.loop.run_in_executor(None, self.do_polaroid, img)
        file=discord.File(buffer, filename="polaroid.png")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Polaroid Avatar", icon_url=member.avatar_url)
        e.set_image(url="attachment://polaroid.png")
        await ctx.remove(file=file, embed=e)

    @commands.command()
    async def floor(self, ctx, *, member: discord.Member = None):
        '''Floor the avatar'''
        if not member:
            member = ctx.author
        url = member.avatar_url_as(size=512, format="png")
        async with ctx.typing():
            img = BytesIO(await url.read())
            img.seek(0)
            buffer = await self.bot.loop.run_in_executor(None, self.do_floor, img)
        file=discord.File(buffer, filename="floor.png")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Floored Avatar", icon_url=member.avatar_url)
        e.set_image(url="attachment://floor.png")
        await ctx.remove(file=file, embed=e)

    @commands.command()
    async def cube(self, ctx, *, member: discord.Member = None):
        '''Cube the avatar'''
        if not member:
            member = ctx.author
        url = member.avatar_url_as(size=512, format="png")
        async with ctx.typing():
            img = BytesIO(await url.read())
            img.seek(0)
            buffer = await self.bot.loop.run_in_executor(None, self.do_cube, img)
        file=discord.File(buffer, filename="cube.png")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Cubed Avatar", icon_url=member.avatar_url)
        e.set_image(url="attachment://cube.png")
        await ctx.remove(file=file, embed=e)

    @commands.command()
    async def spread(self, ctx, *, member: discord.Member = None):
        '''Spreads the avatar'''
        if not member:
            member = ctx.author
        url = member.avatar_url_as(size=512, format="png")
        async with ctx.typing():
            img = BytesIO(await url.read())
            img.seek(0)
            buffer = await self.bot.loop.run_in_executor(None, self.do_spread, img)
        file=discord.File(buffer, filename="spread.gif")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Spreaded Avatar", icon_url=member.avatar_url)
        e.set_image(url="attachment://spread.gif")
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
    async def wash(self, ctx, *, member: discord.Member = None):
        '''Wash the avatar'''
        if not member:
            member = ctx.author
        url = member.avatar_url_as(size=512, format="png")
        async with ctx.typing():
            img = BytesIO(await url.read())
            img.seek(0)
            buffer = await self.bot.loop.run_in_executor(None, self.do_wash, img)
        file=discord.File(buffer, filename="wash.gif")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Washed Avatar", icon_url=member.avatar_url)
        e.set_image(url="attachment://wash.gif")
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
    async def achievement(self, ctx, *, text: str):
        '''Make a minecraft achievement'''
        async with ctx.typing():
            if len(text) > 20:
                text = text[:17] + "..."
            buffer = await self.bot.loop.run_in_executor(None, self.do_mc, text)
        file=discord.File(buffer, filename="achievement.png")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Achievement", icon_url=ctx.author.avatar_url)
        e.set_image(url="attachment://achievement.png")
        await ctx.remove(file=file, embed=e)

def setup(bot):
    bot.add_cog(image(bot))
