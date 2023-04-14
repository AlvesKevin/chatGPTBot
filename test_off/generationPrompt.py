import openai
import json
from tqdm import tqdm


# Définir votre clé d'API OpenAI
openai.api_key = "TON-API-OPENAI"

# Définir les exemples de prompts que vous voulez utiliser
example_prompts = ["[STYLE: Speedpainting] [COLORS: Red, Amber] [SHAPE: Vintage Van] [THEME: Road Trip] [MEDIUM: 2D Game Art] Generate an image with natural phenomena and forestpunk elements. Aspect Ratio 2:3. Chaos level 8.  Resolution 750 x 750",
                   "[STYLE: Vibrant Futurism] [COLORS: Dark Aquamarine, Red, Silver, Blue] [SHAPE: Dreadnought Female Art] [THEME: Stargate Comic] Create a multilayered texture with dynamic pose. Aspect Ratio 9:16. Chaos level 7 Style expressive.",
                   "[MEDIUM: Photography] [THEME: Portrait] [FEATURES: Green Eyes, Red Hair, Light Freckles, Jewelry] Create a realistic, detailed image with aperture f1.6. Aspect Ratio 9:16. Resolution 750 x 750 ",
                   "[THEME: Steampunk City] [MEDIUM: Comic Doodle] [STYLE: Isometric] Create an image in aspect ratio 3:4. Resolution 750 x 750. Quantity 1. Variation 5.",
                   "[MEDIUM: Illustration] [THEME: Cthulhu Mythos] [STYLE: Hyperrealistic] [COLORS: Red, Blue] Create an 8K HD illustration in maximal details and cinematic style. Aspect Ratio 2:3 ",
                   "[MEDIUM: Industrial Look Robot] [THEME: Game/Film] [STYLE: Dark Green] [THEME: Quantumpunk] Create an 8K photorealistic detail with hyper-realistic details. Aspect Ratio 9:16. Chaos level 7 Style expressive.",
                   "[MEDIUM: Traditional Japanese Art] [THEME: High School Student] [STYLE: Anime-Inspired Characters] [COLORS: Dark Teal, Light Beige] Create a dramatic image using shadows. Aspect Ratio 4:7 Style expressive.",
                   "[MEDIUM: Animated Film] [THEME: Dog] [FEATURES: Flowers, Bathtub] Create a detailed 3D animation style render by Disney Pixar studio. Aspect Ratio 3:4. Resolution 750 x 750 ",
                   "[MEDIUM: Flat Cartoon Vector] [THEME: Woman Traveler] [FEATURES: Photo Camera, Map] Create a character design. Stylize 500 ",
                    "[STYLE: Speedpainting] [COLORS: Red, Amber] [SHAPE: Vintage Van] [THEME: Road Trip] [MEDIUM: 2D Game Art] Generate an image with natural phenomena and forestpunk elements. Aspect Ratio 2:3. Chaos level 8. Resolution 750 x 750.",
                    "[STYLE: Vibrant Futurism] [COLORS: Dark Aquamarine, Red, Silver, Blue] [SHAPE: Dreadnought Female Art] [THEME: Stargate Comic] Create a multilayered texture with dynamic pose. Aspect Ratio 9:16. Chaos level 7 Style expressive.",
                    "[MEDIUM: Photography] [THEME: Portrait] [FEATURES: Brown Eyes, Black Hair, Nose Piercing] Create a dramatic, moody image with aperture f1.8. Aspect Ratio 3:4. Resolution 1000 x 1000.",
                    "[THEME: Underwater World] [MEDIUM: Digital Art] [STYLE: Hyperrealistic] [COLORS: Blue, Green] Create an 8K HD illustration in maximal details and cinematic style. Aspect Ratio 2:3.",
                    "[MEDIUM: Fantasy Book Cover] [THEME: Dragon] [STYLE: Epic] [FEATURES: Fire Breathing] Create an image with a majestic dragon in a fiery landscape. Aspect Ratio 16:9. Resolution 1920 x 1080.",
                    "[MEDIUM: Abstract Painting] [THEME: Music] [STYLE: Colorful] [FEATURES: Musical Notes] Create a vibrant abstract painting inspired by music. Aspect Ratio 1:1. Resolution 1000 x 1000.",
                    "[MEDIUM: Poster Design] [THEME: Travel] [FEATURES: Vintage Typography] [STYLE: Retro] Create a vintage travel poster with retro typography. Aspect Ratio 2:3. Resolution 750 x 1000.",
                    "[MEDIUM: Book Illustration] [THEME: Fairy Tale] [FEATURES: Castle, Princess, Prince] [STYLE: Storybook] Create a whimsical storybook illustration of a castle with a princess and a prince. Aspect Ratio 4:3.",
                    "[MEDIUM: Concept Art] [THEME: Science Fiction] [FEATURES: Alien Planet] [STYLE: Futuristic] Create a futuristic concept art of an alien planet with strange creatures and landscapes. Aspect Ratio 16:9. Resolution 1920 x 1080.",
                    "[MEDIUM: Caricature] [THEME: Celebrity] [FEATURES: Big Nose, Glasses] [STYLE: Cartoon] Create a funny caricature of a celebrity with a big nose and glasses. Aspect Ratio 1:1. Resolution 1000 x 1000."
                   ]

# Générer 100 prompts basés sur les structures de prompts fournies
generated_prompts = []
for i in tqdm(range(5), desc="Génération des prompts"):
    prompt_index = i % len(example_prompts)  # Sélectionner une structure de prompt
    example_prompt = example_prompts[prompt_index]
    mymessage = "une montagne"
    prompt = f"Apprend à générer un prompt cohérent avec la structure suivante {example_prompt} et avec un nouveau sujet et de nouveau parametre."
    response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=1,
            max_tokens=100,
            n=1,
            stop=None,
            frequency_penalty=0,
            presence_penalty=0,
            api_key="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")
    generated_prompt = response["choices"][0]["text"].strip()

    # Vérifier la répétition de mots dans le prompt
    prompt_words = generated_prompt.split()
    word_count = {}
    for word in prompt_words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    repeated_words = [word for word in word_count.keys() if word_count[word] > 1]
    while repeated_words:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=1,
            max_tokens=100,
            n=1,
            stop=None,
            frequency_penalty=0,
            presence_penalty=0,
            api_key="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")
        generated_prompt = response["choices"][0]["text"].strip()
        prompt_words = generated_prompt.split()
        word_count = {}
        for word in prompt_words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
        repeated_words = [word for word in word_count.keys() if word_count[word] > 1]

    generated_prompts.append(generated_prompt)

# Enregistrer les prompts générés dans un fichier JSON
with open('prompts.json', 'w') as f:
    json.dump(generated_prompts, f, indent=4)

# Afficher un message dans le terminal pour indiquer que les prompts ont été enregistrés
print("Les prompts ont été enregistrés dans le fichier prompts.json.")
