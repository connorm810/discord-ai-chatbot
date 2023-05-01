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


# !genimg command that generates an image based on user's prompt
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


# !code command that provides link to github repo
@client.command(
    name="code",
    brief="Provides link to GitHub page",
    help="Provides a direct link to the GitHub repo for this Discord bot."
)
async def code_link(ctx):
    await ctx.channel.send("Sure, here you go: https://github.com/connorm810/discord-ai-chatbot/tree/master")


# Listens for mentions in chat and responds using OpenAI
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
