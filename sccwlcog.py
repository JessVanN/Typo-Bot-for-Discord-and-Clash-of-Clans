import gspread
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g
import pandas as pd
import bdGX
from tabulate import tabulate
from discord.ext import commands
from datetime import date, timedelta, datetime
from dateutil.parser import parse
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
        
#

class sccwl(commands.Cog,name="12. SWCWL Sign up"):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(brief="signup for sccwl",help="Sign up for sccwl",aliases=['signup',"sccwlsignup"] )
    async def sccwl(self,ctx,*, altmem: discord.Member="none"):
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
        # if len(df2)==1:
        #     df2=df2[["Tag","CurrentName", "TH","AssgnClan"]]
        #     df2= df2.rename(columns={"AssgnClan":"HomeClan"})
        #     df2.reset_index(inplace=True, drop=True)
        #     df2.index += 1 
        #     dfsu=pd.read_excel("SCCWL signups.xlsx")
        #     dfsu.dropna(subset=['Tag'], inplace=True)
        #     dfsu=dfsu[pd.to_datetime(dfsu['Time']).dt.month==datetime.now().month]
        #     dfsu=dfsu['Tag'].to_list()
        #     df2['Done'] = df2.apply(lambda x: done(x['Tag'], dfsu), axis = 1)
        #     df3=df2.loc[1]
        #     df3s=df3[["Done","Tag", "TH","CurrentName"]]
        #     await ctx.send(f"```{df3s.to_string()}```")
        if len(df2)>0:
            df2=df2[["Tag","CurrentName", "TH","AssgnClan"]]
            df2= df2.rename(columns={"AssgnClan":"HomeClan"})
            df2.reset_index(inplace=True, drop=True)
            df2.index += 1 
            dfsu=pd.read_excel("SCCWL signups.xlsx")
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
            msg12=await ctx.send(f":regional_indicator_a: {ctx.author.mention} Please type the number (not the tag) in the first column for account that you want to sign up for SCCWL ex. `1`(one at a time please)")
            msg = await self.bot.wait_for('message', check=check, timeout=100.0)
            await msg.delete(delay=5)
            try: 
                df3=df2.loc[int(msg.content)]
            except:
                await ctx.send ("*That is not an allowed response, you need to type the single digit number in from of the account not the tag, please start over and type `!signup` again*")
            df3s=df3[["Tag", "TH","CurrentName"]]
            await sendmsg1.edit(content=f"```{df3s.to_string()}```")
        else:
            await ctx.send(f"{memtag.mention} You do not have any linked accounts please type `!myaccountis #YourClashIDHere`")
            return
        msg123=await ctx.send(f"""**:regional_indicator_b: {ctx.author.mention} For Supercell CWL, are you Opting this account in or out**
Type `1` for Opting In
Type `2` for Opting Out/Benched
Type `3` for  in for a partial week (please leave a note at step :regional_indicator_e: )""")
        await msg12.delete(delay=0) 
        msgopt = await self.bot.wait_for('message', check=check, timeout=100.0)
        if str(msgopt.content)=="2":
            df3["Opting"]="Out"
            msg123456=await ctx.send(f"""**:regional_indicator_e: {memtag.mention} Please type any notes you would like to send** to the roster team lead. All notes __**must**__ to be sent in one message and uneditted. If you requested a different team, indicate who this account is were not comfortable playing with or why. Type ` . ` if you have no notes""")
            try:
                msgnote = await self.bot.wait_for('message', check=check, timeout=240.0)
                await msg123.delete(delay=0)      
                await msgopt.delete(delay=1)
                df3print=df3.copy()
                df3print=df3print.drop(['Done']).to_string()
                df3["Notes"]=msgnote.content
            except asyncio.TimeoutError:
                await ctx.send(f'{ctx.author.mention} Um... you had 3 minutes, clearly your notes are taking too long. Why dont you just DM them to Ronnie')
                df3print=df3.copy()
                df3print=df3print.drop(['Done']).to_string()
                df3["Notes"]="none"
            await ctx.send(f":white_check_mark: {ctx.author.mention} All done, so easy, please repeat for any other accounts you need to sign up. Here is the data I recorded for {memtag.display_name} (note excluded)")
            await msgnote.delete(delay=0)
            await msg123456.delete(delay=0)
            await ctx.send(f"```{df3print}```")
            df3['DiscordID']=str(memberid)
            df3['DiscordName']=str(memtag.display_name)
            df3['Time']=str(datetime.now())
            df4=pd.read_excel("SCCWL signups.xlsx")
            df4=df4.append(df3)
            df4.sort_values(['Tag','Time',], axis=0, ascending=True, inplace=True, na_position='last')
            df4.drop_duplicates(subset=['Tag'], keep='last', inplace=True)
            df4=df4[['Time','Tag', 'CurrentName','DiscordID', 'DiscordName',  'TH', 'HomeClan', 'Opting', 'Placement', 'Planning',  'Notes']]
            df4.to_excel("SCCWL signups.xlsx")
            rchan=ctx.get_channel(790977509448482834)
            await rchan.send(f"```{df3print}```")
            await rchan.send(f"with note: {msgnote.content}")
        else:
            if str(msgopt.content)=="1":
                msg2="In"
            elif str(msgopt.content)=="3":
                msg2="Partial Week"
            else:
                await ctx.send ("*That is not an allowed response, you can only type a number 1-3, please start over and type `!signup` again*")

            df3["Opting"]=msg2
            msg1234=await ctx.send(f"""**:regional_indicator_c: {ctx.author.mention} Are you happy with this accounts team last season?**
Type `1` for Yes, prefer the same team
Type `2` for No, prefer the same clan rank but a different team
Type `3` for Prefer to be placed higher (than my previous month)
Type `4` for Prefer to be placed lower (than my previous month)
Type `5` for This is my first SCCWL with GX
""")
            msgplc = await self.bot.wait_for('message', check=check, timeout=100.0)
            await msg123.delete(delay=0)      
            await msgopt.delete(delay=1)
            if isinstance(msgplc.content, str):
                if str(msgplc.content)=="1":
                    msg3="Same"
                elif str(msgplc.content)=="2":
                    msg3="Different with same rank"
                elif str(msgplc.content)=="3":
                    msg3="Higher"
                elif str(msgplc.content)=="4":
                    msg3="Lower"
                elif str(msgplc.content)=="5":
                    msg3="New App"
                else:
                    await ctx.send ("*That is not an allowed response, you can only type a number 1-5, please start over and type `!signup` again*")
                df3["Placement"]=msg3
                msg12345=await ctx.send(f"""**:regional_indicator_d: {ctx.author.mention}  All teams will have 2 -3 hours at the beginning of war set aside for Discord base selections. After assignments are posted, remaining bases are first come first serve, but please announce your calls on discord.
Type the number `1` to continue """)
                msgplan = await self.bot.wait_for('message', check=check, timeout=100.0)
                await msg1234.delete(delay=0)      
                await msgplc.delete(delay=1)
                if isinstance(msgplan.content, str):
                    if str(msgplan.content)=="1":
                        msg4="plan"
                    else:
                        await ctx.send ("*That is not an allowed response, you can only type the number `1`, please start over and type `!signup` again*")
                    df3["Planning"]=msg4
                    msg123456=await ctx.send(f"""**:regional_indicator_e: {ctx.author.mention} Please type any notes you would like to send** to the roster team. All notes __**must**__ to be sent in one message and uneditted. If you requested a different team, indicate who this account is not comfortable playing with or why. Type ` . ` if you have no notes""")
                    try:
                        msgnote = await self.bot.wait_for('message', check=check, timeout=240.0)
                        await msg12345.delete(delay=0)
                        await msgplan.delete(delay=1)
                        df3print=df3.copy()
                        df3print=df3print.drop(['Done']).to_string()
                        df3["Notes"]=msgnote.content
                    except asyncio.TimeoutError:
                        await ctx.send(f'{ctx.author.mention} Um... you had 3 minutes, clearly your notes are taking too long. Why dont you just DM them to Ronnie')
                        df3print=df3.copy()
                        df3print=df3print.drop(['Done']).to_string()
                        df3["Notes"]="none"
                    await ctx.send(f":white_check_mark: {ctx.author.mention} All done, so easy, please repeat for any other accounts you have. Here is the data I recorded for {memtag.display_name} (note excluded)")
                    try:
                        await msg123456.delete(delay=0)   
                        await msgnote.delete(delay=0)
                    except:
                        pass
                    await ctx.send(f"```{df3print}```")
                    df3['DiscordID']=str(memberid)
                    df3['DiscordName']=str(memtag.display_name)
                    df3['Time']=str(datetime.now())
                    df4=pd.read_excel("SCCWL signups.xlsx")
                    df4=df4.append(df3)
                    df4.sort_values(['Time','Tag'], axis=0, ascending=True, inplace=True, na_position='last')
                    df4.drop_duplicates(subset=['Tag'], keep='last', inplace=True)
                    df4=df4[['Time','Tag', 'CurrentName','DiscordID', 'DiscordName',  'TH', 'HomeClan', 'Opting', 'Placement', 'Planning',  'Notes']]
                    df4.to_excel("SCCWL signups.xlsx")
                    rchan=ctx.guild.get_channel(790977509448482834)
                    await rchan.send(f"```{df3print}```")
                    await rchan.send(f"with note: {msgnote.content}")
                else:
                   await ctx.send(f"{memtag.mention} Please only type a single digit number, now you have to start over :cry:")
            else:
                await ctx.send(f"{memtag.mention} Please only type a single digit number, now you have to start over :cry:") 

        #https://medium.com/@vince.shields913/reading-google-sheets-into-a-pandas-dataframe-with-gspread-and-oauth2-375b932be7bf
    @commands.command(brief="Loads Clans, roster and Database Between Typo and google")
    async def loadsheets(self, ctx):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
                 'credentials.json', scope) # Your json file here
        gc = gspread.authorize(credentials)
        wks = gc.open_by_key("1qoD-cZQffOVBwJdNYTD868nEsknyphksKBLzEhhIueo").worksheet("Clans")
        data = wks.get_all_values()
        headers = data.pop(0)
        clandict = pd.DataFrame(data, columns=headers)
        clandict=clandict[clandict['Active']=='Yes']
        clandict.to_excel("GXclans.xlsx")
        await ctx.send("Clans List Imported")
        try:
            dfsign = pd.read_excel("SCCWL signups.xlsx")
            dfsign.dropna(subset=['Tag'], inplace=True)
            dfsign=dfsign[['Time','Tag', 'CurrentName','DiscordID', 'DiscordName',  'TH', 'HomeClan', 'Opting', 'Placement', 'Planning',  'Notes']]
            dfsign2=dfsign[pd.to_datetime(dfsign['Time']).dt.month==datetime.now().month]
            dfsign2.sort_values(['Time','Tag'], axis=0, ascending=True, inplace=True, na_position='last')
            #dfsign.set_index("Tag",inplace=True)
            spreadsheet_key = "1AB3hksv3WlAH0om-GBgjVcWZoIhCR6o4K6UDTWDvQWk" #dont change this, this is google sheet location!
            d2g.upload(dfsign2, spreadsheet_key, wks_name='DiscordSignup', credentials=credentials, row_names=True)  #df is the pandas table you are sending, wqill overright the entire previsous upload
            await ctx.send("Signups Exported")        
        except Exception as ex:
            await ctx.send(ex)
        df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        df.set_index("Tag",inplace=True)
        df=df[['CurrentName','PreviousName','DiscordID','FirstDate','LastDate','STATUS','Note','clan_name','clan_tag','role','TH','townHallWeaponLevel','heroes',"AssgnClan",'DOB']]
        spreadsheet_key = "1AB3hksv3WlAH0om-GBgjVcWZoIhCR6o4K6UDTWDvQWk" #dont change this, this is google sheet location!
        d2g.upload(df, spreadsheet_key, wks_name='Database API Data', credentials=credentials, row_names=True)  #df is the pandas table you are sending, wqill overright the entire previsous upload
        await ctx.send("DataBase Exported")   

    @commands.command(brief='Tag every account who has not yet !signup',help= "Fines every Current clan members and every assigned member and removes names that have signed up, and tags what remains")
    @commands.has_role("Co-Leader")
    async def tagsignup(self, ctx):
        dfdb = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        dfsu = pd.read_excel("SCCWL signups.xlsx")
        dfsu=dfsu[pd.to_datetime(dfsu['Time']).dt.month==datetime.now().month]
        botchan=ctx.guild.get_channel(750778909221716108) 
        
        clans= pd.read_excel("GXclans.xlsx")
        clanlist=clans[['Shortcut','Name',"DiscordRole"]].dropna()
        clansclist=clanlist['Shortcut'].to_list()
        clannmlist=clanlist['Name'].to_list()
        
        dfdb=dfdb[dfdb['TH']>=13]
        dfdb1=dfdb[dfdb["STATUS"]=='Current']
        dfdb1=dfdb1[dfdb1["clan_name"].isin(clannmlist)]         
        
        dfdb2=dfdb[dfdb["AssgnClan"].isin(clansclist)]
        dfdb=dfdb1.append(dfdb2)
        
        dfdb.drop_duplicates(inplace=True)
        dfdb=dfdb[['Tag', 'CurrentName', 'DiscordID', 'STATUS', 'TH', 'AssgnClan','DOB']]
        
        dfsu["Signedup"]=1
        dfsu['Tag']= dfsu['Tag'].apply(bdGX.fix_bottag)
        dfsu["Tag"]=dfsu["Tag"].str.upper()
        dfsu=dfsu[['Tag','Signedup']]
        df=dfdb.merge(dfsu,how="left", on="Tag")
        df=df[df["Signedup"]!=1]
        df.sort_values(['DiscordID','CurrentName'], axis=0,inplace=True, na_position='last')
        df=df[['Tag', 'CurrentName', 'DiscordID']]
        df=df[df["DiscordID"]!="0"]
        for index, row in df.iterrows():
            try:
                member= ctx.guild.get_member(int(row['DiscordID']))
                await ctx.send(f"{member.mention} *needs to* `!signup` *{row['CurrentName']} {row['Tag']}* in <#750778909221716108>" )
            except:
                await ctx.send(f"cannot find {row.DiscordID} for account {row['CurrentName']} {row['Tag']} ")
        await ctx.send(f"__{len(df)} The Above is a list of TH13 or higher accounts assigned to a home clan or currently in a home clan that have **NOT YET SIGNED UP** for SCCWL. Please GO TO {botchan.mention} and `!signup` or you may be left out of CWL (Please note this process is different than last month), if you dont want play in SCCWL this month that is fine but if you also don't want to get tagged every day after the 20th then fill ut the signup and opt out__")

        #https://medium.com/@vince.shields913/reading-google-sheets-into-a-pandas-dataframe-with-gspread-and-oauth2-375b932be7bf
    @commands.command(brief="Collect Cam Attack data send to roster")
    async def loadattackdata(self, ctx):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
                 'credentials.json', scope) # Your json file here
        gc = gspread.authorize(credentials)
        wks = gc.open_by_key("1kyL0r5wLfa3lHn42gpc9rPF2AMawyV_9X4pdYM2KBuM").worksheet("All War Data")
        data = wks.get_all_values()
        headers = data.pop(0)
        attackdf = pd.DataFrame(data, columns=headers)
        attackdf=attackdf[attackdf["season"]==f"{datetime.today().strftime('%Y-%m')}"]
        attackdf=attackdf[attackdf["attackerType"]=="Normal"]
        attackdf=attackdf[['attackerTag', 'clanName','stars', 'destruction']]
        attackdf["Number of Attacks"]=float(1.0)
        attackdf.loc[attackdf["stars"]=='3','3 Star Hit Rate']=1 
        attackdf.loc[attackdf["stars"].isin(['0','1']),'Failed Hit Rate']=1
        attackdf["stars"]=attackdf["stars"].astype(float)
        attackdf["destruction"]=attackdf["destruction"].astype(float)
        adf1=attackdf.groupby(['attackerTag', 'clanName']).sum()
        adf1["stars"]=round(adf1["stars"]/adf1["Number of Attacks"],2)
        adf1["destruction"]=round(adf1["destruction"]/adf1["Number of Attacks"],0)
        adf1["Failed Hit Rate"]=round(adf1["Failed Hit Rate"]/adf1["Number of Attacks"],2)
        adf1["3 Star Hit Rate"]=round(adf1["3 Star Hit Rate"]/adf1["Number of Attacks"],2)
        adf1.reset_index(inplace=True)
        spreadsheet_key = "1AB3hksv3WlAH0om-GBgjVcWZoIhCR6o4K6UDTWDvQWk" #dont change this, this is google sheet location!
        d2g.upload(adf1, spreadsheet_key, wks_name='attackdataexport', credentials=credentials, row_names=True)  #df is the pandas table you are sending, wqill overright the entire previsous upload
        await ctx.send("Attacks Exported")   


    @commands.command(brief='Tag all the members not yet in their rotsered SCCWL team',help= " Tag Cat herding day",aliases=['catherding'])
    @commands.has_role("Co-Leader")
    async def cat_herding(self, ctx):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
                 'credentials.json', scope) # Your json file here
        gc = gspread.authorize(credentials)
        wks = gc.open_by_key("1AB3hksv3WlAH0om-GBgjVcWZoIhCR6o4K6UDTWDvQWk").worksheet("roster tag export")
        data = wks.get_all_values()
        headers = data.pop(0)
        rostdf = pd.DataFrame(data, columns=headers)
        rostdf=rostdf[rostdf["Tag"]!="??"]
        rostdf=rostdf[rostdf["Tag"]!=""]
        dfdb = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        df=dfdb.merge(rostdf, how ="left", on="Tag")
        df=df[~df["Rostered Team"].isna()]
        df=df[['Tag', 'CurrentName', 'DiscordID', 'clan_name', 'Rostered Team']]
        df=df[df['clan_name']!=df['Rostered Team']]
        df.sort_values(['Rostered Team','CurrentName'], axis=0,inplace=True, na_position='last')
        for index, row in df.iterrows():
            try:
                member= ctx.guild.get_member(int(row['DiscordID']))
                await ctx.send(f"{member.mention} Move {row['CurrentName']} ({row['Tag']}) to :arrow_forward: **{row['Rostered Team']}** for SCCWL :cat: Currenting sitting in {row['clan_name']}" )
            except:
                await ctx.send(f"cannot find {row.DiscordID} for account {row['CurrentName']} {row['Tag']} :scream:")
        await ctx.send(f"Done: {len(df)} cats left to herd")

    @commands.command(brief='Prefill the form for Captians to provide feedback for all their members',help= "OMG DID YOU SEE WHAT THIS PLAYER DID",aliases=['createcaptainfeedback'])
    @commands.has_role("Co-Leader")
    async def NewCaptainFeedback(self, ctx):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
                 'credentials.json', scope) # Your json file here
        gc = gspread.authorize(credentials)
        wks = gc.open_by_key("1AB3hksv3WlAH0om-GBgjVcWZoIhCR6o4K6UDTWDvQWk").worksheet("roster tag export")
        data = wks.get_all_values()
        headers = data.pop(0)
        rostdf = pd.DataFrame(data, columns=headers)
        rostdf=rostdf[rostdf["Tag"]!="??"]
        rostdf=rostdf[rostdf["Tag"]!=""]
        dfdb = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        df=rostdf.merge(dfdb, how ="left", on="Tag")
        df=df[[ 'Rostered Team', 'CurrentName', 'TH','Tag']]
        df["Summary"]="Select Note"
        df["Note"]=""
        r2d2=rostdf["Rostered Team"].drop_duplicates().to_list()
        spreadsheet_key = "1w9QdV745aPXe0KNiqX2ZAlKU-8zSOh2elZV9TrA14n8"
        for item in r2d2:
            df2=df[df["Rostered Team"]==item]
            df2=df2[[ 'CurrentName','Tag',"Summary","Note"]]
            wks_name = item #change this for each table
            d2g.upload(df2, spreadsheet_key, wks_name, credentials=credentials, row_names=False)#df is the pandas table you are sending, wqill overright the entire previsous upload
            await ctx.send(f"DataBase Exported for {wks_name}")
            await asyncio.sleep(10)

    @commands.command(brief='Gather the captain feedback for all their members',help= "OMG DID YOU SEE WHAT THIS PLAYER DID",aliases=['gathercaptainfeedback'])
    @commands.has_role("Co-Leader")
    async def CollectCaptainFeedback(self, ctx):
        await ctx.send(f"Starting: will send confirmtion when done")
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
                 'credentials.json', scope) # Your json file here
        gc = gspread.authorize(credentials)
        gfile = gc.open_by_key("1w9QdV745aPXe0KNiqX2ZAlKU-8zSOh2elZV9TrA14n8")
        dfall=pd.DataFrame()
        wkscount = len(gfile.worksheets())
        for wksnum in range(1,wkscount):
            worksheet = gfile.get_worksheet(wksnum)
            data = worksheet.get_all_values()
            headers = data.pop(0)
            df = pd.DataFrame(data, columns=headers)
            dfall=dfall.append(df)
        wks_name = "Tpyo Captain Feedback"
        spreadsheet_key = "1AB3hksv3WlAH0om-GBgjVcWZoIhCR6o4K6UDTWDvQWk"
        dfall=dfall[['Tag','CurrentName', 'Summary','Note']]
        dfall.set_index('Tag', drop=True,inplace=True)
        dfall=dfall[dfall['CurrentName'].str.len() >3]
        print(dfall)
        d2g.upload(dfall, spreadsheet_key, wks_name, credentials=credentials)#df is the pandas table you are sending, wqill overright the entire previsous upload
        await ctx.send(f"DataBase Exported for {wks_name}")

def setup(bot):
    bot.add_cog(sccwl(bot))               