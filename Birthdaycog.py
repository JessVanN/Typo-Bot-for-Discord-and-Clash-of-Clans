import discord
import pandas as pd
from datetime import datetime
from discord.ext import commands
from datetime import date, timedelta, datetime
from dateutil.parser import parse
import asyncio

pd.set_option('mode.chained_assignment', None)
pd.set_option('precision',18)
pd.set_option('display.float_format', lambda x: '%18.f' % x)

def updatefd(df):
    delta=parse(str(df.DOB))-datetime.now()
    test=delta.days
    if (test < 12) and (test > -4):
        return df.DOB
    else:
        return 'Delete'

class birth(commands.Cog,name="05. Birthday List"):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(brief="Enter someone else's birthday",help="To enter someone's Birthday, type ^yourbirthday @tag month/day",aliases=['addbdayfor','addbirthdayfor'])
    async def yourbirthday(self,ctx, tagmember: discord.Member, monthdate:str):
        df = pd.read_excel("DiscordMem Database.xlsx")
        dt = parse(monthdate)
        df.set_index("DiscordID",inplace=True)
        date2 = dt.strftime("%b %d")
        df.at[str(tagmember.id),'DOB']= str(dt.strftime("%m-%d"))
        df.sort_values(by='DOB', ascending=True)
        df.reset_index(inplace=True)
        df.to_excel("DiscordMem Database.xlsx")
        text= f"{tagmember.mention}, your birthday is now recorded as {str(date2)}, enter month then date if this is incorrect"
        await ctx.send(text)
        
    @commands.command(brief="Birthdays coming up",help="A list of birthdays within 2 days before or 7 days after the current date",aliases=['birthdayssoon'])
    async def birthdays(self,ctx):
        df = pd.read_excel("DiscordMem Database.xlsx")
        df=df.fillna('01-01-01')
        df['DOB'] = df.apply(updatefd, axis = 1)
        df=df[df.DOB!='Delete']
        if df.empty:
            await ctx.send("No birthdays coming up :cry:")
        else:
            await ctx.send("Birthdays Coming up this week, or missed in the last few days")
            for index, row in df.iterrows():
                try:
                    member= ctx.message.guild.get_member(int(row.DiscordID))
                    dob= parse(row['DOB']).strftime("%b %d")
                    await ctx.send(f"{member.display_name} has a birthday on {str(dob)}. Happy Birthday :birthday: :tada:")
                except:
                    pass

    @commands.command(brief="Enter your location",help="To enter your location, type ^mybirthday month/day",aliases=['Iamfrom',"Myinfo",'addbday','addbirthday','mybirthday'] )
    async def DOBandLocation(self,ctx):
       # df = pd.read_excel("DiscordMem Database.xlsx")
       # df.set_index("DiscordID",inplace=True)
        try:
            def check(m):
                 return m.author == ctx.author and m.channel == ctx.channel
            await ctx.send(f"{ctx.author.mention} Please type your Date of Birth in this format MM/DD/YYYY, year is optional")
            msg = await self.bot.wait_for('message', check=check, timeout=60.0)
            monthdate=str(msg.content)
            dt = parse(monthdate)
            date2 = dt.strftime("%b %d")
            await ctx.send(f"{ctx.author.mention} Thank you, your DOB is recorded as {date2}. Now please type your Country  of residence (spelled accurately) for our map project, or type 'pass'  to skip")
            msg = await self.bot.wait_for('message', check=check, timeout=60.0)
            country=str(msg.content)
            await ctx.send(f"{ctx.author.mention} Thank you, your Country is recorded as {country}. Now please type your State/Region of residence (spelled accurately) for our map project, or type 'pass' to skip")
            msg = await self.bot.wait_for('message', check=check, timeout=60.0)
            state=str(msg.content)
            await ctx.send(f"{ctx.author.mention} Thank you, your Region is recorded as {state}. Now please type your city of residence (spelled accurately) for our map project, or type 'pass'  to skip")
            msg = await self.bot.wait_for('message', check=check, timeout=60.0)
            city=str(msg.content)
            df2=pd.DataFrame({"DiscordID":str(ctx.message.author.id),'Date': date.today(),'Name': ctx.author.display_name,'DOB':str(dt.strftime("%m-%d")),'City':city,'State':state,'Country':country},index=[0])
            df = pd.read_excel("DiscordMem Database.xlsx")
            df=df.append(df2)
            df.reset_index(inplace=True)
            df=df[["DiscordID",'Name','Date','DOB','City','State','Country']]
            df.to_excel("DiscordMem Database.xlsx")
            text= f"{ctx.author.mention} Thank you, your city is recorded as {city}. All done for now, your Berfday is {date2} and you live in {city} {state} {country}. The map will be manually updated by an admin to include you later, but for now check out this https://www.google.com/maps/d/drive?state=%7B%22ids%22%3A%5B%221dTlrDex1XzGZ_Yx_EdAKfPG2EeW_nfJA%22%5D%2C%22action%22%3A%22open%22%2C%22userId%22%3A%22101717158436257211322%22%7D&usp=sharing"
            await ctx.send(text)
        except asyncio.TimeoutError:
            await ctx.send('Uh Oh, too slow, pls try again')
            
