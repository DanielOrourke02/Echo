

from utilities import *
from eco_support import *


class Farming(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Command to plant carrots
    @commands.command()
    async def plant(self, ctx, amount: int=None):
        user_id = ctx.author.id
        user_balance = get_user_balance(user_id)

        if amount is None: # if they didnt enter an amount
            embed = discord.Embed(color=embed_error)
            embed.title = "Incorrect usage"
            embed.description = f"{ctx.author.mention}, Please enter the amount you want to plant. Usage: `{prefix}plant <amount>`"
            embed.color = embed_error

            await ctx.send(embed=embed)
            return

        total_cost = amount * cost_per_carrot # total cost of planting their amount of carrots

        embed = discord.Embed(color=discord.Color.green())

        # Check if the user has planted in the last 24 hours or has no plants planted
        if user_id in last_planting_time:
            time_since_last_plant = datetime.datetime.now() - last_planting_time[user_id]
            if time_since_last_plant < datetime.timedelta(hours=config.get('carrot_growth_duration')):
                embed.title = "Wait a Little Longer"
                embed.description = f"{ctx.author.mention}, You can only plant carrots once every 24 hours. Please wait a bit longer before planting again."
                embed.color = embed_error
                await ctx.send(embed=embed)
                return

        if amount > max_carrot_planted: # max carrots that you can plant (you can change this in the config)
            embed.title = "Too Many Carrots"
            embed.description = f"{ctx.author.mention}, You cannot plant more than {max_carrot_planted} carrots."
            embed.color = embed_error
            await ctx.send(embed=embed)
            return

        if user_balance < total_cost: # if they are too poor
            embed.title = "Not Enough Balance"
            embed.description = f"{ctx.author.mention}, You need ${total_cost} to plant {amount} carrots"
            embed.color = embed_error
            await ctx.send(embed=embed)
            return

        # Check if the user has no plants planted
        if not user_has_plants(user_id):
            plant_carrots(user_id, amount)
            last_planting_time[user_id] = datetime.datetime.now()  # Update the last planting time
            embed.title = "Carrots Planted"
            embed.description = f"{ctx.author.mention}, You have planted {amount} carrots."
            await ctx.send(embed=embed)
        else:
            embed.title = "Planting Error"
            embed.description = f"{ctx.author.mention}, You already have plants planted. Harvest them before planting again."
            embed.color = embed_error
            await ctx.send(embed=embed)


    @commands.command(aliases=['har'])
    async def harvest(self, ctx):
        user_id = str(ctx.author.id)
        user_plantations = load_user_plants() # load planted crops
        plantation = user_plantations.get(user_id) # get what that user has planted (and when)

        if plantation: 
            current_time = time.time()
            time_left_seconds = max(0, plantation['time_planted'] + growth_duration - current_time) # time left of growth (if their is any left)
            growth_percentage = min(100, ((growth_duration - time_left_seconds) / growth_duration) * 100) # calculate growth percentage

            if time_left_seconds <= 0:
                harvested_amount = plantation['amount_planted'] # get how much they can harvest/how much they planted

                total_profit = harvested_amount * carrot_sell # calculate total profit
                update_user_balance(user_id, total_profit) # sell corps and add money 
                del user_plantations[user_id]  # Removing the plantation record

                embed = discord.Embed(title="Success", description=f"{ctx.author.mention}, You have successfully harvested {harvested_amount} carrots and earned ${total_profit}.", color=discord.Colour.green())
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Info", description=f"{ctx.author.mention}, Your carrots are not ready yet. They are {int(growth_percentage)}% grown.", color=embed_error)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Error", description=f"{ctx.author.mention}, You don't have any crops planted.", color=embed_error)
            await ctx.send(embed=embed)

        save_user_plants(user_plantations) # save data


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Farming Cog Loaded! {Fore.RESET}')
        global user_carrot_plantations
        user_carrot_plantations = load_user_plants() # load plantd crops


def farming_setup(bot):
    bot.add_cog(Farming(bot))
