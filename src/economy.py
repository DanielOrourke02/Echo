

from utilities import *
from eco_support import *


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='inventory', aliases=['hotbar', 'inv'])
    async def inventory(self, ctx):
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
        await ctx.respond(embed=embed)

    
    # Command to give money to a user (TO REMOVE DO /GIVE <USER> -<amount>)
    @commands.slash_command(name='give')
    @commands.check(is_admin) # Only one user can do this (put the id in config.json)
    async def give(self, ctx, user: commands.MemberConverter, amount: int):
        update_user_balance(user.id, amount)
        embed = discord.Embed(
            title="Coins Given!",
            description=f"Admin {ctx.author.display_name} has given {amount} coins to {user.display_name}.",
            color=discord.Color.orange()
        )

        # Send the embed
        await ctx.respond(embed=embed)


    # Command to remove items from a users inventory
    @commands.slash_command(name='remove_item')
    @commands.check(is_admin) # Only one user can do this (put the id in config.json)
    async def remove_item(self, ctx, user: commands.MemberConverter, item: str):
        remove_item_from_inventory(user.id, item)
        embed = discord.Embed(
            title="Coins Given!",
            description=f"Admin {ctx.author.display_name} has removed {item} from {user.display_name} inventory!.",
            color=discord.Color.orange()
        )

        # Send the embed
        await ctx.respond(embed=embed)

    
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
            await ctx.respond(embed=embed)
    

    # pay another user money
    @commands.slash_command(name='pay', help="Pay another user")
    async def pay(self, ctx, user: commands.MemberConverter, amount: int):
        if amount is None or amount <= 0:
            embed = discord.Embed(
                title="Invalid Amount",
                description="Please specify a valid positive amount to pay. Usage: `/pay <user> <amount>`",
                color=discord.Color.orange()
            )
            await ctx.respond(embed=embed)
            return

        payer_id = str(ctx.author.id)
        user_id = str(user.id)

        if payer_id == user_id: # check if they tried to pay themself
            embed = discord.Embed(
                title="Payment Error",
                description="You can't pay yourself.",
                color=discord.Color.orange()
            )
            await ctx.respond(embed=embed)
            return

        if amount > get_user_balance(payer_id): # if they dont have enough money
            embed = discord.Embed(
                title="Insufficient Balance",
                description="You don't have enough coins to make that payment.",
                color=discord.Color.orange()
            )
            await ctx.respond(embed=embed)
            return

        # Assuming update_user_balance and get_user_balance are defined elsewhere
        update_user_balance(payer_id, -amount) # reduce the mount they paid
        update_user_balance(user_id, amount) # add it to the reciver

        embed = discord.Embed(
            title="Payment Successful",
            description=f"You successfully paid {user.mention} {amount} coins!",
            color=discord.Color.orange()
        )
        await ctx.respond(embed=embed)


    # buy items from the list of items
    @commands.slash_command(name='buy', help="Buy item from the shop")
    async def buy(self, ctx, item_name: str):
        if item_name not in shop_items:
            embed = discord.Embed(
                title="Item Not Found",
                description="Item not found in the shop.",
                color=discord.Color.orange()
            )
            await ctx.respond(embed=embed)
            return

        item_name = item_name.lower() # make it lower case (prevent stuff like eXaMPLE by changing to to example)

        user = ctx.author

        item_cost = shop_items[item_name]['cost']
        user_balance = get_user_balance(user.id)

        if user_balance < item_cost:
            embed = discord.Embed(
                title="Insufficient Coins",
                description="You do not have enough coins to buy this item.",
                color=discord.Color.orange()
            )
            await ctx.respond(embed=embed)
            return

        update_user_balance(user.id, -item_cost)
        add_item_to_inventory(user.id, item_name)
        log_purchase(user.id, 1, user.name, shop_items[item_name]['name'], item_cost)

        # Check if the item has (role) in its name and assign the role
        # Role values and colours are in 'eco_support.py'
        if "(role)" in shop_items[item_name]['name'].lower(): 
            role_name = shop_items[item_name]['name'].split(" (")[0]  # Extract role name
            await assign_role_to_user(ctx, role_name)

        embed = discord.Embed(
            title="Purchase Successful",
            description=f"You have successfully bought {shop_items[item_name]['name']} for {item_cost} coins.",
            color=discord.Color.green()
        )
        await ctx.respond(embed=embed)


    @commands.slash_command()
    async def dig(self, ctx):
        user_id = ctx.author.id

        # Check if the user has a 'shovel' in their inventory
        user_inventory = get_user_inventory(user_id)
        if 'shovel' not in user_inventory:
            embed = discord.Embed(
                title="Unable to Dig",
                description="You need a shovel to dig! Acquire a shovel and try again.",
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed)
            return

        if not can_dig(user_id):
            embed = discord.Embed(
                title="Cooldown Active",
                description="You've already gone digging in the past 15 minutes. Please wait for the cooldown.",
                color=discord.Color.orange()
            )
            await ctx.respond(embed=embed)
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
            description=f"You found: {won_item['name']}! Check your inventory with '/inventory'.",
            color=discord.Color.orange()
        )
        await ctx.respond(embed=embed)

        amount = random.randint(1000, 1600)

        user_balances[f"{user_id}_last_dig"] = time.time()
        update_user_balance(ctx.author.id, amount)

        embed = discord.Embed(
            title="Coins Found",
            description=f"You found: {amount} coins! Your new balance is: {get_user_balance(ctx.author.id)}.",
            color=discord.Color.orange()
        )
        await ctx.respond(embed=embed)


    @commands.slash_command()
    async def hunt(self, ctx):
        user_id = ctx.author.id

        # Check if the user has a 'bow' in their inventory
        # if not dont let them run the hunt command
        user_inventory = get_user_inventory(user_id)
        if 'bow' not in user_inventory:
            embed = discord.Embed(
                title="Unable to Hunt",
                description="You need a bow to hunt! Find one using /scrap!",
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed)
            return

        if not can_hunt(user_id):
            embed = discord.Embed(
                title="Cooldown Active",
                description="You've already hunted in the past 10 minutes. Please wait for the cooldown.",
                color=discord.Color.orange()
            )
            await ctx.respond(embed=embed)
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
            description=f"You found: {won_item['name']}! Check your inventory with '/inventory'.",
            color=discord.Color.orange()
        )
        await ctx.respond(embed=embed)

        amount = random.randint(600, 1300)

        user_balances[f"{user_id}_last_hunt"] = time.time()
        update_user_balance(ctx.author.id, amount)

        embed = discord.Embed(
            title="Coins Found",
            description=f"You found: {amount} coins! Your new balance is: {get_user_balance(ctx.author.id)}.",
            color=discord.Color.orange()
        )
        await ctx.respond(embed=embed)


    @commands.slash_command()
    async def scrap(self, ctx):
        user_id = ctx.author.id

        if not can_scavenge(user_id):
            embed = discord.Embed(
                title="Cooldown Active",
                description="You've already scavenged in the past 5 minutes. Please wait for the cooldown.",
                color=discord.Color.orange()
            )
            await ctx.respond(embed=embed)
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
            description=f"You found: {won_item['name']}! Check your inventory with '$inventory'.",
            color=discord.Color.orange()
        )
        await ctx.respond(embed=embed)

        amount = random.randint(400, 800)

        user_balances[f"{user_id}_last_scavenge"] = time.time()
        update_user_balance(ctx.author.id, amount)

        embed = discord.Embed(
            title="Coins Found",
            description=f"You found: {amount} coins! Your new balance is: {get_user_balance(ctx.author.id)}.",
            color=discord.Color.orange()
        )
        await ctx.respond(embed=embed)


    @commands.slash_command(name='beg', help='beg for money', aliases=['bed', 'begger', 'begging'])
    async def beg(self, ctx):
        user_id = ctx.author.id

        if not can_beg(user_id):
            embed = discord.Embed(
                title="Cooldown Active",
                description="You begged in the past 30s. Wait the cooldown.",
                color=discord.Color.orange()
            )
            await ctx.respond(embed=embed)
            return

        amount = random.randint(100, 200)

        update_user_balance(user_id, amount)

        embed = discord.Embed(
            title="Successful Begging",
            description=f'You begged and some idiot gave you {amount}.',
            color=discord.Color.orange()
        )
        await ctx.respond(embed=embed)

        # Correctly update the last beg time
        user_balances[f"{user_id}_last_beg"] = time.time()


    @commands.slash_command(name='daily', help="Daily reward", aliases=['dail'])
    async def daily(self, ctx):
        user_id = ctx.author.id

        if not can_claim_daily(user_id):
            embed = discord.Embed(
                title="Daily Reward Already Claimed",
                description="You've already claimed your daily reward. Please wait for the cooldown.",
                color=discord.Color.orange()
            )
            await ctx.respond(embed=embed)
            return

        amount = 1000  # Daily reward amount
        update_user_balance(user_id, amount)
        set_last_claim_time(user_id)

        embed = discord.Embed(
            title="Daily Reward Claimed",
            description=f'You have claimed your daily reward of {amount} coins!',
            color=discord.Color.orange()
        )
        await ctx.respond(embed=embed)

        # Update user's last claim time (if needed)
        user_balances[f"{user_id}_last_daily"] = time.time()


    @commands.slash_command(name='sell', help='Sell items in your inventory')
    async def sell(self, ctx, item_id):
        user_id = ctx.author.id

        item_id = item_id.lower() # make it lower to prevent stuff like LeG.SwoRD 

        if item_id not in combined_items:
            embed = discord.Embed(
                title="Invalid Item ID",
                description="Invalid item ID.",
                color=discord.Color.orange()
            )
            await ctx.respond(embed=embed)
            return

        user_inventory = get_user_inventory(user_id)
        user = await self.bot.fetch_user(ctx.author.id)
        username = user.name

        if item_id not in user_inventory:
            embed = discord.Embed(
                title="Item Not Found",
                description="You don't have this item in your inventory.",
                color=discord.Color.orange()
            )
            await ctx.respond(embed=embed)
            return

        item_info = combined_items[item_id]
        item_name = item_info["name"]
        item_sell_price = item_info["sell"]

        # Update user's balance
        update_user_balance(user_id, item_sell_price)

        # Remove the item from the user's inventory
        remove_item_from_inventory(user_id, item_id)

        embed = discord.Embed(
            title="Item Sold",
            description=f"You sold {item_name} for {item_sell_price} coins. Your new balance is: {get_user_balance(user_id)}!",
            color=discord.Color.orange()
        )
        await ctx.respond(embed=embed)


    global lottery_pool
    global required_participants
    global entry_fee
    global refund_timer
    global refund_lottery_tickets
    lottery_pool = set()
    required_participants = 5
    entry_fee = 1000
    refund_timer = 30  # seconds

    @commands.slash_command(name='enterlottery', help='Enter the lottery for a chance to win big!', aliases=['lottery'])
    async def enterlottery(self, ctx):
        user_id = str(ctx.author.id)

        # Check if user has enough balance
        if get_user_balance(user_id) < entry_fee:
            embed = discord.Embed(
                title="Lottery Entry Error",
                description=f"{ctx.author.mention}, you need 1000 coins to enter the lottery.",
                color=embed_error
            )
            await ctx.respond(embed=embed)
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
        await ctx.respond(embed=embed)

        # Check if lottery pool has enough members to draw
        if len(lottery_pool) >= required_participants:
            winner_id = random.choice(list(lottery_pool))
            update_user_balance(winner_id, 5000)
            embed = discord.Embed(
                title="Lottery Winner!",
                description=f"Congratulations <@{winner_id}>! You won the 5000 coins lottery prize!",
                color=discord.Color.green()
            )
            await ctx.respond(embed=embed)
            lottery_pool.clear()

        # If not enough participants, start a refund timer
        if len(lottery_pool) < required_participants:
            await asyncio.sleep(refund_timer)
            if len(lottery_pool) < required_participants:
                try:
                    await refund_lottery_tickets()  # Use await here
                    await ctx.respond('Refunded lottery tickets do to not enough participants!')
                except Exception as e:
                    await ctx.respond('Error while refunding lottery tickets: {e}')
                    print(f'{Fore.CYAN}Error while attempting to refund lottery tickets. {Fore.RED}ERROR: {e}{Fore.RESET}')
                

    async def refund_lottery_tickets():
        # Refund entry fee to all participants
        for user_id in lottery_pool:
            update_user_balance(user_id, entry_fee)

        lottery_pool.clear()
        print("Refunded lottery tickets.")


    @commands.slash_command(name='deposit', help='Deposit coins into your bank account')
    async def deposit(self, ctx, amount=None):
        if amount == 'all':
            amount = get_user_balance(ctx.author.id)
        else:
            try:
                amount = int(amount)
            except ValueError:
                await ctx.respond("Please enter a valid amount.")
                return

        if amount <= 0 or amount > get_user_balance(ctx.author.id):
            await ctx.respond("Invalid amount.")
            return

        if get_bank_balance(ctx.author.id) + amount > max_bank_size:  # Max bank limit
            await ctx.respond(f"Bank limit exceeded. Max storage is {max_bank_size} coins.")
            return

        update_user_balance(ctx.author.id, -amount)
        update_bank_balance(ctx.author.id, amount)

        # Embed the message
        embed = discord.Embed(
            title="Deposit Successful",
            description=f'{amount} coins deposited to your bank account.',
            color=discord.Color.blue()
        )
        await ctx.respond(embed=embed)


    @commands.slash_command(name='withdraw', help='Withdraw coins from your bank account')
    async def withdraw(self, ctx, amount=None):
        if amount == 'all':
            amount = get_bank_balance(ctx.author.id)
        else:
            try:
                amount = int(amount)
            except ValueError:
                await ctx.respond("Please enter a valid amount.")
                return

        if amount <= 0 or amount > get_bank_balance(ctx.author.id):
            await ctx.respond("Invalid amount.")
            return

        update_bank_balance(ctx.author.id, -amount)
        update_user_balance(ctx.author.id, amount)

        # Embed the message
        embed = discord.Embed(
            title="Withdraw Successful",
            description=f'{amount} coins withdrawn from your bank account.',
            color=discord.Color.green()
        )
        await ctx.respond(embed=embed)


    @commands.slash_command(name='baltop', aliases=['topbalance', 'richest', 'topbal', 'balancetop'])
    async def baltop(self, ctx):
        # Check if the file exists and is not empty
        if not os.path.exists('user_data.json') or os.path.getsize('user_data.json') == 0:
            await ctx.respond("No data available.")
            return

        try:
            with open('user_data.json', 'r') as f:
                data = json.load(f)
                user_balances = data.get("user_balances", {})
        except json.JSONDecodeError:
            await ctx.respond("Error reading user data.")
            return

        # Extracting user ID and balance, ignoring other keys
        balances = {user_id: data for user_id, data in user_balances.items() if user_id.isdigit() and isinstance(data, int)}

        # Sorting the dictionary by balance and getting top 10
        top_balances = dict(sorted(balances.items(), key=lambda item: item[1], reverse=True)[:10])

        # Creating an embedded message with orange color
        embed = discord.Embed(
            title="Top Balances",
            description="\n".join([f"<@{user_id}>: {balance}" for user_id, balance in top_balances.items()]),
            color=discord.Color.orange()
        )

        # Sending the leaderboard
        await ctx.respond(embed=embed)



    @commands.slash_command(name='balance', help="Check your balance", aliases=['bal'])
    async def balance(self, ctx):
        user_id = ctx.author.id
        pocket_money = get_user_balance(user_id)
        bank_balance = get_user_bank_balance(user_id)

        embed = discord.Embed(
            title="Balance",
            description=f'Money On hand: {pocket_money} coins\nBank Balance: {bank_balance}/150000 coins',
            color=discord.Color.orange()
        )
        await ctx.respond(embed=embed)


    global robbery_cooldown
    robbery_cooldown = {}  # Dictionary to track cooldowns

    @commands.slash_command(name='rob', help="Attempt to rob another user")
    async def rob(self, ctx, victim: commands.MemberConverter):
        robber_id = str(ctx.author.id)
        victim_id = str(victim.id)

        # Check for cooldown
        if robber_id in robbery_cooldown and time.time() - robbery_cooldown[robber_id] < 3600:
            await ctx.respond("You can't rob anyone yet. Please wait for the cooldown.")
            return

        # Set cooldown
        robbery_cooldown[robber_id] = time.time()

        # Check if both users have the minimum balance
        if get_user_balance(robber_id) < 100 or get_user_balance(victim_id) < 600:
            await ctx.respond("Either you or the victim does not have enough coins.")
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
        else:
            penalty_amount = int(get_user_balance(robber_id) * 0.20)  # 20% of robber's balance
            update_user_balance(robber_id, -penalty_amount)

            # Embed for failure
            embed = discord.Embed(
                title="Robbery Failed",
                description=f"The robbery failed! You've lost {penalty_amount} coins.",
                color=embed_error()
            )

        await ctx.respond(embed=embed)
    

    @commands.slash_command(name='gamble', help="Gamble your money 1/3 chance")
    async def gamble(self, ctx, amount: str = None):
        if amount is None:
            embed = discord.Embed(
                title="Gamble Command",
                description="Please specify an amount to gamble. Usage: `$gamble <amount>`",
                color=discord.Color.orange()
            )
            await ctx.respond(embed=embed)
            return

        # Check if the user entered "max"
        if amount.lower() == "max":
            amount = min(get_user_balance(ctx.author.id), max_bet)
        else:
            try:
                amount = int(amount)
            except ValueError:
                embed = discord.Embed(
                    title="Invalid Input",
                    description="Please enter a valid amount or 'max'.",
                    color=discord.Color.orange()
                )
                await ctx.respond(embed=embed)
                return

        if amount <= 0 or amount > get_user_balance(ctx.author.id) or amount > max_bet:
            embed = discord.Embed(
                title="Invalid Bet Amount",
                description=f"Invalid bet amount. You can bet up to {max_bet} coins.",
                color=discord.Color.orange()
            )
            await ctx.respond(embed=embed)
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
        await ctx.respond(embed=result_embed)


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Economy Cog Loaded! {Fore.RESET}')


def setup(bot):
    bot.add_cog(Economy(bot))
