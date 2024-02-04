

from installation import SETUP_INSTALL
SETUP_INSTALL() # INSTALLS REQUIREMENTS

from utilities import *
from eco_support import *

from blackjack import Blackjack
from crafting import Crafting
from farming import Farming
from economy import Economy
from moderation import Moderation
from slots import Slots
from help import Help
from fun import Fun
from fishing import Fishing


intents = discord.Intents.all()

# Create Bot instance with intents
bot = commands.Bot(command_prefix=config.get('prefix'), intents=intents, help_command=None)


# function that loads cogs
async def setup_bot():
    bot.add_cog(Crafting(bot))
    bot.add_cog(Economy(bot))
    bot.add_cog(Fun(bot))
    bot.add_cog(Farming(bot))
    bot.add_cog(Help(bot))
    bot.add_cog(Moderation(bot))
    bot.add_cog(Blackjack(bot))
    bot.add_cog(Slots(bot))
    bot.add_cog(Fishing(bot))


@bot.event
async def on_ready():
    await lock_function(bot, save_locked_channels, unlock_channel_after_delay)

    print(f"{t}{Fore.LIGHTBLUE_EX} | Ready and online - {bot.user.display_name}\n{Fore.RESET}")  # Show login message
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{prefix}help"))  # set presence to 'Listening to .help'

    guilds(bot)  # call guilds function, this will output what guilds the bot is in (if enabled in config)


# Use an asynchronous function to run the setup and the bot
async def run_bot():
    await setup_bot() # load cogs
    await bot.start(token)


# Run the bot using the asynchronous function
asyncio.run(run_bot())
