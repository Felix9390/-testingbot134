import discord
import time

def wait(t):
    time.sleep(t)

# Bot online system
DISCORD_TOKEN = "YOUR TOKEN"

# Startup Messages
print("Bot by Felix | Flame v0.2")
wait(.2)
print("Starting...")
wait(.2)
print("Status: Online")
wait(.2)
print("Done, bot is active!")
wait(.2)

# Define req intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Creating Client
client = discord.Client(intents=intents)

# Define function to validate parameters
def validate_params(name=None, question=None, options=None, countdown=None):
    # Validate poll name
    if not name:
        return "err"

    # Validate poll question
    if not question:
        return "err"

    # Validate poll options
    if not options or len(options) < 2:
        return "err"

    # Validate countdown
    try:
        countdown = int(countdown)
    except ValueError:
        return "err"

    if countdown < 0:
        return "err"

    return "ok"

# Prefix Variable
prefix = "/"

# Function to check if user has a higher role than the bot
def has_higher_role(user):
    bot_member = user.guild.get_member(client.user.id)
    if user.top_role >= bot_member.top_role:
        return True
    return False

# Command: Lock Server
async def lock_server(message):
    print("\n")
    print("command executed !!!")
    print("\n")

    # Lock all channels
    for channel in message.guild.channels:
        await channel.set_permissions(message.guild.default_role, send_messages=False)

    # Lock all roles
    for role in message.guild.roles:
        await role.edit(permissions=discord.Permissions.none())

    # Remove administrator from all roles
    for role in message.guild.roles:
        permissions = role.permissions
        permissions.administrator = False
        await role.edit(permissions=permissions)

    # Find the user with the highest role
    highest_role = None
    for member in message.guild.members:
        if not highest_role:
            highest_role = member.top_role
        elif member.top_role > highest_role:
            highest_role = member.top_role

    # Send a message to the user with the highest role
    if highest_role:
        embed = discord.Embed(title="Server Locked", description="The server has been locked.", color=discord.Color.red())
        await highest_role.send(embed=embed)
    else:
        embed = discord.Embed(title="Server Locked", description="The server has been locked.", color=discord.Color.red())
        await message.channel.send(embed=embed)

# Command: Ban User
async def ban_user(message):
    print("\n")
    print("command executed !!!")
    print("\n")
    # Get the mentioned user from the message
    user = message.mentions[0]
    reason = message.content.split(" ")[2:]
    reason = " ".join(reason)

    if not has_higher_role(user):
        # Ban the user
        await user.ban(reason=reason)
        # Send a message to the channel
        await message.channel.send(f"{user.name} has been banned from the server for {reason}.")
    else:
        embed = discord.Embed(title="Error", description="You cannot ban a user with a higher role than the bot.", color=discord.Color.red())
        await message.channel.send(embed=embed)

# Command: Warn User
async def warn_user(message):
    print("\n")
    print("command executed !!!")
    print("\n")
    # Get the mentioned user from the message
    user = message.mentions[0]
    reason = message.content.split(" ")[2:]
    reason = " ".join(reason)

    if not has_higher_role(user):
        # Send a warning message to the user's DMs
        embed = discord.Embed(title="Warning", description=f"You've been warned for {reason}.", color=discord.Color.orange())
        await user.send(embed=embed)

        # Send a message to the channel and ping the user
        embed = discord.Embed(title="Warning", description=f"{user.mention} has been warned for {reason}.", color=discord.Color.orange())
        await message.channel.send(embed=embed)
    else:
        embed = discord.Embed(title="Error", description="You cannot warn a user with a higher role than the bot.", color=discord.Color.red())
        await message.channel.send(embed=embed)

# Command: Mute User
async def mute_user(message):
    print("\n")
    print("command executed !!!")
    print("\n")
    # Get the mentioned user from the message
    user = message.mentions[0]
    reason = message.content.split(" ")[2:]
    reason = " ".join(reason)

    if not has_higher_role(user):
        # Get the Muted role from the server
        muted_role = discord.utils.get(message.guild.roles, name="Muted")

        if not muted_role:
            # Create the Muted role if it doesn't exist
            muted_role = await message.guild.create_role(name="Muted")

            # Set the permissions for the Muted role
            for channel in message.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False)

        # Add the Muted role to the member
        await user.add_roles(muted_role, reason=reason)

        # Send a message to the channel
        await message.channel.send(f"{user.mention} has been muted for {reason}.")
    else:
        embed = discord.Embed(title="Error", description="You cannot mute a user with a higher role than the bot.", color=discord.Color.red())
        await message.channel.send(embed=embed)

