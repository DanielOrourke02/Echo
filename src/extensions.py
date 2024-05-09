

from utilities import *
from eco_support import *






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
        embed = discord.Embed(title="Crafting Recipes", color=discord.Colour.green())
        
        for recipe_name, ingredients in crafting_recipes.items():
            recipe_text = ', '.join([f"{count}x {item}" for item, count in ingredients.items() if item != 'result'])
            embed.add_field(name=recipe_name, value=recipe_text, inline=False)

        embed.set_footer(text=f"Made by mal023")

        await ctx.send(embed=embed)


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

                embed.set_footer(text=f"Made by mal023")

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

                    embed.set_footer(text=f"Made by mal023")

                    await ctx.send(embed=embed)
                else:
                    # Remove used items from inventory and add crafted item
                    for ingredient, count in recipe.items():
                        if ingredient != 'result':
                            for _ in range(count):
                                remove_item_from_inventory(user_id, ingredient)

                    add_item_to_inventory(user_id, recipe['result'])

                    embed = discord.Embed(title="Crafting Successful", description=f"You have crafted {recipe['result']}.", color=discord.Color.green())

                    embed.set_footer(text=f"Made by mal023")

                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Error", description="This item cannot be crafted or does not exist.", color=embed_error)
                embed.set_footer(text=f"Made by mal023")
                await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Crafting Cog Loaded! {Fore.RESET}')


def crafting_setup(bot):
    bot.add_cog(Crafting(bot))






# COOKING COG






