

from utilities import *
from eco_support import *


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['inv'])
    async def inventory(self, ctx, user: commands.MemberConverter=None):
        if user is None:
            user_id = ctx.author.id
            inventory = get_user_inventory(user_id)

            # Use Counter to count the occurrences of each item in the inventory
            item_counts = Counter(inventory)

            # Create an embed to display the inventory
            embed = discord.Embed(title=f"{ctx.author.name}'s Inventory", color=embed_error)
            
            # Add fields for each unique item and its count
            for item, count in item_counts.items():
                embed.add_field(name=item, value=f"Count: {count}", inline=True)

            # Send the inventory as an embed
            await ctx.send(embed=embed)
        else:
            user_id = user.id
            inventory = get_user_inventory(user_id)

            # Use Counter to count the occurrences of each item in the inventory
            item_counts = Counter(inventory)

            # Create an embed to display the inventory
            embed = discord.Embed(title=f"{user.display_name}'s Inventory", color=embed_error)
            
            # Add fields for each unique item and its count
            for item, count in item_counts.items():
                embed.add_field(name=item, value=f"Count: {count}", inline=True)

            # Send the inventory as an embed
            await ctx.send(embed=embed)

    
    # Command to give money to a user (TO REMOVE DO /GIVE <USER> -<amount>)
    @commands.command()
    @commands.check(is_admin) # Only one user can do this (put the id in config.json)
    async def give(self, ctx, user: commands.MemberConverter, amount: int):
        update_user_balance(user.id, amount)
        embed = discord.Embed(
            title="Coins Given!",
            description=f"Admin {ctx.author.display_name} has given {amount} coins to {user.display_name}.",
            color=discord.Color.green()
        )

        # Send the embed
        await ctx.send(embed=embed)


    # Command to remove items from a users inventory
    @commands.command()
    @commands.check(is_admin) # Only one user can do this (put the id in config.json)
    async def remove_item(self, ctx, user: commands.MemberConverter, item: str):
        remove_item_from_inventory(user.id, item)
        embed = discord.Embed(
            title="Coins Given!",
            description=f"Admin {ctx.author.display_name} has removed {item} from {user.display_name} inventory!.",
            color=discord.Color.green()
        )

        # Send the embed
        await ctx.send(embed=embed)

    
    # Error handling for the give command
    @give.error
    async def give_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            # Create an embed for the error message with red color
            embed = discord.Embed(
                title="Permission Denied",
                description="You don't have permission to use this command.",
                color=embed_error
            )
            await ctx.send(embed=embed)
    

    # pay another user money
    @commands.command()
    async def pay(self, ctx, user: commands.MemberConverter=None, amount: int=None):
        if amount is None or amount <= 0:
            embed = discord.Embed(
                title="Invalid Amount",
                description=f"Please specify an amount to pay. Usage: `{prefix}pay <@user> <amount>`",
                color=embed_error
            )
            await ctx.send(embed=embed)
            return
        
        if user is None:
            embed = discord.Embed(
                title="Not a user",
                description=f"Please specify a user. Usage: `{prefix}pay <@user> <amount>`",
                color=embed_error
            )
            await ctx.send(embed=embed)
            return         

        payer_id = str(ctx.author.id)
        user_id = str(user.id)

        if payer_id == user_id: # check if they tried to pay themself
            embed = discord.Embed(
                title="Payment Error",
                description="You can't pay yourself.",
                color=embed_error
            )
            await ctx.send(embed=embed)
            return

        if amount > get_user_balance(payer_id): # if they dont have enough money
            embed = discord.Embed(
                title="Insufficient Balance",
                description="You don't have enough coins to make that payment.",
                color=embed_error
            )
            await ctx.send(embed=embed)
            return

        # Assuming update_user_balance and get_user_balance are defined elsewhere
        update_user_balance(payer_id, -amount) # reduce the mount they paid
        update_user_balance(user_id, amount) # add it to the reciver

        embed = discord.Embed(
            title="Payment Successful",
            description=f"You successfully paid {user.mention} {amount} coins!",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)


    # buy items from the list of items
    @commands.command()
    async def buy(self, ctx, item_name: str=None):
        if item_name not in shop_items: # check if the item is in the shop
            embed = discord.Embed(
                title="Item Not Found",
                description="Item not found in the shop.",
                color=embed_error
            )
            await ctx.send(embed=embed)
            return
        elif item_name is None:
            embed = discord.Embed(
                title="Incorrect buy usage",
                description=f"Please specify an item name. Usage: `{prefix}buy <item_name>`",
                color=embed_error
            )
            await ctx.send(embed=embed)
            return

        item_name = item_name.lower() # make it lower case (prevent stuff like eXaMPLE by changing to to example)

        user = ctx.author

        item_cost = shop_items[item_name]['cost'] # get the item cost
        user_balance = get_user_balance(user.id) # get the user balance

        if user_balance < item_cost: # if they dont have enough output an error message
            embed = discord.Embed(
                title="Insufficient Coins (poor)",
                description="You do not have enough coins to buy this item.",
                color=embed_error
            )
            await ctx.send(embed=embed)
            return

        update_user_balance(user.id, -item_cost) # update their user balance
        add_item_to_inventory(user.id, item_name) # add the item to their inventory
        log_purchase(user.id, 1, user.name, shop_items[item_name]['name'], item_cost) # log the purchase

        # Check if the item has (role) in its name and assign the role
        # Role values and colours are in 'eco_support.py'
        if "(role)" in shop_items[item_name]['name'].lower(): # if the item name has (role) inside the str we know its a role you can buy
            role_name = shop_items[item_name]['name'].split(" (")[0]  # Extract role name
            await assign_role_to_user(ctx, role_name) # give role to the author/user

        embed = discord.Embed(
            title="Purchase Successful",
            description=f"You have successfully bought {shop_items[item_name]['name']} for {item_cost} coins.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)


    @commands.command()
    async def dig(self, ctx):
        user_id = ctx.author.id

        # Check if the user has a 'shovel' in their inventory
        user_inventory = get_user_inventory(user_id)
        if 'shovel' not in user_inventory:
            embed = discord.Embed(
                title="Unable to Dig",
                description=f"You need a shovel to dig! Acquire a shovel and try again.",
                color=embed_error
            )
            await ctx.send(embed=embed)
            return

        # check for a cooldown
        if not can_dig(user_id):
            embed = discord.Embed(
                title="Cooldown Active",
                description="You've already gone digging in the past 15 minutes. Please wait for the cooldown.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return

        # Simulate winning an item based on chances
        chosen_item = random.choices(list(cosmetics_items.keys()), weights=[item["chance"] for item in cosmetics_items.values()], k=1)[0]

        # Get the details of the won item
        won_item = cosmetics_items[chosen_item]

        # Update user's last dig time
        user_balances[f"{user_id}_last_dig"] = time.time()

        # Add the won item to the user's inventory
        add_item_to_inventory(user_id, chosen_item)

        embed = discord.Embed(
            title="Item Found",
            description=f"You found: {won_item['name']}! Check your inventory with `{prefix}inventory`.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

        amount = random.randint(1000, 1600) # random amount of money

        user_balances[f"{user_id}_last_dig"] = time.time() # update cooldown
        update_user_balance(ctx.author.id, amount) # update balance

        embed = discord.Embed(
            title="Coins Found",
            description=f"You found: {amount} coins! Your new balance is: {get_user_balance(ctx.author.id)}.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)


    @commands.command()
    async def hunt(self, ctx):
        user_id = ctx.author.id

        # Check if the user has a 'bow' in their inventory
        # if not dont let them run the hunt command
        user_inventory = get_user_inventory(user_id)
        if 'bow' not in user_inventory:
            embed = discord.Embed(
                title="Unable to Hunt",
                description=f"You need a bow to hunt! Find one using `{prefix}scrap`!",
                color=embed_error
            )
            await ctx.send(embed=embed)
            return

        # check if they can hunt (not on cooldown)
        if not can_hunt(user_id):
            embed = discord.Embed(
                title="Cooldown Active",
                description="You've already hunted in the past 10 minutes. Please wait for the cooldown.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return

        # Simulate winning an item based on chances
        chosen_item = random.choices(list(cosmetics_items.keys()), weights=[item["chance"] for item in cosmetics_items.values()], k=1)[0]

        # Get the details of the won item
        won_item = cosmetics_items[chosen_item]

        # Update user's last hunt time
        user_balances[f"{user_id}_last_hunt"] = time.time()

        # Add the won item to the user's inventory
        add_item_to_inventory(user_id, chosen_item)

        embed = discord.Embed(
            title="Item Found",
            description=f"You found: {won_item['name']}! Check your inventory with `{prefix}inventory`",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

        amount = random.randint(600, 1300) # random money amount

        user_balances[f"{user_id}_last_hunt"] = time.time() # update cooldown
        update_user_balance(ctx.author.id, amount) # update balance

        embed = discord.Embed(
            title="Coins Found",
            description=f"You found: {amount} coins! Your new balance is: {get_user_balance(ctx.author.id)}.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)


    @commands.command()
    async def scrap(self, ctx):
        user_id = ctx.author.id

        if not can_scavenge(user_id):
            embed = discord.Embed(
                title="Cooldown Active",
                description="You've already scavenged in the past 5 minutes. Please wait for the cooldown.",
                color=embed_error
            )
            await ctx.send(embed=embed)
            return

        # Simulate winning an item based on chances
        chosen_item = random.choices(list(cosmetics_items.keys()), weights=[item["chance"] for item in cosmetics_items.values()], k=1)[0]

        # Get the details of the won item
        won_item = cosmetics_items[chosen_item]
        
        # Update user's last scavenge time
        user_balances[f"{user_id}_last_scavenge"] = time.time()

        # Add the won item to the user's inventory
        add_item_to_inventory(user_id, chosen_item)

        embed = discord.Embed(
            title="Item Found",
            description=f"You found: {won_item['name']}! Check your inventory with `{prefix}inventory`",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

        amount = random.randint(400, 800)

        user_balances[f"{user_id}_last_scavenge"] = time.time()
        update_user_balance(ctx.author.id, amount)

        embed = discord.Embed(
            title="Coins Found",
            description=f"You found: {amount} coins! Your new balance is: {get_user_balance(ctx.author.id)}.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)


    @commands.command()
    async def beg(self, ctx):
        user_id = ctx.author.id

        if not can_beg(user_id):
            embed = discord.Embed(
                title="Cooldown Active",
                description="You begged in the past 30s. Wait the cooldown.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return

        amount = random.randint(100, 200)

        update_user_balance(user_id, amount)

        embed = discord.Embed(
            title="Successful Begging",
            description=f'You begged and some idiot gave you {amount}.',
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

        # Correctly update the last beg time
        user_balances[f"{user_id}_last_beg"] = time.time()


    @commands.command()
    async def daily(self, ctx):
        user_id = ctx.author.id

        if not can_claim_daily(user_id):
            embed = discord.Embed(
                title="Daily Reward Already Claimed",
                description="You've already claimed your daily reward. Please wait for the cooldown.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return

        update_user_balance(user_id, daily_reward)
        set_last_claim_time(user_id) # update daily cooldown

        embed = discord.Embed(
            title="Daily Reward Claimed",
            description=f'You have claimed your daily reward of {daily_reward} coins!',
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

        # Update user's last claim time (if needed)
        user_balances[f"{user_id}_last_daily"] = time.time()


    @commands.command()
    async def sell(self, ctx, item_id: str=None):
        user_id = ctx.author.id

        if item_id is None:
            embed = discord.Embed(
                title="Incorrect Usage",
                description=f"Incorrect usage. Please use: `{prefix}sell <item>`",
                color=embed_error
            )
            await ctx.send(embed=embed)
            return
        
        item_id = item_id.lower() # make it lower to prevent stuff like LeG.SwoRD 

        if item_id not in combined_items: # check if the item is in the sell list
            embed = discord.Embed(
                title="Invalid Item ID",
                description="Invalid item ID.",
                color=embed_error
            )
            await ctx.send(embed=embed)
            return

        user_inventory = get_user_inventory(user_id)
        user = await self.bot.fetch_user(ctx.author.id) 

        if item_id not in user_inventory: # check if they own the item
            embed = discord.Embed(
                title="Item Not Found",
                description="You don't have this item in your inventory.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return

        item_info = combined_items[item_id] # id
        item_name = item_info["name"] # name
        item_sell_price = item_info["sell"] # price

        # Update user's balance
        update_user_balance(user_id, item_sell_price)

        # Remove the item from the user's inventory
        remove_item_from_inventory(user_id, item_id)

        embed = discord.Embed(
            title="Item Sold",
            description=f"You sold {item_name} for {item_sell_price} coins. Your new balance is: {get_user_balance(user_id)}!",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)


    global refund_lottery_tickets

    @commands.command(aliases=['lottery', 'lotto'])
    async def enterlottery(self, ctx):
        user_id = str(ctx.author.id)

        # Check if user has enough balance
        if get_user_balance(user_id) < entry_fee:
            embed = discord.Embed(
                title="Lottery Entry Error",
                description=f"{ctx.author.mention}, you need 1000 coins to enter the lottery.",
                color=embed_error
            )
            await ctx.send(embed=embed)
            return

        # Deduct entry fee from user's balance
        update_user_balance(user_id, -entry_fee)
        
        # Add user to the lottery pool
        lottery_pool.add(user_id)
        embed = discord.Embed(
            title="Lottery Entry",
            description=f"{ctx.author.mention} has entered the Lottery! (Entry fee: 1000 coins). You are now in a chance to win 5K!",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

        # Check if lottery pool has enough members to draw
        if len(lottery_pool) >= required_participants:
            winner_id = random.choice(list(lottery_pool)) # random winner
            update_user_balance(winner_id, 5000)
            embed = discord.Embed(
                title="Lottery Winner!",
                description=f"Congratulations <@{winner_id}>! You won the 5000 coins lottery prize!",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            lottery_pool.clear() # clear the lottery pool for a new lottery

        # If not enough participants, start a refund timer
        if len(lottery_pool) < required_participants:
            await asyncio.sleep(refund_timer)
            if len(lottery_pool) < required_participants:
                try:
                    await refund_lottery_tickets()
                    embed = discord.Embed(
                        title="Not enough Participants!!",
                        description=f"Refunded lottery tickets. Not enough participants!",
                        color=discord.Color.orange()
                    )
                    await ctx.send(embed=embed)
                except Exception as e:
                    embed = discord.Embed(
                        title="Error",
                        description=f"Error while refunding lottery tickets.",
                        color=embed_error
                    )
                    await ctx.send(embed=embed)
                    print(f'{Fore.CYAN}Error while attempting to refund lottery tickets. {Fore.RED}ERROR: {e}{Fore.RESET}')
                

    async def refund_lottery_tickets():
        # Refund entry fee to all participants
        for user_id in lottery_pool:
            update_user_balance(user_id, entry_fee)

        lottery_pool.clear()
        print("Refunded lottery tickets.")


    @commands.command()
    async def deposit(self, ctx, amount=None):
        if amount == 'all': # deposit as much as possible
            amount = get_user_balance(ctx.author.id)
        elif amount == None:
            embed = discord.Embed(
                title="Incorrect deposit usage!",
                description=f"Incorrect deposit usage, please use: `{prefix}deposit <amount>`",
                color=embed_error
            )   
            await ctx.send(embed=embed)
            return
        else:
            try:
                amount = int(amount)
            except ValueError:
                embed = discord.Embed(
                    title="Invalid deposit amount",
                    description=f"Please enter a valid amount.",
                    color=embed_error
                )
                await ctx.send(embed=embed)
                return

        if amount <= 0 or amount > get_user_balance(ctx.author.id):
            embed = discord.Embed(
                title="Invalid deposit amount",
                description=f"Please enter a valid amount.",
                color=embed_error
            )
            await ctx.send(embed=embed)
            return

        if get_bank_balance(ctx.author.id) + amount > max_bank_size:  # Max bank limit
            embed = discord.Embed(
                title="Bank limit Reached",
                description=f"Bank limit exceeded. Max storage is {max_bank_size} coins.",
                color=embed_error
            )
            await ctx.send(embed=embed)
            return

        update_user_balance(ctx.author.id, -amount)
        update_bank_balance(ctx.author.id, amount)

        # Embed the message
        embed = discord.Embed(
            title="Deposit Successful",
            description=f'{amount} coins deposited to your bank account.',
            color=embed_colour
        )
        await ctx.send(embed=embed)


    @commands.command()
    async def withdraw(self, ctx, amount: int=None):
        if amount is None: # if they didnt enter an amount
            embed = discord.Embed(
                title="Incorrect withdraw usage!",
                description=f'Incorrect withdraw usage. Please use: `{prefix}withdraw <amount>`',
                color=embed_error
            )
            await ctx.send(embed=embed)
            return
        
        elif amount <= 0 or amount > get_bank_balance(ctx.author.id): # check if they have that amount to withdraw
            embed = discord.Embed(
                title="Invalid withdraw amount",
                description=f'Invalid withdraw amount. Please try again.',
                color=embed_error
            )
            await ctx.send(embed=embed)
            return

        update_bank_balance(ctx.author.id, -amount)
        update_user_balance(ctx.author.id, amount)

        # Embed the message
        embed = discord.Embed(
            title="Withdraw Successful",
            description=f'{amount} coins withdrawn from your bank account.',
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)


    @commands.command(aliases=['top', 'balancetop', 'balance_top'])
    async def baltop(self, ctx):
        # Check if the file exists and is not empty
        if not os.path.exists('user_data.json') or os.path.getsize('user_data.json') == 0: # access money json file and get the top 10 people
            await ctx.send("No data available.")
            return

        try:
            with open('user_data.json', 'r') as f:
                data = json.load(f)
                user_balances = data.get("user_balances", {})
        except json.JSONDecodeError:
            await ctx.send("Error reading user data.")
            return

        # Extracting user ID and balance, ignoring other keys
        balances = {user_id: data for user_id, data in user_balances.items() if user_id.isdigit() and isinstance(data, int)}

        # Sorting the dictionary by balance and getting top 10
        top_balances = dict(sorted(balances.items(), key=lambda item: item[1], reverse=True)[:10]) # complex asf idk how it works

        # Creating an embedded message with orange color
        embed = discord.Embed(
            title="Top Balances",
            description="\n".join([f"<@{user_id}>: {balance}" for user_id, balance in top_balances.items()]),
            color=discord.Color.orange()
        )

        # Sending the leaderboard
        await ctx.send(embed=embed)



    @commands.command(aliases=['bal'])
    async def balance(self, ctx):
        user_id = ctx.author.id
        pocket_money = get_user_balance(user_id)
        bank_balance = get_user_bank_balance(user_id)

        embed = discord.Embed(
            title="Balance",
            description=f'Money On hand: {pocket_money} coins\nBank Balance: {bank_balance}/{max_bank_size} coins',
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)


    @commands.command(aliases=['steal'])
    async def rob(self, ctx, victim: commands.MemberConverter):
        robber_id = str(ctx.author.id)
        victim_id = str(victim.id)

        # Check for cooldown
        if robber_id in robbery_cooldown and time.time() - robbery_cooldown[robber_id] < 3600:
            embed = discord.Embed(
                title="Cooldown",
                description=f'Wait the cooldown. You cant rob everyone buddy.',
                color=embed_error
            )
            await ctx.send(embed=embed)
            return

        # Set cooldown
        robbery_cooldown[robber_id] = time.time()

        # Check if both users have the minimum balance
        if get_user_balance(robber_id) < 100 or get_user_balance(victim_id) < 600:
            embed = discord.Embed(
                title="Rob fail lmao",
                description=f'Either you or the victim does not have enough coins. LOL',
                color=embed_error
            )
            await ctx.send(embed=embed)
            return

        if random.randint(0, 9) < 4:  # 50% chance of success
            robbed_amount = int(get_user_balance(victim_id) * 0.20)  # 20% of victim's balance
            update_user_balance(robber_id, robbed_amount)
            update_user_balance(victim_id, -robbed_amount)

            # Embed for success
            embed = discord.Embed(
                title="Robbery Success",
                description=f"You successfully robbed {robbed_amount} coins from {victim.mention}!",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            penalty_amount = int(get_user_balance(robber_id) * 0.20)  # 20% of robber's balance
            update_user_balance(robber_id, -penalty_amount)

            # Embed for failure
            embed = discord.Embed(
                title="Robbery Failed",
                description=f"The robbery failed! You've lost {penalty_amount} coins.",
                color=embed_error()
            )

        await ctx.send(embed=embed)
    
#-----------------GAMBLING GAMES-----------------

    @commands.command(aliases=['g'])
    async def gamble(self, ctx, amount: str = None):
        if amount is None: # if they didnt enter an amount to gamble
            embed = discord.Embed(
                title="Gamble Command",
                description=f"Please specify an amount to gamble. Usage: `{prefix}gamble <amount>`",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return

        # Check if the user entered "max"
        if amount.lower() == "max":
            amount = min(get_user_balance(ctx.author.id), max_bet) # gamble as much as possible (within max gamble limit)
        else:
            try:
                amount = int(amount)
            except ValueError:
                embed = discord.Embed(
                    title="Invalid Input",
                    description="Please enter a valid amount or 'max'.",
                    color=discord.Color.orange()
                )
                await ctx.send(embed=embed)
                return

        if amount <= 0 or amount > get_user_balance(ctx.author.id) or amount > max_bet:
            embed = discord.Embed(
                title="Invalid Bet Amount",
                description=f"Invalid bet amount. You can bet up to {max_bet} coins.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return

        # Gambling logic with 1/3 chance of winning
        if random.choice([True, False, False]):  # 1/3 chance
            # User wins
            update_user_balance(ctx.author.id, amount)
            result_description = f"You won {amount} coins!"
            result_color = discord.Color.green()
        else:
            update_user_balance(ctx.author.id, -amount)
            result_description = f"You lost {amount} coins!"
            result_color = embed_error

        # Send result embed
        result_embed = discord.Embed(
            title="Gamble Result",
            description=result_description,
            color=result_color
        )
        await ctx.send(embed=result_embed)


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Economy Cog Loaded! {Fore.RESET}')


def economy_setup(bot):
    bot.add_cog(Economy(bot))
