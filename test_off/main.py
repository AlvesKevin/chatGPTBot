import discord
import openai

openai.api_key = "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"

intents = discord.Intents.default()
intents.members = True

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Bot is ready')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    prompt = message.content

    # Envoyer un message "en train d'écrire"
    async with message.channel.typing():

        if message.content.startswith('/monbot'):
            prompt = message.content[8:]
            completions = openai.Completion.create(
                engine="davinci",
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )

        generated_text = completions.choices[0].text.strip()

        # Découpe le texte en plusieurs parties de 2000 caractères maximum
        message_parts = [generated_text[i:i + 2000] for i in range(0, len(generated_text), 2000)]

        # Envoie chaque partie du message séparément
        for part in message_parts:
            await message.channel.send(part)

client.run('MTA5Mzk3OTA0NDY2OTgzNzMxMg.Gvyc-y.knv0ngvCttV4DwwNxHctAXhqz0uO9f4__IiFlE')
