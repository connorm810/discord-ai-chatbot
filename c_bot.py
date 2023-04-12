# URL = https://discord.com/api/oauth2/authorize?client_id=1095554417031385129&permissions=2147494912&scope=applications.commands%20bot

import os
import discord
import openai
import requests
from discord.ext import commands

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
OPENAI_TOKEN = os.environ["OPENAI_TOKEN"]
STABLE_KEY = os.environ["STABLE_KEY"]

openai.api_key = OPENAI_TOKEN
intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)


@client.command(
    name="genimg",
    brief="Generates an image using Stable Diffusion",
    help="Provide a prompt for the Stable Diffusion API to use and it will generate an image."
)
async def generate_image(ctx, *args):
    response = ""

    for arg in args:
        response = response + " " + arg

    await ctx.channel.send(f"Attempting to generate an image with prompt: {response}")

    try:
        r = requests.post(
            "https://api.deepai.org/api/stable-diffusion",
            data={
                'text': response,
                "grid_size": "1",
                "width": "1536",
                "height": "768"
            },
            headers={
                'Api-Key': STABLE_KEY,
            }
        )
        print(r.json())

        await ctx.channel.send(r.json()["output_url"])
    except:
        await ctx.channel.send("Sorry, but I'm having a little trouble. Try asking that again.")


@client.event
async def on_message(message):
    # Don't respond to self
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        # OpenAI
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{message.content}",
            max_tokens=2048,
            temperature=0.6
        )

        # Send the response
        try:
            await message.channel.send(response.choices[0].text)
        except:
            await message.channel.send("Sorry, but I'm having a little trouble. Try asking that again.")

    await client.process_commands(message)


# Runs the bot
client.run(DISCORD_TOKEN)
