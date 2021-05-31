import discord
from discord.ext import commands, tasks
import config as con
import database as db

bot = commands.Bot(
    command_prefix="s#",
    case_insensitive=True,
    description="Ottawa bot anti raid",
    intents=discord.Intents.all()
)
bot.remove_command("help")

cogs = [
    "anti-bot",
    "anti-roles",
    "anti-channels",
    "anti-ban",
    "anti-kick",
    "anti-exe"
]


@tasks.loop(minutes=30)
async def reset_date():
    db.reset()


@bot.event
async def on_ready():
    reset_date.start()
    await bot.change_presence(status=discord.Status.offline)
    for i in cogs:
        bot.load_extension("cogs.%s" % i)
    print(bot.user)


bot.run(con.token)
