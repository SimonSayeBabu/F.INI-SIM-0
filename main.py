import discord
from scrap import *
from datetime import date, timedelta
from flask import Flask
from threading import Thread
from discord.ext import tasks, commands
from itertools import cycle

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)
app = Flask('')
bot.remove_command('help')

@app.route('/')
def main():
    return "Your Bot Is Ready"


def run():
    app.run(host="0.0.0.0", port=8000)


def keep_alive():
    server = Thread(target=run)
    server.start()


status = cycle(["JoJo's Bizarre Adventure", "Mushoku Tensei"])


@bot.event
async def on_ready():
    change_status.start()
    print(f'We have logged in as {bot.user}')


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=next(status)))


@bot.event
async def on_message(message):
    if message.content == '$help':
        await message.channel.send(
            "Voici la liste des commandes: \n**$cours** : affiche les cours de la journée. \n**$cours demain** : affiche les cours de la journée de demain. \n**$cours** *jj mm aaaa*: Donne les cours a la date indiquée."
        )

    if message.content == '$cours':
        d1 = date.today()
        today = d1.strftime("%Y-%m-%d")
        edt = export()
        cours = []
        for elmt in edt:
            confirm = 0
            for i in range(len(today)):
                if elmt["start"][i] == today[i]:
                    confirm += 1
            if confirm == 10:
                cours.append(elmt)
        if len(cours) == 0:
            await ctx.send("Il n'y a pas cours aujourd'hui !")
        else:
            await message.channel.send("Voici les cours **d'aujourd'hui** ! : \n" +
                                   affichage(cours))

    if message.content == '$cours demain':
        d1 = date.today() + timedelta(days=1)
        tomorrow = d1.strftime("%Y-%m-%d")
        edt = export()
        cours = []
        for elmt in edt:
            confirm = 0
            for i in range(len(tomorrow)):
                if elmt["start"][i] == tomorrow[i]:
                    confirm += 1
            if confirm == 10:
                cours.append(elmt)
        if len(cours) == 0:
            await ctx.send("Il n'y a pas cours demain !")
        else:
            await message.channel.send("Voici les cours de **demain** ! : \n" +
                                   affichage(cours))

    await bot.process_commands(message)


@bot.command()
async def cours(ctx, jj, mm, aaaa):
    listeM = [
        "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"
    ]
    string = aaaa + '-' + mm + '-' + jj
    if len(string) >= 11 and len(aaaa) != 4 and mm not in listeM:
        return (await ctx.send(
            "Le **format** de la commande est incorrect, utiliser le format suivant : $cours jj mm aaaa"
        ))
    edt = export()
    cours = []
    for elmt in edt:
        confirm = 0
        for i in range(len(string)):
            if elmt["start"][i] == string[i]:
                confirm += 1
        if confirm == 10:
            cours.append(elmt)
    if len(cours) == 0:
        await ctx.send(
            "Il n'y a pas cours a cette date ou la date n'a pas été entrée de la bonne maniere. \n Essayer le format suivant : $cours jj mm aaaa"
        )
    else:
        await ctx.send("Voici les cours de " + string + "! : \n" +
                       affichage(cours))


#    add $cours xx/xx/xx

TOKEN = 'MTAyMjEwNDk3Mjc0NzM2MjM0Ng.GGzc-4.mge7E5iIRtNKvoK2n6BIBqzDXGOcxWT8fvL6PA'
bot.run(TOKEN)
