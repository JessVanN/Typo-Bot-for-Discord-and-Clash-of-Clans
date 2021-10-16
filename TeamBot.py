import discord
import pandas as pd
import bottokens
from discord.ext import commands
import io
import asyncio
pd.set_option('mode.chained_assignment', None)
bot = commands.Bot(command_prefix='!')

#events
@bot.event
async def on_guild_join(guild):
    listchans=guild.text_channels
    chansend=guild.get_channel(listchans[0].id)
    await guild.create_role(name="Admin", permissions=discord.Permissions(8),color=discord.Color.green(),mentionable=True)
    embed=discord.Embed(title="How to Setup this Server", description="Thank you for adding __**BaseBot**__. This Program is designed and maintained by Jess#8791 a member of the Golden X Esports community.", color=0xdaa520, )
    embed.set_author(name="Jess#8791", url="https://discord.gg/xjBQnaP")
    embed.add_field(name="Server", value="Please start with a fresh server so this bot does not interact with any of your current setup. It must have full admin privledges and will create roles channels and categories.", inline=False)
    embed.add_field(name="Roles", value="The first step. TypoTeams has created a role named `Admin`. Please assign it to yourself and anyone trustyworthy to have full server control. Next, and importantly change the @everyone role to NOT be able to read text channels and see voice channels, this will prevent teams in your server from seeing each others plans.", inline=False)
    embed.add_field(name="Run Setup", value="Next any Admin may type `!setup`, this will create a welcome room structure and the base roles for admins and team leaders. After This please see the #how_to_use_this_server channel", inline=False)
    embed.set_footer(text="Support/Demo https://discord.gg/xjBQnaP")
    await chansend.send(embed=embed)

@bot.event
async def on_member_join(member):
    guild=member.guild
    chan=guild.system_channel
    bot_text = f"""**Welcome {member.mention} to the Team Planning Server**. 
This server is designed to help you team coordinated offensive and defensive bases. Please read the #how_to_use_this_server channel and ask admins to give you a role for you team."""
    await chan.send(bot_text)

@bot.event
async def on_member_remove(member):
    guild=member.guild
    chan=guild.system_channel
    bot_text = f'{member.mention} left the server. Goodbye {member.name}'
    await chan.send(bot_text)

@bot.event
async def on_raw_reaction_add(ctx):
    if ctx.emoji.name=='⤵️':
        channel=bot.get_channel(ctx.channel_id)
        category=channel.category
        newchan=await category.create_text_channel('⤵-Reacted Base')
        message= await channel.fetch_message(ctx.message_id)
        file = message.attachments[0]
        attachment_bytes = await file.read() 
        file = discord.File(io.BytesIO(attachment_bytes), file.filename, spoiler=file.is_spoiler())
        await newchan.send(message.content,file=file)
        tagme=bot.get_user(ctx.user_id)
        await newchan.send(tagme.mention)

#setup
@bot.command(help= "Report the setup info", aliases=[ 'howtosetup'])
async def HowToSetup(ctx):
    embed=discord.Embed(title="How to Setup this Server", description="Thank you for adding __**BaseBot**__. This Program is designed and maintained by Jess#8791 a member of the Golden X Esports community.", color=0xdaa520, )
    embed.set_author(name="Jess#8791", url="https://discord.gg/xjBQnaP")
    embed.add_field(name="Server", value="Please start with a fresh server so this bot does not interact with any of your current setup. It must have full admin privledges and will create roles channels and categories.", inline=False)
    embed.add_field(name="Roles", value="The first step. TypoTeams has created a role named `Admin`. Please assign it to yourself and anyone trustyworthy to have full server control. Next, and importantly change the @everyone role to NOT be able to read text channels and see voice channels, this will prevent teams in your server from seeing each others plans.", inline=False)
    embed.add_field(name="Run Setup", value="Next any Admin may type `!setup`, this will create a welcome room structure and the base roles for admins and team leaders. After This please see the #how_to_use_this_server channel", inline=False)
    embed.set_footer(text="Support/Demo https://discord.gg/xjBQnaP")
    await ctx.send(embed=embed)

