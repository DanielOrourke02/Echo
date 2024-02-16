

from helpers import *
from utilities import *
from eco_support import *


class Slots(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    def check_bet(self, ctx, bet):
        user_id = ctx.author.id
        bal = get_user_balance(user_id)
        if bet is None:
            return True
        elif bet < bal:
            pass
        elif bet > bal:
            return False


    @commands.command(brief='Slot machine\nbet must be 1-3', usage='slots *[bet]', aliases=['slot'])
    async def slots(self, ctx: commands.Context, bet: int=None):
        if self.check_bet(ctx, bet=bet) is False:
            embed = discord.Embed(
                title="BROKE ASF",
                description=f"{ctx.author.mention}, You do not have enough money to gamble that amount",
                color=embed_error
            )
            await ctx.send(embed=embed)
            return
        elif self.check_bet(ctx, bet=bet) is True:
            embed = discord.Embed(
                title="Enter a bet",
                description=f"{ctx.author.mention}, Please enter a bet amount. Usage: `{prefix}slots <bet>`",
                color=embed_error
            )
            await ctx.send(embed=embed)
            return
            

        path = os.path.join('src/pictures/')
        facade = Image.open(f'{path}slot-face.png').convert('RGBA')
        reel = Image.open(f'{path}slot-reel.png').convert('RGBA')

        rw, rh = reel.size
        item = 180
        items = rh//item

        s1 = random.randint(1, items-1)
        s2 = random.randint(1, items-1)
        s3 = random.randint(1, items-1)

        win_rate = 45/100

        if random.random() < win_rate:
            symbols_weights = [3.5, 7, 15, 25, 55] # 
            x = round(random.random()*100, 1)
            pos = bisect.bisect(symbols_weights, x)
            s1 = pos + (random.randint(1, (items/6)-1) * 6)
            s2 = pos + (random.randint(1, (items/6)-1) * 6)
            s3 = pos + (random.randint(1, (items/6)-1) * 6)
            # ensure no reel hits the last symbol
            s1 = s1 - 6 if s1 == items else s1
            s2 = s2 - 6 if s2 == items else s2
            s3 = s3 - 6 if s3 == items else s3

        images = []
        speed = 6
        for i in range(1, (item//speed)+1):
            bg = Image.new('RGBA', facade.size, color=(255,255,255))
            bg.paste(reel, (25 + rw*0, 100-(speed * i * s1)))
            bg.paste(reel, (25 + rw*1, 100-(speed * i * s2))) # dont ask me why this works, but it took me hours
            bg.paste(reel, (25 + rw*2, 100-(speed * i * s3)))
            bg.alpha_composite(facade)
            images.append(bg)

        # Generate a unique filename using uuid
        unique_filename = str(uuid.uuid4()) + '.gif'
        fp = os.path.join('src/pictures/', unique_filename)

        images[0].save(
            fp,
            save_all=True,
            append_images=images[1:],
            duration=50
        )

        file = discord.File(fp, filename=unique_filename)
        message = await ctx.send(file=file)

        result = ('lost', bet)
        update_user_balance(ctx.author.id, bet*-1)

        if (1+s1)%6 == (1+s2)%6 == (1+s3)%6:
            symbol = (1+s1)%6
            reward = [4, 80, 40, 25, 10, 5][symbol] * bet
            result = ('won', reward)
            update_user_balance(ctx.author.id, reward)

        embed = make_embed(
            title=(
                f'{ctx.author.display_name}, You {result[0]} {result[1]} credits' +
                ('.' if result[0] == 'lost' else '!')
            ),
            description=(
                f'{ctx.author.display_name}, You now have ' +
                f'**£{get_user_balance(ctx.author.id)}**'
            ),
            color=(
                embed_error if result[0] == "lost"
                else discord.Color.green()
            )
        )

        embed.set_image(url=f"attachment://{unique_filename}")
        await message.edit(content=None, embed=embed)

        os.remove(fp)


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Slots Cog Loaded! {Fore.RESET}')


def slots_setup(bot: commands.Bot):
    bot.add_cog(Slots(bot))
