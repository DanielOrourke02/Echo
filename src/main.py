

from installation import SETUP_INSTALL
SETUP_INSTALL() # INSTALLS REQUIREMENTS

from utilities import *
from eco_support import *

from blackjack import Blackjack
from economy import Economy
from moderation import Moderation
from slots import Slots
from help import Help
from fun import Fun

from extensions import Crafting
from extensions import Farming
from extensions import Cooking


intents = discord.Intents.all()

# Create Bot instance with intents
bot = commands.Bot(command_prefix=config.get('prefix'), intents=intents, help_command=None)


# function that loads cogs
async def setup_bot():
    await bot.add_cog(Crafting(bot))
    await bot.add_cog(Economy(bot))
    await bot.add_cog(Fun(bot))
    await bot.add_cog(Farming(bot))
    await bot.add_cog(Help(bot))
    await bot.add_cog(Moderation(bot))
    await bot.add_cog(Blackjack(bot))
    await bot.add_cog(Slots(bot))
    await bot.add_cog(Cooking(bot))


@bot.event
async def on_ready():
    await lock_function(bot, save_locked_channels, unlock_channel_after_delay)

    print(f"{t}{Fore.LIGHTBLUE_EX} | Ready and online - {bot.user.display_name}\n{Fore.RESET}")  # Show login message
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{prefix}help"))  # set presence to 'Listening to .help'

    guilds(bot)  # call guilds function, this will output what guilds the bot is in (if enabled in config)
    
    
@bot.event
async def on_message(message):
    if link_ban == 'true':
        if any(link in message.content for link in BANNED_LINKS):
            await message.delete()

            embed = discord.Embed(
                title="Discord Links Are Forbidden!",
                description=f"{message.author.mention} Discord links are not allowed in this server.",
                color=discord.Color.red()
            )

            embed.set_footer(text="Made by mal023")

            await message.channel.send(embed=embed)
            return

    await bot.process_commands(message)
        
        
if message_delete == 'true':
    @bot.event
    async def on_message_delete(message):
        try:
            channel = bot.get_channel(logging_channel_id)
            embed = discord.Embed(
                title="Message Deleted",
                description=f"**Message sent by:** {message.author.mention}\n"
                            f"**Content:** {message.content}",
                color=discord.Color.red()
            )
            await channel.send(embed=embed)
        except Exception as e:
            print(e)
        
        # Delete the original message
        await message.delete()

# Use an asynchronous function to run the setup and the bot
async def run_bot():
    await setup_bot() # load cogs
    await bot.start(token)


# Run the bot using the asynchronous function
asyncio.run(run_bot())
