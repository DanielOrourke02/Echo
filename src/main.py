

from installation import SETUP_INSTALL
SETUP_INSTALL() # installs packages. this is enabled by default. after running this for the first time, you can set 'skip_installation' to 'true'


from utilities import *
from eco_support import *


from blackjack import blackjack_setup
from crafting import crafting_setup
from farming import farming_setup
from economy import economy_setup
from moderation import mod_setup
from slots import slots_setup
from help import help_setup
from fun import fun_setup


intents = discord.Intents.all()

# Create Bot instance with intents
bot = commands.Bot(command_prefix=config.get('prefix'), intents=intents, help_command=None)


@bot.event
async def on_ready():
    await lock_function(bot, save_locked_channels, unlock_channel_after_delay)

    print(f"{t}{Fore.LIGHTBLUE_EX} | Ready and online - {bot.user.display_name}\n{Fore.RESET}") # Show login message 
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{prefix}help")) # set presence to 'Listening to .help'

    guilds(bot) # call guilds function, this will output what guilds the bot is in (if enabled in config)


# Add cogs
crafting_setup(bot)
economy_setup(bot)
fun_setup(bot)
farming_setup(bot)
help_setup(bot)
mod_setup(bot)
blackjack_setup(bot)
slots_setup(bot)

bot.run(token)
