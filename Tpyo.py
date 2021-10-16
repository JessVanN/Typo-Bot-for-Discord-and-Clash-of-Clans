import discord
import pandas as pd
import bottokens
from discord.ext import commands
from HelpPaginator import HelpPaginator, CannotPaginate
#import nest_asyncio
#nest_asyncio.apply()

pd.set_option('mode.chained_assignment', None)
pd.set_option('precision',18)
pd.set_option('display.float_format', lambda x: '%18.f' % x)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True, description="TpyoBot developed in python by Jess:8791, Help Server Join Code: SS7QK3W")
bot.remove_command('help')

@bot.command(name='help')
async def help(ctx, *, command: str = None):
    """Shows help about a command or the bot"""
    try:
        if command is None:
            p = await HelpPaginator.from_bot(ctx)
        else:
            entity = bot.get_cog(command)
            if entity is None:
                clean = command.replace('@', '@\u200b')
                return await ctx.send(f'Command or category "{clean}" not found.')
            elif isinstance(entity, commands.Command):
                p = await HelpPaginator.from_command(ctx, entity)
            else:
                p = await HelpPaginator.from_cog(ctx, entity)

        await p.paginate()
    except Exception as e:
        await ctx.send(e)

@bot.group(name='reload', hidden=True, invoke_without_command=True)
async def _reload(ctx, *, module):
    """Reloads a module."""
    try:
        bot.reload_extension(module)
    except commands.ExtensionError as e:
        await ctx.send(f'{e.__class__.__name__}: {e}')
    else:
        await ctx.send('\N{OK HAND SIGN}')


bot.load_extension("generalcog") #1
bot.load_extension("claimcog") #2
bot.load_extension("clanlistcog")#3
bot.load_extension("dbcog")#4
bot.load_extension("Birthdaycog")#5
bot.load_extension("urlcog") #6
bot.load_extension("quotecog")#7
bot.load_extension("movementcog")#8
bot.load_extension("rolecog")#9
bot.load_extension("assigncog")#10
bot.load_extension("cleancog")#11
bot.load_extension("sccwlcog")#12
bot.load_extension("signupcog")#13
#bot.load_extension("unusedcog")

             
bot.run(bottokens.tpyo)

