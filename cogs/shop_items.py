from discord.ext import commands
from colorama import Fore
from time import ctime
import discord

import sys
sys.path.append('/home/ubuntu/h/priviate-discord-bot-main/cogs')

from libs import t

cosmetics_items = {
    "C.sword": {"name": "Common Sword", "sell": 1000, "chance": 50},
    "Un.sword": {"name": "Uncommon Sword", "sell": 1500, "chance": 30},
    "paper/roll": {"name": "Roll paper for weed", "sell": 1500, "chance": 30},
    "R.sword": {"name": "Rare Sword", "sell": 2500, "chance": 25},
    "weed": {"name": "Weed", "sell": 5000, "chance": 25},
    "Leg.sword": {"name": "Legendary Sword", "sell": 5000, "chance": 15},
    "Gun": {"name": "Glock-18", "sell": 8000, "chance": 15},
    "Stick": {"name": "Dildo", "sell": 10000, "chance": 10},
    "Sulphur": {"name": "Sulphur", "sell": 500, "chance": 40},
    "Charcoal": {"name": "Charcoal", "sell": 300, "chance": 50},
    "Duct_Tape": {"name": "Duct Tape", "sell": 200, "chance": 60},
    "Alarm_Clock": {"name": "Alarm Clock", "sell": 700, "chance": 30},
    "Potato": {"name": "Potato", "sell": 100, "chance": 70},  # For a humorous touch
    "Mystery_Electronics": {"name": "Mystery Electronics", "sell": 1000, "chance": 20},
    "David4": {"name": "David's 4th ball", "sell": 15000, "chance": 2},
    "infinity": {"name": "Infinity Gauntlet", "sell": 25000, "chance": 1}
}

shop_items = {
    "mute1d": {"name": "Mute someone (1d)", "cost": 100000},
    "mute15m": {"name": "Mute someone (15mins)", "cost": 50000},
    "mute10m": {"name": "Mute someone (10mins)", "cost": 35000},
    "mute5m": {"name": "Mute someone (5mins)", "cost": 25000},
    "role": {"name": "Get a Custom Role", "cost": 30000}
}


def setup_shops(bot):


    @bot.command(name='shop', help="View the shop")
    async def shop(ctx):
        embed = discord.Embed(
            title="Item Shop",
            description="Here are the items you can buy:",
            color=discord.Color.blue()
        )

        for item_id, item_info in shop_items.items():
            embed.add_field(name=f"{item_info['name']} (ID: {item_id})", value=f"Cost: {item_info['cost']} coins", inline=False)

        await ctx.send(embed=embed)


    @bot.command(name='cosmetics', help='Views the cosmetics you can find')
    async def cosmetics(ctx):
        embed = discord.Embed(title="Available Cosmetics", color=discord.Color.blue())

        for item_id, item_info in cosmetics_items.items():
            name = item_info["name"]
            sell_price = item_info["sell"]
            chance = item_info.get("chance", "N/A")  # Default to "N/A" if 'chance' key is not found

            embed.add_field(name=f"{item_id}: {name}", value=f"Sell Price: {sell_price} | Chance: {chance}%", inline=True)

        await ctx.send(embed=embed)
