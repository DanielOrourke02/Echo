

from eco_support import *
from utilities import *


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

            meth_sell_price = 4000

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
                    return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['sell', 'pass']

                try:
                    response = await self.bot.wait_for('message', timeout=30.0, check=check)

                    print("Response received:", response.content.lower())  # Debug print statement

                    if response.content.lower() == 'sell':
                        if '..' in conversation.lower():
                            total_profit = len(conversation) * meth_sell_price

                            for _ in range(loop_count):
                                remove_item_from_inventory(user_id, 'meth')
                                update_user_balance(user_id, -total_profit)

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
                        description=f"An error occurred while processing your request. Please try again later.",
                        color=embed_error,
                    )

                    embed.set_footer(text=f"Made by mal023")

                    await message.edit(embed=embed)

                    return
        except Exception as e:
            print(e)
            

        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Cooking Cog Loaded! {Fore.RESET}')


def economy_setup(bot):
    bot.add_cog(Cooking(bot))
