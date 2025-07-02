from discord.ext import commands, tasks
import discord
import requests
import io
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="*", intents=intents)
mode = "SFW"

@bot.event
async def on_ready():
    status = discord.Status.online if mode == "SFW" else discord.Status.dnd
    activity = discord.Game("Kawai vibes only❤" if mode == "SFW" else "Don't leave me alone today🥺")
    await bot.change_presence(status=status, activity=activity)
    print(f"Nuko-Chan is online in {mode} mode.")

@bot.command()
async def toggle(ctx):
    global mode
    mode = "NSFW" if mode == "SFW" else "SFW"
    await on_ready()
    await ctx.send(f"Mode switched to {mode}!")

@bot.command()
async def pic(ctx, *, prompt: str):
    await ctx.send("Generating image...")
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(
        "https://api-inference.huggingface.co/models/hakurei/waifu-diffusion",
        headers=headers, json={"inputs": prompt}
    )
    if response.ok:
        await ctx.send(file=discord.File(io.BytesIO(response.content), filename="nuko.png"))
    else:
        await ctx.send("Image generation failed.")

bot.run(DISCORD_TOKEN)
