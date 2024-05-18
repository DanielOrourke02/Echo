

from utilities import *
from eco_support import *


economy_command_descriptions = {
    "balance": "Check your current bank and pocket balance.",
    "networth <@user>": "Check your networth (assets included)",
    "baltop": "Leaderboard of the richest people (networth)",
    "daily": "Claim your daily reward.",
    "shop": "View the available items in the shop.",
    "trade <@user> <item_id>": "Gives an item to a player",
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
    "craft <recipe_name>": "Craft items.",
    "recipes": "Shows craftable items and what you need for it.",
    "blackjacks <amount>": "Play a cool interactive blackjacks game.",
    "slots <amount>": "Gamble away your money without a chance of winning.",
    "gamble <amount>": f"Gamble your money with 1/3 chance of winning (max {max_bet})",
    "shoot <@user>": "Shoot someone (gun/m4a1 needed)",
    "bomb <@user>": "Bomb someone (c4 needed)",
    "cook": "Cook 5 Crystal Meth",
    "streets": "Sell 5 bags of cystal Meth for 4k each. NOTE: Police exist",
}



class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=['helpme'])
    async def help(self, ctx):
        command_descriptions = {
            "help": "Shows this message",
            "moderation": "List moderator commands.",
            "tutorial": "Choose a tutorial (economy game, moderation etc).",
            "economy": "List economy commands.",
            "invite": "Invite the bot to your server.",
            "ping": "Get the bot's current latency.",
            "say": "Repeat a message.",
            "coinflip <heads/tails>": "Flip a coin.",
            "dice": "Roll a six-sided die.",
            "8ball <question>": "Virtual Eight ball.",
            "qr <https://example.com>": "Generate a QR code from a link.",
            "quote": "Generate a random quote.",
            "membercount": "Get the member count of the server.",
            "calculator <+-*/>": "Perform basic calculations.",
            "joke": "Get a random joke.",
            "user_info <@user>": "Get user on a user.",
            "server_info": "Get the server info.",
            "avatar <@user>": "Get someones avatar or your own"
        }

        embed = discord.Embed(title="Bot Commands", description="List of available commands:", color=discord.Color.green())
        for cmd, desc in command_descriptions.items():
            embed.add_field(name=f"{prefix}{cmd}", value=desc, inline=True)

        embed.set_footer(text=f"Made by mal023")

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

        embed.set_footer(text=f"Made by mal023")
        
        await ctx.send(embed=embed)


    @commands.command(aliases=['eco'])
    async def economy(self, ctx):
        items_per_page = 15
        total_items = len(economy_command_descriptions)
        num_pages = (total_items // items_per_page) + (1 if total_items % items_per_page != 0 else 0)

        current_page = 0
        start_index = current_page * items_per_page
        end_index = min((current_page + 1) * items_per_page, total_items)

        embed = discord.Embed(title=f"Economy Commands | Page {current_page + 1}", description="List of available economy commands:", color=embed_colour)

        for cmd, desc in list(economy_command_descriptions.items())[start_index:end_index]:
            embed.add_field(name=f"{cmd}", value=desc, inline=True)

        embed.set_footer(text=f"Made by mal023")

        message = await ctx.send(embed=embed)

        if num_pages > 1:
            await message.add_reaction('◀️')
            await message.add_reaction('▶️')

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ['◀️', '▶️']

        while True:
            try:
                reaction, _ = await self.bot.wait_for('reaction_add', timeout=60, check=check)
                if str(reaction.emoji) == '▶️' and current_page < num_pages - 1:
                    current_page += 1
                elif str(reaction.emoji) == '◀️' and current_page > 0:
                    current_page -= 1

                start_index = current_page * items_per_page
                end_index = min((current_page + 1) * items_per_page, total_items)

                embed.clear_fields()
                embed.title = f"Economy Commands | Page {current_page + 1}"
                for cmd, desc in list(economy_command_descriptions.items())[start_index:end_index]:
                    embed.add_field(name=f"{cmd}", value=desc, inline=True)

                await message.edit(embed=embed)
                await message.remove_reaction(reaction, ctx.author)
            except asyncio.TimeoutError:
                break


    @commands.command()
    async def shop(self, ctx):
        embed = discord.Embed(
            title="Item Shop",
            description="Here are the items you can buy:",
            color=embed_colour
        )

        for item_id, item_info in shop_items.items():
            embed.add_field(name=f"{item_info['name']} (ID: {item_id})", value=f"Cost: {item_info['cost']} coins", inline=False)

        embed.set_footer(text=f"Made by mal023")
        
        await ctx.send(embed=embed)


    @commands.command(aliases=['cosmos', 'cos', 'cosmetic'])
    async def cosmetics(self, ctx):
        items_per_page = 15
        total_items = len(combined_items)
        num_pages = (total_items // items_per_page) + (1 if total_items % items_per_page != 0 else 0)

        current_page = 0
        start_index = current_page * items_per_page
        end_index = min((current_page + 1) * items_per_page, total_items)

        embed = discord.Embed(title=f"Cosmetics | Page {current_page + 1}", color=embed_colour)

        for item_id, item_info in list(combined_items.items())[start_index:end_index]:
            name = item_info["name"]
            sell_price = item_info["sell"]
            embed.add_field(name=f"{item_id}: {name}", value=f"Sell Price: {sell_price}", inline=True)

        embed.set_footer(text=f"Made by mal023")
        
        message = await ctx.send(embed=embed)

        if num_pages > 1:
            await message.add_reaction('◀️')
            await message.add_reaction('▶️')

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ['◀️', '▶️']

        while True:
            try:
                reaction, _ = await self.bot.wait_for('reaction_add', timeout=60, check=check)
                if str(reaction.emoji) == '▶️' and current_page < num_pages - 1:
                    current_page += 1
                elif str(reaction.emoji) == '◀️' and current_page > 0:
                    current_page -= 1

                start_index = current_page * items_per_page
                end_index = min((current_page + 1) * items_per_page, total_items)

                embed.clear_fields()
                embed.title = f"Cosmetics | Page {current_page + 1}"
                for item_id, item_info in list(combined_items.items())[start_index:end_index]:
                    name = item_info["name"]
                    sell_price = item_info["sell"]
                    embed.add_field(name=f"{item_id}: {name}", value=f"Sell Price: {sell_price}", inline=True)

                await message.edit(embed=embed)
                await message.remove_reaction(reaction, ctx.author)
            except asyncio.TimeoutError:
                break
    
            
    @commands.command()
    async def tutorial(self, ctx):
        try:
            view = View()
            economy = Button(label="Economy", style=discord.ButtonStyle.green)
            moderation = Button(label="Moderation", style=discord.ButtonStyle.blurple)
            
            async def economy_tutorial(ctx, guild, member):
                embed = discord.Embed(
                    title="Economy Game Tutorial",
                    description=f"This will be a short tutorial on how to make money with my extensive and addictive economy game. Please read this atleast twice!\n\n**1. How to make money**\n Making money in this game is actually very simple, there is a range of commands and methods to do this. (`{prefix}beg, {prefix}scrap, {prefix}dig, {prefix}hunt`). These are just a few, for some commands you will need an item to run it e.g to run the `{prefix}dig` command. You need to buy or find a shovel using `{prefix}scrap`. **AND REMEMBER, if you dont store your money in assets (items) or store it in the bank, you can and WILL get robbed.**.\n\n**2. Crafting**\nIf you run commands like {prefix}dig, {prefix}hunt or {prefix}scrap. You will be awarded zesty coins and items. With these items you can craft items that sell for more e.g `{prefix}craft complete_gauntlet` this items sells for 60K. Use `{prefix}recipes` for the list of craftable items and `{prefix}cosmetics` for the list of findable items.\n\n**3. Farming**\nWith money that you now have, you can plant crops, wait for them to grow, then sell them for profit (`{prefix}plant` and `{prefix}harvest`). Each plant costs {cost_per_carrot}, and they each sell for {carrot_sell}, you can plant a max of {max_carrot_planted} crops and they all take {growth_duration/3600} hours to grow.\n\n**4. Gambling**\nPlaying games like `{prefix}blackjack` (`{prefix}bj` for short) or `{prefix}gamble` is a HORRIBLE way to make money, but if you like gambling, go ahead. **'If you wanna put your entire networth on black, then thats gonna be some rags to richest story or the opposite :skull:.' - Wise words of mal (the creator)**\n\n**For a list of all the economy commands run `economy`**\n**For a list of all the findable items run `cosmetics`**",
                    color=discord.Color.gold(),
                )
                
                embed.set_footer(text=f"Made by mal023")
                
                await ctx.send(embed=embed)
            
            async def economy_tutorial_callback(interaction):
                guild = interaction.guild
                member = interaction.user
                await economy_tutorial(ctx, guild, member)

            economy.callback = economy_tutorial_callback
            view.add_item(economy)
            view.add_item(moderation)
            
            embed = discord.Embed(
                title="Tutorial",
                description="Click the button of the tutorial you want to do.",
                color=discord.Color.gold(),
            )
            
            embed.set_footer(text=f"Made by mal023")
            
            await ctx.send(embed=embed, view=view)
        except Exception as e:
            print(e)


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Help Cog Loaded! {Fore.RESET}')


def help_setup(bot):
    bot.add_cog(Help(bot))
