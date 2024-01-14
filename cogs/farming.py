import json
import time
import discord
from discord.ext import commands

from libs import save_user_data, get_user_balance, update_user_balance, DATA_FILE


# Load data from file or initialize if file does not exist
try:
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
        user_balances = data.get('user_balances', {})
        user_bank_balances = data.get('user_bank_balances', {})
        user_carrot_plantations = data.get('user_carrot_plantations', {})
except FileNotFoundError:
    user_balances = {}
    user_bank_balances = {}
    user_carrot_plantations = {}


def plant_carrots(user_id, amount):
    current_time = time.time()
    grow_duration = 3600 * 24  # 2 hours in seconds
    cost_per_carrot = 100
    total_cost = amount * cost_per_carrot

    # Update balance and record plantation details
    update_user_balance(user_id, -total_cost)  # Deducting the cost for planting
    user_carrot_plantations[str(user_id)] = [current_time + grow_duration, amount]
    save_user_data()

import datetime

# Assuming you have a dictionary to track the last planting time for each user
last_planting_time = {}


def setup_farming(bot):

    # Command to plant carrots
    @bot.command()
    async def plant(ctx, amount: int):
        user_id = ctx.author.id
        user_balance = get_user_balance(user_id)
        cost_per_carrot = 100

        total_cost = amount * cost_per_carrot

        embed = discord.Embed(color=discord.Color.green())

        # Check if the user has planted in the last hour
        if user_id in last_planting_time:
            time_since_last_plant = datetime.datetime.now() - last_planting_time[user_id]
            if time_since_last_plant < datetime.timedelta(hours=1):
                embed.title = "Wait a Little Longer"
                embed.description = "You can only plant carrots once every 24hrs. Please wait a bit longer before planting again."
                await ctx.send(embed=embed)
                return

        if user_balance < total_cost:
            embed.title = "Not Enough Balance"
            embed.description = f"You need ${total_cost} to plant {amount} carrots"
        else:
            plant_carrots(user_id, amount)
            last_planting_time[user_id] = datetime.datetime.now()  # Update the last planting time
            embed.title = "Carrots Planted"
            embed.description = f"You have planted {amount} carrots."

        await ctx.send(embed=embed)



    @bot.command()
    async def harvest(ctx):
        user_id = ctx.author.id
        plantation = user_carrot_plantations.get(str(user_id))

        if plantation:
            current_time = time.time()
            time_left_seconds = max(0, plantation[0] - current_time)
            growth_duration = 3600 * 2  # 2 hours in seconds
            growth_percentage = min(100, ((growth_duration - time_left_seconds) / growth_duration) * 100)

            if time_left_seconds <= 0:
                harvested_amount = plantation[1]
                crop_sell_price = 125  # 25% profit after harvest

                total_profit = harvested_amount * crop_sell_price
                update_user_balance(user_id, total_profit)
                del user_carrot_plantations[str(user_id)]  # Removing the plantation record

                embed = discord.Embed(title="Success", description=f"You have successfully harvested {harvested_amount} carrots and earned ${total_profit}.", color=discord.Colour.green())
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Info", description=f"Your carrots are not ready yet. They are {int(growth_percentage)}% grown.", color=discord.Colour.orange())
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Error", description="You don't have any crops planted.", color=discord.Colour.red())
            await ctx.send(embed=embed)
