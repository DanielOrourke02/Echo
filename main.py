# auto install modules
try:
    from discord.ext import commands
    from colorama import Fore
    import requests
    import discord
    import qrcode
except ModuleNotFoundError:
    import os
    os.system('pip install discord')
    os.system('pip install colorama')
    os.system('pip install requests')
    os.system('pip install pillow')
    os.system('pip install qrcode[pil]')
    #os.system('pip install ')

    # if program fails to auto install requirements
    # run this in your terminal
    # pip install -r requirements.txt

from concurrent.futures import ThreadPoolExecutor
from discord.ext import commands
from colorama import Fore
import os

from cogs.libs import get_user_balance, update_user_balance
from cogs.libs import message_log, t
from cogs.economy import setup_economy
from cogs.moderation import setup_moderation
from cogs.shop_items import setup_shops
from cogs.other import setup_other
from cogs.bitcoin import setup_trading
from cogs.farming import setup_farming
from cogs.crafting import setup_crafting


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)

#######################################################################################################################################################
            

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="Invalid Command",
            description="That is not a valid command. Use `$help` to list all available commands!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    else:
        # Handle other types of errors (optional)
        pass


#######################################################################################################################################################
            

@bot.event
async def on_ready():
    print(Fore.LIGHTGREEN_EX, f"{t}{Fore.LIGHTGREEN_EX} | Ready and online - {bot.user.display_name}\n", Fore.RESET)
    await bot.change_presence(activity=discord.Game('discord | $help'))

    try:
        guild_count = 0

        for guild in bot.guilds:
            print(Fore.RED, f"- {guild.id} (name: {guild.name})\n", Fore.RESET)

            guild_count = guild_count + 1

        print(Fore.GREEN, f"{t}{Fore.GREEN} | {bot.user.display_name} is in " + str(guild_count) + " guilds.\n", Fore.RESET)

    except Exception as e:
        print(e)


#################################################################### Help commands ####################################################################


@bot.command(name='help')
async def custom_help(ctx):
    embed = discord.Embed(
        title="Help - My Bot Commands",
        description="List of available commands:\n\nMy prefix is `$`",
        color=discord.Color.blue()
    )

    # Customize these lines with your bot's commands and descriptions
    embed.add_field(name="help", value="Outputs this message.", inline=True)  
    embed.add_field(name="economy", value="Lists economy games.", inline=True)  
    embed.add_field(name="games", value="Lists Games you can play.", inline=True)
    embed.add_field(name="ping", value="Bots latency.", inline=True)
    embed.add_field(name="say <message>", value="Make the bot say something.", inline=True)
    embed.add_field(name="membercount", value="Outputs Guild membercount.", inline=True)
    embed.add_field(name="coinflip <heads/tails>", value="50/50 coinflip.", inline=True)
    embed.add_field(name="invite", value="Sends a bot invite.", inline=True)
    embed.add_field(name="nuke", value="Nukes the channel you're in.", inline=True)
    embed.add_field(name="nuke_everything", value="Nukes all channels.", inline=True)
    embed.add_field(name="delete", value="DELETES all channels", inline=True)
    embed.add_field(name="clear <amount>", value="Deletes messages", inline=True)
    embed.add_field(name="inventory", value="Checks your inventory", inline=True)
    embed.add_field(name="qr <text/link>", value="Generate a QR code.", inline=True)
    embed.add_field(name="weather <location>", value="Get the current weather in a location", inline=True)
    #embed.add_field(name="", value="", inline=True)

    await ctx.send(embed=embed)
    message_log(ctx, 'help')

######################################################################################################################################################

@bot.command(name='economy', aliases=['money', 'eco'])
async def economy(ctx):
    embed = discord.Embed(
        title="Economy - List of Economy games",
        description="List of available economy commands:\n\nMy prefix is `$`",
        color=discord.Color.blue()
    )

    embed.add_field(name="bal", value="Check your current bank and pocket balance.", inline=True)
    embed.add_field(name="baltop", value="Leaderboard of the richest people", inline=True)
    embed.add_field(name="daily", value="Claim your daily reward.", inline=True)
    embed.add_field(name="gamble <amount>", value="Gamble your money with a 50/50 chance of 2x it.", inline=True)
    embed.add_field(name="shop", value="View the available items in the shop.", inline=True)
    embed.add_field(name="cosmetics", value="Lists findable cosmetics/their prices with $scrap.", inline=True)
    embed.add_field(name="buy <item_id>", value="Buy an item from the shop.", inline=True)
    embed.add_field(name="sell <item_id>", value="Sells item for its value", inline=True)
    embed.add_field(name="beg", value="Beg the kind people for money.", inline=True)
    embed.add_field(name="scrap", value="Find cosmetics and money", inline=True)
    embed.add_field(name="inventory", value="lists items inside your inventory.", inline=True)
    embed.add_field(name="lottery", value="Pay 1k in a chance to win 5K (required 5 people).", inline=True)
    embed.add_field(name="pay <amout>", value="Pay someone money", inline=True)
    embed.add_field(name="deposit", value="Deposit money into your bank (GAINS INTREST)", inline=True)
    embed.add_field(name="withdraw", value="Withdraw money from your bank", inline=True)
    embed.add_field(name="rob <@example>", value="Rob a user and potentionaly steal 20% of their On Hand Money. But if you fail you loose 20% of your money", inline=True)
    embed.add_field(name="plant <amount/max>", value="Plant crops (100 each). After harvest crops sell for 125 each.", inline=True)
    embed.add_field(name="harvest", value="Harvest your planted crops.", inline=True)
    embed.add_field(name="craft <recipe_name>", value="Craft items.", inline=True)
    embed.add_field(name="recipes", value="Shows craftable items and what you need for it.", inline=True)
    #embed.add_field(name="", value="", inline=True)

    await ctx.send(embed=embed)
    message_log(ctx, 'economy')

######################################################################################################################################################


#################################################################### Load Comands ####################################################################

setup_shops(bot)
setup_economy(bot)
setup_moderation(bot)
setup_other(bot)
setup_trading(bot)
setup_farming(bot)
setup_crafting(bot)

#######################################################################################################################################################


token = "YOUR_BOT_TOKEN_HERE"
bot.run(token)
