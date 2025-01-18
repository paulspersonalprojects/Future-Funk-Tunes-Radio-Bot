import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
import os



load_dotenv()
TOKEN = os.getenv("Token")


bot = discord.Bot()

def is_connected(ctx):
    return ctx.voice_client and ctx.voice_client.is_connected()



# Ping command
@bot.tree.command(description="Check bot latency")
async def ping(ctx):
    await ctx.respond(f"Latency is {bot.latency:.2f} seconds.")

@bot.tree.command(description="Play the Future funk radio in VC")
async def connect(ctx):
    user = ctx.message.author
    
    if user.voice and user.voice.channel:
        vc = await user.voice.channel.connect()
        source = FFmpegPCMAudio("https://stream.zeno.fm/48533y95cnruv", before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
        vc.play(source)
        await ctx.send(f"Now playing Future Funk Radio in {vc.channel.name}")
    else:
        await ctx.send("You need to be in a voice channel to use this command.")

@bot.tree.command(description="Disconnect from VC")
async def Disconnect(ctx):
    if is_connected(ctx):
        await ctx.voice_client.disconnect()
        await ctx.respond(f"Disconnected")
    
    else:
        await ctx.respond(f"You are not in a voice channel")


bot.run(TOKEN)
