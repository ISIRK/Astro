import discord, random, json
from discord.ext import commands
from discord.ext.commands import BucketType

class economy(commands.Cog):
    '''Economy Commands'''
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    async def register(self, ctx):
        """Registers a bank account with $50"""
        s = await self.bot.db.fetchrow("SELECT * FROM economy WHERE userId = $1", ctx.author.id)
        if s:
            return await ctx.send(embed = discord.Embed(description = "You already have an account!", color=self.bot.color))
        elif not s:
            await self.bot.db.execute("INSERT INTO economy(userId, cashBalance, bankBalance) VALUES($1, $2, $3)", ctx.author.id, 50, 0)
            await ctx.send(embed = discord.Embed(description = "Bank account register succesful, to remove your account run: `delete`", color=self.bot.color))
    
    @commands.command(name = "delete")
    @commands.guild_only()
    async def delete_account(self, ctx):
        """Closes your account"""
        s = await self.bot.db.fetchrow("SELECT * FROM economy WHERE userId = $1", ctx.author.id)
        if s:
            confirm_embed = self.bot.utils.ConfirmMenu(discord.Embed(title="Are you sure you want to close your account?", colour=ctx.bot.color),
                                                   delete_message_after=False)
            confirm = await confirm_embed.prompt(ctx)
            if confirm:
                await self.bot.db.execute("DELETE FROM economy WHERE userId = $1", ctx.author.id)
                await confirm_embed.message.edit(embed=discord.Embed(title="Successfully closed your bank account.",colour=self.bot.color))
        if not s:
            return await ctx.send(embed = discord.Embed(description = f"You don't have an account! Type `{ctx.prefix}register` to make one", color=self.bot.color))
    
    @commands.command(aliases = ["bal"])
    async def balance(self, ctx, *, user: discord.Member = None):
        '''See the balance of yourself or the mentioned user'''
        if not user: user = ctx.author
        s = await self.bot.db.fetchrow("SELECT * FROM ECONOMY WHERE userid = $1", user.id)
        if not s:
            await ctx.send(f"That user doesn't have an account! Type `{ctx.prefix}register` to make one")
            ctx.command.reset_cooldown(ctx)
        else:
            bank, cash = s['bankbalance'], s['cashbalance']
            if not bank: bank = 0
            if not cash: cash = 0
            embed = discord.Embed(
                title = f"{str(user.name)}'s balance:",
                description = f"💰 Cash: ${cash:,}\n🏦 Bank: ${bank:,}",
                color = self.bot.color
            )
            embed.set_thumbnail(icon=user.avatar_url)
            if s['inv']:
                inventory = s['inv']
                embed.add_field(name="Inventory", value=''.join([f'\n{item}' for item in inventory]), inline=False)
            else:
                pass
            await ctx.send(embed = embed)

    @commands.cooldown(1,120,BucketType.user)
    @commands.command()
    async def work(self, ctx):
        '''Work and get a random amount of money in between $1 and $100'''
        s = await self.bot.db.fetchrow("SELECT * FROM ECONOMY WHERE userid = $1", ctx.author.id)
        if not s:
            await ctx.send(f"You don't have an account! Type `{ctx.prefix}register` to make one")
            ctx.command.reset_cooldown(ctx)
        else:
            bal = s['cashbalance']
            pay = random.randint(1, 100)
            thing = ""
            if 'Multiplier' in s['inv']:
                thing = " **(x2 With Multiplier)**"
                pay = random.randint(100, 200)
            total = bal+pay
            await self.bot.db.execute("UPDATE economy SET cashbalance = $1 WHERE userId = $2", total, ctx.author.id)
            await ctx.send(f"You worked and gained ${pay}!{thing}")

    @commands.cooldown(1,30,BucketType.user)
    @commands.command(cooldown_after_parsing=True)
    async def rob(self, ctx, *, user: discord.User):
        '''
        Rob another user
        '''
        user = self.bot.get_user(user.id)
        a = await self.bot.db.fetchrow("SELECT * FROM ECONOMY WHERE userid = $1", ctx.author.id)
        u = await self.bot.db.fetchrow("SELECT * FROM ECONOMY WHERE userid = $1", user.id)
        if not a:
            await ctx.send(f"You don't have an account! Type `{ctx.prefix}register` to make one")
            ctx.command.reset_cooldown(ctx)
        elif not u:
            await ctx.send(f"That user doesn't have an account!")
            ctx.command.reset_cooldown(ctx)
        else:        
            c = random.randint(100, 200)

            if u['cashbalance'] < 400:
                await ctx.send(f"<:PepePoint:759934591590203423> **{user}** doesn't have enough money. Try robbing someone with more money.")
                ctx.command.reset_cooldown(ctx)
            elif u['cashbalance'] > c:
                try:
                    await self.bot.db.execute("UPDATE economy SET cashbalance = $1 WHERE userId = $2", u['cashbalance']-c, user.id)
                    await self.bot.db.execute("UPDATE economy SET cashbalance = $1 WHERE userId = $2", a['cashbalance']+c, ctx.author.id)
                    await ctx.send(f'You stole ${c} from **{user.name}**')
                except Exception as e:
                    await ctx.send(f'```py\n{e}```')

    @commands.cooldown(1,15,BucketType.user)
    @commands.command(cooldown_after_parsing=True)
    async def bet(self, ctx, amount: int):
        '''
        Bet a certain amount of money
        '''
        a = await self.bot.db.fetchrow("SELECT * FROM ECONOMY WHERE userid = $1", ctx.author.id)
        if not a:
            await ctx.send(f"You don't have an account! Type `{ctx.prefix}register` to make one")
            ctx.command.reset_cooldown(ctx)
        else:
            lucky = random.choice([False, True])

            if amount > a['cashbalance']:
                await ctx.send("You can't bet what you dont have.")
            elif amount <= a['cashbalance']:
                if lucky:
                    await self.bot.db.execute("UPDATE economy SET cashbalance = $1 WHERE userId = $2", a['cashbalance']+amount, ctx.author.id)
                    await ctx.send(f"You got lucky and won ${amount}!")
                else:
                    await self.bot.db.execute("UPDATE economy SET cashbalance = $1 WHERE userId = $2", a['cashbalance']-amount, ctx.author.id)
                    await ctx.send(f"Fate doesn't like you, you lost ${amount}.")

    @commands.cooldown(1,15,BucketType.user)
    @commands.command()
    async def slots(self, ctx):
        '''
        Use the slot machines to try and win money
        '''
        a = await self.bot.db.fetchrow("SELECT * FROM ECONOMY WHERE userid = $1", ctx.author.id)
        if not a:
            await ctx.send(f"You don't have an account! Type `{ctx.prefix}register` to make one")
            ctx.command.reset_cooldown(ctx)
        else:
            slots = ['🎁', '⭐', '7️⃣']
            out1 = random.choice(slots)
            out2 = random.choice(slots)
            out3 = random.choice(slots)

            if out1 is out2 and out3 is out2:
                win = True
            else:
                win = False

            if win:
                await self.bot.db.execute("UPDATE economy SET cashbalance = $1 WHERE userId = $2", a['cashbalance']+5000, ctx.author.id)

            embed = discord.Embed(title="Slot Machine", description=f"```{out1} {out2} {out3}```", color=self.bot.color)
            embed.add_field(name="Earnings", value=f"{'$5,000' if win else 'None'}")
            await ctx.send(embed=embed)

    @commands.cooldown(1,3,BucketType.user)
    @commands.command(aliases=['dep'])
    async def deposit(self, ctx, amount: int = None):
        '''
        Deposit your money into the bank.
        
        If `amount` is none then it will deposit everything.
        '''
        s = await self.bot.db.fetchrow("SELECT * FROM ECONOMY WHERE userid = $1", ctx.author.id)
        if not s:
            await ctx.send(f"You don't have an account! Type `{ctx.prefix}register` to make one")
        else:
            cash = s['cashbalance']
            if cash == 0:
                await ctx.send('No Money in your wallet.')
            elif amount is None:
                await self.bot.db.execute("UPDATE economy SET cashbalance = 0, bankbalance = cashbalance+bankbalance WHERE userId = $1", ctx.author.id)
                await ctx.send(f"Deposited ${cash} into the bank.")
            elif amount > cash:
                await ctx.send("You can't deposit what you don't have.")
            else:
                await self.bot.db.execute("UPDATE economy SET cashbalance = $1, bankbalance = $2 WHERE userId = $3", s['cashbalance']-amount, s['bankbalance']+amount, ctx.author.id)
                await ctx.send(f"Deposited ${amount} into the bank.")

    @commands.cooldown(1,3,BucketType.user)
    @commands.command(aliases=['wd'])
    async def withdraw(self, ctx, amount: int = None):
        '''
        Withdraw your money from the bank.
        
        If `amount` is none then it will withdraw everything.
        '''
        s = await self.bot.db.fetchrow("SELECT * FROM ECONOMY WHERE userid = $1", ctx.author.id)
        if not s: 
            await ctx.send(f"You don't have an account! Type `{ctx.prefix}register` to make one")
        else:
            bank = s['bankbalance']
            if bank == 0:
                await ctx.send('No Money in your bank.')
            elif amount is None:
                await self.bot.db.execute("UPDATE economy SET cashbalance = cashbalance+bankbalance, bankbalance = 0 WHERE userId = $1", ctx.author.id)
                await ctx.send(f"Withdrawn ${bank} from the bank.")
            elif amount > bank:
                await ctx.send("You can't withdraw what you don't have.")
            else:
                await self.bot.db.execute("UPDATE economy SET cashbalance = $1, bankbalance = $2 WHERE userId = $3", s['cashbalance']+amount, s['bankbalance']-amount, ctx.author.id)
                await ctx.send(f"Withdrawn ${amount} from the bank.")
    
    @commands.cooldown(1, 43200, BucketType.user)
    @commands.command()
    async def daily(self, ctx):
        '''Get daily coins.'''
        s = await self.bot.db.fetchrow("SELECT * FROM ECONOMY WHERE userid = $1", ctx.author.id)
        if not s: 
            await ctx.send(f"You don't have an account! Type `{ctx.prefix}register` to make one")
            ctx.command.reset_cooldown(ctx)
        else:
            await self.bot.db.execute("UPDATE economy SET cashbalance = cashbalance+1000 WHERE userId = $1", ctx.author.id)
            await ctx.send("Collected **1,000** daily coins!")

    @commands.command()
    async def cooldowns(self, ctx):
        '''See what commands can be used.'''
        yes = '❌'
        no = '✅'
        daily = self.bot.get_command('daily').is_on_cooldown(ctx)
        work = self.bot.get_command('work').is_on_cooldown(ctx)
        rob = self.bot.get_command('rob').is_on_cooldown(ctx)
        bet = self.bot.get_command('bet').is_on_cooldown(ctx)
        slots = self.bot.get_command('slots').is_on_cooldown(ctx)
        embed=discord.Embed(title="Cooldowns", description=f'Daily: {yes if daily else no}\nWork: {yes if work else no}\nRob: {yes if rob else no}\nBet: {yes if bet else no}\nSlots: {yes if slots else no}', color=self.bot.color)
        await ctx.send(embed=embed)
        

    @commands.cooldown(1,3,BucketType.user)
    @commands.group(brief="Main commands")
    async def shop(self, ctx):
        '''A shop to buy things with your coins. WIP'''
        
        embed = discord.Embed(title=f"{ctx.guild.name}'s Shop", description=f"To buy and item use **{ctx.prefix}shop buy <number>**", color=self.bot.color)
        embed.add_field(name="`1` - Multiplier", value="💰 Multiply your earnings when you work!\n> Cost: **$100,000**", inline=False)
        embed.set_footer(text=self.bot.footer)
        embed.set_author(name="Shop", icon_url=ctx.guild.icon_url)

        if ctx.invoked_subcommand is None:
            await ctx.send(embed=embed)

    @shop.command()
    async def buy(self, ctx, product: int):
        '''
        Buy an item from the shop.
        '''
        a = await self.bot.db.fetchrow("SELECT * FROM ECONOMY WHERE userid = $1", ctx.author.id)
        if not a:
            await ctx.send(f"You don't have an account! Type `{ctx.prefix}register` to make one")
            ctx.command.reset_cooldown(ctx)
        else:
            product = product-1
            inv = {
                'Multiplier' : 100000,
                'test' : 69
            }
            item = list(inv)[product]
            price = inv[item]
            inventory = a['inv']
            balance = a['cashbalance']
            try:
                if item in inventory:
                    await ctx.send('You already have that.')
                else:
                    if balance < price:
                        await ctx.send("You don't have enough money in your wallet.")
                    else:
                        inventory.append(item)
                        await self.bot.db.execute("UPDATE economy SET inv = $1, cashbalance = $2 WHERE userId = $3", inventory, a['cashbalance']-price, ctx.author.id)
                        await ctx.send(f'Successfully bought **{item}** for `{price}`!')
            except Exception as e:
                await ctx.send(f'```py\n{e}```')

def setup(bot):
    bot.add_cog(economy(bot))
