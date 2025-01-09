import discord
from discord import default_permissions
from dotenv import load_dotenv
import os
import vlc

load_dotenv()
bot = discord.bot()

TOKEN = os.getenv("Token")

def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

@bot.comand(description="Sends Latency")
async def ping(ctx):
    await ctx.respond(f"Latency is {bot.latency}")

@bot.command(description="Play the Future funk radio in VC")
async def connect(ctx):
    vc = user.voice.channel
    user = ctx.message.author
    if is_connected():
        await vc.connect()
        await ctx.respond(f"Connected to {vc}")
        await 
    else:
        await ctx.send("You are not in a voice channel")

@bot.slash_command()
async def Disconnect(ctx):
    if is_connected():
        await ctx.respond(f"Disconnected")
    
    else:
        await ctx.respond(f"You are not in a voice channel")