

from eco_support import *
from utilities import *

# File paths
FISH_CAUGHT_FILE = 'fish_caught.json'

# Load fish_caught data from file
def load_fish_caught():
    try:
        with open(FISH_CAUGHT_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# Save fish_caught data to file
def save_fish_caught(fish_caught_data):
    with open(FISH_CAUGHT_FILE, 'w') as file:
        json.dump(fish_caught_data, file, indent=4)


def determine_fishing_outcome():
    # Logic to determine fishing outcome
    fish_types = list(fish_data.keys())
    outcome = random.choices(fish_types, weights=[data['chance'] for data in fish_data.values()], k=1)[0]
    return outcome


class Fishing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fish_caught = load_fish_caught()


    @commands.command()
    async def fish(self, ctx):
        user_id = str(ctx.author.id)

        # Check if they have bait in their inventory
        if 'bait' not in get_user_inventory(user_id):
            embed = discord.Embed(
                title="No bait (thats bait)",
                description=f"{ctx.author.mention}, You need bait for fishing! Buy some using: `{prefix}buy bait` (250 per bait)",
                color=embed_colour
            )
            await ctx.send(embed=embed)
            return

        outcome = determine_fishing_outcome()

        # Ensure the user is in the fish_caught dictionary
        if user_id not in self.fish_caught:
            self.fish_caught[user_id] = {'fish_count': 0}

        # Process the outcome and update player's inventory
        add_item_to_inventory(user_id, outcome)
        remove_item_from_inventory(ctx.author.id, 'bait')

        item_info = combined_items['bait'] # id
        item_sell_price = item_info["sell"] # price

        # Update user balance (subtract the cost of bait)
        update_user_balance(user_id, -item_sell_price)

        # Update fish caught leaderboard
        self.fish_caught[user_id]['fish_count'] += 1

        # Send an embed indicating the fishing result
        embed = discord.Embed(
            title="Fishing Result",
            description=f"{ctx.author.mention}, you caught a {outcome}!",
            color=embed_colour
        )
        embed.add_field(name="Sell Price", value=f"Sell for {fish_data[outcome]['sell']} coins")

        await ctx.send(embed=embed)


    @commands.command()
    async def fishc(self, ctx):
        user_id = str(ctx.author.id)

        # Ensure the user is in the fish_caught dictionary
        if user_id not in self.fish_caught:
            self.fish_caught[user_id] = {'fish_count': 0}

        fish_count = self.fish_caught[user_id]['fish_count']

        # Send an embed indicating the user's fish count
        embed = discord.Embed(
            title="Your Fish Count",
            description=f"{ctx.author.mention}, you have caught {fish_count} fishes!",
            color=embed_colour
        )

        await ctx.send(embed=embed)


    @commands.command()
    async def leaderboard(self, ctx):
        # Get the top fishers
        top_users = Counter(self.fish_caught).most_common(10)

        # Create an embed to display the leaderboard
        embed = discord.Embed(
            title="Fishing Leaderboard",
            description=f"{ctx.author.mention}, here are the top fishers!",
            color=embed_colour
        )

        # Display the top fishers in the embed
        for rank, (user_id, data) in enumerate(top_users, 1):
            user = self.bot.get_user(int(user_id))
            fish_count = data if isinstance(data, int) else data.get('fish_count', 0)
            embed.add_field(name=f"{rank}. {user.name}", value=f"{fish_count} fish caught", inline=False)

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Fishing Cog Loaded! {Fore.RESET}')


def fish_setup(bot):
    bot.add_cog(Fishing(bot))
