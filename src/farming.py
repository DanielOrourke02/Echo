

from utilities import *
from eco_support import *


class Farming(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Command to plant carrots
    @commands.slash_command()
    async def plant(self, ctx, amount: int):
        user_id = ctx.author.id
        user_balance = get_user_balance(user_id)

        total_cost = amount * cost_per_carrot

        embed = discord.Embed(color=discord.Color.green())

        if amount < 500:
            # Check if the user has planted in the last hour
            if user_id in last_planting_time:
                time_since_last_plant = datetime.datetime.now() - last_planting_time[user_id]
                if time_since_last_plant < datetime.timedelta(hours=1):
                    embed.title = "Wait a Little Longer"
                    embed.description = "You can only plant carrots once every 24hrs. Please wait a bit longer before planting again."
                    await ctx.respond(embed=embed)
                    return

            if user_balance < total_cost:
                embed.title = "Not Enough Balance"
                embed.description = f"You need ${total_cost} to plant {amount} carrots"
            else:
                plant_carrots(user_id, amount)
                last_planting_time[user_id] = datetime.datetime.now()  # Update the last planting time
                embed.title = "Carrots Planted"
                embed.description = f"You have planted {amount} carrots."

            await ctx.respond(embed=embed)
        elif amount > max_carrot_planted:
            embed.title = "Too much carrots"
            embed.description = f"You cannot plant more than {max_carrot_planted}."
            await ctx.respond(embed=embed)


    @commands.slash_command()
    async def harvest(self, ctx):
        user_id = ctx.author.id
        plantation = user_carrot_plantations.get(str(user_id))

        if plantation:
            current_time = time.time()
            time_left_seconds = max(0, plantation[0] - current_time)
            growth_percentage = min(100, ((growth_duration - time_left_seconds) / growth_duration) * 100)

            if time_left_seconds <= 0:
                harvested_amount = plantation[1]

                total_profit = harvested_amount * carrot_sell
                update_user_balance(user_id, total_profit)
                del user_carrot_plantations[str(user_id)]  # Removing the plantation record

                embed = discord.Embed(title="Success", description=f"You have successfully harvested {harvested_amount} carrots and earned ${total_profit}.", color=discord.Colour.green())
                await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(title="Info", description=f"Your carrots are not ready yet. They are {int(growth_percentage)}% grown.", color=discord.Colour.orange())
                await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title="Error", description="You don't have any crops planted.", color=embed_error)


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Farming Cog Loaded! {Fore.RESET}')


def setup(bot):
    bot.add_cog(Farming(bot))