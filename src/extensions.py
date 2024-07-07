

from utilities import *
from eco_support import *


"""
SCROLL TO THE BOTTOM FOR A SHORT BUT SIMPLE
GUIDE ON HOW TO ADD AND CREATE YOUR OWN COGS
(basically extensions of the bot)
"""





# FARMING COG






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
                
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
                
                await ctx.send(embed=embed)
                return

            total_cost = amount * cost_per_carrot # total cost of planting their amount of carrots

            embed = discord.Embed(color=discord.Color.green())

            # Check if the user has already planted carrots
            if user_has_plants(user_id):
                embed.title = "Wait a Little Longer"
                
                embed.description = f"{ctx.author.mention}, Your plants take {config.get('carrot_growth_duration')} hours to grow. Try harvesting them using: `{prefix}harvest`."
                
                embed.color = embed_error
                
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
                
                await ctx.send(embed=embed)
                return

            # Check if the user is trying to plant too many carrots
            if amount > max_carrot_planted:
                embed.title = "Too Many Carrots"
                
                embed.description = f"{ctx.author.mention}, You cannot plant more than {max_carrot_planted} carrots."
                
                embed.color = embed_error
                
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
                
                await ctx.send(embed=embed)
                return

            # Check if the user has enough balance
            if user_balance < total_cost:
                embed.title = "Not Enough Balance"
                
                embed.description = f"{ctx.author.mention}, You need {total_cost} zesty coins to plant {amount} carrots"
                
                embed.color = embed_error
                
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
                
                await ctx.send(embed=embed)
                return

            # Plant carrots
            plant_carrots(user_id, amount)

            # Send success message
            embed.title = "Carrots Planted"
            
            embed.description = f"{ctx.author.mention}, You have planted {amount} carrots."
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
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
                    embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="Info", description=f"{ctx.author.mention}, Your carrots are not ready yet. They are {int(growth_percentage)}% grown.", color=embed_error)
                    embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Error", description=f"{ctx.author.mention}, You don't have any crops planted.", color=embed_error)
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
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






# CRAFTING COG






class Crafting(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        
    @commands.command()
    async def recipes(self, ctx):
        """
        Displays crafting recipes.

        Parameters:
            ctx (commands.Context): The context of the command.

        Returns:
            None
        """
        try:
            embed = discord.Embed(title="Crafting Recipes", description="The 🎉 emoji means you have the materials to craft that item!", color=discord.Colour.green())

            user_id = ctx.author.id
            user_inventory = get_user_inventory(user_id)

            for recipe_id, recipe_details in crafting_recipes.items():
                missing_items = {}
                for ingredient, count in recipe_details.items():
                    if ingredient != 'result' and (user_inventory.count(ingredient) < count):
                        missing_items[ingredient] = count - user_inventory.count(ingredient)

                if not missing_items:  # If there are no missing items for this recipe
                    result_sell_price = craftables.get(recipe_id, {}).get('sell', 'unknown price')
                    recipe_text = ', '.join([f"{count}x {combined_items[item]['name']}" for item, count in recipe_details.items() if item != 'result'])
                    embed.add_field(name=f"{recipe_id} 🎉", value=f"**Sell price: {result_sell_price}**\n{recipe_text}", inline=False)
                else:
                    recipe_text = ', '.join([f"{count}x {combined_items[item]['name']}" for item, count in recipe_details.items() if item != 'result'])
                    embed.add_field(name=f"{recipe_id}", value=f"**Sell price: {craftables.get(recipe_id, {}).get('sell', 'unknown price')}**\n{recipe_text}", inline=False)

            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(e)
            print(e)


    @commands.command()
    async def craft(self, ctx, item_name: str=None):
        """
        Craft an item using the specified recipe.

        Parameters:
            ctx (commands.Context): The context of the command.
            item_name (str): The name of the item to craft.

        Returns:
            None
        """
        user_id = ctx.author.id

        try:
            # Check if item_name is empty
            if item_name is None:
                embed = discord.Embed(title="Incorrect Usage", description=f"Correct usage: `{ctx.prefix}craft <item>`", color=embed_error)

                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

                await ctx.send(embed=embed)
                return

            item_name = item_name.lower()

            if item_name in crafting_recipes:
                recipe = crafting_recipes[item_name]
                inventory = get_user_inventory(user_id)
                missing_items = {}

                # Check for each item in the recipe
                for ingredient, count in recipe.items():
                    if ingredient != 'result' and (inventory.count(ingredient) < count):
                        missing_items[ingredient] = count - inventory.count(ingredient)

                # If missing items
                if missing_items:
                    missing_items_text = ', '.join([f"{count}x {item}" for item, count in missing_items.items()])

                    embed = discord.Embed(title="Missing Items", description=f"You are missing {missing_items_text} for crafting {item_name}.", color=embed_error)

                    embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

                    await ctx.send(embed=embed)
                else:
                    # Remove used items from inventory and add crafted item
                    for ingredient, count in recipe.items():
                        if ingredient != 'result':
                            for _ in range(count):
                                remove_item_from_inventory(user_id, ingredient)

                    add_item_to_inventory(user_id, recipe['result'])

                    embed = discord.Embed(title="Crafting Successful", description=f"You have crafted {recipe['result']}.", color=discord.Color.green())

                    embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Error", description="This item cannot be crafted or does not exist.", color=embed_error)
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
                await ctx.send(embed=embed)
        except Exception as e:
            print(e)
        
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Crafting Cog Loaded! {Fore.RESET}')


def crafting_setup(bot):
    bot.add_cog(Crafting(bot))




# HEISTS COG





class Heists(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Heists Cog Loaded! {Fore.RESET}')


def Heists_setup(bot):
    bot.add_cog(Heists(bot))





# JOBS COG





class Jobs(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Jobs Cog Loaded! {Fore.RESET}')


def Jobs_setup(bot):
    bot.add_cog(Jobs(bot))





# SPECIAL EVENTS COG





class Events(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Events Cog Loaded! {Fore.RESET}')


def Events_setup(bot):
    bot.add_cog(Events(bot))





# PROPERTIES COG





class Properties(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Properties Cog Loaded! {Fore.RESET}')


def Properties_setup(bot):
    bot.add_cog(Properties(bot))





# MONEY PRINTING COG





class Printing(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Money Printing Cog Loaded! {Fore.RESET}')


def Printing_setup(bot):
    bot.add_cog(Printing(bot))




# EXAMPLE COG (add your own extensions to the bot)
# Go back to main.py and import your cog (line 20)
# then add it to the 'setup_bot' function (line 41)

"""
class Example(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def example(self, ctx):
        embed = discord.Embed(
            title="Example",
            description=f"{ctx.author.mention}, This is an example command! ",
            color=embed_colour, # embed_colour is a cyan colour (located in utilities.py)
        )

        embed.set_footer(text=f"Extension made by xxx") # replace with your username

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Example Cog Loaded! {Fore.RESET}')

def example_setup(bot):
    bot.add_cog(Example(bot))
"""
