

from installation import *
from utilities import *
from eco_support import *


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(name="help", description="Get help for commands")
    async def help_command(self, ctx, command: Option(str, "Enter a command to get help on", required=False, default=None)):
        # Command descriptions
        command_descriptions = {
            "moderation": "List moderator commands.",
            "economy": "List economy commands.",
            "ping": "Get the bot's current latency.",
            "say": "Repeat a message.",
            "coinflip": "Flip a coin.",
            "dice": "Roll a six-sided die.",
            "dailyquote": "Get a daily quote from an API.",
            "qr": "Generate a QR code from a link.",
            "membercount": "Get the member count of the server.",
            "calculator": "Perform basic calculations.",
            "joke": "Get a random joke."
        }


        # Check if a specific command is asked for
        if command:
            if command.lower() in command_descriptions:
                description = command_descriptions[command.lower()]
                embed = discord.Embed(title=f"/{command}", description=description, color=embed_colour)
                await ctx.respond(embed=embed)
            else:
                await ctx.respond(f"Command '{command}' not found.")
        else:
            # List all commands if no specific command is asked for
            embed = discord.Embed(title="Bot Commands", description="List of available commands:", color=embed_colour)
            for cmd, desc in command_descriptions.items():
                embed.add_field(name=f"/{cmd}", value=desc, inline=True)
            await ctx.respond(embed=embed)


    @commands.slash_command(name="moderation", description="Get help for moderation commands")
    @commands.has_permissions(manage_guild=True)
    async def moderation_command(self, ctx, command: Option(str, "Enter a moderation command to get help on", required=False, default=None)):
        # Moderation command descriptions
        moderation_descriptions = {
            "kick": "Kick a user from the server.",
            "ban": "Ban a user from the server.",
            "mute": "Mute a user in the server.",
            "clear": "Clear a specified number of messages in a text channel.",
            "ticketpanel": "Create a ticket panel for support.",
            "setup-verify": "Set up a verification panel.",
            "lockchannel": "Lock a channel for a specified duration.",
            "unlockchannel": "Unlock a channel.",
            "lockserver": "Lock the entire server for a specified duration.",
            "unlockserver": "Unlock the entire server."
        }

        # Check if a specific moderation command is asked for
        if command:
            command_key = command.lower()  # Ensure command is treated as a string
            if command_key in moderation_descriptions:
                description = moderation_descriptions[command_key]
                embed = discord.Embed(title=f"/{command}", description=description, color=discord.Color.green())
                await ctx.respond(embed=embed)
            else:
                await ctx.respond(f"Moderation command '{command}' not found.")
        else:
            # List all moderation commands if no specific command is asked for
            embed = discord.Embed(title="Moderation Commands", description="List of available moderation commands:", color=discord.Color.green())
            for cmd, desc in moderation_descriptions.items():
                embed.add_field(name=f"/{cmd}", value=desc, inline=True)
            await ctx.respond(embed=embed)


    @commands.slash_command(name="economy", description="Get help for economy commands")
    async def economy(self, ctx, command: Option(str, "Enter an economy command to get help on", required=False, default=None)):
        # Check if a specific command is asked for
        economy_command_descriptions = {
            "bal": "Check your current bank and pocket balance.",
            "baltop": "Leaderboard of the richest people",
            "daily": "Claim your daily reward.",
            "gamble <amount>": "Gamble your money with a 50/50 chance of 2x it.",
            "shop": "View the available items in the shop.",
            "cosmetics": "Lists findable cosmetics/their prices with $scrap.",
            "buy <item_id>": "Buy an item from the shop.",
            "sell <item_id>": "Sells item for its value",
            "beg": "Beg the kind people for money.",
            "scrap": "Find cosmetics and money",
            "inventory": "Lists items inside your inventory.",
            "lottery": "Pay 1k in a chance to win 5K (required 5 people).",
            "pay <amount>": "Pay someone money",
            "deposit": "Deposit money into your bank (GAINS INTEREST)",
            "withdraw": "Withdraw money from your bank",
            "rob <@example>": "Rob a user and potentially steal 20% of their On Hand Money. But if you fail you lose 20% of your money",
            "plant <amount/max>": "Plant crops (100 each), max 100 planted at a time. After harvest, crops sell for 150 each.",
            "harvest": "Harvest your planted crops.",
            "craft <recipe_name>": "Craft items.",
            "recipes": "Shows craftable items and what you need for it."
        }


        if command:
            command_key = command.lower()  # Ensure command is treated as a string
            if command_key in economy_command_descriptions:
                description = economy_command_descriptions[command_key]
                embed = discord.Embed(title=f"/{command}", description=description, color=embed_colour)
                await ctx.respond(embed=embed)
            else:
                await ctx.respond(f"Economy command '{command}' not found.")
        else:
            # List all economy commands if no specific command is asked for
            embed = discord.Embed(title="Economy Commands", description="List of available economy commands:", color=discord.Color.blue())
            # Add fields for each economy command
            # You can use the same dictionary as in your original command
            for cmd, desc in economy_command_descriptions.items():
                embed.add_field(name=f"/{cmd}", value=desc, inline=True)
            await ctx.respond(embed=embed)


    @commands.slash_command()
    async def shop(self, ctx):
        embed = discord.Embed(
            title="Item Shop",
            description="Here are the items you can buy:",
            color=discord.Color.blue()
        )

        for item_id, item_info in shop_items.items():
            embed.add_field(name=f"{item_info['name']} (ID: {item_id})", value=f"Cost: {item_info['cost']} coins", inline=False)

        await ctx.respond(embed=embed)


    commands.slash_command()
    async def cosmetics(self, ctx):
        embed = discord.Embed(title="Available Cosmetics", color=discord.Color.blue())

        for item_id, item_info in cosmetics_items.items():
            name = item_info["name"]
            sell_price = item_info["sell"]
            chance = item_info.get("chance", "N/A")  # Default to "N/A" if 'chance' key is not found

            embed.add_field(name=f"{item_id}: {name}", value=f"Sell Price: {sell_price} | Chance: {chance}%", inline=True)

        await ctx.respond(embed=embed)


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Help Cog Loaded! {Fore.RESET}')


def setup(bot):
    bot.add_cog(Help(bot))
