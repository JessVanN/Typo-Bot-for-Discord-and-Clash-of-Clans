import discord
import pandas as pd
from discord.ext import commands
import bdGX
import BotStringsGX
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g

pd.set_option('mode.chained_assignment', None)
pd.set_option('precision',18)
pd.set_option('display.float_format', lambda x: '%18.f' % x)

class urllinks(commands.Cog,name="06. Links and URLs"):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(brief="List servers of interest",help= "returns instructions on how to use WarMatch", aliases=['server','serverlinks'])
    async def servers(self, ctx):
        bot_text = BotStringsGX.Server_text
        await ctx.send(bot_text)

    @commands.command(brief="Invite to GX",help= "returns an invite link to the current server")
    async def invite(self, ctx):
        await ctx.send('https://discord.gg/dAT8964')

    @commands.command(brief="Get link to clash account",help= "provide a tag and return link to in-game profile", aliases=['clash_link', 'clash'])
    async def clashlink(self, ctx, user_text:str):
        tag= bdGX.fix_clashtag(user_text)
        bot_text = 'https://link.clashofclans.com/?action=OpenPlayerProfile&tag='+tag
        await ctx.send(bot_text)
        
    @commands.command(brief="Get link to a clan",help= "provide a tag and return link to in-game profile", aliases=['clan_link','clanlinks', 'link','links','cl'])
    async def clanlink(self, ctx, user_text:str):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
                 'credentials.json', scope) # Your json file here
        gc = gspread.authorize(credentials)
        wks = gc.open_by_key("1qoD-cZQffOVBwJdNYTD868nEsknyphksKBLzEhhIueo").worksheet("Clans")
        data = wks.get_all_values()
        headers = data.pop(0)
        clandict = pd.DataFrame(data, columns=headers)
        clanlist=clandict[['Shortcut','ID']].set_index("Shortcut")['ID'].to_dict()
        clantag=clanlist.get(str.upper(user_text))
        bot_text = 'https://link.clashofclans.com/?action=OpenClanProfile&tag='+clantag[1:]
        await ctx.send(bot_text)
    
    @commands.command(brief="Get link to clash of state for an account",help= "Provide a tag and return link to ClashofStats", aliases=['clashofstats','coslink','cos'])
    async def clashofstatslink(self, ctx, user_text:str):
        tag= bdGX.fix_bottag(user_text)[1:]
        bot_text = 'https://www.clashofstats.com/players/'+tag+'/history/'
        await ctx.send(bot_text)

    @commands.command(brief="Tweet Tweet",help= "Twitter links")
    async def twitter(self, ctx):
        bot_text =  """https://twitter.com/GoldenXcoc"""
        await ctx.send(bot_text)

def setup(bot):
    bot.add_cog(urllinks(bot))               