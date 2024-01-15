

from libs import Fore, discord, t
from discord.ext import commands
from libs import message_log

def setup_moderation(bot):
    @bot.command(name="nuke", help="Nuke channel")
    @commands.has_permissions(manage_channels=True, manage_messages=True)
    async def nuke(ctx):
        channel_name = ctx.channel.name

        # Deleting the channel
        await ctx.channel.delete()

        # Cloning and re-creating the channel
        new_channel = await ctx.channel.clone(reason="Channel was purged")

        # Restoring the channel's position
        await new_channel.edit(position=ctx.channel.position)

        # Sending a confirmation message in the new channel
        embed = discord.Embed(
            title="Channel Nuked",
            description=f"The channel **{channel_name}** was purged and recreated.",
            color=discord.Color.orange()
        )
        await new_channel.send(embed=embed)


        print(Fore.RED, f'{t}{Fore.RED} | $nuke {ctx.channel} | Executed By {ctx.author}', Fore.RESET)

    @nuke.error
    async def nuke_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            # Create an embed for missing permissions error
            embed = discord.Embed(
                title="Permission Denied",
                description="You need 'Manage Channels' and 'Manage Messages' permissions to use this command.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            # Handle other types of errors
            embed = discord.Embed(
                title="Error",
                description=f"An error occurred: {error}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            print(f'Error in nuke command: {error}')


    # Nukes/Purges every single channel in the guild
    @bot.command(name="nuke_everything", help="Nuke everything")
    @commands.has_permissions(administrator=True)
    async def nuke_everything(ctx):
        # Get the guild from the interaction
        guild = ctx.guild

        # Iterate through channels in the guild
        for channel in guild.channels:
            try:
                # Check if the channel is a category
                if isinstance(channel, discord.CategoryChannel):
                    continue  # Skip categories

                # Get the category ID of the channel
                category_id = channel.category_id

                # Delete the channel
                await channel.delete(reason="Channel was purged")

                # Clone the channel
                new_channel = await channel.clone(reason="Channel was purged")

                # Set the new channel's position to match the original channel
                await new_channel.edit(position=channel.position)

                # If the original channel was in a category, assign the new channel to the same category
                if category_id:
                    category = guild.get_channel(category_id)
                    if category:
                        await new_channel.edit(category=category)

                await new_channel.send(f"This Channel was purged.")

                print(Fore.RED, f'Purged {channel} | Executed By {ctx.user}', Fore.RESET)
            except Exception as e:
                print(Fore.RED, f"Failed to purge {channel}! | Error: {e}", Fore.RESET)

        print(Fore.MAGENTA, f"{t}{Fore.MAGENTA} | $nuke_everything | {ctx.channel} | Executed By {ctx.author}", Fore.RESET)

    @nuke_everything.error
    async def nuke_everything_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need 'Administrator' permissions to use this command.")
        else:
            await ctx.send(f"An error occurred: {error}")
            print(f'Error in nuke_everything command: {error}')


    # This command Deletes every single channel in the guild
    @bot.command(name="delete", help="Delete every channel")
    @commands.has_permissions(administrator=True)
    async def delete(ctx):
        for channel in ctx.guild.channels:
            try:
                await channel.delete(reason="Nuked")
            except Exception as e:
                print(Fore.RED, f"Failed to delete channel | Error: {e}")

        print(Fore.MAGENTA, f"{t}{Fore.MAGENTA} | $delete | {ctx.channel} | Deleted all channels | Executed By {ctx.author}", Fore.RESET)

    @delete.error
    async def delete_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need 'Administrator' permissions to use this command.")
        else:
            await ctx.send(f"An error occurred: {error}")
            print(f'Error in delete command: {error}')


    @bot.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, amount: int):
        if amount < 1:
            await ctx.send("Please specify a number greater than 0.")
            return

        await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message itself
        await ctx.send(f'{amount} messages have been deleted.', delete_after=5)  # Message will auto-delete after 5 seconds

        print(Fore.CYAN, f"{t}{Fore.CYAN} | $clear {amount} | {ctx.channel} | Executed By {ctx.author}", Fore.RESET)

    @clear.error
    async def clear_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify the number of messages to delete.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please enter a valid number.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the necessary permissions to use this command.")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("Error in command execution. Messages older than 2 weeks cannot be deleted.")
        else:
            await ctx.send("An unexpected error occurred.")
            print(f'Error in clear command: {error}')  # Optional: To log the error in console