#Clarify you must assign Admins role to yourself
@bot.command(help= "This command sets up the welcome channels and Team Leaders roles", aliases=[ 'Setup'])
@commands.has_permissions(administrator=True)
async def setup(ctx):
#    createrole
    role= await ctx.guild.create_role(name="Team Leader", permissions=discord.Permissions(201326608),color=discord.Color.gold(),mentionable=True)
    await ctx.message.author.add_roles(role)
    await ctx.send("TpyoTeams has created a role for Team Leaders, please leave this role name unchanged, this role will allow selected people to create new team channels, manage messages within their team and adjust nicknames. Please assign this to anyone who should be allow to create a team and then proceed to the How To channel")
    overwrites = {
    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True),
    }
    gen= await ctx.guild.create_category(f"Welcome-General",overwrites=overwrites)
    await gen.create_text_channel('welcome_goodbye')
    chan1=await gen.create_text_channel('how-to-use-this-server')
    embed=discord.Embed(title="How to Use This Server", description="This server is a private Team Planning Server for small team war planning. No one will be able to access anyone's plans or teams except server Admins who manage the server and are here manage roles and bots.", color=0xdaa520)
    embed.set_author(name="Jess#8791", url="https://discord.gg/xjBQnaP")
    embed.add_field(name="Creating a Team", value="""1. Server admins should assign the Team Leader role to anyone allowed to create new Team channels. Once you have team leader roles, type `!CreateTeam YourTeamName NumberofPlayers`. 
For example for a team of 6 rotating players on team EPICteam I would type `!createteam EPIC 6`. This will generate all the channels. 

2. Make sure your team members join and have the admins assign them their team role, for security no one else can have permissions to assign roles, or else they would be able to access other teams rooms.""", inline=False)
    await chan1.send(embed=embed)
    embed=discord.Embed(title="Team Claims",color=0xdaa520)
    embed.set_author(name="Jess#8791", url="https://discord.gg/xjBQnaP")
    embed.add_field(name="\u200b", value="""3. Each member of the team should type `!claim' in a channel in one of the player categories for themselves, and the team leader rename the categories to the player names.

4. Begin posting potential bases in the untested bases section, one base per channel. After testing, if the base is approved and ready for war, they should type `!move ChannelRename` for the channel to be moved to their category. Where they can take notes on it (wars used, traps, how it was hit), to ensure the team knows what bases each player has ready for use. 

ex. `!move JessIslandBase` will move the channel to Jess's claimed cateory and renammane the channel to JessIslandBase.""", inline=False)
    embed.add_field(name="\u200b", value="""You may also move a base by using `!moveto #tagchannel ChannelRename` in which you tag a channel in the category you want your current channel to move to.

ex. `!moveto #players2base awesomebase1` will move the channel to players2 section, and rename the channel to Awesomebase1.

5. When a base is not longer suitable for war, the player should to move it to the archived bases sections. To do this type `!archive #TagArchive ChannelRename`
ex !archive #team_archive_note 
Will move the channel to the same category as the tagged channel and add the work "Archived" to the end since no rename was given""", inline=False)
    await chan1.send(embed=embed)
    embed=discord.Embed(title="To setup a War",color=0xdaa520)
    embed.set_author(name="Jess#8791", url="https://discord.gg/xjBQnaP")
    embed.add_field(name="\u200b", value="""`!setupwar @TagTeamRole EnemyName&Date WarSize`
Ex. !setupwar @EricTeam OneHiveFeb20 10

This Creates: 
A Category titled what you entered for EnemyName&Date (no spaces permitted), 
A War Info Channel 
A Discussion Channel
A Channel for Each Enemy Base for the *WarSize* you enter
    (Enter any number up to 50, wars larger than 20 are not recommended due to discord channel limits).
    
Ex. `!startwar @EpicTeam BadEnemyTeamFeb2020 5` for a 5v5 war against BET team in Feburary""", inline=False)
    embed.set_footer(text="Support/Demo https://discord.gg/xjBQnaP")
    await chan1.send(embed=embed)
    embed=discord.Embed(title="Screenshot Base Dump",color=0xdaa520)
    embed.set_author(name="Jess#8791", url="https://discord.gg/xjBQnaP")
    embed.add_field(name="\u200b", value="""The purpose of The Base_screenshot_dump channel is for players to post images of potential bases to build, and the Teams Bot has a built in function to make this efficient

1. Post all your bases, each should be a SINGLE post with both the base image and all text together.

2. If your team decides a base should be built react with :arrow_heading_down: `:arrow_heading_down:` (this exact emoji)
This will repost the message you reacted to and create a new channel at the bottom of the same category with this Image/Text and name the channel '⤵-Reacted Base'. For you to build and test.""", inline=False)
    embed.set_footer(text="Support/Demo https://discord.gg/xjBQnaP")
    await chan1.send(embed=embed)

    await gen.create_text_channel('all-teams-chat', overwrites=overwrites)
    await gen.create_voice_channel('General Voice', overwrites=overwrites)

