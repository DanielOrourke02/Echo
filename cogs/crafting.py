from libs import get_user_inventory, add_item_to_inventory, remove_item_from_inventory, DATA_FILE
import discord
from discord.ext import commands


crafting_recipes = {
    "Excalibur": {
        "Gun": 1,
        "Leg.sword": 1,
        "result": "Excalibur"  # A powerful sword
    },
    "Assault_Rifle": {
        "Gun": 2,
        "R.sword": 1,
        "result": "Assault_Rifle"  # An advanced firearm
    },
    "Comedy_Stick": {
        "Stick": 1,
        "David4": 1,
        "result": "Comedy_Stick"  # A unique and humorous item
    },
    "Ultimate_Power_Gauntlet": {
        "infinity": 1,
        "Leg.sword": 1,
        "David4": 1,
        "result": "Ultimate_Power_Gauntlet"  # The most powerful item in the game
    }
}

# Adding the C4 recipe
crafting_recipes["C4"] = {
    "Sulphur": 2,
    "Charcoal": 1,
    "Duct_Tape": 3,
    "Alarm_Clock": 1,
    "Potato": 5,  # Because why not?
    "Electronics": 2,
    "result": "C4"  # The crafted item
}

# Adding the C4 recipe
crafting_recipes["Joint"] = {
    "paper/roll": 1,
    "weed": 1,
    "result": "Joint"  # The crafted item
}


def setup_crafting(bot):
    @bot.command(aliases=['craftables'])
    async def recipes(ctx):
        embed = discord.Embed(title="Crafting Recipes", color=discord.Colour.green())
        for recipe_name, ingredients in crafting_recipes.items():
            recipe_text = ', '.join([f"{count}x {item}" for item, count in ingredients.items() if item != 'result'])
            embed.add_field(name=recipe_name, value=recipe_text, inline=False)

        await ctx.send(embed=embed)
        

    @bot.command()
    async def craft(ctx, item_name):
        user_id = ctx.author.id
        if item_name in crafting_recipes:
            recipe = crafting_recipes[item_name]
            inventory = get_user_inventory(user_id)
            missing_items = {}

            # Check for each item in the recipe
            for ingredient, count in recipe.items():
                if ingredient != 'result' and (inventory.count(ingredient) < count):
                    missing_items[ingredient] = count - inventory.count(ingredient)

            # If missing items
            if missing_items:
                missing_items_text = ', '.join([f"{count}x {item}" for item, count in missing_items.items()])
                embed = discord.Embed(title="Missing Items", description=f"You are missing {missing_items_text} for crafting {item_name}.", color=discord.Colour.red())
                await ctx.send(embed=embed)
            else:
                # Remove used items from inventory and add crafted item
                for ingredient, count in recipe.items():
                    if ingredient != 'result':
                        for _ in range(count):
                            remove_item_from_inventory(user_id, ingredient)
                add_item_to_inventory(user_id, recipe['result'])
                embed = discord.Embed(title="Crafting Successful", description=f"You have crafted {recipe['result']}.", color=discord.Colour.green())
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Error", description="This item cannot be crafted or does not exist.", color=discord.Colour.red())
            await ctx.send(embed=embed)
