import discord
from discord.ext import commands
from discord import app_commands
import os
import requests
import io

TOKEN = os.getenv("DISCORD_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")
BOT_MODE = "SFW"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="*", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.dnd if BOT_MODE == "NSFW" else discord.Status.online,
        activity=discord.Game("Don't leave me alone today🥺" if BOT_MODE == "NSFW" else "Kawai vibes only❤")
    )
    print(f"Neko-Chan is online in {BOT_MODE} mode.")
    await tree.sync()

@tree.command(name="toggle", description="Toggle NSFW/SFW mode")
async def toggle(interaction: discord.Interaction):
    global BOT_MODE
    BOT_MODE = "NSFW" if BOT_MODE == "SFW" else "SFW"
    await bot.change_presence(
        status=discord.Status.dnd if BOT_MODE == "NSFW" else discord.Status.online,
        activity=discord.Game("Don't leave me alone today🥺" if BOT_MODE == "NSFW" else "Kawai vibes only❤")
    )
    await interaction.response.send_message(f"Neko-Chan is now in {BOT_MODE} mode.")

@tree.command(name="pic", description="Generate image from prompt")
@app_commands.describe(prompt="Image description")
async def pic(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt}
    response = requests.post("https://api-inference.huggingface.co/models/hakurei/waifu-diffusion", headers=headers, json=payload)
    if response.status_code == 200:
        image = response.content
        await interaction.followup.send(file=discord.File(io.BytesIO(image), filename="image.png"))
    else:
        await interaction.followup.send("Image generation failed.")

bot.run(TOKEN)
