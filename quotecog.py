import discord
import pandas as pd
from discord.ext import commands
import random
import typing
from tabulate import tabulate


pd.set_option('mode.chained_assignment', None)
pd.set_option('precision',18)
pd.set_option('display.float_format', lambda x: '%18.f' % x)

class quote(commands.Cog,name="07. Custom Quotes"):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(brief="Get a random quote for a @tag or word",help="Selects a random quote from all available for Tagged player or phrase",)
    async def quote(self, ctx, what: typing.Union[discord.Member, str]):
        df = pd.read_excel("CustomQuotes.xlsx")
        df=df[df.guildid.astype(str)==(str(ctx.guild.id))]
        try:
            if type(what)==discord.member.Member:
                df2=df.loc[df.DiscordID.astype(str)==(str(what.id))]
                df3=df2['Quote'].tolist()
                await ctx.send(random.choice(df3))
            if type(what)==str:
                df2=df.loc[df.DiscordID.astype(str)==(str(what))]
                df3=df2['Quote'].tolist()
                await ctx.send(random.choice(df3))
        except:
            await ctx.send("That didn't work, the person or text you entered has no quotes")   
    
    @commands.command(brief="Program a new quote",help="Add a quote for a @discordtag or one word phrase followed by the text quote", aliases=['NewQuote'])
    async def addquote(self, ctx, what: typing.Union[discord.Member, str], *, quotetext:str):
        df = pd.read_excel("CustomQuotes.xlsx")
        df=df[["guildid","WhoNotes","DiscordID","Quote"]]
        try:
            if type(what)==discord.member.Member:
                new= pd.DataFrame({"guildid":str(ctx.guild.id), 
                            "DiscordID":str(what.id),
                            "Quote":quotetext}, index=[0])
            elif type(what)==str:
                new= pd.DataFrame({"guildid":str(ctx.guild.id), 
                            "DiscordID":str(what),
                            "Quote":quotetext}, index=[0])
            df["guildid"]=df["guildid"].astype(str)
            df2=df.append(new)
            df2.reset_index(drop=True,inplace=True)
            df2.to_excel("CustomQuotes.xlsx")
            await ctx.send(f"Success added {new}")
        except:
            await ctx.send("Error:The required arguement is ^addquote @tagmember/OrTypeAWord then quotable phrase here")
            
    @commands.command(brief="List all quote for a @tag or word",help="List all quotes a member has", aliases=['ListQuotes'])
    async def listquote(self, ctx, what: typing.Union[discord.Member, str]=None):
        if what==None:
            df = pd.read_excel("CustomQuotes.xlsx")
            df=df.sort_values(["DiscordID"])
            df=df['DiscordID'].tolist()
            dfsend=[]
            for item in df:
                try:
                    name=f"@ {ctx.guild.get_member(int(item)).display_name}"
                    dfsend.append(name)
                except:
                    dfsend.append(item)
            dfsend2=pd.DataFrame(dfsend,columns=["Options"])
            dfsend2.drop_duplicates(subset="Options",inplace=True)
            await ctx.send(tabulate(dfsend2))
        else:
            df = pd.read_excel("CustomQuotes.xlsx")
            df=df[df.guildid.astype(str)==(str(ctx.guild.id))]
            try:
                if type(what)==discord.member.Member:
                    df2=df.loc[df.DiscordID.astype(str)==(str(what.id))]
                    df2=df2[['Quote']]
                    await ctx.send(df2)
                elif type(what)==str:
                    df2=df.loc[df.DiscordID.astype(str)==(str(what))]
                    df2=df2[['Quote']]
                    await ctx.send(df2)
            except:
                await ctx.send("That didn't work, the person or text you entered has no quotes")   
    
#    @commands.command( aliases=['DeleteQuote'])
#    @commands.has_permissions(administrator=True)
#    async def deletequote(self, ctx, what: typing.Union[discord.Member, str], integer:int):
#        df = pd.read_excel("CustomQuotes.xlsx")
#        df=df[["guildid","WhoNotes","DiscordID","Quote"]]
#        try:
#            if type(what)==discord.member.Member:
#                cond1=~df.DiscordID.astype(str).isin([str(what.id)])
#                cond2=df.index!=integer
#                df=df[ cond1 & cond2 ]  
#                df2=df[df.DiscordID.astype(str).isin([str(what.id)])]
#                df.to_excel("CustomQuotes.xlsx")
#                if df2.empty:
#                    await ctx.send(f"No remaining quotes for this Player")
#                else:
#                    await ctx.send(f"remaining quotes for this text are")
#                    await ctx.send(df2)
#            elif type(what)==str:
#                cond1=~df.DiscordID.astype(str).isin([str(what)])
#                cond2=df.index!=integer
#                df=df[ cond1 & cond2 ]  
#                df2=df[df.DiscordID.astype(str).isin([str(what)])]
#                df.to_excel("CustomQuotes.xlsx")
#                if df2.empty:
#                    await ctx.send(f"No remaining quotes for this text")
#                else:
#                    await ctx.send(f"remaining quotes for this text are")
#                    await ctx.send(df2)
#        except:
#            await ctx.send("That didn't work, type ^deletequote Text 1, the number is the number that appears in ^listquoutes text") 
            
def setup(bot):
    bot.add_cog(quote(bot))               