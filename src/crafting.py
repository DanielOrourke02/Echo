

from utilities import *
from eco_support import *


class Crafting(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command()
    async def recipes(self, ctx):
        embed = discord.Embed(title="Crafting Recipes", color=discord.Colour.green())
        for recipe_name, ingredients in crafting_recipes.items():
            recipe_text = ', '.join([f"{count}x {item}" for item, count in ingredients.items() if item != 'result'])
            embed.add_field(name=recipe_name, value=recipe_text, inline=False)

        await ctx.respond(embed=embed)
        

    @commands.slash_command()
    async def craft(self, ctx, item_name: str):
        user_id = ctx.author.id

        item_name = item_name.lower # prevent case errors

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
                await ctx.respond(embed=embed)
            else:
                # Remove used items from inventory and add crafted item
                for ingredient, count in recipe.items():
                    if ingredient != 'result':
                        for _ in range(count):
                            remove_item_from_inventory(user_id, ingredient)
                add_item_to_inventory(user_id, recipe['result'])
                embed = discord.Embed(title="Crafting Successful", description=f"You have crafted {recipe['result']}.", color=discord.Colour.green())
                await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title="Error", description="This item cannot be crafted or does not exist.", color=discord.Colour.red())
            await ctx.respond(embed=embed)


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Crafting Cog Loaded! {Fore.RESET}')

def setup(bot):
    bot.add_cog(Crafting(bot))
