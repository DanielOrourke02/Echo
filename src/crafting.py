

from utilities import *
from eco_support import *


class Crafting(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot


    @commands.command()
    async def recipes(self, ctx):
        """
        Displays crafting recipes.

        Parameters:
            ctx (commands.Context): The context of the command.

        Returns:
            None
        """
        embed = discord.Embed(title="Crafting Recipes", color=discord.Colour.green())
        
        for recipe_name, ingredients in crafting_recipes.items():
            recipe_text = ', '.join([f"{count}x {item}" for item, count in ingredients.items() if item != 'result'])
            embed.add_field(name=recipe_name, value=recipe_text, inline=False)

        embed.set_footer(text=f"Made by mal023")

        await ctx.send(embed=embed)


    @commands.command()
    async def craft(self, ctx, item_name: str=None):
        """
        Craft an item using the specified recipe.

        Parameters:
            ctx (commands.Context): The context of the command.
            item_name (str): The name of the item to craft.

        Returns:
            None
        """
        user_id = ctx.author.id

        try:
            # Check if item_name is empty
            if item_name is None:
                embed = discord.Embed(title="Incorrect Usage", description=f"Correct usage: `{ctx.prefix}craft <item>`", color=embed_error)

                embed.set_footer(text=f"Made by mal023")

                await ctx.send(embed=embed)
                return

            item_name = item_name.lower()

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

                    embed = discord.Embed(title="Missing Items", description=f"You are missing {missing_items_text} for crafting {item_name}.", color=embed_error)

                    embed.set_footer(text=f"Made by mal023")

                    await ctx.send(embed=embed)
                else:
                    # Remove used items from inventory and add crafted item
                    for ingredient, count in recipe.items():
                        if ingredient != 'result':
                            for _ in range(count):
                                remove_item_from_inventory(user_id, ingredient)

                    add_item_to_inventory(user_id, recipe['result'])

                    embed = discord.Embed(title="Crafting Successful", description=f"You have crafted {recipe['result']}.", color=discord.Color.green())

                    embed.set_footer(text=f"Made by mal023")

                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Error", description="This item cannot be crafted or does not exist.", color=embed_error)
                embed.set_footer(text=f"Made by mal023")
                await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Crafting Cog Loaded! {Fore.RESET}')


def crafting_setup(bot):
    bot.add_cog(Crafting(bot))
