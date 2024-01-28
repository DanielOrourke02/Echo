

from utilities import *


intents = discord.Intents.default()
intents.members = True
intents.messages = True 

bot = commands.Bot(command_prefix="/", intents=intents) 

@bot.event
async def on_ready():
    await lock_function(bot, save_locked_channels, unlock_channel_after_delay)

    print(f"{t}{Fore.LIGHTBLUE_EX} | Ready and online - {bot.user.display_name}\n{Fore.RESET}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/help"))

    guilds(bot)


@bot.event
async def on_member_join(member):
    user_join(bot, member_join, welcome_channel_id, welcome_message)


# Add cogs 
bot.load_extension('help')
bot.load_extension('moderation')
bot.load_extension('fun')
bot.load_extension('economy')
bot.load_extension('crafting')
bot.load_extension('farming')

bot.run(token)
