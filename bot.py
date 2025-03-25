import discord
from discord import app_commands
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
import os
import requests
import json
import time


load_dotenv()


intents = discord.Intents.default()
Client = discord.Client(intents=intents)
tree = app_commands.CommandTree(Client)

@Client.event
async def on_ready():
    await tree.sync()
    await Client.change_presence(activity=discord.Streaming(name=fetch_data(), url="https://zeno.fm/radio/future-fnk/"))
    print("Bot is up and running")

    while True:
        time.sleep(5) #Add Infinite Delay Loop that runs code every 5 seconds
        await Client.change_presence(activity=discord.Streaming(name=fetch_data(), url="https://zeno.fm/radio/future-fnk/"))




def fetch_data():
    url = "https://api.zeno.fm/mounts/metadata/subscribe/48533y95cnruv"
    try:
        # Open a streaming connection to the URL
        with requests.get(url, stream=True) as response:
            if response.status_code == 200:
                print("Listening for data...")
                # Process lines as they arrive
                for line in response.iter_lines(decode_unicode=True):
                    if line and line.startswith("data:"):
                        # Extract the JSON part after "data:"
                        data_content = line[5:].strip()
                        try:
                            # Parse the JSON to extract the song name
                            data_json = json.loads(data_content)
                            song_name = data_json.get("streamTitle")
                            if song_name:
                                return song_name
                        except json.JSONDecodeError:
                            print("Error decoding JSON from data:", data_content)
            else:
                print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
                return "error"
    except requests.RequestException as e:
        print(f"An error occurred: {e}")



def is_connected(interaction):
    return interaction.user.voice

# Ping command
@tree.command(name="ping", description="Check bot latency")
async def ping(interaction):
    await interaction.response.send_message(f"Latency is {Client.latency:.2f} seconds.")
    

@tree.command(name="connect", description="Play the Future funk radio in VC. Can also move to another channel")
async def connect(interaction):
    bot_voice = interaction.guild.voice_client
    user = interaction.user

    if bot_voice:
        # we're in a channel already
            if bot_voice.channel.id == user.voice.channel.id:
                # in the same voice channel as the user already
                await interaction.response.send_message("Bot is already in your VC")
                return

        # move channels now - we're in VC but not the user's VC
            await bot_voice.move_to(user.voice.channel)
            await interaction.response.send_message("Moved to your channel")
            return

    
    if interaction.user.voice:

        vc = await user.voice.channel.connect()

        source = discord.FFmpegPCMAudio(executable="ffmpeg-master-latest-win64-gpl-shared\\bin\\ffmpeg.exe", source="https://stream.zeno.fm/48533y95cnruv")
        vc.play(source)
        await interaction.response.send_message(f"Now playing Future Funk Radio in {vc.channel.name}")
 

    else:
        await interaction.response.send_message("You need to be in a voice channel to use this command.")

@tree.command(name="disconnecttt", description="Disconnect from VC")
async def Disconnect(interaction):
    if is_connected(interaction):
        bot_voice = interaction.guild.voice_client
        await bot_voice.disconnect(force=False)
        await interaction.response.send_message(f"Disconnected")

    else:
        await interaction.response.send_message(f"You are not in a voice channel")




@tree.command(name="nowplaying", description="Check whats playing right now in the Radio")
async def getsonginfo(interaction):
    stream_title = fetch_data()
    print(stream_title)
    await interaction.response.send_message(f"Now Playing: " + stream_title)


Client.run(os.getenv("Token"))
