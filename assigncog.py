import gspread
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g
import discord
import pandas as pd
import numpy as np
import bdGX
import asyncio
from discord.ext import commands
from tabulate import tabulate
from datetime import date, timedelta, datetime

pd.set_option('mode.chained_assignment', None)
pd.set_option('precision',18)
pd.set_option('display.float_format', lambda x: '%18.f' % x)

class assign(commands.Cog,name="10. Assign Home Clans"):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(brief='Assign a member to a home clan',help="To assign a clash account to their home clan, type assign clanshortcut #clashtag, alternatively instead of a shortcut you can assign to GONE/KICK/FAIL",aliases=['assign_clan','assignto','assign_to'])
    @commands.has_role("Co-Leader")
    async def assignclan(self,ctx, clan, clashtag):
        try:
            tag=bdGX.fix_bottag(clashtag)
            df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
            clandict = pd.read_excel("GXclans.xlsx")
            shortcuts=clandict['Shortcut'].values.tolist()
            df.set_index("Tag", inplace=True)
            if str.upper(clan) in shortcuts:
                df.at[tag,"AssgnClan"]=str.upper(clan)
                df.to_excel("MemberDatabase GX tpyo.xlsx")
                df2= df.loc[tag]
                df2=df2[['CurrentName',"AssgnClan"]]
                await ctx.send(f"{df2.CurrentName} is now assigned to {clan}")
                regroles=clandict[['Shortcut','DiscordRole']].dropna().set_index("Shortcut")['DiscordRole'].to_dict()
                roleassign=regroles.get(str.upper(clan))
                try:
                    dfmem= df.loc[df.index.isin([tag])]
                    member= ctx.message.guild.get_member(int(dfmem.DiscordID))
                    role = discord.utils.get(ctx.message.guild.roles, name=roleassign)
                    if roleassign:
                        await member.add_roles(role)
                        await ctx.send(f"{roleassign} added for {member.name} ")
                except Exception as ex:
                    await ctx.send(ex)
                    await ctx.send(f"Role add for this clan failed, please manually give them the clan role")
            elif str.upper(clan) in ['GONE','KICK','FAIL']:
                df.at[tag,"AssgnClan"]=str.upper(clan)
                df.to_excel("MemberDatabase GX tpyo.xlsx")
                df2= df.loc[tag]
                df2=df2[['CurrentName',"AssgnClan"]]
                await ctx.send(f"{df2.CurrentName} is now assigned to {df2.AssgnClan}")
            else: 
                await ctx.send ("Please use a shortcut for one of the 8 main clans")
        except:
            await ctx.send ("please type ^assignto clan #clashtag, or instead of a clan they can be set to gone, kick, or fail")
    
    @commands.command(brief="List everyone assigned to a clan",help="To list the clash accounts assign to a clan type ^assigned clanshortcut",aliases=['home','HomeClan'])
    async def assigned(self,ctx, clan):
        df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        df2=df[df["AssgnClan"]==str.upper(clan)]
        df2=df2[['Tag','STATUS','CurrentName','LastDate']]
        df2['LastDate']=df2['LastDate'].dt.strftime('%Y-%m-%d').astype(str)
        df2.sort_values(['LastDate','CurrentName'], axis=0, inplace=True, na_position='last') 
        await ctx.send(f"The following accounts are assigned to {str.upper(clan)}")
        df_lines = [f"{row.Tag:<10} {row.LastDate:<10} {row.CurrentName}" for row in df2.itertuples()]
        df_send = "```\nTag        Lastdate   CurrentName\n"
        for line in df_lines:
            new_df_send = f'{df_send}{line}\n'
            if len(new_df_send) > 1997:
                await ctx.send(f'{df_send}```')
                df_send = f'```\n'
            else:
                df_send = new_df_send
        await ctx.send(f'{df_send}```')

    @commands.command(brief='Breakdown of assignments', description='Breakdown of how many people assign to each clan', aliases=['assbd'])
    async def assignbreakdown(self, ctx):
            df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
            df= df.loc[~df['AssgnClan'].isnull()]
            df.sort_values(['TH'], axis=0, ascending=True, inplace=True, na_position='last')
            df=df[['Tag','AssgnClan', 'TH']]
            df['TH']=df['TH'].astype('int')
            df2=pd.value_counts(df.TH, sort=False).to_frame()
            await ctx.send(f"```{tabulate(df2)}```")
            regrole= pd.read_excel("GXclans.xlsx")
            regclans=regrole['Shortcut'].to_list()
            df3=df.groupby(['AssgnClan','TH']).count()
            df3.reset_index(inplace=True)
            df3=df3[df3['AssgnClan'].isin(regclans)]
            df3['TH']="TH"+df3['TH'].astype(str)
            df3=df3.pivot(index='AssgnClan', columns='TH', values='Tag')
            df3.replace(np.nan,0,inplace=True)
            df4=df3[df3.columns[::-1]]
            df4=df4.astype(int)
            df4["Total"]=df4.sum(axis = 1)
            df4=df4[["TH13","TH12","TH11","TH10",'Total']]
            df4.reset_index(inplace=True)
            df_lines = [f"{row.Total:<5}:{row.TH13:<2}/{row.TH12:<2}/{row.TH11:<2}/{row.TH10:<2} {row.AssgnClan}" for row in df4.itertuples()]
            df_send = "```\nTotal:13/12/11/10   Clan\n"
            for line in df_lines:
                new_df_send = f'{df_send}{line}\n'
                if len(new_df_send) > 1997:
                    await ctx.send(f'{df_send}```')
                    df_send = f'```\n'
                else:
                    df_send = new_df_send
            await ctx.send(f'{df_send}```')

    #https://medium.com/@vince.shields913/reading-google-sheets-into-a-pandas-dataframe-with-gspread-and-oauth2-375b932be7bf
    @commands.command(brief="db to google for the assigned clansheets",help="Downloads the database for each clan to the assigned clan sheet")
    @commands.has_role("Co-Leader")
    async def loadclans(self, ctx):
        #try:
            scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                     'credentials.json', scope) # Your json file here
            gc = gspread.authorize(credentials)
            #updateclanlist
            wks = gc.open_by_key("1qoD-cZQffOVBwJdNYTD868nEsknyphksKBLzEhhIueo").worksheet("Clans")
            data = wks.get_all_values()
            headers = data.pop(0)
            clandict = pd.DataFrame(data, columns=headers)
            clandict=clandict[clandict['Active']=='Yes']
            clandict.to_excel("GXclans.xlsx")
            await ctx.send("Clans List Imported")        
    
            clans= pd.read_excel("GXclans.xlsx")
            clandict=clans[['Shortcut','Name',"DiscordRole"]].dropna().set_index("Shortcut")['Name'].to_dict()
            clanlist=clans[['Shortcut','Name',"DiscordRole"]].dropna()
            clanlist=clanlist['Shortcut'].to_list()
            
            clanlist2=clans[['Shortcut','Name',"DiscordRole"]].dropna()
            clanlist2=clanlist2['Name'].to_list()
            clanlist2.append('Unassigned Current Members')
            
            df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
            dfupdate= pd.DataFrame()
            for item in clanlist2:
                wks = gc.open_by_key("1qoD-cZQffOVBwJdNYTD868nEsknyphksKBLzEhhIueo").worksheet(item)
                data = wks.get_all_values()
                headers = data.pop(0)
                try:
                    clandata = pd.DataFrame(data, columns=headers)
                    df2=clandata[['Tag','Change']]
                    dfupdate=dfupdate.append(df2)
                except:
                    await ctx.send(f"{item} failed")
                
           # await ctx.send(f"Google sheet imported successfully")
            
            dfupdate=dfupdate.loc[dfupdate['Change']!='no change']
            dfupdate['Change'] = dfupdate['Change'].apply(lambda x: '' if x == "unknown" else x)
            dfupdate.loc[dfupdate['Change']=='unknown']=" "
            dfupdate['AssgnClan']=dfupdate['Change'].str.upper().str.strip()
            df.set_index("Tag", inplace=True)
            dfupdate.set_index("Tag", inplace=True)
            dfupdate=dfupdate[['AssgnClan']]
            df.update(dfupdate)
            df.to_excel('MemberDatabase GX tpyo.xlsx')
            await ctx.send("Clan assignments have been updated from the change column in the google sheet. The next set of update have a 10 second delay between each requests Please be patient")
            
            df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
            df=df[['Tag','CurrentName','DiscordID','FirstDate','LastDate','STATUS','clan_name','TH','heroes','AssgnClan']]
            df['Change']="no change"
            df.sort_values(["CurrentName","STATUS",'LastDate','FirstDate'], axis=0, inplace=True, na_position='last')
            #df.set_index("Tag", inplace=True)
            spreadsheet_key = "1qoD-cZQffOVBwJdNYTD868nEsknyphksKBLzEhhIueo" #ID for Master Roster Sheet
            for item in clanlist:
                df2=df[df['AssgnClan']==str(item)]
                wks_name = clandict.get(str.upper(item)) #change this for each table
                d2g.upload(df2, spreadsheet_key, wks_name, credentials=credentials, row_names=False)#df is the pandas table you are sending, wqill overright the entire previsous upload
                await ctx.send(f"DataBase Exported for {wks_name}")
                # await asyncio.sleep(10)