# Command: Unmute User
async def unmute_user(message):
    print("\n")
    print("command executed !!!")
    print("\n")
    # Get the mentioned user from the message
    user = message.mentions[0]

    if not has_higher_role(user):
        # Get the Muted role from the server
        muted_role = discord.utils.get(message.guild.roles, name="Muted")

        if muted_role in user.roles:
            # Remove the Muted role from the member
            await user.remove_roles(muted_role)

            # Send a message to the channel
            await message.channel.send(f"{user.mention} has been unmuted.")
        else:
            await message.channel.send(f"{user.mention} is not muted.")
    else:
        embed = discord.Embed(title="Error", description="You cannot unmute a user with a higher role than the bot.", color=discord.Color.red())
        await message.channel.send(embed=embed)

# First Command: Creating Poll
@client.event
async def on_message(message):
    try:
        if message.content.startswith(prefix + "start_poll"):
            print("\n")
            print("command executed !!!")
            print("\n")
            params = message.content.split(";")
            name = params[1].replace("/start_poll ","").strip()
            question = params[2].strip()
            options = [x.strip() for x in params[3].strip().split(",")]
            options_count = len(options)
            countdown = params[4]
            print(f"vars setted {name} / {question} / {options} / {options_count} / {countdown}")

            error = validate_params(name, question, options, countdown)

            if error == "err":
                embed = discord.Embed(title="Error", description=error, color=discord.Color.red())
                await message.channel.send(embed=embed)
                print("\n")
                print("ERROR in poll cmd, idk why")
                print("\n")
                return

            option_list = "\n".join(options)
            col = discord.Color.blue()
            embed = discord.Embed(title=f"POLL: {name}", description=f"**{question}\n{option_list},  (**react with numbers**)", color=col)

            print("\n")
            print("no error?? good")
            print("\n")
            send = await message.channel.send(embed=embed)
            print("\n")
            print(str(send))
            print("\n")
        elif message.content.startswith(prefix + "test"):
            print("\n")
            print("command executed !!!")
            print("\n")
            params = message.content.split(";")
            col = discord.Color.blue()
            embed = discord.Embed(title="title: test1", description="**test desc \n test line**", color=col)
            print("\n")
            print("no error?? good")
            print("\n")
            send = await message.channel.send(embed=embed)
            print(str(send))
            print("\n")
        elif message.content.startswith(prefix + "kick"):
            await kick_user(message)
        elif message.content.startswith(prefix + "ban"):
            await ban_user(message)
        elif message.content.startswith(prefix + "warn"):
            await warn_user(message)
        elif message.content.startswith(prefix + "mute"):
            await mute_user(message)
        elif message.content.startswith(prefix + "unmute"):
            await unmute_user(message)
        elif message.content.startswith(prefix + "lock_server"):
            await lock_server(message)
        elif message.content.startswith(prefix + "unlock_server"):
            print("\n")
            print("command executed !!!")
            print("\n")
            # Unlock all channels
            for channel in message.guild.channels:
                await channel.set_permissions(message.guild.default_role, send_messages=True)

            # Unlock all roles
            for role in message.guild.roles:
                await role.edit(permissions=discord.Permissions.all())

            # Find the user with the highest role
            highest_role = None
            for member in message.guild.members:
                if not highest_role:
                    highest_role = member.top_role
                elif member.top_role > highest_role:
                    highest_role = member.top_role

            # Send a message to the user with the highest role
            if highest_role:
                embed = discord.Embed(title="Server Unlocked", description="The server has been unlocked.", color=discord.Color.green())
                await highest_role.send(embed=embed)
            else:
                embed = discord.Embed(title="Server Unlocked", description="The server has been unlocked.", color=discord.Color.green())
                await message.channel.send(embed=embed)
    except:
        pass


# Run the bot
client.run(DISCORD_TOKEN)

