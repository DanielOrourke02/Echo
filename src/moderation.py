

from installation import *
from utilities import *


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # Ticket Panel Command
    @commands.command()
    async def ticket_panel(self, ctx, *message: str):
        view = View()
        button = Button(label="Create Ticket", style=discord.ButtonStyle.green)

        if not message:
            message = "Click the button below to create a support ticket."
        else:
            message = " ".join(message)

        async def ticket_button_callback(interaction):
            guild = interaction.guild
            member = interaction.user
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=True)
            }
            ticket_channel = await guild.create_text_channel(f"ticket-{member.display_name}", overwrites=overwrites)
            await ticket_channel.send(f"{member.mention} Welcome to your ticket!")
            await interaction.response.send_message(f"Ticket created: {ticket_channel.mention}", ephemeral=True)

        button.callback = ticket_button_callback
        view.add_item(button)

        embed = discord.Embed(title="Support Tickets", description=message, color=embed_colour)
        await ctx.send(embed=embed, view=view)


    # Verification Setup Command
    @commands.command()
    async def setup_verify(self, ctx, verify_role: str=None, message: str=None):
        view = View()
        button = Button(label="Verify", style=discord.ButtonStyle.green)

        if verify_role or message is None:
            embed = discord.Embed(color=embed_error)
            embed.title = "Incorrect usage"
            embed.description = f"{ctx.author.mention}, Incorrect usage. Please try: `{prefix}setup_verify <@role> <message>`"
            embed.color = embed_error

            await ctx.send(embed=embed)
            return

        async def verify_button_callback(interaction):
            guild = interaction.guild
            member = interaction.user

            # Use the 'role' parameter captured during setup
            assigned_role = discord.utils.get(guild.roles, name=verify_role)

            if assigned_role:
                await member.add_roles(assigned_role)
                await interaction.response.send_message(f"You have been verified and received the {assigned_role.mention} role.", ephemeral=True)
            else:
                await interaction.response.send_message(f"Error: '{verify_role}' role not found. Please create the role and try again.", ephemeral=True)

        button.callback = verify_button_callback
        view.add_item(button)

        embed = discord.Embed(title="Verification Panel", description=message, color=embed_colour)
        await ctx.send(embed=embed, view=view)


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason: str = "No reason provided"):
        try:
            await member.kick(reason=reason)
            await member.send(f"You have been kicked in {ctx.guild.name} by an admin. Reason: {reason}") # dm user 
            embed = discord.Embed(title="Kick", description=f"{member.mention} has been kicked.\nReason: {reason}", color=discord.Color.red())
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send(f"{ctx.author.mention}, I do not have permission to kick {member.mention}.")


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason: str = "No reason provided"):
        try:
            await member.ban(reason=reason)
            await member.send(f"You have been banned in {ctx.guild.name} by an admin. Reason: {reason}") # dm user 
            embed = discord.Embed(title="Ban", description=f"{member.mention} has been banned.\nReason: {reason}", color=discord.Color.red())
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send(f"{ctx.author.mention}, I do not have permission to ban {member.mention}.")


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, reason: str = "No reason provided"):
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")

        if not mute_role:
            # If the "Muted" role doesn't exist, create it
            mute_role = await ctx.guild.create_role(name="Muted", reason="Creating Muted role for mute command")
            
            # Loop through all the channels in the server and deny send message permissions for the "Muted" role
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, send_messages=False)

        # Assign the "Muted" role to the specified user
        await member.add_roles(mute_role, reason=f"Muted by {ctx.author} for reason: {reason}")
        await member.send(f"You have been muted in {ctx.guild.name} by an admin. Reason: {reason}") # dm user 

        # Create an embed for the confirmation message
        embed = discord.Embed(title="User Muted", description=f"{member.mention} has been muted.", color=discord.Color.red())
        embed.add_field(name="Reason", value=reason)
        embed.set_footer(text=f"Muted by {ctx.author}")

        # Send the embed
        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, reason: str = "No reason provided"):
        # Get the "Muted" role
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")

        if not mute_role:
            # If the "Muted" role doesn't exist, you can handle this as you prefer.
            # For example, you can send a message saying the role doesn't exist or create it.
            await ctx.send(f"{ctx.author.mention}, The 'Muted' role doesn't exist.")
            return

        # Remove the "Muted" role from the specified user
        await member.remove_roles(mute_role, reason=f"Unmuted by {ctx.author} for reason: {reason}")
        await member.send(f"You have been unmuted in {ctx.guild.name} by an admin. Reason: {reason}")  # dm user

        # Create an embed for the confirmation message
        embed = discord.Embed(title="User Unmuted", description=f"{member.mention} has been unmuted.", color=discord.Color.green())
        embed.add_field(name="Reason", value=reason)
        embed.set_footer(text=f"Unmuted by {ctx.author}")

        # Send the embed
        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = None):
        if amount is None:
            embed = discord.Embed(title="Error", description=f"{ctx.author.mention}, You need to specify the number of messages to clear.", color=embed_colour)
            await ctx.send(embed=embed)
            return

        if amount > 1000:
            embed = discord.Embed(title="Error", description=f"{ctx.author.mention}, You can only clear up to 1000 messages at a time.", color=embed_colour) 
            await ctx.send(embed=embed)
            return

        await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed(title="Messages Cleared", description=f"{amount} messages have been cleared.", color=embed_colour) 
        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock_channel(self, ctx, channel: discord.TextChannel = None, duration: str = None, reason: str = "No reason provided"):
        # If channel is not provided, use the current channel
        channel = channel or ctx.channel

        # Convert duration to seconds
        seconds = convert_to_seconds(duration)
        if seconds is None:
            embed = discord.Embed(title="Error", description="Invalid duration format. Use s, m, h, or d.", color=embed_colour) 
            await ctx.send(embed=embed)
            return

        # Change channel permissions
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        embed = discord.Embed(title="Channel Locked", description=f"{channel.mention} locked for {duration}. Reason: {reason}", color=embed_colour)  
        await ctx.send(embed=embed)

        # Convert datetime to string before including it in a serializable context
        unlock_time_str = (datetime.datetime.now() + datetime.timedelta(seconds=seconds)).strftime("%Y-%m-%d %H:%M:%S")

        # Save locked channel state with the time as a string
        locked_channels[channel.id] = {"unlock_time": unlock_time_str}
        save_locked_channels()

        # Schedule unlock after duration
        await asyncio.sleep(seconds)
        if channel.id in locked_channels:  # Check if still locked
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
            del locked_channels[channel.id]
            save_locked_channels()
            await channel.send(f"Channel unlocked automatically after {duration}.")


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock_channel(self, ctx, channel: discord.TextChannel = None):
        if not channel:
            await ctx.send("Please mention the channel you want to unlock.")
            return

        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        if channel.id in locked_channels:
            del locked_channels[channel.id]
            save_locked_channels()

        await ctx.send(f"Channel {channel.mention} unlocked.")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def lock_server(self, ctx, duration: str = None, reason: str = "No reason provided"):
        if not duration:
            await ctx.send("Please specify a duration for the lock. Use s, m, h, or d.")
            return

        seconds = convert_to_seconds(duration)
        if seconds is None:
            await ctx.send("Invalid duration format. Use s, m, h, or d.")
            return

        for channel in ctx.guild.text_channels:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            locked_channels[channel.id] = {"unlock_time": datetime.datetime.now() + datetime.timedelta(seconds=seconds)}

        save_locked_channels()
        await ctx.send(f"Server locked for {duration}. Reason: {reason}")

        await asyncio.sleep(seconds)
        for channel_id in list(locked_channels.keys()):
            channel = ctx.guild.get_channel(channel_id)
            if channel:
                await channel.set_permissions(ctx.guild.default_role, send_messages=True)
                del locked_channels[channel_id]

        save_locked_channels()
        await ctx.send("Server unlocked automatically after the duration.")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unlock_server(self, inter):
        for channel in inter.guild.text_channels:
            await channel.set_permissions(inter.guild.default_role, send_messages=True)
            if str(channel.id) in locked_channels:
                del locked_channels[str(channel.id)]
        
        save_locked_channels()
        await inter.response.send_message("Server unlocked.")

    # DEFINE THE ADMIN ID IN THE CONFIG

    @commands.command(aliases=['config', 'view', 'view_config', 'cfig'])
    @commands.check(is_admin) # only runs for one user id (the owner)
    async def config_view(self, ctx):
        # Create an embed to display config data
        embed = discord.Embed(title='Reading config.json', description='Here are the config details:', color=embed_colour)
        
        # Add config details to the embed
        # config is defined in utilities.py
        for key, value in config.items():
            if key.lower() == 'token':
                value = '[hidden for security reasons]'  # Replace token value with asterisks
            embed.add_field(name=f'`{key}`', value=f'`{value}`', inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(is_admin) # only runs for one user id (owner)
    async def config_edit(self, ctx, key=None, value=None):
        if key is None:
            embed = discord.Embed(
                title="Incorrect usage",
                description=f"{ctx.author.mention}, Incorrect usage. Please use (**CASE SENSITIVE**): `{prefix}config_edit <name> <new_value>`",
                color=embed_error
            )
            await ctx.send(embed=embed)
            return
        
        if value is None:
            embed = discord.Embed(
                title="Incorrect usage",
                description=f"{ctx.author.mention}, Incorrect usage. Please use (**CASE SENSITIVE**): `{prefix}config_edit <name> <new_value>`",
                color=embed_error
            )
            await ctx.send(embed=embed)
            return

        # Update the config dictionary
        config[key] = value

        # Save the updated config to the config file
        with open('config.json', 'w') as file:
            json.dump(config, file, indent=4)

        # Create an embed to confirm the update
        embed = discord.Embed(title='Config Updated', color=embed_colour)
        embed.add_field(name='**Variable**', value=key, inline=False)
        embed.add_field(name='**New Value**', value=value, inline=False)

        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Moderation Cog Loaded! {Fore.RESET}')


def mod_setup(bot):
    bot.add_cog(Moderation(bot))
