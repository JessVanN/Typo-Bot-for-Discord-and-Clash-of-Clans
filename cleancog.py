import discord
import pandas as pd
from discord.ext import commands
from datetime import date, timedelta, datetime
import bdGX


pd.set_option('mode.chained_assignment', None)
pd.set_option('precision',18)
pd.set_option('display.float_format', lambda x: '%18.f' % x)

class cleanclan(commands.Cog,name="11. Clean Up Members"):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(brief='Clash account with no owner in discord',help='List all of the current in game member not linked to an in server discord account', aliases=['discordcleanup'])
    @commands.has_role("Clan Leaders")
    async def notindiscord(self, ctx):
        df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        df2=df[df.STATUS=="Current"]
        df2=df2[["DiscordID","CurrentName", "Tag",'TH','clan_name']]
        df2.reset_index(drop=True,inplace=True)
        guildnow=ctx.guild
        df2["DiscordName"]= df2.apply(lambda x:bdGX.altsname(x, guildnow, ctx), axis=1)
        df2.sort_values(['TH'], axis=0, ascending=False, inplace=True, na_position='last')
        df2.sort_values(['DiscordName'], axis=0, ascending=True, inplace=True, na_position='last')
        df3=df2[["DiscordName","CurrentName",'Tag','clan_name']]
        df3=df3.rename(columns={"CurrentName":"InGameAccount"})
        df4=df3.loc[df3["DiscordName"].isin([" ID-NotInServer", " NotAssigned"])]
        #dfsend=tabulate(df4,  headers="keys",showindex="never")
        await ctx.send(f"The followng is a list of clash accounts that have either not been linked to a discord act or the discord account is not in the server")
        #await ctx.send(f"```{dfsend}```")
        df_lines = [f'{row.Tag:<10} {row.InGameAccount} {row.clan_name}' for row in df4.itertuples()]
        df_send = "```\nTag        Name\n"
        for line in df_lines:
            new_df_send = f'{df_send}{line}\n'
            if len(new_df_send) > 1997:
                await ctx.send(f'{df_send}```')
                df_send = f'```\n'
            else:
                df_send = new_df_send
        await ctx.send(f'{df_send}```')
    
    @commands.command(brief='Discord accounts with no one in clan',help='List all of the discords accounts with the member role who do not have an account in game for 10 days')
    @commands.has_role("Clan Leaders")
    async def notinclan(self, ctx):
        df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        df=df[~df.Tag.isin(["#123abc12"])]
        df=df[df.DiscordID.astype('int64') >1]
        df.sort_values(["LastDate"], axis=0, ascending=False, inplace=True, na_position='last')
        df.sort_values(['DiscordID',"STATUS"], axis=0, ascending=True, inplace=True, na_position='last')
        df2=df[["DiscordID","CurrentName","TH","STATUS","LastDate"]]
        df2.drop_duplicates('DiscordID',keep='first',inplace=True)
        df2=df2[~df2.STATUS.isin(["Current"])]
        df2["test"]=df["LastDate"]+timedelta(days=10)
        df3=df2[df2['test']<=datetime.now()]
        guildnow=ctx.guild
        df3.reset_index(drop=True,inplace=True)
        df3["DiscordName"]= df3.apply(lambda x:bdGX.altsname(x, guildnow, ctx), axis=1)
        df3=df3.loc[df3["DiscordName"]!=" ID-NotInServer"]
        await ctx.send(f"The followng is a list of discord clash members but the account has been out of clans for more than 10 days.")
        for index, row in df3.iterrows():
            member= ctx.message.guild.get_member(int(row.DiscordID))
            role = discord.utils.find(lambda r: r.name == 'Clash of Clans', ctx.message.guild.roles)
            role2 = discord.utils.find(lambda r: r.name == 'Safe Guest', ctx.message.guild.roles)
            if role in member.roles:
                if role2 not in member.roles:
                    await ctx.send(f"```{row.DiscordName} with clash account {row.CurrentName} last seen {row.LastDate}```")
                else:
                    pass
            else:
                pass
        await ctx.send(f"The followng is a list of discord clash members not linked to any account in the database. i.e. old members who left or need linked")
        dflist=df["DiscordID"]
        dflist=dflist.values.tolist()
        for member in ctx.guild.members:
            if str(member.id) in dflist:
                pass
            else:
                role = discord.utils.find(lambda r: r.name == 'Clash of Clans', ctx.guild.roles)
                role2 = discord.utils.find(lambda r: r.name == 'Safe Guest', ctx.guild.roles)
                if role in member.roles:
                    if role2 not in member.roles:
                        await ctx.send(f"{member.display_name}")
                    else:
                        pass
        
    @commands.command(brief='For CJ base server',help='For the base server which discord members are not longer in the family' )
    @commands.has_permissions(administrator=True)
    async def basenotinclan(self, ctx):
        df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        df=df[~df.Tag.isin(["#123abc12"])]
        df=df[df.DiscordID.astype('int64') >1]
        df.sort_values(["LastDate"], axis=0, ascending=False, inplace=True, na_position='last')
        df.sort_values(['DiscordID',"STATUS"], axis=0, ascending=True, inplace=True, na_position='last')
        df2=df[["DiscordID","CurrentName","TH","STATUS","LastDate"]]
        df2.drop_duplicates('DiscordID',keep='first',inplace=True)
        df2=df2[~df2.STATUS.isin(["Current"])]
        df2["test"]=df["LastDate"]+timedelta(days=10)
        df3=df2[df2['test']<=datetime.now()]
        guildnow=ctx.guild
        df3.reset_index(drop=True,inplace=True)
        df3["DiscordName"]= df3.apply(lambda x:bdGX.altsname(x, guildnow, ctx), axis=1)
        df3=df3.loc[df3["DiscordName"]!=" ID-NotInServer"]
        await ctx.send(f"The followng is a list of discord clash members but the account has been out of clans for more than 10 days.")
        for index, row in df3.iterrows():
            member= ctx.message.guild.get_member(int(row.DiscordID))
            await ctx.send(f"```{member.display_name} with clash account {row.CurrentName} last seen {row.LastDate}```")
        df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        df=df[~df.Tag.isin(["#123abc12"])]
        df=df[df.DiscordID.astype('int64') >1]
        df.sort_values(["LastDate"], axis=0, ascending=False, inplace=True, na_position='last')
        df.sort_values(['DiscordID',"STATUS"], axis=0, ascending=True, inplace=True, na_position='last')
        dflist=df["DiscordID"]
        dflist=dflist.values.tolist()
        for member in ctx.guild.members:
            if str(member.id) in dflist:
                pass
            else:
                await ctx.send(f"{member.display_name} not linked to any account in the database")
        await ctx.send("Done")    
        
def setup(bot):
    bot.add_cog(cleanclan(bot))               