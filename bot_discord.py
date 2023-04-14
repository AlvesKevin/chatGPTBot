import os
import random
import json
import openai
import discord
from discord import Intents
from discord.ext import commands



openai.api_key = OPENAI_API_KEY
intents = Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

def load_image_prompts():
    with open('image_prompts.json', 'r') as file:
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


async def generate_prompt_with_chatgpt(prompt, subject):
    # Ajout des balises spécifiques en fonction du sujet
    if "chateau dans le ciel" in subject.lower():
        guided_prompt = f"En utilisant l'exemple de prompt suivant : '{prompt}', créez un nouveau prompt original, pertinent et détaillé pour Midjourney, une IA de génération d'image, sur le thème d'un château dans le ciel. Décrivez l'environnement, les couleurs et les formes qui le composent."
    elif "forêt enchantée" in subject.lower():
        guided_prompt = f"En utilisant l'exemple de prompt suivant : '{prompt}', créez un nouveau prompt original, pertinent et détaillé pour Midjourney, une IA de génération d'image, sur le thème d'une forêt enchantée. Décrivez l'environnement, les couleurs et les formes qui la composent."
    else:
        guided_prompt = f"En utilisant l'exemple de prompt suivant : '{prompt}', créez un nouveau prompt original, pertinent et détaillé pour Midjourney, une IA de génération d'image, sur le thème de {subject}."

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=guided_prompt,
        temperature=0.7,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()

@bot.command(name='generate_prompt')
async def generate_prompt_command(ctx):
    base_prompt = generate_prompt()
    message = ctx.message
    subject = message.content
    generated_prompt = await generate_prompt_with_chatgpt(base_prompt, subject)
    await send_large_message(ctx.channel, f"Prompt généré pour Midjourney : {generated_prompt}")


bot.run(DISCORD_TOKEN)
