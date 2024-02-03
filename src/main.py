

from installation import SETUP_INSTALL
SETUP_INSTALL() # installs packages. this is enabled by default. after running this for the first time, you can set 'skip_installation' to 'true'


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


intents = discord.Intents.all()

# Create Bot instance with intents
bot = commands.Bot(command_prefix=config.get('prefix'), intents=intents, help_command=None)


@bot.event
async def on_ready():
    await lock_function(bot, save_locked_channels, unlock_channel_after_delay)

    print(f"{t}{Fore.LIGHTBLUE_EX} | Ready and online - {bot.user.display_name}\n{Fore.RESET}") # Show login message 
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{prefix}help")) # set presence to 'Listening to .help'

    guilds(bot) # call guilds function, this will output what guilds the bot is in (if enabled in config)


async def setup_bot():
    # Add cogs with await
    await bot.add_cog(Crafting(bot))
    await bot.add_cog(Economy(bot))
    await bot.add_cog(Fun(bot))
    await bot.add_cog(Farming(bot))
    await bot.add_cog(Help(bot))
    await bot.add_cog(Moderation(bot))
    await bot.add_cog(Blackjack(bot))
    await bot.add_cog(Slots(bot))

# Call the setup_bot function in an asynchronous context
asyncio.run(setup_bot())

bot.run(token)