class Cooking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cook(self, ctx):
        user_id = ctx.author.id

        user_inventory = get_user_inventory(user_id)

        if 'stove' not in user_inventory:
            embed = discord.Embed(
                title="Unable to cook",
                description=f"{ctx.author.mention}, You need a stove to start cooking! Buy one using `{prefix}buy stove`!",
                color=embed_error
            )
                
            embed.set_footer(text="Made by mal023")
                
            await ctx.send(embed=embed)
            return

        if 'red' not in user_inventory:
            embed = discord.Embed(
                title="Unable to cook",
                description=f"{ctx.author.mention}, You need at least one Red phosphorus to start cooking! Buy it using `{prefix}buy red`!",
                color=embed_error
            )
                
            embed.set_footer(text="Made by mal023")
                
            await ctx.send(embed=embed)
            return
        
        if 'chemical' not in user_inventory:
            embed = discord.Embed(
                title="Unable to cook",
                description=f"{ctx.author.mention}, You need at least one chemical to start cooking! Buy it using `{prefix}buy chemical`!",
                color=embed_error
            )
                
            embed.set_footer(text="Made by mal023")
                
            await ctx.send(embed=embed)
            return
        
        remove_item_from_inventory(user_id, 'chemical')

        remove_item_from_inventory(user_id, 'red')

        embed = discord.Embed(
            title="Who let him cook?",
            description="You have started cooking meth.",
            color=embed_colour
        )
        embed.set_footer(text="Made by mal023")

        message = await ctx.send(embed=embed)

        await asyncio.sleep(2)
        # Edit the message to indicate heating the pan
        embed.description = f"Turning on the stove..."
        await message.edit(embed=embed)

        await asyncio.sleep(3)
        # Edit the message to indicate heating up the pan#
        embed.description = f"Heating up the pan..."
        await message.edit(embed=embed)

        await asyncio.sleep(3)
        # Edit the message to indicate adding ingredients
        embed.description = f"Adding special ingredients..."
        await message.edit(embed=embed)

        await asyncio.sleep(3)

        # Start a timer for 30 seconds with updates every 3 seconds
        for i in range(11):
            progress = i * 10
            embed.description = f"Cooking in progress... {progress}% complete"
            await message.edit(embed=embed)
            await asyncio.sleep(3)

        # Add meth to the user's inventory
        for i in range(5):
            add_item_to_inventory(user_id, 'meth')

        # After completion, you can update the message to indicate it's done
        embed.description = f"Cooking is complete! 5 Meth has been cooked! Sell them on the streets using `{prefix}streets`."
        await message.edit(embed=embed)


    @commands.command()
    async def streets(self, ctx, amount: int=None):
        user_id = ctx.author.id
        user_inventory = get_user_inventory(user_id)

        if amount is None:
            embed = discord.Embed(
                title="Incorrect usage",
                description=f"{ctx.author.mention}, incorrect usage. Please try: `{prefix}streets <amount2sell>",
                color=embed_error
            )
            await ctx.send(embed=embed)
            return
        
        if amount > 15:
            embed = discord.Embed(
                title="Max Meth sell",
                description=f"{ctx.author.mention}, You can only sell 15 meth all at once!",
                color=embed_error
            )
            await ctx.send(embed=embed)
            return

        if amount <= 0:
            embed = discord.Embed(
                title="Invalid amount",
                description=f"{ctx.author.mention}, please enter a valid amount greater than zero.",
                color=embed_error
            )
            await ctx.send(embed=embed)
            return
        
        meth_count = sum(item == 'meth' for item in user_inventory)
        if meth_count < amount:
            embed = discord.Embed(
                title="Insufficient meth",
                description=f"{ctx.author.mention}, You only have {meth_count} meth to sell, which is less than the requested amount of {amount}.",
                color=embed_error
            )
            await ctx.send(embed=embed)
            return

        try:
            user_id = ctx.author.id
            
            if not can_sell_meth(user_id):
                embed = discord.Embed(
                    title="Cooldown Active",
                    description=f"{ctx.author.mention}, The streets are empty. Try again in 1 hour.",
                    color=embed_error
                )
                    
                embed.set_footer(text=f"Made by mal023")
                    
                await ctx.send(embed=embed)
                return
            
            if 'meth' not in user_inventory:
                embed = discord.Embed(
                    title="Unable to sell",
                    description=f"{ctx.author.mention}, You don't have any meth to sell! Cook some using `{prefix}cook`!",
                    color=embed_error
                )

                embed.set_footer(text="Made by mal023")

                await ctx.send(embed=embed)

                return

            update_last_action_time(user_id, "sell")

            conversations = [
                "Hey, do you have the special item in stock? Can I buy?",
                "Hi, I'm interested in the special item. Is it available for purchase?",
                "Hello, I heard you're selling the special goods. Can I get some?",
                "Hi there, are the special items available? I'd like to buy some.",
                "Hey, I'm looking to buy the special item. Do you have it?",
                "Excuse me, do you sell the special goods? I'd like to make a purchase.",
                "Hi, I'm interested in buying the special item. Is it in stock?",
                "Hey, can I buy the special goods from you?",
                "Hello, do you have the special item available for purchase?",
                "Hi, I'd like to buy the special goods. Are they available?",
                "Excuse me, are you selling the special item? I'd like to buy it.",
                "Hello, I'm interested in purchasing the special goods. Can I buy them here?",
                "Hi, do you sell the special item? I'd like to make a purchase.",
                "Hey, are the special goods available for purchase?",
                "Hello, I'd like to buy the special item. Can I do that here?",
                "Hi there, do you have the special goods in stock? I want to buy them.",
                "Hi, I'm interested in purchasing the special item. Can I buy it now?",
                "Hey, I heard you have the special goods. Can I buy some?",
                "Hello, are the special items available for purchase? I'd like to buy.",
                "Hi, I'm looking to buy the special goods. Do you have them?"
            ]

            chosen_conversations = []

            for i in range(amount):
                try:
                    conversation = random.choice(conversations)
                    conversations.remove(conversation)  # Remove the chosen conversation from the list to avoid repetition

                    # Randomly determine whether to add '..' to the conversation
                    if random.random() < 0.45:
                        position = random.randint(0, len(conversation))
                        modified_conversation = conversation[:position] + " .. " + conversation[position:]
                        chosen_conversations.append(modified_conversation)
                    else:
                        chosen_conversations.append(conversation)
                except Exception as e:
                    print(e)

            embed = discord.Embed(title="Selling on the streets", description="Respond by entering 'sell' or 'pass' in chat.", color=embed_colour)

            loop_count = 0

            for conversation in chosen_conversations:
                loop_count += 1

                embed.clear_fields()
                embed.add_field(name="Conversation", value=f"{conversation}", inline=False)
                message = await ctx.send(embed=embed)
                    
                def check(m):
                    try:
                        print(f"Checking message: {m.content} from {m.author} in {m.channel}")  # Debug print
                        condition = m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['sell', 'pass']
                        print(f"Condition met: {condition}")  # Debug print
                        return condition
                    except Exception as e:
                        print(e)
                        return e

                try:
                    response = await self.bot.wait_for('message', timeout=15.0, check=check)

                    print("Response received:", response.content.lower())  # Debug print statement

                    if response.content.lower() == 'sell':
                        if '..' in conversation.lower():
                            total_profit = len(conversation) * meth_sell_price

                            for _ in range(loop_count):
                                remove_item_from_inventory(user_id, 'meth')

                            embed = discord.Embed(
                                title="Got caught!",
                                description="You just sold to a cop! You got arrested and all your goods were taken!",
                                color=embed_error
                            )
                            embed.set_footer(text="Made by mal023")

                            await message.edit(embed=embed)

                            return
                        else:
                            # Successful sale
                            embed = discord.Embed(
                                title="You just sold meth.",
                                description=f"{ctx.author.mention}, Successfully sold 1 meth for {meth_sell_price}",
                                color=discord.Color.green(),
                            )
                            embed.set_footer(text=f"Made by mal023")

                            await message.edit(embed=embed)

                            update_user_balance(user_id, meth_sell_price)
                            remove_item_from_inventory(user_id, 'meth')
                    else:
                        embed = discord.Embed(
                            title="Pass",
                            description=f"{ctx.author.mention}, You chose not to sell to the person.",
                            color=embed_colour,  # Corrected color assignment
                        )
                        embed.set_footer(text=f"Made by mal023")

                        await message.edit(embed=embed)
                except asyncio.TimeoutError:
                    embed = discord.Embed(
                        title="Too slow",
                        description=f"{ctx.author.mention}, You took too long to respond.",
                        color=embed_error,
                    )
                    embed.set_footer(text=f"Made by mal023")

                    await message.edit(embed=embed)

                    return
                
                except Exception as e:
                    print("An error occurred:", e)  # Debug print statement

                    embed = discord.Embed(
                        title="Error",
                        description=f"An error occurred while processing your request. Please try again later. {e}",
                        color=embed_error,
                    )

                    embed.set_footer(text=f"Made by mal023")

                    await message.edit(embed=embed)

                    return
        except Exception as e:
            print(e)

            embed = discord.Embed(
                title="Error",
                description=f"{e}",
                color=embed_error,
            )

            embed.set_footer(text=f"Made by mal023")

            await ctx.send(embed=embed)
            

        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Cooking Cog Loaded! {Fore.RESET}')


def economy_setup(bot):
    bot.add_cog(Cooking(bot))





# WALLETS COG





class Droped_Wallets(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Wallets Cog Loaded! {Fore.RESET}')


def Droped_Wallets_setup(bot):
    bot.add_cog(Droped_Wallets(bot))





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




# EXAMPLE COG (add your own extensions)
# Go back to main.py and import your cog
# then add it to the 'setup_bot' function

"""
class Example(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def example(self, ctx):
        embed = discord.Embed(
            title="Example",
            description=f"{ctx.author.mention}, This is an example command! ",
            color=embed_colour,
        )

        embed.set_footer(text=f"Made by mal023")

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Example Cog Loaded! {Fore.RESET}')

def example_setup(bot):
    bot.add_cog(Example(bot))
"""