@bot.command(help= "Will repost the How-to channel infomation", aliases=[ 'howto'])
async def howtochannel(ctx):
    embed=discord.Embed(title="How to Use This Server", description="This server is a private Team Planning Server for 5 man or other small team defensive base planning. No one will be able to access anyone's plans or teams except server Admins who manage the server and are here manage roles and bots.", color=0xdaa520)
    embed.set_author(name="Jess#8791", url="https://discord.gg/xjBQnaP")
    embed.add_field(name="Creating a Team", value="""1. To get started the server admins should assign the Team Leader role to anyone they would allow to create new Team systems. Once you have team leader roles, type `!CreateTeam Name NumberofPlayers`. For Example for a team of 6 rotating players on team EPICteam I would type `!createteam EPIC 6`. Do this only 1 time, it will generate all the channels, and your team name must be one word. ", inline=False)

2. Make sure your team members join and have the admins assign them their team role, for security no one else can have permissions to assign roles, or else they would be able to access other teams rooms.""", inline=False)
    await ctx.send(embed=embed)
    embed=discord.Embed(title="Team Claims",color=0xdaa520)
    embed.set_author(name="Jess#8791", url="https://discord.gg/xjBQnaP")
    embed.add_field(name="\u200b", value="""3. Each member of the team should type `!claim' in a channel in one of the player categories for themselves, and the team leader rename the categories to the player names.

4. Begin posting potential bases in the untested bases section, one base per channel. After testing, if the base is approved and ready for war, they should type `!move ChannelRename` for the channel to be moved to their category. Where they can take notes on it (wars used, traps, how it was hit), to ensure the team knows what bases each player has ready for use. 

ex. `!move JessIslandBase` will move the channel to Jess's claimed cateory and renammane the channel to JessIslandBase.""", inline=False)
    embed.add_field(name="\u200b", value="""You may also move a base by using `!moveto #tagchannel ChannelRename` in which you tag a channel in the category you want your current channel to move to.

ex. `!moveto #players2base awesomebase1` will move the channel to players2 section, and rename the channel to Awesomebase1.

5. When a base is not longer suitable for war, the player should to move it to the archived bases sections. To do this type `!archive #TagArchive ChannelRename`
ex !archive #team_archive_note 
Will move the channel to the same category as the tagged channel and add the work "Archived" to the end since no rename was given""", inline=False)
    await ctx.send(embed=embed)
    embed=discord.Embed(title="To setup a War",color=0xdaa520)
    embed.set_author(name="Jess#8791", url="https://discord.gg/xjBQnaP")
    embed=discord.Embed(title="To setup a War",color=0xdaa520)
    embed.set_author(name="Jess#8791", url="https://discord.gg/xjBQnaP")
    embed.add_field(name="\u200b", value="""`!setupwar @TagTeamRole EnemyName&Date WarSize`
Ex. !setupwar @EricTeam OneHiveFeb20 10

This Creates: 
A Category titled what you entered for EnemyName&Date (no spaces permitted), 
A War Info Channel 
A Discussion Channel
A Channel for Each Enemy Base for the *WarSize* you enter
    (Enter any number up to 50, wars larger than 20 are not recommended due to discord channel limits).
    
Ex. `!startwar @EpicTeam BadEnemyTeamFeb2020 5` for a 5v5 war against BET team in Feburary""", inline=False)
    embed.set_footer(text="Support/Demo https://discord.gg/xjBQnaP")
    await ctx.send(embed=embed)
    embed=discord.Embed(title="Screenshot Base Dump",color=0xdaa520)
    embed.set_author(name="Jess#8791", url="https://discord.gg/xjBQnaP")
    embed.add_field(name="\u200b", value="""The purpose of The Base_screenshot_dump channel is for players to post images of potential bases to build, and the Teams Bot has a built in function to make this efficient

1. Post all your bases, each should be a SINGLE post with both the base image and all text together.

2. If your team decides a base should be built react with :arrow_heading_down: `:arrow_heading_down:` (this exact emoji)
This will repost the message you reacted to and create a new channel at the bottom of the same category with this Image/Text and name the channel '⤵-Reacted Base'. For you to build and test.""", inline=False)
    embed.set_footer(text="Support/Demo https://discord.gg/xjBQnaP")
    await ctx.send(embed=embed)


