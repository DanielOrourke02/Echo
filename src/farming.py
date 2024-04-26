

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
        
        try:
            if amount is None: # if they didn't enter an amount
                embed = discord.Embed(color=embed_error)
                
                embed.title = "Incorrect usage"
                
                embed.description = f"{ctx.author.mention}, Please enter the amount you want to plant. Usage: `{prefix}plant <amount>`"
                
                embed.set_footer(text=f"Made by mal023")
                
                await ctx.send(embed=embed)
                return

            total_cost = amount * cost_per_carrot # total cost of planting their amount of carrots

            embed = discord.Embed(color=discord.Color.green())

            # Check if the user has already planted carrots
            if user_has_plants(user_id):
                embed.title = "Wait a Little Longer"
                
                embed.description = f"{ctx.author.mention}, Your plants take {config.get('carrot_growth_duration')} hours to grow. Try harvesting them using: `{prefix}harvest`."
                
                embed.color = embed_error
                
                embed.set_footer(text=f"Made by mal023")
                
                await ctx.send(embed=embed)
                return

            # Check if the user is trying to plant too many carrots
            if amount > max_carrot_planted:
                embed.title = "Too Many Carrots"
                
                embed.description = f"{ctx.author.mention}, You cannot plant more than {max_carrot_planted} carrots."
                
                embed.color = embed_error
                
                embed.set_footer(text=f"Made by mal023")
                
                await ctx.send(embed=embed)
                return

            # Check if the user has enough balance
            if user_balance < total_cost:
                embed.title = "Not Enough Balance"
                
                embed.description = f"{ctx.author.mention}, You need {total_cost} zesty coins to plant {amount} carrots"
                
                embed.color = embed_error
                
                embed.set_footer(text=f"Made by mal023")
                
                await ctx.send(embed=embed)
                return

            # Plant carrots
            plant_carrots(user_id, amount)

            # Send success message
            embed.title = "Carrots Planted"
            
            embed.description = f"{ctx.author.mention}, You have planted {amount} carrots."
            
            embed.set_footer(text=f"Made by mal023")
            
            await ctx.send(embed=embed)

            # Update last action time
            update_last_action_time(user_id, "plant")
        except Exception as e:
            print(e)



    @commands.command(aliases=['har'])
    async def harvest(self, ctx):
        user_id = str(ctx.author.id)
        user_plantations = load_user_plants() # load planted crops
        plantation = user_plantations.get(user_id) # get what that user has planted (and when)
        try:
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
                    embed.set_footer(text=f"Made by mal023")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="Info", description=f"{ctx.author.mention}, Your carrots are not ready yet. They are {int(growth_percentage)}% grown.", color=embed_error)
                    embed.set_footer(text=f"Made by mal023")
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Error", description=f"{ctx.author.mention}, You don't have any crops planted.", color=embed_error)
                embed.set_footer(text=f"Made by mal023")
                await ctx.send(embed=embed)

            save_user_plants(user_plantations) # save data
        except Exception as e:
            print(e)
            

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Farming Cog Loaded! {Fore.RESET}')
        global user_carrot_plantations
        user_carrot_plantations = load_user_plants() # load plantd crops


def farming_setup(bot):
    bot.add_cog(Farming(bot))
