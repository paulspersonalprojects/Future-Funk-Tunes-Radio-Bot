import discord, ffmpeg
from discord import app_commands
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
import os



load_dotenv()


intents = discord.Intents.default()
Client = discord.Client(intents=intents)
tree = app_commands.CommandTree(Client)

@Client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=765412221130899466))
    print("Ready!")


def is_connected(interaction):
    return interaction.user.voice

# Ping command
@tree.command(name="ping", description="Check bot latency", guild=discord.Object(id=765412221130899466))
async def ping(interaction):
    await interaction.response.send_message(f"Latency is {Client.latency:.2f} seconds.")
    

@tree.command(name="connect", description="Play the Future funk radio in VC", guild=discord.Object(id=765412221130899466))
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

@tree.command(name="disconnecttt", description="Disconnect from VC", guild=discord.Object(id=765412221130899466))
async def Disconnect(interaction):
    if is_connected(interaction):
        bot_voice = interaction.guild.voice_client
        await bot_voice.disconnect(force=False)
        await interaction.response.send_message(f"Disconnected")

    else:
        await interaction.response.send_message(f"You are not in a voice channel")


Client.run(os.getenv("Token"))
