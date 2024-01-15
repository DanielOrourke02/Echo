

from libs import message_log, Fore, shop_items, user_balances,  ctime, discord, asyncio, random, time, json, os, t, DATA_FILE, ADMIN_USER_ID, user_bank_balances, cosmetics_items, save_user_data, get_bank_balance, get_user_balance, get_user_inventory, get_user_bank_balance, add_item_to_inventory, remove_item_from_inventory, update_bank_balance, update_user_balance, can_beg, can_claim_daily, can_scavenge, set_last_claim_time, log_purchase, log_sell, is_admin
from discord.ext import commands
from libs import message_log
import requests
import qrcode as qrc


def setup_other(bot):
    @bot.command(name='generate_qr', aliases=['qr'])
    async def qrcode(ctx, *, content: str):
        # Create a QR code
        qr = qrc.QRCode(
            version=1,
            error_correction=qrc.constants.ERROR_CORRECT_L,  # Adjusted this line
            box_size=10,
            border=4,
        )
        qr.add_data(content)
        qr.make(fit=True)

        # Create an image from the QR code data
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image to a file (you can customize the filename)
        img.save('generated_qr.png')

        # Send the generated QR code image to the user
        with open('generated_qr.png', 'rb') as file:
            qr_file = discord.File(file, filename='generated_qr.png')
            await ctx.send(file=qr_file)

        os.remove('generated_qr.png')


    @bot.command(name='weather')
    async def weather(ctx, *, location: str):
        api_key = '124ae1234546' # YOUR WEATHER API KEY HERE
        base_url = 'http://api.weatherapi.com/v1/current.json'  # Example API URL
        complete_url = f"{base_url}?key={api_key}&q={location}"

        response = requests.get(complete_url)
        weather_data = response.json()

        if response.status_code == 200:
            # Extracting data from the API response
            temperature = weather_data['current']['temp_c']
            weather_condition = weather_data['current']['condition']['text']
            humidity = weather_data['current']['humidity']
            wind_speed = weather_data['current']['wind_mph']

            # Creating an embed to display the weather
            embed = discord.Embed(title=f"Weather in {location}", color=discord.Colour.blue())
            embed.add_field(name="Temperature", value=f"{temperature}°C")
            embed.add_field(name="Condition", value=weather_condition)
            embed.add_field(name="Humidity", value=f"{humidity}%")
            embed.add_field(name="Wind Speed", value=f"{wind_speed} mph")

            await ctx.send(embed=embed)
        else:
            await ctx.send("Sorry, I couldn't fetch the weather data. Please try again later.")


    @bot.command(name="coinflip", help="Guess heads or tails in a coin flip game")
    async def coinflip(ctx, guess: str = None):
        if guess is None:
            embed = discord.Embed(
                title="Missing Guess!",
                description="Please provide a guess. Use '$coinflip heads' or '$coinflip tails'.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return

        # Check if the guess is valid
        guess = guess.lower()
        if guess not in ['heads', 'tails']:
            embed = discord.Embed(
                title="Invalid Guess!",
                description="Please choose 'heads' or 'tails'.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return

        # Flip the coin
        result = random.choice(['heads', 'tails'])

        # Create the embed
        embed = discord.Embed(color=discord.Color.orange())

        # Check if the user's guess is correct
        if guess == result:
            embed.title = "You Win!"
            embed.description = f"It landed on {result}. Congratulations!"
        else:
            embed.title = "You Lose!"
            embed.description = f"It landed on {result}. Better luck next time!"

        # Optionally add a thumbnail or image
        embed.set_thumbnail(url="https://github.com/DanielJones02/Active-Projects/blob/main/images/icon.png")

        # Send the embed
        await ctx.send(embed=embed)
        
        message_log(ctx, "coinflip", guess)


    @bot.command(name="ping", help="Test the bot's latency")
    async def ping(ctx):
        # Create an orange/black themed embed
        embed = discord.Embed(
            title="Pong!",
            description=f"Latency: {round(bot.latency * 1000)}ms",  # Convert latency to milliseconds
            color=discord.Color.orange()
        )
        embed.set_footer(text=f"Executed By {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

        # Send the embed
        await ctx.send(embed=embed)

        message_log(ctx, "ping")


    @bot.command(name='membercount', help='Displays the number of members in the server')
    async def membercount(ctx):
        guild = ctx.guild
        member_count = guild.member_count

        # Create an embed with an orange/black theme
        embed = discord.Embed(
            title=f"{guild.name} Member Count",
            description=f"{guild.name} has {member_count} members.",
            color=discord.Color.orange()  # Orange color for the embed
        )
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

        # Send the embed
        await ctx.send(embed=embed)

        message_log(ctx, "membercount", member_count)


    @bot.command(name="say", help="Say something")
    async def say(ctx, *, message: str):
        # Create an orange/black themed embed
        embed = discord.Embed(
            title="Say Command",
            description=message,
            color=discord.Color.orange()  # Orange color for the embed
        )
        embed.set_footer(text=f"Said by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

        # Send the embed
        await ctx.send(embed=embed)

        message_log(ctx, "say", message)


    @bot.command(name="invite", help="Invite me to your server")
    async def invite(ctx):
        invite_url = 'https://discord.com/api/oauth2/authorize?client_id=1075434463217066014&permissions=8&scope=bot'
        
        # Create an embed with orange color using discord.Color.orange()
        embed = discord.Embed(
            title="Invite Me to Your Server!",
            description=f"Add me to your server and have access to all my commands!\n[Click here to invite]({invite_url})",
            color=discord.Color.orange()
        )

        # Sending the embed
        await ctx.send(embed=embed)

        message_log(ctx, "invite")
