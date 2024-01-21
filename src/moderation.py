

from installation import *
from utilities import *


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Ticket Panel Command
    @commands.slash_command(name="ticketpanel", description="Create a ticket panel")
    async def ticket_panel(self, ctx):
        view = View()
        button = Button(label="Create Ticket", style=discord.ButtonStyle.green) 

        async def ticket_button_callback(interaction):
            guild = interaction.guild
            member = interaction.user
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=True)
            }
            ticket_channel = await guild.create_text_channel(f"ticket-{member.display_name}", overwrites=overwrites)
            await ticket_channel.respond(f"{member.mention} Welcome to your ticket!")
            await interaction.response.respond_message(f"Ticket created: {ticket_channel.mention}", ephemeral=True) 

        button.callback = ticket_button_callback
        view.add_item(button) 

        embed = discord.Embed(title="Support Tickets", description="Click the button below to create a support ticket.", color=embed_colour)
        await ctx.respond(embed=embed, view=view) 


    # Verification Setup Command
    @commands.slash_command(name="setup-verify", description="Set up a verification panel")
    async def setup_verify(self, ctx, role: str, message: str):
        view = View()
        button = Button(label="Verify", style=discord.ButtonStyle.green)

        async def verify_button_callback(interaction):
            guild = interaction.guild
            member = interaction.user

            # Use the 'role' parameter captured during setup
            assigned_role = discord.utils.get(guild.roles, name=role)

            if assigned_role:
                await member.add_roles(assigned_role)
                await interaction.response.respond_message(f"You have been verified and received the {assigned_role.mention} role.", ephemeral=True)
            else:
                await interaction.response.respond_message(f"Error: '{role}' role not found. Please create the role and try again.", ephemeral=True)

        button.callback = verify_button_callback
        view.add_item(button)

        embed = discord.Embed(title="Verification Panel", description=message, color=embed_colour)
        await ctx.respond(embed=embed, view=view)


    @commands.slash_command(name="kick", description="Kick a user from the server")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: Option(discord.Member, "User to kick"), reason: Option(str, "Reason for kick", default="No reason provided")):
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(title="Kick", description=f"{member.mention} has been kicked.\nReason: {reason}", color=embed_error)
            await ctx.respond(embed=embed)
        except discord.Forbidden:
            await ctx.respond("I do not have permission to kick this user.") 


    @commands.slash_command(name="ban", description="Ban a user from the server")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: Option(discord.Member, "User to ban"), reason: Option(str, "Reason for ban", default="No reason provided")):
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(title="Ban", description=f"{member.mention} has been banned.\nReason: {reason}", color=embed_error)
            await ctx.respond(embed=embed)
        except discord.Forbidden:
            await ctx.respond("I do not have permission to ban this user.") 


    @commands.slash_command(name="mute", description="Mute a user in the server")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: Option(discord.Member, "User to mute"), reason: Option(str, "Reason for mute", default="No reason provided")):
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")

        if not mute_role:
            # If the "Muted" role doesn't exist, create it
            mute_role = await ctx.guild.create_role(name="Muted", reason="Creating Muted role for mute command")
            
            # Loop through all the channels in the server and deny respond message permissions for the "Muted" role
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, respond_messages=False)

        # Assign the "Muted" role to the specified user
        await member.add_roles(mute_role, reason=f"Muted by {ctx.author} for reason: {reason}")

        # Create an embed for the confirmation message
        embed = discord.Embed(title="User Muted", description=f"{member.mention} has been muted.", color=embed_error)
        embed.add_field(name="Reason", value=reason)
        embed.set_footer(text=f"Muted by {ctx.author}")

        # Send the embed
        await ctx.respond(embed=embed)


    @commands.slash_command(name="clear", description="Clear a specified number of messages in a text channel")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: Option(int, "Number of messages to clear")):
        await ctx.channel.purge(limit=amount + 1) 


    @commands.slash_command(name="lockchannel", description="Lock a channel for a specified duration")
    @commands.has_permissions(manage_channels=True)
    async def lock_channel(self, ctx, channel: Option(discord.TextChannel, "Channel to lock"), duration: Option(str, "Duration (s/m/h/d)"), reason: Option(str, "Reason for lock", default="No reason provided")):
        # Convert duration to seconds
        seconds = convert_to_seconds(duration)
        if seconds is None:
            await ctx.respond("Invalid duration format. Use s, m, h, or d.")
            return

        # Change channel permissions
        await channel.set_permissions(ctx.guild.default_role, respond_messages=False)
        await ctx.respond(f"Channel {channel.mention} locked for {duration}. Reason: {reason}")

        # Convert datetime to string before including it in a serializable context
        unlock_time_str = (datetime.datetime.now() + datetime.timedelta(seconds=seconds)).strftime("%Y-%m-%d %H:%M:%S")

        # Save locked channel state with the time as a string
        locked_channels[channel.id] = {"unlock_time": unlock_time_str}
        save_locked_channels()

        # Schedule unlock after duration
        await asyncio.sleep(seconds)
        if channel.id in locked_channels:  # Check if still locked
            await channel.set_permissions(ctx.guild.default_role, respond_messages=True)
            del locked_channels[channel.id]
            save_locked_channels()
            await channel.respond(f"Channel unlocked automatically after {duration}.")


    @commands.slash_command(name="unlockchannel", description="Unlock a channel")
    @commands.has_permissions(manage_channels=True)
    async def unlock_channel(self, ctx, channel: Option(discord.TextChannel, "Channel to unlock")):
        await channel.set_permissions(ctx.guild.default_role, respond_messages=True)
        if channel.id in locked_channels:
            del locked_channels[channel.id]
            save_locked_channels()
        await ctx.respond(f"Channel {channel.mention} unlocked.")


    @commands.slash_command(name="lockserver", description="Lock the entire server for a specified duration")
    @commands.has_permissions(administrator=True)
    async def lock_server(self, ctx, duration: Option(str, "Duration (s/m/h/d)"), reason: Option(str, "Reason for lock", default="No reason provided")):
        seconds = convert_to_seconds(duration)
        if seconds is None:
            await ctx.respond("Invalid duration format. Use s, m, h, or d.")
            return

        for channel in ctx.guild.text_channels:
            await channel.set_permissions(ctx.guild.default_role, respond_messages=False)
            locked_channels[channel.id] = {"unlock_time": datetime.datetime.now() + datetime.timedelta(seconds=seconds)}
            await ctx.respond(f"Channel {channel.mention} locked for {duration}. Reason: {reason}")
        
        save_locked_channels()
        await ctx.respond(f"Server locked for {duration}. Reason: {reason}")

        await asyncio.sleep(seconds)
        for channel_id in list(locked_channels.keys()):
            channel = ctx.guild.get_channel(channel_id)
            if channel:
                await channel.set_permissions(ctx.guild.default_role, respond_messages=True)
                del locked_channels[channel_id]
        
        save_locked_channels()
        await ctx.respond("Server unlocked automatically after the duration.")


    @commands.slash_command(name="unlockserver", description="Unlock the entire server")
    @commands.has_permissions(administrator=True)
    async def unlock_server(self, inter):
        for channel in inter.guild.text_channels:
            await channel.set_permissions(inter.guild.default_role, respond_messages=True)
            if str(channel.id) in locked_channels:
                del locked_channels[str(channel.id)]
        
        save_locked_channels()
        await inter.response.respond_message("Server unlocked.")


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Moderation Cog Loaded! {Fore.RESET}')

def setup(bot):
    bot.add_cog(Moderation(bot))