#    @commands.command(brief="Enter your location",help="To enter your location, type ^mybirthday month/day",aliases=['yourMyinfo','yourbirthday'] )
#    async def youarefrom(self,ctx, tagmember: discord.Member):
#        df = pd.read_excel("DiscordMem Database.xlsx")
#        df.set_index("DiscordID",inplace=True)
#        try:
#            def check(m):
#                 return m.author == ctx.author and m.channel == ctx.channel
#            await ctx.send("Please type the Date of Birth in this format MM/DD/YYYY, year is optional")
#            msg = await self.bot.wait_for('message', check=check, timeout=20.0)
#            monthdate=str(msg.content)
#            dt = parse(monthdate)
#            date2 = dt.strftime("%b %d")
#            await ctx.send(f"Thank you, their DOB is recorded as {date2}. Now please type their Country  of residence (spelled accurately) for our map project, or type 'pass'  to skip")
#            msg = await self.bot.wait_for('message', check=check, timeout=20.0)
#            country=str(msg.content)
#            await ctx.send(f"Thank you, their Country is recorded as {country}. Now please their your State/Region of residence (spelled accurately) for our map project, or type 'pass' to skip")
#            msg = await self.bot.wait_for('message', check=check, timeout=20.0)
#            state=str(msg.content)
#            await ctx.send(f"Thank you, their Region is recorded as {state}. Now please type their city of residence (spelled accurately) for our map project, or type 'pass'  to skip")
#            msg = await self.bot.wait_for('message', check=check, timeout=20.0)
#            city=str(msg.content)
#            await ctx.send(f"Thank you, their city is recorded as {city}. All done for now.")
#            df.at[str(tagmember.id),'DOB']= str(dt.strftime("%m-%d"))
#            df.at[str(tagmember.id),'City']= city
#            df.at[str(tagmember.id),'State']= state
#            df.at[str(tagmember.id),'Country']= country
#            df.reset_index(inplace=True)
#            df=df[["DiscordID",'DOB','City','State','Country']]
#            df.to_excel("DiscordMem Database.xlsx")
#            text= f"Congratulations, {tagmember.display_name} Berfday is {date2} and lives in {city} {state} {country}. The map will me updated to include them later, but for now check out this https://www.google.com/maps/d/drive?state=%7B%22ids%22%3A%5B%221dTlrDex1XzGZ_Yx_EdAKfPG2EeW_nfJA%22%5D%2C%22action%22%3A%22open%22%2C%22userId%22%3A%22101717158436257211322%22%7D&usp=sharing"
#            await ctx.send(text)
#        except asyncio.TimeoutError:
#            await ctx.send('Uh Oh, too slow, pls try again')

    @commands.command(brief="admin get data for maps",aliases=['downloadmapdata'])
    @commands.has_role("Co-Leader")
    async def getmapdata(self,ctx):
        df = pd.read_excel("DiscordMem Database.xlsx")
        df=df.sort_values(by=['DiscordID','Date'], ascending=True)
        df.drop_duplicates(subset=['DiscordID'], keep='last', inplace=True)
        memlist=[]
        for mem in ctx.guild.members:
            memlist.append(str(mem.id))
        df2=df.set_index("DiscordID")
        df3=df2[df2.index.isin(memlist)]
        for index, row in df3.iterrows():
            df3.loc[index, 'Name']=ctx.guild.get_member(int(index)).display_name
        df3=df3[['Name','DOB','City','State','Country']]
        df3.to_excel("demographicstosend.xlsx")
        uploadfile=discord.File("demographicstosend.xlsx")
        df.to_excel("DiscordMem Database.xlsx")
        await ctx.send(file=uploadfile)

            
def setup(bot):
    bot.add_cog(birth(bot))               