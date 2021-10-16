import discord
import pandas as pd
import bdGX
from discord.ext import commands
from tabulate import tabulate
import numpy as np

pd.set_option('mode.chained_assignment', None)
pd.set_option('precision',18)
pd.set_option('display.float_format', lambda x: '%18.f' % x)

class clanlist(commands.Cog,name="03. List Clan info"):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(brief="Breakdown of a clan",help= "Returns a breakdown of Members for a specific clan", aliases=['bd'])
    async def breakdown(self, ctx, clanshort):
        #try:
            clanshort=str.upper(clanshort)
            clandict = pd.read_excel("GXclans.xlsx")
            clanlist=clandict[['Shortcut','ID']].set_index("Shortcut")['ID'].to_dict()
            clanlist2=clandict[['Shortcut','Name']].set_index("Shortcut")['Name'].to_dict()
            df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
            df= df.loc[df['STATUS'].isin(['Current'])]
            df= df.loc[df['clan_tag']==(clanlist.get(clanshort))]
            df.sort_values(['TH'], axis=0, ascending=False, inplace=True, na_position='last')
            df=df[['Tag','CurrentName', 'TH']]
            df2=pd.value_counts(df.TH, sort=False).to_frame()
            await ctx.send(f"```{tabulate(df2)}```")
            dfsum=df2['TH'].sum()
            await ctx.send(f"This clan has {dfsum} accounts")
