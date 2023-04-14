import os
import random
import json
import openai
import discord
from discord import Intents
from discord.ext import commands

DISCORD_TOKEN = 'MTA5Mzk3OTA0NDY2OTgzNzMxMg.Gvyc-y.knv0ngvCttV4DwwNxHctAXhqz0uO9f4__IiFlE'
OPENAI_API_KEY = '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'

openai.api_key = OPENAI_API_KEY
intents = Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

def load_image_prompts():
    with open('../image_prompts.json', 'r') as file:
        data = json.load(file)
    return data['prompts']

image_prompts = load_image_prompts()

def generate_prompt():
    return random.choice(image_prompts)

async def send_large_message(channel, text, max_chars=2000):
    if len(text) <= max_chars:
        await channel.send(text)
        return

    text_parts = [text[i:i + max_chars] for i in range(0, len(text), max_chars)]

    for part in text_parts:
        await channel.send(part)


async def generate_prompt_with_chatgpt(prompt):
    guided_prompt = f"En utilisant l'exemple de prompt suivant : '{prompt}', créez un nouveau prompt original, pertinent, detaillé et basé sur mon message pour Midjourney, une IA de génération d'image"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=guided_prompt,
        temperature=0.7,
        max_tokens=50,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()

@bot.command(name='generate_prompt')
async def generate_prompt_command(ctx):
    base_prompt = generate_prompt()
    generated_prompt = await generate_prompt_with_chatgpt(base_prompt)
    await send_large_message(ctx.channel, f"Prompt généré pour Midjourney : {generated_prompt}")


bot.run(DISCORD_TOKEN)
