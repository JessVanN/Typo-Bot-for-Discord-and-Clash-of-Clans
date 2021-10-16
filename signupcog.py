from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g
import pandas as pd
from tabulate import tabulate
from discord.ext import commands
from datetime import date, timedelta, datetime
import asyncio
import discord

pd.set_option('mode.chained_assignment', None)
pd.set_option('precision',18)
pd.set_option('display.float_format', lambda x: '%18.f' % x)

def done(tag, dfsu):
    if tag in dfsu:
        return'Y'
    else:
        return'N'

class signup(commands.Cog,name="13. Signup events"):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(brief="signup for Mobile Open Season 6", help="Sign up events")
    async def MOsignup(self,ctx, *, altmem: discord.Member="none"):
        df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        df=df[df["TH"]>=13]
        if altmem=="none":
            memberid=ctx.message.author.id
            memtag=ctx.message.author
        else:
            leadrole=ctx.guild.get_role(709943956766720020) 
            if leadrole in ctx.author.roles:
                memberid=altmem.id
                memtag=altmem
            else:
                await ctx.send("Only Co-Leaders can sign another person up, to sign yourself up do not tag a discord member.")
        df2= df.loc[df.DiscordID.astype(str)==(str(memberid))]
        df2.sort_values(['TH'], axis=0, ascending=False, inplace=True, na_position='last')
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        if not df2.empty:
            df2=df2[["Tag","CurrentName", "TH","AssgnClan"]]
            df2= df2.rename(columns={"AssgnClan":"HomeClan"})
            df2.reset_index(inplace=True, drop=True)
            df2.index += 1 
            dfsu=pd.read_excel("MO signups.xlsx")
            dfsu.dropna(subset=['Tag'], inplace=True)
            dfsu=dfsu[pd.to_datetime(dfsu['Time']).dt.month==datetime.now().month]
            dfsu=dfsu['Tag'].to_list()
            df2['Done'] = df2.apply(lambda x: done(x['Tag'], dfsu), axis = 1)
            df2s=df2[["Done","Tag", "TH", "CurrentName"]]
            df2s.reset_index(inplace=True)
            df_lines = [f"{row.index:<2} {row.Done:<2}{row.Tag:<10} {row.TH:<2} {row.CurrentName}" for row in df2s.itertuples()]
            df_send = "```#  ✔ Tag        TH Name\n"
            for line in df_lines:
                new_df_send = f'{df_send}{line}\n'
                df_send = new_df_send
            sendmsg1=await ctx.send(f'{df_send}```')
            msg12=await ctx.send(f":regional_indicator_a: {ctx.author.mention} Please type the number (not the tag) in the first column for account that you want to sign up for **North American Mobile Open** ex. `1`(one at a time please)")
            msg = await self.bot.wait_for('message', check=check, timeout=100.0)
            try: 
                df3=df2.loc[int(msg.content)]
            except:
                await ctx.send ("*That is not an allowed response, you need to type the single digit number in from of the account not the tag, please start over and type `!mosignup` again*")
            df3s=df3[["Tag", "TH","CurrentName"]]
            await sendmsg1.edit(content=f"```{df3s.to_string()}```")
            msg123=await ctx.send(f"""**:regional_indicator_b: {ctx.author.mention} Are you Opting this account in or out**
Type `1` for Opting In
Type `2` for Opting Out""")
            msgopt = await self.bot.wait_for('message', check=check, timeout=100.0)
            await msg.delete(delay=1)
            if str(msgopt.content)=="2":
                await msgopt.delete(delay=1)
                df3["Opting"]="Out"
                msg123456=await ctx.send(f"""**:regional_indicator_c: {memtag.mention} Please type any notes you would like to send**. All notes __**must**__ to be sent in one message and uneditted. Type `Pass` if you have no notes""")
                try:
                    msgnote = await self.bot.wait_for('message', check=check, timeout=240.0)
                    await msgopt.delete(delay=5)
                    df3print=df3.copy()
                    df3print=df3print.drop(['Done']).to_string()
                    df3["Notes"]=msgnote.content
                except asyncio.TimeoutError:
                    await ctx.send(f'{ctx.author.mention} Um... you had 4 minutes, clearly your notes are taking too long. Why dont you just DM them to Ronnie')
                    df3print=df3.copy()
                    df3print=df3print.drop(['Done']).to_string()
                    df3["Notes"]="none"
                await ctx.send(f":white_check_mark: {ctx.author.mention} All done, so easy. Here is the data I recorded for {memtag.display_name} (note excluded)")
                try:
                    await msg12.delete(delay=0) 
                    await msg123.delete(delay=0)               
                    await msg123456.delete(delay=0)   
                    await msgnote.delete(delay=0)
                except:
                    pass
                await ctx.send(f"```{df3print}```")
                df3['DiscordID']=str(memberid)
                df3['DiscordName']=str(memtag.display_name)
                df3['Time']=str(datetime.now())
                df4=pd.read_excel("MO signups.xlsx")
                df4=df4.append(df3)
                df4.sort_values(['Tag','Time',], axis=0, ascending=True, inplace=True, na_position='last')
                df4.drop_duplicates(subset=['Tag'], keep='last', inplace=True)
                df4.to_excel("MO signups.xlsx")

            else:
                if str(msgopt.content)=="1":
                    msg2="In"
                else:
                    await ctx.send ("*That is not an allowed response, you can only type a number 1-2, please start over and type `!mosignup` again*")

                df3["Opting"]=msg2
                msg1234=await ctx.send(f"""**:regional_indicator_c: {ctx.author.mention} What Country are you from in North America??**""")
                msgplc = await self.bot.wait_for('message', check=check, timeout=100.0)
                await msgopt.delete(delay=5)
                if isinstance(msgplc.content, str):
                    df3["Location"]=msgplc.content
                    msg12345=await ctx.send(f"""**:regional_indicator_d: {ctx.author.mention} What is your ideal playing time window, (each team needs 8 wars and more than a 50% win rate during phase one, so when are you really available)?**
Type `1` for Afternoons
Type `2` for Evenings (after 9est)
Type `3` for Weekends
Type `4` for Any""")
                    msgplan = await self.bot.wait_for('message', check=check, timeout=100.0)
                    await msgplc.delete(delay=5)
                    await msgplan.delete(delay=5)
                    if isinstance(msgplan.content, str):
                        if str(msgplan.content)=="1":
                            msg4="Afternoon"
                        elif str(msgplan.content)=="2":
                            msg4="Evenings"
                        elif str(msgplan.content)=="3":
                            msg4="Weekends"
                        elif str(msgplan.content)=="4":
                            msg4="Any"
                        else:
                            await ctx.send ("*That is not an allowed response, you can only type a number 1-4, please start over and type `!mosignup` again*")
                        df3["Availbility"]=msg4
                        
                        msg123456=await ctx.send(f"""**:regional_indicator_e: {ctx.author.mention} What type of team are you looking for in terms of competitiveness?**
Type `1` for All out-Play to win it all
Type `2` for Lets Win but not kill oursleves doing it
Type `3` for Winning is nice but lets have fun too""")
                        msgplan = await self.bot.wait_for('message', check=check, timeout=100.0)
                        await msgplan.delete(delay=5)
                        if isinstance(msgplan.content, str):
                            if str(msgplan.content)=="1":
                                msg4="Competitive"
                            elif str(msgplan.content)=="2":
                                msg4="Semi"
                            elif str(msgplan.content)=="3":
                                msg4="Casual"
                            else:
                                await ctx.send ("*That is not an allowed response, you can only type a number 1-3, please start over and type `!mosignup` again*")
                            df3["Competitive"]=msg4
                        
                            msg1234567=await ctx.send(f"""**:regional_indicator_f: {ctx.author.mention} Do you want a team that voice plans during wars?**
Type `1` for Yes
Type `2` for Sometimes
Type `3` for No""")
                            msgplan = await self.bot.wait_for('message', check=check, timeout=100.0)
                            await msgplan.delete(delay=5)
                            if isinstance(msgplan.content, str):
                                if str(msgplan.content)=="1":
                                    msg4="Yes"
                                elif str(msgplan.content)=="2":
                                    msg4="Some"
                                elif str(msgplan.content)=="3":
                                    msg4="No"
                                else:
                                    await ctx.send ("*That is not an allowed response, you can only type a number 1-3, please start over and type `!mosignup` again*")
                                df3["Voice"]=msg4
                            
                                msg12345678=await ctx.send(f"""**:regional_indicator_g: {ctx.author.mention} Would you like to participate in leading a team (I.E. Responsililities!!!)?**
Type `1` for Willing to Lead
Type `2` for Willing to Co-Lead
Type `3` for Just Play Please""")
                                msgplan = await self.bot.wait_for('message', check=check, timeout=100.0)
                                await msgplan.delete(delay=5)
                                if isinstance(msgplan.content, str):
                                    if str(msgplan.content)=="1":
                                        msg4="Lead"
                                    elif str(msgplan.content)=="2":
                                        msg4="CO-lead"
                                    elif str(msgplan.content)=="3":
                                        msg4="Member"
                                    else:
                                        await ctx.send ("*That is not an allowed response, you can only type a number 1-2, please start over and type `!mosignup` again*")
                                    df3["Leader"]=msg4
                                    msg123456789=await ctx.send(f"""**:regional_indicator_h: {memtag.mention} Please type any notes you would like to send**. 
SPECIFICALLY: do you have players in mind you do and do not want to play with, list them *Do:... Do not:...*, Do you have any restrictions on your availbility
All notes __**must**__ be sent in one message and uneditted. Type `Pass` if you have no notes""")
                                    try:
                                        msgnote = await self.bot.wait_for('message', check=check, timeout=240.0)
                                        await msgplan.delete(delay=1)
                                        df3print=df3.copy()
                                        df3print=df3print.drop(['Done']).to_string()
                                        df3["Notes"]=msgnote.content
                                    except asyncio.TimeoutError:
                                        await ctx.send(f'{ctx.author.mention} Um... you had 4 minutes, clearly your notes are taking too long. Why dont you just DM them to Ronnie')
                                        df3print=df3.copy()
                                        df3print=df3print.drop(['Done']).to_string()
                                        df3["Notes"]="none"
                                    await ctx.send(f":white_check_mark: {ctx.author.mention} All done, so easy. Here is the data I recorded for {memtag.display_name} (note excluded)")
                                    try:
                                        await msg12.delete(delay=0) 
                                        await msg123.delete(delay=0)               
                                        await msg1234.delete(delay=0)               
                                        await msg12345.delete(delay=0)               
                                        await msg123456.delete(delay=0)   
                                        await msg1234567.delete(delay=0)               
                                        await msg12345678.delete(delay=0)  
                                        await msg123456789.delete(delay=0)  
                                        await msgnote.delete(delay=0)
                                    except:
                                        pass
                                    await ctx.send(f"```{df3print}```")
                                    df3['DiscordID']=str(memberid)
                                    df3['DiscordName']=str(memtag.display_name)
                                    df3['Time']=str(datetime.now())
                                    df4=pd.read_excel("MO signups.xlsx")
                                    df4=df4.append(df3)
                                    df4=df4[["Time","Tag","CurrentName","DiscordID","DiscordName","TH","HomeClan","Done","Opting","Location","Availbility","Competitive","Leader","Voice","Notes"]]
                                    df4.sort_values(['Time','Tag'], axis=0, ascending=True, inplace=True, na_position='last')
                                    df4.drop_duplicates(subset=['Tag'], keep='last', inplace=True)
                                    df4.to_excel("MO signups.xlsx")
                    else:
                       await ctx.send(f"{memtag.mention} Please only type a single digit number, now you have to start over :cry:")
                else:
                    await ctx.send(f"{memtag.mention} Please only type a single digit number, now you have to start over :cry:") 
        else:
            await ctx.send(f"{memtag.mention} You do not have any linked accounts please type `!myaccountis #YourClashIDHere`")

    @commands.command(brief="Send MO signups to Google")
    async def loadMO(self, ctx):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
                 'credentials.json', scope) # Your json file here
        try:
            dfsign = pd.read_excel("MO signups.xlsx")
            dfsign.dropna(subset=['Tag'], inplace=True)
            dfsign=dfsign[dfsign["Opting"]!="Out"]
            dfsign=dfsign[["Time","Tag","CurrentName","DiscordID","DiscordName","TH","HomeClan","Done","Opting","Location","Availbility","Competitive","Leader","Voice","Notes"]]
            dfsign.sort_values(['Time','Tag'], axis=0, ascending=True, inplace=True, na_position='last')
            spreadsheet_key = "1pv0XsVX2Yai-RnuhF_js_3BfggIJqmDNcbtJ336z7FM" #dont change this, this is google sheet location!
            d2g.upload(dfsign, spreadsheet_key, wks_name='Sheet1', credentials=credentials, row_names=True)  #df is the pandas table you are sending, wqill overright the entire previsous upload
            await ctx.send("MO Signups Exported")        
        except Exception as ex:
            await ctx.send(ex)
            
    @commands.command(brief="signup for Mobile Open Season 6", help="Sign up events")
    async def signup1v1(self,ctx, *, altmem: discord.Member="none"):
        df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        df=df[df["TH"]>=13]
        if altmem=="none":
            memberid=ctx.message.author.id
            memtag=ctx.message.author
        else:
            leadrole=ctx.guild.get_role(709943956766720020) 
            if leadrole in ctx.author.roles:
                memberid=altmem.id
                memtag=altmem
            else:
                await ctx.send("Only Co-Leaders can sign another person up, to sign yourself up do not tag a discord member.")
        df2= df.loc[df.DiscordID.astype(str)==(str(memberid))]
        df2.sort_values(['TH'], axis=0, ascending=False, inplace=True, na_position='last')
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        if not df2.empty:
            df2=df2[["Tag","CurrentName", "TH","AssgnClan"]]
            df2= df2.rename(columns={"AssgnClan":"HomeClan"})
            df2.reset_index(inplace=True, drop=True)
            df2.index += 1 
            dfsu=pd.read_excel("MO signups.xlsx")
            dfsu.dropna(subset=['Tag'], inplace=True)
            dfsu=dfsu[pd.to_datetime(dfsu['Time']).dt.month==datetime.now().month]
            dfsu=dfsu['Tag'].to_list()
            df2['Done'] = df2.apply(lambda x: done(x['Tag'], dfsu), axis = 1)
            df2s=df2[["Done","Tag", "TH", "CurrentName"]]
            df2s.reset_index(inplace=True)
            df_lines = [f"{row.index:<2} {row.Done:<2}{row.Tag:<10} {row.TH:<2} {row.CurrentName}" for row in df2s.itertuples()]
            df_send = "```#  ✔ Tag        TH Name\n"
            for line in df_lines:
                new_df_send = f'{df_send}{line}\n'
                df_send = new_df_send
            sendmsg1=await ctx.send(f'{df_send}```')
            msg12=await ctx.send(f":regional_indicator_a: {ctx.author.mention} Please type the number (not the tag) in the first column for account that you want to sign up for **GOLDEN X INTERNAL 1v1 TOURNAMENT** ex. `1`(one at a time please)")
            msg = await self.bot.wait_for('message', check=check, timeout=100.0)
            try: 
                df3=df2.loc[int(msg.content)]
            except:
                await ctx.send ("*That is not an allowed response, you need to type the single digit number in from of the account not the tag, please start over and type `!signup1v1` again*")
            df3s=df3[["Tag", "TH","CurrentName"]]
            await sendmsg1.edit(content=f"```{df3s.to_string()}```")
            msg123=await ctx.send(f"""**:regional_indicator_b: {ctx.author.mention} Are you Opting this account in or out**
Type `1` for Opting In
Type `2` for Opting Out""")
            msgopt = await self.bot.wait_for('message', check=check, timeout=100.0)
            await msg.delete(delay=1)
            if str(msgopt.content)=="2":
                await msgopt.delete(delay=1)
                df3["Opting"]="Out"
                msg123456=await ctx.send(f"""**:regional_indicator_c: {memtag.mention} Please type any notes you would like to send**. All notes __**must**__ to be sent in one message and uneditted. Type `Pass` if you have no notes""")
                try:
                    msgnote = await self.bot.wait_for('message', check=check, timeout=240.0)
                    await msgopt.delete(delay=5)
                    df3print=df3.copy()
                    df3print=df3print.drop(['Done']).to_string()
                    df3["Notes"]=msgnote.content
                except asyncio.TimeoutError:
                    await ctx.send(f'{ctx.author.mention} Um... you had 4 minutes, clearly your notes are taking too long. Why dont you just DM them to Ronnie')
                    df3print=df3.copy()
                    df3print=df3print.drop(['Done']).to_string()
                    df3["Notes"]="none"
                await ctx.send(f":white_check_mark: {ctx.author.mention} All done, so easy. Here is the data I recorded for {memtag.display_name} (note excluded)")
                try:
                    await msg12.delete(delay=0) 
                    await msg123.delete(delay=0)               
                    await msg123456.delete(delay=0)   
                    await msgnote.delete(delay=0)
                except:
                    pass
                await ctx.send(f"```{df3print}```")
                df3['DiscordID']=str(memberid)
                df3['DiscordName']=str(memtag.display_name)
                df3['Time']=str(datetime.now())
                df4=pd.read_excel("MO signups.xlsx")
                df4=df4.append(df3)
                df4.sort_values(['Tag','Time',], axis=0, ascending=True, inplace=True, na_position='last')
                df4.drop_duplicates(subset=['Tag'], keep='last', inplace=True)
                df4.to_excel("MO signups.xlsx")
            else:
                if str(msgopt.content)=="1":
                    msg2="In"
                else:
                    await ctx.send ("*That is not an allowed response, you can only type a number 1-2, please start over and type `!mosignup` again*")

                df3["Opting"]=msg2
                msg1234=await ctx.send(f"""**:regional_indicator_c: {ctx.author.mention} Would you prefer the Tournament be held on a weekend (Saturday Sunday), or weekday (Monday-Friday))?**
Type `1` for Weekend
Type `2` for Weekdays
Type `3` for Any""")
                msgplan = await self.bot.wait_for('message', check=check, timeout=100.0)
                await msgopt.delete(delay=5)
                await msgplan.delete(delay=5)
                if isinstance(msgplan.content, str):
                    if str(msgplan.content)=="1":
                        msg4="Weekend"
                    elif str(msgplan.content)=="2":
                        msg4="Weekdays"
                    elif str(msgplan.content)=="3":
                        msg4="Any"
                    else:
                        await ctx.send ("*That is not an allowed response, you can only type a number 1-4, please start over and type `!signup1v1` again*")
                    df3["Availbility"]=msg4

                    msg12345=await ctx.send(f"""**:regional_indicator_d: {memtag.mention} Please type any notes you would like to send**. 
Do you have any restrictions on your availbility
All notes __**must**__ be sent in one message and uneditted. Type `Pass` if you have no notes""")
                    try:
                        msgnote = await self.bot.wait_for('message', check=check, timeout=240.0)
                        await msgplan.delete(delay=1)
                        df3print=df3.copy()
                        df3print=df3print.drop(['Done']).to_string()
                        df3["Notes"]=msgnote.content
                    except asyncio.TimeoutError:
                        await ctx.send(f'{ctx.author.mention} Um... you had 4 minutes, clearly your notes are taking too long. Why dont you just DM them to Ronnie')
                        df3print=df3.copy()
                        df3print=df3print.drop(['Done']).to_string()
                        df3["Notes"]="none"
                    await ctx.send(f":white_check_mark: {ctx.author.mention} All done, so easy. Here is the data I recorded for {memtag.display_name} (note excluded)")
                    try:
                        await msg12.delete(delay=0) 
                        await msg123.delete(delay=0)               
                        await msg1234.delete(delay=0)               
                        await msg12345.delete(delay=0)   
                        await msgnote.delete(delay=0)
                    except:
                        pass
                    await ctx.send(f"```{df3print}```")
                    df3['DiscordID']=str(memberid)
                    df3['DiscordName']=str(memtag.display_name)
                    df3['Time']=str(datetime.now())
                    df4=pd.read_excel("MO signups.xlsx")
                    df4=df4.append(df3)
                    df4=df4[["Time","Tag","CurrentName","DiscordID","DiscordName","TH","HomeClan","Done","Opting","Availbility","Notes"]]
                    df4.sort_values(['Time','Tag'], axis=0, ascending=True, inplace=True, na_position='last')
                    df4.drop_duplicates(subset=['Tag'], keep='last', inplace=True)
                    df4.to_excel("MO signups.xlsx")
                else:
                   await ctx.send(f"{memtag.mention} Please only type a single digit number, now you have to start over :cry:")
        else:
            await ctx.send(f"{memtag.mention} You do not have any linked accounts please type `!myaccountis #YourClashIDHere`")

    @commands.command(brief="Send MO signups to Google")
    async def load1v1(self, ctx):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
                 'credentials.json', scope) # Your json file here
        try:
            dfsign = pd.read_excel("MO signups.xlsx")
            dfsign.dropna(subset=['Tag'], inplace=True)
            dfsign=dfsign[dfsign["Opting"]!="Out"]
            dfsign=dfsign[["Time","Tag","CurrentName","DiscordID","DiscordName","TH","HomeClan","Done","Opting","Availbility","Notes"]]
            dfsign.sort_values(['Time','Tag'], axis=0, ascending=True, inplace=True, na_position='last')
            spreadsheet_key = "1pv0XsVX2Yai-RnuhF_js_3BfggIJqmDNcbtJ336z7FM" #dont change this, this is google sheet location!
            d2g.upload(dfsign, spreadsheet_key, wks_name='Sheet1', credentials=credentials, row_names=True)  #df is the pandas table you are sending, wqill overright the entire previsous upload
            await ctx.send("MO Signups Exported")        
        except Exception as ex:
            await ctx.send(ex)

def setup(bot):
    bot.add_cog(signup(bot))               