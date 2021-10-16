import gspread
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g
import discord
import pandas as pd
from discord.ext import commands
from datetime import date, timedelta, datetime
from tabulate import tabulate
import bdGX

pd.set_option('mode.chained_assignment', None)
pd.set_option('precision',18)
pd.set_option('display.float_format', lambda x: '%18.f' % x)

class db(commands.Cog,name="04. DataBase Commands"):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(brief='List all in Database by Status',help= "Get a list of all members in the database with a specific status (VERY LONG) !status Current/Kicked/Gone")
    @commands.has_role("Co-Leader")
    async def dbstatus(self, ctx, user_text:str):
        df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        df= df.loc[df['STATUS'] == user_text]
        df.sort_values(['LastDate','FirstDate'], axis=0, ascending=False, inplace=True, na_position='last') ###
        df=df[['Tag', 'CurrentName']]
        df_lines = [f'{row.Tag:<10} {row.CurrentName}' for row in df.itertuples()]
        df_send = "```\n"
        for line in df_lines:
            new_df_send = f'{df_send}{line}\n'
            if len(new_df_send) > 1997:
                await ctx.send(f'{df_send}```')
                df_send = f'```\n'
            else:
                df_send = new_df_send
        await ctx.send(f'{df_send}```')
 
#    @commands.command(brief='List all ever Kicked',help= "Returns list of all kicked", aliases=['kickedlist'])
#    @commands.has_role("CG War Clan Leadership")
#    async def kicked(self, ctx):
#        df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
#        df= df.loc[df['STATUS'].isin(['Kicked'])]
#        df.sort_values(['LastDate'], axis=0, ascending=False, inplace=True, na_position='last')
#        df=df[['Tag','CurrentName', 'LastDate']]
#        df['LastDate']=df['LastDate'].astype('str')
#        df_lines = [f'{row.Tag:<12} {row.LastDate:<12} {row.CurrentName}' for row in df.itertuples()]
#        df_send = "```\nTag          LeaveDate    Name\n"
#        for line in df_lines:
#            new_df_send = f'{df_send}{line}\n'
#            if len(new_df_send) > 1997:
#                await ctx.send(f'{df_send}```')
#                df_send = f'```\n'
#            else:
#                df_send = new_df_send
#        await ctx.send(f'{df_send}```')
    
    
    @commands.command(brief='Lookup a tag in the database',help= "Lookup a tag in database", aliases=['player_info','pch'])
    async def lookup(self, ctx, *, user_text: str):
        tag= bdGX.fix_bottag(user_text)
        df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        df= df.loc[df['Tag'].isin([tag])]
        df2=df[["Tag","CurrentName","PreviousName","FirstDate","LastDate","STATUS","IsElder","ReadRules","clan_name","clan_tag","role","TH","townHallWeaponLevel","heroes","AssgnClan",'DOB']]
        df2=df2.transpose()
        member= ctx.message.guild.get_member(int(df.DiscordID))
        dfnote=list(df['Note'])
        if df2.empty:
            await ctx.send("Cannot find that tag")
        else:
            dfsend= "```" + tabulate(df2, headers="keys") + "```"
            await ctx.send(dfsend)
            try:
                await ctx.send (f"This account is owned by discord user {member.display_name}")
            except:
                pass
            try:           
                await ctx.send (f"This account has the note: {dfnote}")
            except:
                pass          


    @commands.command(brief="Search accounts",help="Search for accounts with the charaters you entered appearing in the name...",aliases=["search"])
    async def find(self,ctx, text):
        df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        df=df.dropna(subset=["CurrentName"])
        df3=df[df['CurrentName'].str.contains(text,case=False)]
        df3.sort_values(['TH'], axis=0, ascending=False, inplace=True, na_position='last') 
        df3.reset_index(inplace=True, drop=True)
        df3.index += 1 
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        if not df3.empty:
            df4=df3[["CurrentName", "TH", "Tag"]]
            dfsend=tabulate(df4,  headers="keys")
            await ctx.send(f"```{dfsend}```")
#            await ctx.send(f"{ctx.author.mention} Please type the number (not the tag) of the account you want to lookup")
#            msg = await self.bot.wait_for('message', check=check, timeout=60.0)
#            df5=df3.loc[int(msg.content)]
#            print(df5)
#            member= ctx.message.guild.get_member(int(df5.DiscordID))
#            df5=df5[["Tag","CurrentName","PreviousName","FirstDate","LastDate","STATUS","IsElder","ReadRules","clan_name","clan_tag","role","TH","townHallWeaponLevel","heroes","AssgnClan",'DOB']]
#            df5["FirstDate"]=pd.to_datetime(df5["FirstDate"])
#            df5["LastDate"]=pd.to_datetime(df5["LastDate"])
#            df5=df5.transpose()
#            dfsend= "```" + tabulate(df5, headers="keys") + "```"
#            await ctx.send(dfsend)
#            try:
#                member= ctx.message.guild.get_member(int(df5.DiscordID))
#                await ctx.send (f"This account is owned by discord user {member.display_name}")
#            except:
#                pass
#            try:      
#                dfnote=list(df5['Note'])
#                await ctx.send (f"This account has the note: {dfnote}")
#            except:
#                pass          
        else:
            await ctx.send("Error: no associated accounts, try search for a a word with no spaces")
            
    
    
    @commands.command(brief='Lookup notes on a clashtag',help= "Lookup a note by a single player tag (leadership only)", aliases=['note'])
    @commands.has_role("Co-Leader")
    async def notes(self, ctx, *, user_text: str):
        tag=bdGX.fix_bottag(user_text)
        df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        df= df.loc[df['Tag'].isin([tag])]
        if df.empty:
            await ctx.send("Cannot find that tag")
        else:
            print1= "Here is the note for for :" + df['Tag']+' '+df['CurrentName']
            df2=list(df['Note'])
            await ctx.send(print1)
            await ctx.send(df2)

def setup(bot):
    bot.add_cog(db(bot))               