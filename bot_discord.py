import random
import json
import openai
from discord import Intents
from discord.ext import commands
import asyncio
import requests

DISCORD_TOKEN = 'votre clé api'
OPENAI_API_KEY = 'votre clé api'

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
        return await channel.send(text)

    text_parts = [text[i:i + max_chars] for i in range(0, len(text), max_chars)]

    messages = []
    for part in text_parts:
        message = await channel.send(part)
        messages.append(message)

    return messages[-1] if messages else None


async def generate_prompt_with_chatgpt(prompt, subject):
    # Ajout des balises spécifiques en fonction du sujet
    if "chateau dans le ciel" in subject.lower():
        guided_prompt = f"En utilisant l'exemple de prompt suivant : '{prompt}', créez un nouveau prompt original, pertinent et détaillé pour Midjourney, une IA de génération d'image, sur le thème d'un château dans le ciel. Décrivez l'environnement, les couleurs et les formes qui le composent."
    elif "forêt enchantée" in subject.lower():
        guided_prompt = f"En utilisant l'exemple de prompt suivant : '{prompt}', créez un nouveau prompt original, pertinent et détaillé pour Midjourney, une IA de génération d'image, sur le thème d'une forêt enchantée. Décrivez l'environnement, les couleurs et les formes qui la composent."
    else:
        #guided_prompt = f"En utilisant l'exemple de prompt suivant : '{prompt}', créez un nouveau prompt original, pertinent et détaillé pour Midjourney, une IA de génération d'image, sur le thème de {subject}."
        guided_prompt = f"En utilisant l'exemple de prompt suivant : '{prompt}', créez un nouveau prompt original, pertinent et détaillé pour Midjourney, une IA de génération d'image, sur le thème de {subject}. Si c'est un lieu décris l'environnement, les couleurs, les textures, les odeurs et les sons qui le composent. Si c'est un être vivant detail sa couleur, sa façon d'être, ses émotions, son apparence, si c'est quelque chose d'autre essaie juste de le décrire au mieux"

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
    prompt_message = await send_large_message(ctx.channel, f"Prompt généré pour Midjourney : {generated_prompt}")

    def check_author(author):
        def inner_check(reaction, user):
            return user == author and str(reaction.emoji) in ['✅', '🔄']

        return inner_check

    await prompt_message.add_reaction('✅')
    await prompt_message.add_reaction('🔄')

    try:
        reaction, user = await bot.wait_for('reaction_add', check=check_author(message.author), timeout=60.0)

        if str(reaction.emoji) == '✅':
            data = {
                "content": f"/imagine {generated_prompt}"
            }
            headers = {
                "Authorization": f"Bot {DISCORD_TOKEN}"
            }
            response = requests.post(f"https://discord.com/api/v9/channels/{840735917995458614}/messages", json=data, headers=headers)
            if response.status_code == 200:
                await ctx.send("Commande exécutée avec succès.")
            else:
                await ctx.send(f"Erreur lors de l'exécution de la commande : {response.status_code}")
        elif str(reaction.emoji) == '🔄':
            await generate_prompt_command(ctx)
    except asyncio.TimeoutError:
        await prompt_message.delete()
        await send_large_message(ctx.channel, "Temps écoulé, prompt supprimé.")

bot.run(DISCORD_TOKEN)