#Generic Functions
@bot.command(help= "clear #: deletes posts in the same channel", aliases=[ 'CLear'])
@commands.has_role("Team Leader")
async def clear(ctx, number: int):
    if not 1 < number <=100:
        await ctx.send("Can only clear between 2 and 99 messages at a time")
    deleted = await ctx.channel.purge(limit=number)
    await ctx.channel.send('Deleted {} message(s)'.format(len(deleted)))

@bot.command(help= "spam *words: text after a star will be sent to all channels in this category", aliases=[ 'Spam'])
async def spam(ctx, *, user_text:str):
    s=user_text
    note=s.split("*")[1]
    if ctx.channel.category:
        for chan in ctx.channel.category.text_channels:
            await chan.send(note)

@bot.command(help= "help @someone: returns date of discord join and # roles", aliases=['Info'])
async def info(ctx, *, member: discord.Member):
    fmt = '{0} joined on {0.joined_at} and has {1} roles.{2} {}'
    await ctx.send(fmt.format(member, len(member.roles), member.id))

@bot.command(help= "!test if bot is online", aliases=['Test'])
async def test(ctx):
    bot_text =  "I am here...now let's get to work ... :rolling_eyes:"
    await ctx.send(bot_text)
    
@bot.command(help= "WARNING: deletes every txtchannel in the category, Admins only")
@commands.has_permissions(administrator=True)
async def deletechannels(ctx):
    chans= ctx.channel.category.text_channels
    for x in chans:
        await x.delete()

#team setup
@bot.command(help= "!createteam TeamName NumberofPlayer to create a new team system",aliases=['CreateTeam',"create_team","Create_Team"])
@commands.has_role("Team Leader")
async def createteam(ctx, usertext, num:int):
    try:
        role= await ctx.guild.create_role(name=usertext,color=discord.Color.green(),mentionable=True)
        await ctx.message.author.add_roles(role)
        overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        role: discord.PermissionOverwrite(read_messages=True),
        }
        gen= await ctx.guild.create_category(f"{usertext}- General",overwrites=overwrites)
        await gen.create_text_channel('Announcements')
        await gen.create_text_channel('Results')
        await gen.create_text_channel('GeneralChat', overwrites=overwrites)
        await gen.create_voice_channel('Voice', overwrites=overwrites)
        untested= await ctx.guild.create_category(f"{usertext}- Untested Defensive Bases",overwrites=overwrites)
        await untested.create_text_channel('Notes')
        await untested.create_text_channel('Base ScreenShot Dump')
        for x in range(1,11):
           await untested.create_text_channel(f"Base-{str(x)}")
        playercount=int(num+1)
        for x in range (1,playercount):
            p= await ctx.guild.create_category(f"{usertext}- Player {str(x)}",overwrites=overwrites)
            notep=await p.create_text_channel('Notes')
            await notep.send("One player please claim this category with `!claim`. One player only, uses this section to !move bases that you are ready to use in wars.")
            await p.create_text_channel(f'Player {str(x)}-Base A')
            await p.create_text_channel(f'Player {str(x)}-Base B')        
        used= await ctx.guild.create_category(f"{usertext}- Archived Bases",overwrites=overwrites)
        notarc=await used.create_text_channel(f'{usertext} Archive Notes') 
        guildid=str(ctx.guild.id)
        channelid=str(notarc.id)
        df=pd.read_excel("BaseBotDataArchive.xlsx")
        app=pd.DataFrame([[guildid, role.id,channelid]], columns=["ServerID","RoleID","ClaimChannelID"])
        df3=df.append(app)
        df3=df3[["ServerID","RoleID","ClaimChannelID"]]
        df3.to_excel("BaseBotDataArchive.xlsx")
        await notarc.send("This Category is for you to move your base channels down when they will no longer be suitable for wars")
    except:
        await ctx.send("""type `!CreateTeam NameofTeam NumberofPlayers`. 
For Example for a team of 6 rotating players on team EPICteam I would type `!createteam EPIC 6`.""")

#Claiming and moving
@bot.command(help= "!claim your category in a text channel in that category", aliases=['Claim',"claim_category"])
async def claim(ctx):
    memberid=str(ctx.message.author.id)
    guildid=str(ctx.guild.id)
    channelid=str(ctx.channel.id)
    app=pd.DataFrame([[guildid, memberid,channelid]], columns=["ServerID","DiscordID","ClaimChannelID"])
    df=pd.read_excel("BaseBotData.xlsx")
    for index,x in df.iterrows():
        if x["DiscordID"]==memberid:
            if x["ServerID"]==guildid:
                x["ClaimChannelID"]=channelid
    df3=df.append(app)
    df3.drop_duplicates(subset=["ServerID","DiscordID"],keep="last",inplace=True)
    df3=df3[["ServerID","DiscordID","ClaimChannelID"]]
    df3.to_excel("BaseBotData.xlsx")
    await ctx.send("You have claimed this section as your bases, channels for you will move only to this section, other people may claim the same section, but 1 person may only claim one category per server")