#https://github.com/maybelinot/df2gspread/issues/34         
            df3=df[df['AssgnClan'].isna()]
            df3=df3[df3['STATUS']=='Current']
            df4=df[~df['AssgnClan'].isna()]
            df4=df4[df4['AssgnClan'].str.contains('GONE|FAIL|KICK')]
            df4=df4[df4['STATUS']=='Current']
            df3=df3.append(df4)
            wks_name = 'Unassigned Current Members' #change this for each table
            d2g.upload(df3, spreadsheet_key, wks_name, credentials=credentials, row_names=False)  #df is the pandas table you are sending, wqill overright the entire previsous upload
            await ctx.send(f"DataBase Exported for {wks_name}")  
            # await asyncio.sleep(10)
            
#            df4=df[~df['AssgnClan'].isna()]
#            df4=df4[df4['AssgnClan'].str.contains('GONE|FAIL|KICK')]
#            wks_name = 'Gone/Kicked/Failed' #change this for each table
#            d2g.upload(df4, spreadsheet_key, wks_name, credentials=credentials, row_names=False)  #df is the pandas table you are sending, wqill overright the entire previsous upload
#            await ctx.send(f"DataBase Exported for {wks_name}")  
#        except Exception as ex:
#            await ctx.send(ex)

##    #https://medium.com/@vince.shields913/reading-google-sheets-into-a-pandas-dataframe-with-gspread-and-oauth2-375b932be7bf
#    @commands.command(brief="Google to DB for the assigned clansheets",help="Sends Changes in each account assigned clan back to the database for each clan sheet")
#    async def uploadclans(self, ctx):
#        try:
#            scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#            credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope) # Your json file here
#            gc = gspread.authorize(credentials)
#            #updateclanlist
#            wks = gc.open_by_key("1qoD-cZQffOVBwJdNYTD868nEsknyphksKBLzEhhIueo").worksheet("Clans")
#            data = wks.get_all_values()
#            headers = data.pop(0)
#            clandict = pd.DataFrame(data, columns=headers)
#            clandict=clandict[clandict['Active']=='Yes']
#            clandict.to_excel("GXclans.xlsx")
#            await ctx.send("Clans List Imported")        
#    
#            clans= pd.read_excel("GXclans.xlsx")
#            clanlist=clans[['Shortcut','Name',"DiscordRole"]].dropna()
#            clanlist=clanlist['Name'].to_list()
#            clanlist.append('Unassigned Current Members')
#            clanlist.append('Gone/Kicked/Failed')
#    
#            df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
#            dfupdate= pd.DataFrame()
#            for item in clanlist2:
#                wks = gc.open_by_key("1qoD-cZQffOVBwJdNYTD868nEsknyphksKBLzEhhIueo").worksheet(item)
#                data = wks.get_all_values()
#                headers = data.pop(0)
#                try:
#                    clandata = pd.DataFrame(data, columns=headers)
#                    df2=clandata[['Tag','Change']]
#                    dfupdate=dfupdate.append(df2)
#                except:
#                    await ctx.send(f"{item} failed")
#                
#           # await ctx.send(f"Google sheet imported successfully")
#            
#            dfupdate=dfupdate.loc[dfupdate['Change']!='no change']
#            dfupdate['AssgnClan']=dfupdate['Change'].str.upper().str.strip()
#            df.set_index("Tag", inplace=True)
#            dfupdate.set_index("Tag", inplace=True)
#            dfupdate=dfupdate[['AssgnClan']]
#            df.update(dfupdate)
#            df.to_excel('MemberDatabase GX tpyo.xlsx')
#            await ctx.send("Clan assignments have been updated from the change column in the google sheet")
#        except Exception as ex:
#            await ctx.send(ex)

def setup(bot):
    bot.add_cog(assign(bot))               