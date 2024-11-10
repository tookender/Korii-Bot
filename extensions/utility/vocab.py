import discord
from discord.ext import commands
import random
from ._base import UtilityBase

vocabulary = {
    "Wie heißt du?": "Tu t'appelles comment?",
    "Ich heiße Leo. Und du?": "Je m'appelle Leo. Et toi?",
    "Wie alt bist du?": "Tu as quel âge?",
    "Ich bin 14 Jahre Alt. Und du?": "J'ai 14 ans. Et toi?",
    "Ich bin in der achten Klasse.": "Je suis en quatrième.",
    "Hast du Geschwister?": "Tu as des frères et soeurs?",
    "Ich habe einen Bruder. / Ich habe keine Geschwister": "J'ai un frère. / Je n'ai pas de frères et soeurs.",
    "Hast du ein Haustier?": "Tu as un animal?",
    "Ich habe einen Hund. / Ich habe kein Haustier.": "J'ai un chien. / Je n'ai pas d'animal.",
    "Meine Eltern sind zusammen/getrennt.": "Mon parents sont ensembles/séparés.",
    "Ich habe eine Allergie.": "J'ai un allergie.",
    "Ich esse kein Fleisch, weil ich Vegetarier/in bin": "Je ne mange pas de viande, parce que je suis végétarien/ne.",
    "Fußball ist nicht mein Ding.": "Le foot ce n'est pas mon truc",
    "Ich mag / liebe Videospiele.": "J'aime / J'adore les jeux vidéo",
    "Ich mag / liebe es, Minecraft zu spielen": "J'aime / J'adore joéur á Minecraft",
    "Ich hasse / mag Shoppen nicht (so sehr)": "Je n'aime pas / Je deteste la shopping",
    "Ich hasse es / mag es nicht (so sehr) zu arbeiten.": "Je n'aime pas / Je deteste travailler.",
    "Ich bin ein Fan von Kylian Mbappé.": "Je suis fan de Kylian Mbappé",
    "Pomme ist mein Lieblingssängerin.": "Pomme est ma chanteuse préferée.",
    "Ich bevorzuge es, (Museen zu besichtigen).": "Moi, je préfère (visiter des musées)",
    "Für mich, ist Sport der Horror!": "Pour moi, le sport c'est l'horreur",
    "Ich treibe Sport/ klettere / spiele Gitarre.": "Je fais du sport / de l'escalade / de la guitare."
}

active_games = {}

class VocabularyCommand(UtilityBase):
    @commands.command(name="vocab")
    async def vocab(self, ctx):
        if ctx.author.id in active_games:
            await ctx.send("You are already in a game. Type 'stop' to end it.")
            return

        active_games[ctx.author.id] = True
        await ctx.send("Starting the vocabulary game! Type 'stop' to end it.")

        while active_games.get(ctx.author.id):
            german_phrase = random.choice(list(vocabulary.keys()))
            french_answer = vocabulary[german_phrase]

            embed = discord.Embed(title="Translate to French", description=german_phrase, color=discord.Color.blue())
            await ctx.send(embed=embed)

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            msg = await self.bot.wait_for("message", check=check)

            if msg.content.lower() == "stop":
                del active_games[ctx.author.id]
                await ctx.send("Game stopped.")
                return

            if msg.content.strip() == french_answer:
                embed = discord.Embed(title="Correct!", description="Well done!", color=discord.Color.green())
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Incorrect!", description="You need to correct it to proceed.", color=discord.Color.red())
                await ctx.send(embed=embed)