@bot.command(help= "Moves a channel to your claim category, optional channel rename",aliases=['Move'])
async def move(ctx, name="nonexist"):
    try:
        df=pd.read_excel("BaseBotData.xlsx")
        memberid=str(ctx.message.author.id)
        guildid=str(ctx.guild.id)
    
        for index,x in df.iterrows():
            if x["DiscordID"]==memberid:
                if x["ServerID"]==guildid:
                    category=ctx.guild.get_channel(int(x["ClaimChannelID"])).category
        await ctx.channel.edit(category=category)
        if name != "nonexist":
            await ctx.channel.edit(name=name)
    except:
        await ctx.send("""You must `!claim` a player category first, type !claim in ant text channel in your category.
You may optional rename this channel as a second statement, Type a name with no spaces
 ex. !move RenameToThis""")

@bot.command(help= "moveto #ToThisTagedchannel newChannelName", aliases=["MoveTo","movehere"])
async def moveto(ctx, chanarch: discord.TextChannel, name="nonexist"):
    try:
        category=ctx.guild.get_channel(chanarch.id).category
        await ctx.channel.edit(category=category)
        if name != "nonexist":
            await ctx.channel.edit(name=name)
    except:
        await ctx.send("""Please tag a channel in the category you want to move this channel to.
You may optional rename this channel as a second statement, Type a name with no spaces
 ex. !moveto #taggedchannel RenameToThis""")

@bot.command(help= "!archive #ToThisTagedchannel", aliases=["Archive"])
async def archive(ctx, chanarch: discord.TextChannel, name="-Archived"):
    try:
        category=ctx.guild.get_channel(chanarch.id).category
        await ctx.channel.edit(category=category)
        if name == "-Archived":
            namechan=f"{ctx.channel.name}{name}"
            await ctx.channel.edit(name=namechan)
    except:
        await ctx.send("""Please tag a channel in the Archive category.
You may optional rename this channel as a second statement, if you do not "-Archived" will be added to the end of the current name
 ex. !archive #taggedchannel RenameToThis""")

@bot.command(help= "!add10: adds 10 base channels to you current category",aliases=["Add10"])
@commands.has_role("Team Leader")
async def add10(ctx):
    category=ctx.channel.category
    for x in range(1,11):
       await category.create_text_channel(f"Base-{str(x)}")

#createWars
@bot.command(help= "!startwar @TeamRole EnemyNameDate NumPlayers to create a new war",aliases=['StartWar',"start_war","Start_War",'setupwar'])
@commands.has_role("Team Leader")
async def startwar(ctx, role: discord.Role, usertext:str, Enemy:int):
    try:
        if Enemy in range(1,51):
            overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True),
            }
            gen= await ctx.guild.create_category(f"{usertext}",overwrites=overwrites)
            await gen.create_text_channel('War Info')
            await gen.create_text_channel('War Planning')
            enct=int(Enemy+1)
            for x in range(1,enct):
               await gen.create_text_channel(f"Enemy-{str(x)}")
        else:
            await ctx.send("Please enter !startwar @tagyourteam Nameyourenemy ANumber1o50")
    except:
        await ctx.send("""!setupwar @TagYourTeam EnemyName&Date WarSize`
You must discord tag your teams role, then Provide a name for the war with no spaces I recommend enemy team name and Date, finally provide a number of players on enemy team 5 (not five)
Ex. !setupwar @CoolTeam NotCoolTeamFeb20 10""")
        
@bot.command(help= "!addwarhere WarDate NumOfEnemies adds a 2nd war to same opponent",aliases=['addwarhere'])
@commands.has_role("Team Leader")
async def AddWarHere(ctx, usertext:str, Enemy:int):
    try:
        if Enemy in range(5,51):
            cat=ctx.channel.category
            await cat.create_text_channel(f'{usertext} War Planning')
            enct=int(Enemy+1)
            for x in range(1,enct):
               await cat.create_text_channel(f"{usertext} Enemy-{str(x)}")
    except:
        await ctx.send("""Please enter !addwar DateofWar ANumber1o50
Date must not have spaces , and Number of enemies must be between 5 and 50""")
        

bot.run(bottokens.team)
