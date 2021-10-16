import discord
import pandas as pd
from tabulate import tabulate
import bdGX
import time
from discord.ext import commands
import asyncio
pd.set_option('mode.chained_assignment', None)
pd.set_option('precision',18)
pd.set_option('display.float_format', lambda x: '%18.f' % x)

class claim(commands.Cog,name="02. Claim accounts"):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(brief="List Your clash accounts",help="List All Accounts linked to your Discord ID weather current or not",aliases=['my_account','myaccount','my_accounts'])
    async def myaccounts(self,ctx):
        df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        memberid=ctx.message.author.id
        df2= df.loc[df.DiscordID.astype(str)==(str(memberid))]
        df2.sort_values(['TH'], axis=0, ascending=False, inplace=True, na_position='last')
        if not df2.empty:
            df2=df2[["CurrentName", "TH", "Tag"]]
            dfsend=tabulate(df2,  headers="keys",showindex="never")
            await ctx.send(f"```{dfsend}```")
            await ctx.send(f"If any accounts are missing from this list you may add them with ^myaccountis #clashidhere")
        else:
            await ctx.send("Error: no associated accounts")
    
    @commands.command(brief="List all accounts linked to tagged member",help="List All Accounts linked to a tagged Discord ID weather current or not",aliases=['your_account','youraccount','your_accounts'])
    async def youraccounts(self,ctx, member: discord.Member):
        df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        memberid=member.id
        df3= df.loc[df.DiscordID.astype(str)==(str(memberid))]
        df3.sort_values(['TH'], axis=0, ascending=False, inplace=True, na_position='last') 
        if not df3.empty:
            df3=df3[["CurrentName", "TH", "Tag"]]
            dfsend=tabulate(df3,  headers="keys",showindex="never")
            await ctx.send(f"```{dfsend}```")
        else:
            await ctx.send("Error: no associated accounts or Jess needs to fix th 0s")
            
    @commands.command(brief="Link a new account",help= "Link your accounts to your discord ^myaccountis #clashtag", aliases=['my_account_is'])
    async def myaccountis(self,ctx, *, user_text:str):
        tag=bdGX.fix_bottag(user_text)
        play, hero= bdGX.get_player_info(tag)
        memberid=ctx.message.author.id
        guildnow=ctx.guild
        mem=guildnow.get_member(memberid).display_name
        if not play.empty:
            df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
            if not df.loc[df["Tag"]==tag].empty:
                memname=df.loc[df["Tag"]==tag, "CurrentName"]
                memname=memname.to_string(index=False)
                df.set_index("Tag", inplace=True)
                df.at[tag,'DiscordID']= str(memberid)
                df.at[tag,'FirstDate']= str(time.strftime("%Y-%m-%d"))
                df["DiscordID"]=df.DiscordID.fillna(0).astype(str)
                df.to_excel("MemberDatabase GX tpyo.xlsx")
                await ctx.send(f"{mem} is in control of {memname} {tag}")
            else:
                try:
                    play= play.rename(columns={"tag":"mem_tag"})
                    play.set_index("mem_tag",drop=True, inplace=True)
                    memdf= pd.concat([play,hero], axis=1, join="inner", sort=True)
                    memdf['Tag']=memdf.index
                    memdf['CurrentName']=memdf['name']
                    memdf['STATUS']='Alt'
                    memdf['Notes']="member self added alt:"+ str(time.strftime("%m/%d/%Y"))
                    memdf['DiscordID']= str(memberid)
                    memdf.at[tag,'FirstDate']= str(time.strftime("%Y-%m-%d"))
                    memdf= memdf.rename(columns={"clan.tag":"clan_tag", "clan.name":"clan_name", "townHallLevel":"TH"})
                    merger1= df.append(memdf,sort=False)
                    merger1['Grand Warden'].fillna(0, inplace=True)
                    merger1['Archer Queen'].fillna(0, inplace=True)
                    merger1['Barbarian King'].fillna(0, inplace=True)
                    merger1['Royal Champion'].fillna(0, inplace=True)
                    merger1['heroes']= merger1['Barbarian King'].map(int).map(str)+'/'+merger1['Archer Queen'].map(int).map(str) +'/'+merger1['Grand Warden'].map(int).map(str)+'/'+merger1['Royal Champion'].map(int).map(str)
        
                    merger1=merger1[['Tag','CurrentName','PreviousName','DiscordID','FirstDate','LastDate','STATUS','IsElder','ReadRules','Note','clan_name','clan_tag','name','role','TH','townHallWeaponLevel','Archer Queen','Barbarian King','Grand Warden','Royal Champion','heroes','AssgnClan','DOB']]
                    merger1.reset_index(drop=True, inplace=True)
                    merger1.to_excel('MemberDatabase GX tpyo.xlsx')
                    memname=memdf.loc[memdf["Tag"]==tag, "CurrentName"]
                    memname=memname.to_string(index=False)
                    merger2=merger1[merger1['Tag']==tag]
                    await ctx.send(f"""{mem}, For that Tag, I found a the clash account: {memname} {tag} at TH {play.townHallLevel.values} with heroes at {merger2["Barbarian King"].values}/{merger2["Archer Queen"].values}/{merger2["Grand Warden"].values}/{merger2["Royal Champion"].values}. This account has been added to the database""")
                except Exception as ex:
                    await ctx.send(ex)
                    await ctx.send("That account is not in the database and I was not sucessful in adding it, talk to Jess")
        else:
            await ctx.send("That Account ID does not exist did you type the account ID correctly, try ^myaccountis #clashIDHere")
    
    
    @commands.command(brief="Link a new account to someone else",help= "Link clash accounts to a tagged discord member ^myaccountis #clashtag", aliases=['your_account_is','whodis'])
    async def youraccountis(self,ctx, member: discord.Member, user_text:str):
        tag=bdGX.fix_bottag(user_text)
        play, hero= bdGX.get_player_info(tag)
        play.columns
        hero.columns
        memberid=member.id
        guildnow=ctx.guild
        mem=guildnow.get_member(memberid).display_name
        if not play.empty:
            df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
            if not df.loc[df["Tag"]==tag].empty:
                memname=df.loc[df["Tag"]==tag, "CurrentName"]
                memname=memname.to_string(index=False)
                df.set_index("Tag", inplace=True)
                df.at[tag,'DiscordID']= str(memberid)
                df.DiscordID=df.DiscordID.fillna(0).astype(str)
                df.to_excel("MemberDatabase GX tpyo.xlsx")
                await ctx.send(f"{mem} is in control of {memname} {tag}")
            else:
                try:
                    play= play.rename(columns={"tag":"mem_tag"})
                    play.set_index("mem_tag",drop=True, inplace=True)
                    memdf= pd.concat([play,hero], axis=1, join="inner", sort=True)
                    memdf['Tag']=memdf.index
                    memdf['CurrentName']=memdf['name']
                    memdf['STATUS']='Alt'
                    memdf['Note']="applicant join server on:"+ str(time.strftime("%m/%d/%Y"))
                    memdf['DiscordID']= str(memberid)
                    memdf= memdf.rename(columns={"clan.tag":"clan_tag", "clan.name":"clan_name", "townHallLevel":"TH"})
                    merger1= df.append(memdf,sort=False)
                    merger1['Grand Warden'].fillna(0, inplace=True)
                    merger1['Archer Queen'].fillna(0, inplace=True)
                    merger1['Barbarian King'].fillna(0, inplace=True)
                    merger1['Royal Champion'].fillna(0, inplace=True)
                    merger1['heroes']= merger1['Barbarian King'].map(int).map(str)+'/'+merger1['Archer Queen'].map(int).map(str) +'/'+merger1['Grand Warden'].map(int).map(str)+'/'+merger1['Royal Champion'].map(int).map(str)
                    merger1=merger1[['Tag','CurrentName','PreviousName','DiscordID','FirstDate','LastDate','STATUS','IsElder','ReadRules','Note','clan_name','clan_tag','name','role','TH','townHallWeaponLevel','Archer Queen','Barbarian King','Grand Warden','Royal Champion','heroes','AssgnClan','DOB']]
                    merger1.reset_index(drop=True, inplace=True)
                    merger1.to_excel('MemberDatabase GX tpyo.xlsx')
                    memname=memdf.loc[memdf["Tag"]==tag, "CurrentName"]
                    memname=memname.to_string(index=False)
                    merger2=merger1[merger1['Tag']==tag]
                    await ctx.send(f"""{mem}, For that Tag, I found a the clash account: {memname} {tag} at TH {play.townHallLevel.values} with heroes at {merger2["Barbarian King"].values}/{merger2["Archer Queen"].values}/{merger2["Grand Warden"].values}/{merger2["Royal Champion"].values}. This account has been added to the database""")
                except:
                    await ctx.send("That account is not in the database and I was not sucessful in adding it, talk to Jess")
        else:
            await ctx.send("That Account ID does not exist did you type the account ID correctly, try ^youraccountis @tagthem #clashIDHere")
    
    @commands.command(brief="Unlink an account",help= "Set a clash account as linked to no one",aliases=['youraccountisnot', 'unlink'])
    async def myaccountisnot(self,ctx, *, user_text:str):
        s=user_text
        tag=s.split("+")[0].rstrip()
        tag=bdGX.fix_bottag(tag)
        df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        df.set_index("Tag", inplace=True)
        df.at[tag,'DiscordID']="0"
        df.to_excel("MemberDatabase GX tpyo.xlsx")
        df2= df.loc[tag]
        if df2.empty:
            await ctx.send("That account was not in the database")
        else:
            await ctx.send(F"{tag} is no longer linked to any account, to add a new link use myaccountis or youraccountis")
    
    
    @commands.command(brief="Scan a new player",help="Lookup a clash account, link it to a discord accounts and run searches all in one! ^tpyofind @tag #clashid", aliases=['typo_find','typofind','tf'])
    async def tpyofind(self,ctx, member: discord.Member, user_text:str):
        try:
            tag=bdGX.fix_bottag(user_text)
            play, hero= bdGX.get_player_info(tag)
            if not play.empty:
                memberid=member.id
                guildnow=ctx.guild
                mem=guildnow.get_member(memberid).display_name
                dfmaster = pd.read_excel("MemberDatabase GX tpyo.xlsx")
                if dfmaster.loc[dfmaster["Tag"]==tag].empty:
                    play= play.rename(columns={"tag":"mem_tag"})
                    play.set_index("mem_tag",drop=True,inplace=True)
                    memdf= pd.concat([play,hero], axis=1, join="inner", sort=True)
                    memdf['Tag']=memdf.index
                    memdf['CurrentName']=memdf['name']
                    memdf['STATUS']='Applicant'
                    memdf['Note']="applicant join server on:"+ str(time.strftime("%m/%d/%Y"))
                    memdf['DiscordID']= str(memberid)
                    memdf= memdf.rename(columns={"clan.tag":"clan_tag", "clan.name":"clan_name", "townHallLevel":"TH"})
                    merger1= dfmaster.append(memdf,sort=False)
                    merger1['Grand Warden'].fillna(0, inplace=True)
                    merger1['Archer Queen'].fillna(0, inplace=True)
                    merger1['Barbarian King'].fillna(0, inplace=True)
                    merger1['Royal Champion'].fillna(0, inplace=True)
                    merger1['heroes']= merger1['Barbarian King'].map(int).map(str)+'/'+merger1['Archer Queen'].map(int).map(str) +'/'+merger1['Grand Warden'].map(int).map(str)+'/'+merger1['Royal Champion'].map(int).map(str)
        
                    merger1=merger1[['Tag','CurrentName','PreviousName','DiscordID','FirstDate','LastDate','STATUS','IsElder','ReadRules','Note','clan_name','clan_tag','name','role','TH','townHallWeaponLevel','Archer Queen','Barbarian King','Grand Warden','Royal Champion','heroes',"AssgnClan",'DOB']]
                    merger1.reset_index(drop=True, inplace=True)
                    merger1.to_excel('MemberDatabase GX tpyo.xlsx')
                    memname=memdf.loc[memdf["Tag"]==tag, "CurrentName"]
                    memname=memname.to_string(index=False)
                    merger2=merger1[merger1['Tag']==tag]
                    await ctx.send(f"""{mem}, For that Tag, I found a the clash account: {memname} {tag} at TH {play.townHallLevel.values} with heroes at {merger2["Barbarian King"].values}/{merger2["Archer Queen"].values}/{merger2["Grand Warden"].values}/{merger2["Royal Champion"].values}. This account has been added to the database as an Applicant""")
                else:
                    text= f'{mem} For that Tag, I found a the clash account {play.name.values} at TH {play.townHallLevel.values}. It already exists in the database.'
                    await ctx.send(text)
                    try:
                        df= dfmaster.loc[dfmaster['Tag'].isin([tag])]
                        df2=df[["Tag","CurrentName","PreviousName","FirstDate","LastDate","STATUS","IsElder","ReadRules","clan_name","clan_tag","role","TH","townHallWeaponLevel","heroes","AssgnClan",'DOB']]
                        df2=df2.transpose()
                        dfnote=list(df['Note'])
                        dfsend= "```" + tabulate(df2, headers="keys") + "```"
                        await ctx.send(dfsend)
                        await ctx.send(dfnote)
                        df= pd.read_excel("MemberDatabase GX tpyo.xlsx")
                        df.set_index("Tag", inplace=True)
                        df.at[tag,'DiscordID']= str(memberid)
                        df.to_excel('MemberDatabase GX tpyo.xlsx')
                    except:
                        pass
                await ctx.send("Here is the clashofstats and in game links to this account")
                cls_text = 'https://link.clashofclans.com/?action=OpenPlayerProfile&tag=%23'+tag[1:]
                costag= bdGX.fix_bottag(user_text)[1:]
                cos_text = 'https://www.clashofstats.com/players/'+costag+'/history/'
                await ctx.send(cls_text)
                await ctx.send(cos_text)
                await ctx.send(f"mb cwlbc {costag}")
                await ctx.send(f"mb mlcwbc {costag}")
                #await ctx.send(f"!pch #{costag}")
            else:
                await ctx.send("Tag {tag} returned an error from the API: {code}")
        except:
           await ctx.send("Try typing '^tpyofind @tag #accountid'")
        memctchan=ctx.guild.get_channel(700197122380922940) #updates member count vpice channel
        count=ctx.guild.member_count
        memrole = ctx.guild.get_role(419640575847956520)#member role
        memct=len(memrole.members)    
        count=ctx.guild.member_count
        guestct=count-memct     
        text=f"Member Count:{memct}"
        await memctchan.edit(name=text)  
        gstctchan=ctx.guild.get_channel(814991481428639814)
        text=f"Guest Count:{guestct}"
        await gstctchan.edit(name=text) 

           

    @commands.command(brief="Find who owns a clash account",help= "Find out who owns a clash account, ^whois #clashtag",aliases=['who_clash','whoseclash','clashwhois','whoisclash'])
    async def whoclash(self, ctx, user_text:str):
        try:
            df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
            tag=bdGX.fix_bottag(user_text)
            df.set_index("Tag", inplace=True)
            df2= df.loc[df.index==tag]
            for index, row in df2.iterrows():
                member=ctx.message.guild.get_member(int(row["DiscordID"]))
                await ctx.send(f"The account {tag} {row.CurrentName} account belongs to the user: {member.display_name}")
        except:
            await ctx.send("Error: no associated accounts in the database... or Jess needs to fix something")
                           
def setup(bot):
    bot.add_cog(claim(bot))               