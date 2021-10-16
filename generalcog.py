import discord
import pandas as pd
from discord.ext import commands
from datetime import date, timedelta, datetime
import csv
import bdGX
import BotStringsGX
from pytz import timezone
from dateutil.parser import parse
import pytz
from pandas.io.json import json_normalize
import random

pd.set_option('mode.chained_assignment', None)
pd.set_option('precision',18)
pd.set_option('display.float_format', lambda x: '%18.f' % x)

class general(commands.Cog,name="01. General"):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(brief="When I dip, you dip, we dip",help= "When I dip, you dip, we dip", aliases=['dips','dadip'])
    async def dip(self, ctx):
        await ctx.send("https://www.youtube.com/watch?v=dZPQdZLyHYE")

    @commands.command(brief="Provides info on a discord Member",help= "help @someone: returns date of discord join and # roles")
    async def info(self, ctx, *, member: discord.Member):
        fmt = '{} joined on {} and has {} roles. Discord ID is {} and was created at {}'
        await ctx.send(fmt.format(member, member.joined_at, len(member.roles), member.id, member.created_at))

    @commands.command(brief="Delete messages",help= "clear #: deletes posts in the same channel")
    @commands.has_role("Co-Leader")
    async def clear(self, ctx, number: int):
        if not 1 < number <=100:
            return await ctx.send("Can only clear between 2 and 99 messages at a time")
        deleted = await ctx.channel.purge(limit=number+1)
        await ctx.channel.send('Deleted {} message(s)'.format(len(deleted)))
    
    @commands.command(brief="Shows the Acitivty Formula",help= "returns the activity formula", aliases=['active'])
    async def activity(self, ctx):
        bot_text = 'https://media.discordapp.net/attachments/367368439892803595/585844350941134850/activity_dark.png'
        await ctx.send(bot_text)
        
    # @commands.command(brief="CLINK CLINK CLINK",help= "Updates the Voice channel with the number of drinks the team is up to", aliases=['adddrink'])
    # async def drink(self, ctx, x=1):
    #     channel=ctx.author.voice.channel
    #     try:
    #         num=(channel.name)[-2:]
    #         num=int(num)+x
    #         num=str(str(num).zfill(2))
    #         text=f"Drink Count: {num}"
    #         await channel.edit(name=text)
    #     except:
    #         await channel.edit(name="Drink Count: 01")
    #     if int(num)<10:
    #         await ctx.send("Just getting started")
    #     elif 10<=int(num)<25:
    #         await ctx.send("Oh boy, The party is hoppin")
    #     elif 25<=int(num)<40:
    #         await ctx.send("CLINK CLINK CLINK")
    #     elif 40<=int(num):
    #         await ctx.send("DANGER Will Robinson, DANGER")
            
    @commands.command(brief="Data on the current server",help= "", aliases=['serverinfo'])
    async def server_info(self, ctx, x=1):
        g=ctx.guild
        text=f"""The {g.name} is owner by {g.owner.display_name} and was created at {g.created_at}
 It current has Nitro Boost level {g.premium_tier}
 Channels: {len(g.channels)}
      categories: {len(g.categories)} 
      voice channels: {len(g.voice_channels)} 
      text channels: {len(g.text_channels)} 
Members: {g.member_count} 
Roles: {len(g.roles)}  """
        await ctx.send(text)
        
    @commands.command(brief="Data on the the bots server count",help= "", aliases=['botinfo'])
    async def typoinfo(self, ctx):
        list1=[]
        for guild in self.bot.guilds:
            list1.append(guild.name)
        text=f"""Typobot was created by Jess#8791
Current Latency is {self.bot.latency}
Typo is in {len(self.bot.guilds)} servers
    {str(list1)}
And servers {len(self.bot.users)} discord users"""
        await ctx.send(text)
        print(str(list1))
        
    @commands.command(brief="Have you had your coffee yet",help= "")
    async def GoodMorning(self, ctx):
        msg=await ctx.send("Wait, have you had your coffee yet?")
        emocof ='☕'
        emotea ='🍵'
        emono='🚫'
        await msg.add_reaction(emocof)
        await msg.add_reaction(emotea)
        await msg.add_reaction(emono)
        def check(reaction, user):
            return  str(reaction.emoji) in ['☕', '🍵','🚫'] and user == ctx.author
        emoawait, authmsg = await self.bot.wait_for('reaction_add', check=check, timeout=100.0)
        q2=["Everyday may not be good, BUT There is SOMETHING GOOD in Every day.", 
            "Good Morning to you as well sunshine, ☕!",
            "Top of the morning to you, fine sir!"]
        if emoawait.emoji in ['☕'] :
            q1=["Coffee GOOOOD!",
                "Great attitude is like a good cup of coffee, dont start your day without it"
                "As long as there was coffee in the world, how bad could things be?",
                "Ah coffee. The sweet balm by which we shall accomplish today’s tasks.",
                "If it wasn’t for coffee, I’d have no discernible personality at all.",
                "Coffee, the favorite drink of the civilized world.",
                "Even bad coffee is better than no coffee at all.",
                "Live life today like there is no coffee tomorrow.",
                "I’d never met coffee that wasn’t wonderful. It was just a matter of how wonderful it was.",
                "Humanity runs on coffee",
                "May your coffee be strong and your Monday's be short",
                "May your coffee kick in before reality does",
                """What Goes good with a cup of coffee?
                
                Another cup""",
                "Coffee should be as black as hell, and strong as death, and as sweet as love"]
            q1.extend(q2)
            await ctx.send(random.choice(q1))
        elif emoawait.emoji in ['🍵'] :
            q1=["What makes tea green anyway?",
            "Cheerio",
            "Fancy a cuppa?",
            "If this is coffee, please bring me some tea; but if this is tea, please bring me some coffee.~Abraham Lincoln",
            "Life is like a cup of tea, the taste is up to how you make it.",
            "Strange how a teapot can represent at the same time the comforts of solitude and the pleasures of company.",
            "When there’s tea there’s hope.",
            "Blood Group: Tea Positive",
            "Thank God for tea! What would the world do without tea? How did it exist? I am glad I was not born before tea.– Reverend Sydney Smith",
            """Tea: *[tee]* **noun**
1. a hot drink made by infusing the dried crushed leaves of the tea plant in boiling water
2. a hug in a mug""",
                "Tea should be taken in solitude. – C.S. Lewis",
                "Ecstasy is a glass full of tea and a piece of sugar in the mouth. – Alexander Pushkin"]
            q1.extend(q2)
            await ctx.send(random.choice(q1))
        elif emoawait.emoji=='🚫':
            q1=["Don't talk to me until you bring me coffee 😤",
                'Shh, I am just pretend to be awake',
                '🖕',
                "I don't hate you, I just hate everyone in the morning",
                'Go away',
                "Without my morning coffee, I'm Grumpy and often borderline psychotic, please proceed with caution until properly caffinated",
                "*backing away slowly*",
                "talk to the ✋",
                "why don’t you just go 🖕 off",
                "no coffee, no workie",
                "https://cdn.discordapp.com/attachments/367368439892803595/734970687227428966/on_off_mug.png",
                "Oh that’s right, tea, Earl Grey, hot for you!",
                "It is inhumane, in my opinion, to force people who have a genuine medical need for coffee to wait in line behind people who apparently view it as some kind of recreational activity.",
                "I'll quit my coffee...it won't be easy drinking my Bailey's stright, But I'll get used to it. It'll still be the best part of my morning.",
                "Procaffinating: the tendancy to not start anything until you have had a cup of coffee",
                "Well, pour all the tea in the damn harbor, why don't you"]
            await ctx.send(random.choice(q1))
        
    @commands.command(brief="Draw a Random Number",help= "Coin toss between 1 and 2 , or roll a random number between 1 and a number you enter", aliases=['randomnumber','flipacoin','cointoss','rollthedice'])
    async def rolethedice(self, ctx, x=2):
        await ctx.send(random.randint(1,x))

    @commands.command(brief="Shows what permissions the tagged member has",help='check_permissions @tag: Check the server/channel permissions for the tagged member',aliases=["perms_for", "permissions"])
    async def check_permissions(self, ctx, member: discord.Member):
        # Here we check if the value of each permission is True.
        perms = "\n".join(perm for perm, value in member.guild_permissions if value)
    
        # And to make it look nice, we wrap it in an Embed.
        embed = discord.Embed(title="Permissions for:", description=ctx.guild.name, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))
    
        # \uFEFF is a Zero-Width Space, which basically allows us to have an empty field name.
        embed.add_field(name="\uFEFF", value=perms)
    
        await ctx.send(content=None, embed=embed)
        with open('listfile.txt', 'w',encoding='utf8') as filehandle:
            for channel in ctx.guild.channels:
                name=str(f"@#{channel.name}")
                filehandle.write('%s\n' % str(name))
                perms = "\n".join(perm for perm, value in channel.permissions_for(member) if value)
                filehandle.write('%s\n' % perms)
        uploadfile=discord.File('listfile.txt')
        await ctx.send("This text file is a lit of permissions the tagged members has for every channel in the entire server",file=uploadfile)

    @commands.command(brief="Interview Questions",help= "Returns a set of questions that applications should answer", aliases=['Question'])
    async def questions(self, ctx):
        await ctx.send(BotStringsGX.questions_text)

    @commands.command(brief="Test...if the bot is online",help="Test if bot is online")
    async def test(self, ctx):
        bot_text =  'I am here...you are distracting me from coffee time... :rolling_eyes:'
        await ctx.send(bot_text)
        
    @commands.command(brief="Application Process for Competitive Joins",help='Prints an explanation of the application process for new joins wish to reach the competitive clans within the clan',aliases=['app'])
    async def app_process(self, ctx):
        embed=discord.Embed(title="Competitive App Process", color=0xdaa520)
        embed.set_author(name="Golden X")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/627318604148375588/633293845911830568/GX-28.png")
        embed.add_field(name="\u200b", value="""Anyone who is looking to apply must go through the following process:

:one: You will go through an FC tryout which will consist of you attacking multiple bases using armies of your choosing. We will expect you to show us knowledge of more than one strategy in your tryout. This FC tryout will take anywhere from 30-45 minutes to complete.

:two: Once completed, we will let you know in your app channel the result of your tryout. If we still need to see more from you after your FC tryouts, you'll be instructed on how we will proceed.

What happens if a player passes their trial process?

After you have passed the trial process whether that be through FC tryouts or through an evaluation period, you are now an official member of Golden X and can participate in all events with us.""", inline=False)
        await ctx.send(embed=embed)
        await ctx.channel.edit(name=f"⚔ {ctx.channel.name}")
        
    # @commands.command(brief="Outputs clans that ^loadsheets imports",help="Outputs the clan data was was imported in ^loadsheets")
    # async def checkclans(self, ctx):
    #     clandict = pd.read_excel("GXclans.xlsx")
    #     clanlist=clandict[['Shortcut','ID']].set_index("Shortcut")['ID'].to_dict()
    
    #     cwlrole= pd.read_excel("GXclans.xlsx")
    #     cwlroles=cwlrole[['ID','CWLRole']].dropna().set_index("ID")['CWLRole'].to_dict()
    
    #     regrole= pd.read_excel("GXclans.xlsx")
    #     regroles=regrole[['ID','DiscordRole']].dropna().set_index("ID")['DiscordRole'].to_dict()
     
    #     await ctx.send(f"Clan Shortcuts: \n ```{str(clanlist)}```")
    #     await ctx.send(f"Clan Regular Roles: \n ```{str(regroles)}```")
    #     await ctx.send(f"Roles to be assigned for CWL: \n ```{str(cwlroles)}```")
    
    @commands.command(brief="Daily Clash Facts",help="Pulls a posted fact (message) posted to admin channel",aliases=['clashfacts'])
    async def facts(self, ctx):
        gxchan=ctx.guild.get_channel(742788146605064213)
        msglist= await gxchan.history().flatten()
        message=random.choice(msglist)
        if len(message.attachments)==0:
            await ctx.send(f"{message.content}")
        elif len(message.attachments)>0:
            for item in message.attachments:
                await item.save(fp=item.filename)
                myfile = discord.File(item.filename)
                await ctx.send(f"{message.content}")
                await ctx.send(file=myfile)

    @commands.command(brief="Eric needs a watch",help="Converts Eastern USA time to various time zones, either current time or time entered in 3:00 pm format",aliases=['Time',"ConverTime","clock","ct","ctime"])
    async def converttime(self, ctx, usertext="Now", time="none"):
        timezones = ['US/Pacific', 'US/Eastern', 'Brazil/East', "UTC", 'Europe/Paris', 'Asia/Calcutta', 'Australia/Sydney']
        localFormat = "%I:%M%p"
        try:
            if usertext in ["Now","now",""]:
                utcmoment_naive = datetime.utcnow()
                utcmoment = utcmoment_naive.replace(tzinfo=pytz.utc)
                for tz in timezones:
                    localDatetime = utcmoment.astimezone(pytz.timezone(tz))
                    if tz == 'Asia/Calcutta':
                        ptz="India Standard"
                    else:
                        ptz=tz
                    await ctx.send(f"{ptz}: {localDatetime.strftime(localFormat)}")
                await ctx.send("https://www.worldtimezone.com/index24.php")
            elif usertext[0:3] =="UTC":   
                hours=datetime.now(timezone('UTC')).hour-datetime.now().hour
                dt = parse(time)
                for tz in timezones:
                    localDatetime = dt.astimezone(pytz.timezone(tz))- timedelta(hours=hours) #uses local computer time, must subtract to UTC
                    if tz == 'Asia/Calcutta':
                        ptz="India Standard"
                    else:
                        ptz=tz
                    await ctx.send(f"{ptz}: {localDatetime.strftime(localFormat)}")
                await ctx.send("https://www.worldtimezone.com/index24.php")
            else:
                hours=datetime.now(timezone('EST')).hour-datetime.now().hour
                dt = parse(usertext)
                for tz in timezones:
                    localDatetime = dt.astimezone(pytz.timezone(tz))- timedelta(hours=hours) #uses local computer time, must subtract to EST
                    if tz == 'Asia/Calcutta':
                        ptz="India Standard"
                    else:
                        ptz=tz
                    await ctx.send(f"{ptz}: {localDatetime.strftime(localFormat)}")
                await ctx.send("https://www.worldtimezone.com/index24.php")
        except:
            await ctx.send("Please type `^time now` to convert the current time \nTo convert an EST specific time type it is this format `^time 10:30AM`\nTo convert an UTC time type it is this format `^time UTC 8:00AM`")


    @commands.command(brief="Max Lifetime Records, top 5 per category",help= "Max Lifetime Records amoung current members, top 5 for Donations Defenses WarStars Attacks DEraided ClanGame Highest Trophies and total Trophies", aliases=['lifetimestats'])
    @commands.has_role("Co-Leader")
    async def lifetime(self, ctx):
        claninfolist = []
        #Read current clan members via API for provided clan tag(s) and generate output stats for them
        
        ctl2=pd.read_excel("GXclans.xlsx")
        clanlist=ctl2["ID"].tolist()

        #Read current clan members via API for provided clan tag(s) and generate output stats for them
        for row in clanlist:
            clan_member_list = bdGX.get_clan_list(row)
            for players in clan_member_list['memberList']:
                newinfo = bdGX.get_player_stats(players['tag'])
                claninfolist.append(newinfo)


        lifetimedf= json_normalize(claninfolist)
    
        lifetimedf.sort_values(by='Donations', ascending=False)
        donations5=lifetimedf.nlargest(5, 'Donations')
        donations5.reset_index(inplace=True)
        df_lines = [f'{row.Index:<3}{row.Donations:<9}{row.Name}' for row in donations5.itertuples()]
        donations5send = "```\n"
        for line in df_lines:
            new_df_send = f'{donations5send}{line}\n'
            donations5send = new_df_send
    
        lifetimedf.sort_values(by='BestTrophies', ascending=False)
        BestTrophies5=lifetimedf.nlargest(5, 'BestTrophies')
        BestTrophies5.reset_index(inplace=True)
        df_lines = [f'{row.Index:<3}{row.BestTrophies:<7}{row.Name}' for row in BestTrophies5.itertuples()]
        BestTrophies5send = "```\n"
        for line in df_lines:
            new_df_send = f'{BestTrophies5send}{line}\n'
            BestTrophies5send = new_df_send
    
        lifetimedf.sort_values(by='LegendCups', ascending=False)
        LegendCups5=lifetimedf.nlargest(5, 'LegendCups')
        LegendCups5.reset_index(inplace=True)
        df_lines = [f'{row.Index:<3}{row.LegendCups:<7}{row.Name}' for row in LegendCups5.itertuples()]
        LegendCups5send = "```\n"
        for line in df_lines:
            new_df_send = f'{LegendCups5send}{line}\n'
            LegendCups5send = new_df_send
    
        lifetimedf.sort_values(by='Defenses', ascending=False)
        Defenses5=lifetimedf.nlargest(5, 'Defenses')
        Defenses5.reset_index(inplace=True)
        df_lines = [f'{row.Index:<3}{row.Defenses:<6}{row.Name}' for row in Defenses5.itertuples()]
        Defenses5send = "```\n"
        for line in df_lines:
            new_df_send = f'{Defenses5send}{line}\n'
            Defenses5send = new_df_send
    
        lifetimedf.sort_values(by='WarStars', ascending=False)
        WarStars5=lifetimedf.nlargest(5, 'WarStars')
        WarStars5.reset_index(inplace=True)
        df_lines = [f'{row.Index:<3}{row.WarStars:<5}{row.Name}' for row in WarStars5.itertuples()]
        WarStars5send = "```\n"
        for line in df_lines:
            new_df_send = f'{WarStars5send}{line}\n'
            WarStars5send = new_df_send
    
        lifetimedf.sort_values(by='Attacks', ascending=False)
        Attacks5=lifetimedf.nlargest(5, 'Attacks')
        Attacks5.reset_index(inplace=True)
        df_lines = [f'{row.Index:<3}{row.Attacks:<8}{row.Name}' for row in Attacks5.itertuples()]
        Attacks5send = "```\n"
        for line in df_lines:
            new_df_send = f'{Attacks5send}{line}\n'
            Attacks5send = new_df_send
    
        lifetimedf.sort_values(by='DE', ascending=False)
        DE5=lifetimedf.nlargest(5, 'DE')
        DE5.reset_index(inplace=True)
        df_lines = [f'{row.Index:<3}{row.DE:<10}{row.Name}' for row in DE5.itertuples()]
        DE5send = "```\n"
        for line in df_lines:
            new_df_send = f'{DE5send}{line}\n'
            DE5send = new_df_send
    
        lifetimedf.sort_values(by='ClanGames', ascending=False)
        ClanGames5=lifetimedf.nlargest(5, 'ClanGames')
        ClanGames5=ClanGames5[ClanGames5['ClanGames']>0]
        ClanGames5.reset_index(inplace=True)
        df_lines = [f'{row.Index:<3}{row.ClanGames:<8}{row.Name}' for row in ClanGames5.itertuples()]
        ClanGames5send = "```\n"
        for line in df_lines:
            new_df_send = f'{ClanGames5send}{line}\n'
            ClanGames5send = new_df_send
    
        await ctx.send("__**Top 5 Donators**__")
        await ctx.send(f'{donations5send}```')
        await ctx.send("__**Top 5 Defenses**__")
        await ctx.send(f'{Defenses5send}```')
        await ctx.send("__**Top 5 # of Successful Attacks**__")
        await ctx.send(f'{Attacks5send}```')
        await ctx.send("__**Top 5 WarStars**__")
        await ctx.send(f'{WarStars5send}```')
        await ctx.send("__**Top 5 DE Collected**__")
        await ctx.send(f'{DE5send}```')
        await ctx.send("__**Top 5 Clan Games Points**__")
        await ctx.send(f'{ClanGames5send}```')
        await ctx.send("__**Top 5 Highest Trophies Reached**__")
        await ctx.send(f'{BestTrophies5send}```')
        await ctx.send("__**Top 5 Lifetime Legends Cups Collected**__")
        await ctx.send(f'{LegendCups5send}```')

def setup(bot):
    bot.add_cog(general(bot))               