#            embed=discord.Embed(title=clanlist2.get(clanshort), description="Claninfohere", color=0xdccc65)
#            embed.add_field(name="Breakdown", value=f"{tabulate(df2)}", inline=False)
#            embed.set_footer(text="Please use the emojis to scroll forward")
#            msg= await ctx.send(embed=embed)
#            emobegin = '⏮'
#            emoback = '⏪'
#            emoforward = '⏩'
#            emoend = '⏭'
#            # or '\U0001f44d' or '👍'
#            await msg.add_reaction(emobegin)
       #except:
           # await ctx.send("Error: Please type !bd clanshortcut, for example !bd GX")
    
    @commands.command(brief="Breakdown of the whole family",help= "Returns a breakdown of members in all family clans", aliases=['bdf'])
    async def breakdownfam(self, ctx):
        try:
            df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
            df= df.loc[df['STATUS'].isin(['Current'])]
            df.sort_values(['TH'], axis=0, ascending=False, inplace=True, na_position='last')
            df=df[['Tag','clan_name', 'TH']]
            df['TH']=df['TH'].astype('int')
            df2=pd.value_counts(df.TH, sort=False).to_frame()
            await ctx.send(f"```{tabulate(df2)}```")
            dfsum=df2['TH'].sum()
            await ctx.send(f"The family has {dfsum} accounts")
            regrole= pd.read_excel("GXclans.xlsx")
            regclans=regrole[['Name','DiscordRole']].dropna()
            regclans=regclans['Name'].to_list()
            df3=df.groupby(['clan_name','TH']).count()
            df3.reset_index(inplace=True)
            df3=df3[df3['clan_name'].isin(regclans)]
            df3['TH']="TH"+df3['TH'].astype(str)
            df3=df3.pivot(index='clan_name', columns='TH', values='Tag')
            df3.replace(np.nan,0,inplace=True)
            df4=df3[df3.columns[::-1]]
            df4=df4.astype(int)
            df4["Total"]=df4.sum(axis = 1)
            df4=df4[["TH13","TH12","TH11",'Total']]
            df4.reset_index(inplace=True)
            df_lines = [f"{row.Total:<5}:{row.TH13:<2}/{row.TH12:<2}/{row.TH11:<2}  {row.clan_name}" for row in df4.itertuples()]
            df_send = "```\nTotal:13/12/11   Clan\n"
            for line in df_lines:
                new_df_send = f'{df_send}{line}\n'
                if len(new_df_send) > 1997:
                    await ctx.send(f'{df_send}```')
                    df_send = f'```\n'
                else:
                    df_send = new_df_send
            await ctx.send(f'{df_send}```')
            
        except:
            await ctx.send("Error: Please type !bd clanshortcut, for example !bd GX")

    @commands.command(brief="Lists the clans",help= "A list of family clans and tags", aliases=['clan_tags', 'clantags'])
    async def clans(self,ctx):
        clans=pd.read_excel("GXclans.xlsx")
        clans=clans[['Name','ID','Shortcut']]
        await ctx.send(f"```{tabulate(clans)}```")

    @commands.command(brief="List members of a clan at a TH level",help= "Returns TH# accounts currently in the clan: ^listth 13 ShortCut", aliases=["th",'listh'])
    async def listth(self, ctx, clanshort, number):
        number = int(number)
        clandict = pd.read_excel("GXclans.xlsx")
        clanlist=clandict[['Shortcut','ID']].set_index("Shortcut")['ID'].to_dict()
        df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        clanshort=str.upper(clanshort)
        df= df.loc[df['clan_tag']==(clanlist.get(clanshort))]
        df= df.loc[df['STATUS'] == 'Current']
        df.sort_values(['Archer Queen','Barbarian King','Grand Warden'], axis=0, ascending=False, inplace=True, na_position='last')
        df['Grand Warden'].fillna(0, inplace=True)
        df= df.loc[df['TH'] == number]
        df=df[['TH', 'heroes','CurrentName', 'Tag']]
        if df.empty:
            await ctx.send("No members have that TH level currently, please enter only a number between 3 and 13")
        else:
            dfsend= "```" + tabulate(df, headers="keys",showindex="never") + "```"
            await ctx.send(dfsend)


    @commands.command(brief="List members of a clan",help= "list of discord members and their clash accounts in the specific clan", aliases=['mem'])
    async def members(self, ctx, clanshort):
        clanshort=str.upper(clanshort)
        clandict = pd.read_excel("GXclans.xlsx")
        clanlist=clandict[['Shortcut','ID']].set_index("Shortcut")['ID'].to_dict()
        df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        df2=df[df.STATUS=="Current"]
        df2= df2.loc[df['clan_tag']==(clanlist.get(clanshort))]
        df2=df2[["DiscordID","CurrentName", "TH"]]
        df2.reset_index(drop=True,inplace=True)
        guildnow=ctx.guild
        df2["DiscordName"]= df2.apply(lambda x:bdGX.altsname(x, guildnow, ctx), axis=1)
        df2.sort_values(['DiscordName', "TH"], axis=0, ascending=[True,False], inplace=True, na_position='last')
        df3=df2[["DiscordName","CurrentName", "TH"]]
        df3["count"]=df3.groupby(['DiscordName']).cumcount()+1
        df3["DiscordName"]= df3.apply(lambda x: bdGX.removenames(x), axis=1)
        df3["DiscordName"]=df3["DiscordName"].astype(str).str[0:15]
        df3=df3[["DiscordName","CurrentName","TH"]]
        df3=df3.rename(columns={"CurrentName":"InGameAccount"})
        df_lines = [f'{row.DiscordName:<16} {str(row.TH)[0:2]:<3} {row.InGameAccount:<10} ' for row in df3.itertuples()]
        df_send = "```\nDiscordName         InGameAccounts\n"
        for line in df_lines:
            new_df_send = f'{df_send}{line}\n'
            if len(new_df_send) > 1997:
                await ctx.send(f'{df_send}```')
                df_send = f'```\n'
            else:
                df_send = new_df_send
        await ctx.send(f'{df_send}```')
        

    @commands.command(brief="Breakdown of a clan",help= "Returns a breakdown of Members for a specific clan", aliases=['inthewrongclan','notwhereyoubelong'])
    async def gohome(self, ctx, clanshort):
        clanshort=str.upper(clanshort)
        clandict = pd.read_excel("GXclans.xlsx")
        clandict=clandict[clandict['Shortcut']==clanshort]
        shorts=clandict['Shortcut'].to_list()
        cid=clandict['ID'].to_list()
        df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        dfa=df[df['clan_tag'].isin(cid)]
        dfb=df[df['AssgnClan'].isin(shorts)]   
        df=dfa.append(dfb)
        for index, row in df.iterrows():
            if row['clan_tag'] in cid:
                if row['AssgnClan'] not in shorts:
                    df.loc[index,'keep']=1
            elif row['clan_tag'] not in cid:
                if row['AssgnClan'] in shorts:
                    df.loc[index,'keep']=1
            else:
                df.loc[index,'keep']=2
        df=df[df['keep']==1]
        df.sort_values(["keep",'CurrentName'], axis=0, inplace=True)
        df=df[['Tag',"CurrentName",'TH','clan_name','AssgnClan']]
        df_lines = [f'{row.TH:<3}{row.clan_name:<15} {row.AssgnClan:<5}{row.CurrentName:<16} ' for row in df.itertuples()]
        df_send = "```\nTH InClan / AssignClan  Name\n"
        for line in df_lines:
            new_df_send = f'{df_send}{line}\n'
            if len(new_df_send) > 1997:
                await ctx.send(f'{df_send}```')
                df_send = f'```\n'
            else:
                df_send = new_df_send
        await ctx.send(f'{df_send}```')

        
    @commands.command(brief="Lists all current members in the family",help= "List of discord members and their clash accounts in the the entire family", aliases=['memfam','family'])
    async def membersfam(self, ctx):
        df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        df2=df[df.STATUS.isin(["Current"])]
        df2=df2[["DiscordID","CurrentName", "TH"]]
        df2.reset_index(drop=True,inplace=True)
        guildnow=ctx.guild
        df2["DiscordName"]= df2.apply(lambda x:bdGX.altsname(x, guildnow, ctx), axis=1)
        df2.sort_values(['DiscordName', "TH"], axis=0, ascending=[True,False], inplace=True, na_position='last')
        df3=df2[["DiscordName","CurrentName", "TH"]]
        df3["count"]=df3.groupby(['DiscordName']).cumcount()+1
        df3["DiscordName"]= df3.apply(lambda x: bdGX.removenames(x), axis=1)
        df3["DiscordName"]=df3["DiscordName"].astype(str).str[0:15]
        df3=df3[["DiscordName","CurrentName","TH"]]
        df3=df3.rename(columns={"CurrentName":"InGameAccount"})
        df_lines = [f'{row.DiscordName:<16} {str(row.TH)[0:2]:<3} {row.InGameAccount:<10} ' for row in df3.itertuples()]
        df_send = "```\nDiscordName         InGameAccounts\n"
        for line in df_lines:
            new_df_send = f'{df_send}{line}\n'
            if len(new_df_send) > 1997:
                await ctx.send(f'{df_send}```')
                df_send = f'```\n'
            else:
                df_send = new_df_send
        await ctx.send(f'{df_send}```')


    @commands.command(brief="Tags of accounts in a clan",help= "Returns a list of tags for all current members of the clan listed")
    async def tags(self, ctx, clanshort):
        try:
            clanshort=str.upper(clanshort)
            df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
            clandict = pd.read_excel("GXclans.xlsx")
            clanlist=clandict[['Shortcut','ID']].set_index("Shortcut")['ID'].to_dict()
            df= df.loc[df['clan_tag']==(clanlist.get(clanshort))]
            df= df.loc[df['STATUS'] == 'Current']
            df.sort_values(['CurrentName'], axis=0, ascending=True, inplace=True, na_position='last')
            df=df[['Tag', 'CurrentName']]
            df_lines = [f'{row.Tag:<10} {row.CurrentName}' for row in df.itertuples()]
            df_send = "```\nTag        Name\n"
            for line in df_lines:
                new_df_send = f'{df_send}{line}\n'
                if len(new_df_send) > 1997:
                    await ctx.send(f'{df_send}```')
                    df_send = f'```\n'
                else:
                    df_send = new_df_send
            await ctx.send(f'{df_send}```')
        except:
            await ctx.send('Please type !tag GX or !tag someclanshortcut, to get a list of shortcuts type !clantags') 
        

    @commands.command(brief="First ever join date of all members in a Clan",help= "Returns first join date of all accounts currently in the clan listed")
    async def tenure(self, ctx, clanshort):
        try:
            clanshort=str.upper(clanshort)
            df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
            df= df.loc[df['STATUS'] == 'Current']
            clandict = pd.read_excel("GXclans.xlsx")
            clanlist=clandict[['Shortcut','ID']].set_index("Shortcut")['ID'].to_dict()
            df= df.loc[df['clan_tag']==(clanlist.get(clanshort))]
            df.sort_values(['FirstDate'], axis=0, ascending=True, inplace=True, na_position='last')
            df=df[['FirstDate', 'Tag', 'CurrentName']]
            df['FirstDate']=df['FirstDate'].astype('str')
            df_lines = [f'{row.FirstDate:<10}  {row.Tag:<10}  {row.CurrentName}' for row in df.itertuples()]
            df_send = "```\nJoinDate    Tag         Name\n"
            for line in df_lines:
                new_df_send = f'{df_send}{line}\n'
                if len(new_df_send) > 1997:
                    await ctx.send(f'{df_send}```')
                    df_send = f'```\n'
                else:
                    df_send = new_df_send
            await ctx.send(f'{df_send}```')
        except:
            await ctx.send('Please type !tenure GX or !tenure some clan shortcut, to get a list of shortcuts type !clantags')
        
def setup(bot):
    bot.add_cog(clanlist(bot))               