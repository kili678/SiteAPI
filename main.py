import os
import threading
import asyncio
import discord
from discord.ext import commands
import requests
from flask import Flask

# ========== FLASK SERVER POUR LE PING DE RENDER ==========
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    thread = threading.Thread(target=run_flask)
    thread.start()

# ========== DISCORD BOT ==========
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='', intents=intents)

PECHEURS_ROLE = "Pécheurs"
PECHE_S_CAPITAUX = [
    "Luxure", "Colère", "Envie", "Paresse", "Orgueil", "Gourmandise", "Avarice"
]

def send_data_to_api(owner_name, players_dict):
    url = "https://siteapi-2.onrender.com/owner"  # 🔁 Assure-toi que cette URL correspond à ton API

    # Payload à plat
    payload = {
        "owner": owner_name,
        **players_dict
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"[API] ✅ Données envoyées à /owner : {owner_name}")
        else:
            print(f"[API] ⚠️ Erreur HTTP {response.status_code} : {response.text}")
    except requests.exceptions.Timeout:
        print("[API] ⏱️ Timeout vers l'API")
    except requests.exceptions.ConnectionError:
        print("[API] 🔌 Erreur de connexion")
    except Exception as e:
        print(f"[API] ❌ Exception lors de l'envoi : {e}")

async def periodic_task():
    await bot.wait_until_ready()
    print("[Bot] 🚀 Tâche périodique lancée")

    while not bot.is_closed():
        try:
            if not bot.guilds:
                await asyncio.sleep(30)
                continue

            guild = bot.guilds[0]
            app_info = await bot.application_info()
            owner_name = app_info.owner.name

            role_pecheurs = discord.utils.get(guild.roles, name=PECHEURS_ROLE)
            players = {}

            for peche in PECHE_S_CAPITAUX:
                role_peche = discord.utils.get(guild.roles, name=peche)
                joueur = None

                if role_pecheurs and role_peche:
                    joueur = next(
                        (m for m in guild.members if role_pecheurs in m.roles and role_peche in m.roles),
                        None
                    )

                players[peche] = joueur.name if joueur else "Place vacante"

            send_data_to_api(owner_name, players)
        except Exception as e:
            print(f"[Bot] ❌ Erreur dans la tâche périodique : {e}")

        await asyncio.sleep(60)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    bot.loop.create_task(periodic_task())

@bot.command()
async def bonjour(ctx):
    await ctx.send(f"ta gueule {ctx.author}")

@bot.command()
async def Bonjour(ctx):
    await ctx.send(f"ta gueule {ctx.author}")

@bot.command()
async def zeleph(ctx):
    try:
        await ctx.message.add_reaction("🦊")
    except discord.HTTPException as e:
        print(f"[Erreur] Impossible d'ajouter la réaction : {e}")

@bot.command()
@commands.is_owner()
async def reload(ctx, extension: str = None):
    if extension:
        try:
            await bot.reload_extension(f"cogs.{extension}")
            await ctx.send(f"✅ Extension `{extension}` rechargée.")
        except Exception as e:
            await ctx.send(f"❌ Erreur: `{e}`")
    else:
        reloaded = []
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    await bot.reload_extension(f"cogs.{filename[:-3]}")
                    reloaded.append(filename)
                except Exception as e:
                    await ctx.send(f"❌ Erreur dans `{filename}`: `{e}`")
        await ctx.send(f"✅ Extensions rechargées : {', '.join(reloaded)}")

# ========== LANCEMENT ==========
if __name__ == '__main__':
    keep_alive()
    token = os.environ.get('TOKEN')
    if not token:
        print("❌ TOKEN manquant dans les variables d'environnement.")
        exit(1)
    bot.run(token)
