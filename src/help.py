

from utilities import *
from eco_support import *


# COSMETICS VIEW


class CosmeticsView(discord.ui.View):
    def __init__(self, current_page, num_pages):
        super().__init__()
        self.current_page = current_page
        self.num_pages = num_pages

    @discord.ui.button(label='Previous', style=discord.ButtonStyle.primary)
    async def previous_button(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        if self.current_page > 0:
            self.current_page -= 1
            await send_cosmetics_page(interaction.channel, self.current_page, 10, self.num_pages, self)

    @discord.ui.button(label='Next', style=discord.ButtonStyle.primary)
    async def next_button(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        if self.current_page < self.num_pages - 1:
            self.current_page += 1
            await send_cosmetics_page(interaction.channel, self.current_page, 10, self.num_pages, self)


async def send_cosmetics_page(channel, current_page, items_per_page, num_pages, view):
    start_index = current_page * items_per_page
    end_index = (current_page + 1) * items_per_page
    page_items = list(combined_items.items())[start_index:end_index]

    embed = discord.Embed(title=f"Cosmetics | Page {current_page + 1}")

    for item_id, item_info in page_items:
        name = item_info["name"]
        sell_price = item_info["sell"]
        embed.add_field(name=f"{item_id}: {name}", value=f"Sell Price: {sell_price}", inline=True)

    await channel.send(embed=embed, view=view)


# ECONOMY COMMAND VIEW


economy_command_descriptions = {
    "balance": "Check your current bank and pocket balance.",
    "baltop": "Leaderboard of the richest people",
    "daily": "Claim your daily reward.",
    "shop": "View the available items in the shop.",
    "cosmetics": "Lists all findable items and their sell prices.",
    "buy <item_id>": "Buy an item from the shop.",
    "sell <item_id>": "Sells item for its value",
    "beg": "Beg the kind people for money.",
    "scrap": "Find cosmetics and money",
    "dig": "Dig for cosmetics and money (shovel needed)",
    "hunt": "Hunt for cosmetics and money (bow needed)",
    "inventory": "Lists items inside your inventory.",
    "pay <amount>": "Pay someone money",
    "deposit <amount/max>": "Deposit money into your bank (GAINS 10% every 24h)",
    "withdraw <amount>": "Withdraw money from your bank",
    "rob <@example>": "Rob a user and potentially steal 20% of their On Hand Money. But if you fail you lose 20% of your money",
    "plant <amount>": f"Plant {max_carrot_planted} crops and sell them for {carrot_sell} (buy price is {cost_per_carrot})",
    "harvest": "Harvest your planted crops.",
    "fish": "Go fishing and sell fish for money.",
    "fishc": "Show how many fishes you have caught and flex on other users.",
    "leaderboard": "Top 10 fishes who have caught the most fish.",
    "craft <recipe_name>": "Craft items.",
    "recipes": "Shows craftable items and what you need for it.",
    "blackjacks <amount>": "Play a cool interactive blackjacks game.",
    "slots <amount>": "Gamble away your money without a chance of winning.",
    "lottery": "Pay 1k in a chance to win 5K (required 5 people).",
    "gamble <amount>": f"Gamble your money with 1/3 chance of winning (max {max_bet})",
}


class EconomyView(discord.ui.View):
    def __init__(self, current_page, num_pages):
        super().__init__()
        self.current_page = current_page
        self.num_pages = num_pages

    @discord.ui.button(label='Previous', style=discord.ButtonStyle.primary)
    async def previous_button(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        if self.current_page > 0:
            self.current_page -= 1
            await send_economy_page(interaction.channel, self.current_page, 10, self.num_pages, self)

    @discord.ui.button(label='Next', style=discord.ButtonStyle.primary)
    async def next_button(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        if self.current_page < self.num_pages - 1:
            self.current_page += 1
            await send_economy_page(interaction.channel, self.current_page, 10, self.num_pages, self)


async def send_economy_page(channel, current_page, items_per_page, num_pages, view):
    start_index = current_page * items_per_page
    end_index = (current_page + 1) * items_per_page
    page_items = list(economy_command_descriptions.items())[start_index:end_index]

    embed = discord.Embed(title=f"Economy Commands | Page {current_page + 1}", description="List of available economy commands:", color=discord.Color.green())

    for cmd, desc in page_items:
        embed.add_field(name=f"{cmd}", value=desc, inline=True)

    await channel.send(embed=embed, view=view)



class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=['helpme'])
    async def help(self, ctx):
        command_descriptions = {
            "help": "Shows this message",
            "moderation": "List moderator commands.",
            "economy": "List economy commands.",
            "invite": "Invite the bot to your server.",
            "ping": "Get the bot's current latency.",
            "say": "Repeat a message.",
            "coinflip <heads/tails>": "Flip a coin.",
            "dice": "Roll a six-sided die.",
            "8ball <question>": "Virtual Eight ball.",
            "qr": "Generate a QR code from a link.",
            "quote": "Generate a random quote.",
            "membercount": "Get the member count of the server.",
            "calculator <+-*/>": "Perform basic calculations.",
            "joke": "Get a random joke.",
            "user_info": "Get user on a user.",
            "server_info": "Get the server info.",
            "avatar": "Get someones avatar or your own",
            "shoot <@user>": "Shoot someone (gun/m4a1 needed)",
            "bomb <@user>": "Bomb someone (c4 needed)"
        }

        embed = discord.Embed(title="Bot Commands", description="List of available commands:", color=discord.Color.green())
        for cmd, desc in command_descriptions.items():
            embed.add_field(name=f"{prefix}{cmd}", value=desc, inline=True)

        await ctx.send(embed=embed)


    @commands.command(aliases=['mod'])
    @commands.has_permissions(manage_guild=True)
    async def moderation(self, ctx):
        moderation_descriptions = {
            "kick <@user> <reason>": "Kick a user from the server.",
            "ban <@user> <reason>": "Ban a user from the server.",
            "mute <@user> <reason>": "Mute a user in the server.",
            "unmute <@user> <reason": "Unmute a user in the server.",
            "clear <amount>": "Clear a specified number of messages in a text channel.",
            "lockchannel": "Lock a channel for a specified duration.",
            "unlockchannel": "Unlock a channel.",
            "lockserver": "Lock the entire server for a specified duration.",
            "unlockserver": "Unlock the entire server.",
            "setup_verify <role_name> <message>": "Setup a verification panel",
            "ticket_panel": "Setup a ticket panel"
        }

        embed = discord.Embed(title="Moderation Commands", description="List of available moderation commands:", color=discord.Color.green())
        for cmd, desc in moderation_descriptions.items():
            embed.add_field(name=f"{prefix}{cmd}", value=desc, inline=True)

        await ctx.send(embed=embed)


    @commands.command(aliases=['eco'])
    async def economy(self, ctx):
        items_per_page = 10
        total_items = len(economy_command_descriptions)
        num_pages = (total_items // items_per_page) + (1 if total_items % items_per_page != 0 else 0)

        current_page = 0
        view = EconomyView(current_page, num_pages)
        await send_economy_page(ctx, current_page, items_per_page, num_pages, view)


    @commands.command()
    async def shop(self, ctx):
        embed = discord.Embed(
            title="Item Shop",
            description="Here are the items you can buy:",
            color=embed_colour
        )

        for item_id, item_info in shop_items.items():
            embed.add_field(name=f"{item_info['name']} (ID: {item_id})", value=f"Cost: {item_info['cost']} coins", inline=False)

        await ctx.send(embed=embed)


    @commands.command(aliases=['cosmos', 'cos', 'cosmetic'])
    async def cosmetics(self, ctx):
        items_per_page = 10
        total_items = len(combined_items)
        num_pages = (total_items // items_per_page) + (1 if total_items % items_per_page != 0 else 0)

        current_page = 0
        view = CosmeticsView(current_page, num_pages)
        await send_cosmetics_page(ctx, current_page, items_per_page, num_pages, view)
        

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Help Cog Loaded! {Fore.RESET}')


def help_setup(bot):
    bot.add_cog(Help(bot))
