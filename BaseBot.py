import discord
import pandas as pd
import bottokens
from datetime import date, datetime, timedelta
from discord.ext import commands
import asyncio
pd.set_option('mode.chained_assignment', None)
#tpyo
bot = commands.Bot(command_prefix='%')

pd.set_option('mode.chained_assignment', None)
pd.set_option('precision',18)
pd.set_option('display.float_format', lambda x: '%18.f' % x)

@bot.listen('on_raw_reaction_add')
async def giverole(payload):
    if payload.message_id == 655982322960826373:
        guild=bot.get_guild(payload.guild_id)
        member=guild.get_member(payload.user_id)
        role_name = 'HasRead'
        role = discord.utils.get(guild.roles, name=role_name)
        await member.add_roles(role)
    else:
        pass
      
@bot.event
async def on_raw_reaction_add(ctx):
    channel=bot.get_channel(ctx.channel_id)
    if channel.category.id==(636805825700298762):
        if ctx.emoji.name=='✅':
            channel2=bot.get_channel(655976001519484946)
            mes2=await channel.fetch_message(ctx.message_id)
            sender=bot.get_user(ctx.user_id)
            await channel2.send(f"""{sender.mention}, **claimed** a base with Emoji :white_check_mark::
{mes2.content} 
                
Link to original Post:  <{mes2.jump_url}>""")
                               
@bot.event
async def on_raw_reaction_remove(ctx):
    channel=bot.get_channel(ctx.channel_id)
    if channel.category.id==(636805825700298762):
        if ctx.emoji.name=='✅':
            channel2=bot.get_channel(655976001519484946)
            channel3=bot.get_channel(655976054388686852)
            mes2=await channel.fetch_message(ctx.message_id)
            sender=bot.get_user(ctx.user_id)
            await channel2.send(f"""{sender.mention}, **removed the claim** on this base. 
PLEASE PROVIDE NOTES on how the base performed, in {channel3.mention} :
{mes2.content} 
                
Link to original Post:  <{mes2.jump_url}>""")

@bot.command(help= "clear #: deletes posts in the same channel", aliases=[ 'CLear'])
@commands.has_role("Team Leader")
async def clear(ctx, number: int):
    if not 1 < number <=100:
        await ctx.send("Can only clear between 2 and 99 messages at a time")
    deleted = await ctx.channel.purge(limit=number)
    await ctx.channel.send('Deleted {} message(s)'.format(len(deleted)))

@bot.command(help= "spam *any test after a start will be sent to all channels in this category", aliases=[ 'Spam'])
@commands.has_role("Leader")
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

@bot.command(help= "returns an invite link to the current server", aliases=['Invite', 'INVITE'])
async def invite(ctx):
    await ctx.send('https://discord.gg/Hz5Cdnz')

@bot.command(help= "Test if bot is online", aliases=['Test'])
async def test(ctx):
    bot_text =  'I am here...you are distracting me from coffee time... :rolling_eyes:'
    await ctx.send(bot_text)

@bot.event
async def on_member_join(member):
    if member.guild.id==636796398691418113:
        channel= bot.get_channel(636808134719176725)
        bot_text = f"""**Welcome {member.mention} to Golden X Base Server**. 
    This server is the personal storage of the Golden X family. By being in this server you agree to build at least 1 base a month to share and  mark as claimed (according to directions) any base you use, and to unclaim and provide feedback notes when you stop using it (how it was trippled, weakness, what it defends)
    Most of the base built here are from youtube, streams, wars, or otherwise public video. Traps are often changed but please known they are not unseen bases.
    
    1. Please post what GX clan you are assigned to and when you joined?
    2. Please change your server nickname to list your name and clan name: I.E. CobraJohn|CG War Clan
    3. Please Read the {channel.mention} page."""
        jtchannel= bot.get_channel(653983765475098634)
        if jtchannel:
            await jtchannel.send(bot_text)

@bot.event
async def on_member_remove(member):
    if member.guild.id==636796398691418113:
        bot_text = f'{member.mention} left the server. Goodbye {member.name}'
        jtchannel= bot.get_channel(653983765475098634)
        if jtchannel:
            await jtchannel.send(bot_text)

#@bot.command()
#@commands.has_role("Admins")
#async def deletechannels(ctx):
#    chans= ctx.channel.category.text_channels
#    for x in chans:
#        await x.delete()
        
@bot.command()
@commands.has_role("Admins")
async def tagneedtobuild(ctx):
    post=ctx.guild.get_channel(724076244211335218)   
    category=ctx.channel.category
    datenow= datetime.now()
    dateminus1 = (datenow -timedelta(days=31))
    dateminus2 = (datenow -timedelta(days=62))
    data = [['305333425731010561', "2020-12-31 12:12:12.000000"]] 
    df=pd.DataFrame(data,columns = ['DiscordID', 'Date'])
    for channel in category.text_channels:
        async for message in channel.history(limit=300):
            data=pd.DataFrame([[str(message.author.id), message.created_at]],columns = ['DiscordID', 'Date'])
            df=df.append(data)
    df.sort_values(['DiscordID', 'Date'], axis=0, ascending=False, inplace=True, na_position='last')
    df.drop_duplicates(subset=['DiscordID'], keep='first', inplace=True)
    df['Date']=pd.to_datetime(df['Date'])
    df1=df[df['Date']>=dateminus1]
    df2=df[df['Date']>=dateminus2]
    memrole=ctx.guild.get_role(636797215754420224)   #member
    limmemrole=ctx.guild.get_role(710894122105307181)  #limited-mem
    nonmemrole=ctx.guild.get_role(710897389925433344)  #nonmem
    await post.send("The following members will be moved to Limited Member")
    for mem in memrole.members:
        df1b=df1[df1["DiscordID"]==str(mem.id)]
        df2b=df2[df2["DiscordID"]==str(mem.id)]
        if df1b.empty:
            if df2b.empty:
                await post.send(f'{mem.mention} is 2 months overdue and will be set to Non-Member')  
            else:
                await post.send(f'{mem.mention} is 1 month overdue and will be set to Limited-Member') 
        else:
            pass
    for mem in limmemrole.members:
        df1b=df1[df1["DiscordID"]==str(mem.id)]
        df2b=df2[df2["DiscordID"]==str(mem.id)]
        if df2b.empty:
            await post.send(f'{mem.mention} is 2 months overdue and will be set to Non-Member')  
    for mem in nonmemrole.members:
        df1b=df1[df1["DiscordID"]==str(mem.id)]
        df2b=df2[df2["DiscordID"]==str(mem.id)]
        if df1b.empty:
            await post.send(f'{mem.mention} to return to member please share a current meta base and link')  

@bot.command()
@commands.has_role("Admins")
async def updatememberroles(ctx):
    post=ctx.guild.get_channel(724076244211335218)
    category=ctx.channel.category
    datenow= datetime.now()
    dateminus1 = (datenow -timedelta(days=36))
    dateminus2 = (datenow -timedelta(days=67))
    data = [['305333425731010561', "2020-12-31 12:12:12.000000"]] 
    df=pd.DataFrame(data,columns = ['DiscordID', 'Date'])
    for channel in category.text_channels:
        async for message in channel.history(limit=300):
            data=pd.DataFrame([[str(message.author.id), message.created_at]],columns = ['DiscordID', 'Date'])
            df=df.append(data)
    df.sort_values(['DiscordID', 'Date'], axis=0, ascending=False, inplace=True, na_position='last')
    df.drop_duplicates(subset=['DiscordID'], keep='first', inplace=True)
    df['Date']=pd.to_datetime(df['Date'])
    df1=df[df['Date']>=dateminus1]
    df2=df[df['Date']>=dateminus2]
    memrole=ctx.guild.get_role(636797215754420224)   #member
    limmemrole=ctx.guild.get_role(710894122105307181)  #limited-mem
    nonmemrole=ctx.guild.get_role(710897389925433344)  #nonmem
    await post.send("The following members have had roles changed")
    for mem in nonmemrole.members:
        try:
            df1b=df1[df1["DiscordID"]==str(mem.id)]
            df2b=df2[df2["DiscordID"]==str(mem.id)]
            if len(df1b)>0:
                await mem.add_roles(memrole)
                await mem.remove_roles(nonmemrole)
                await post.send(f'{mem.display_name} is now a member')  
            else:
                pass 
        except:
            pass
    for mem in limmemrole.members:
        try:
            df1b=df1[df1["DiscordID"]==str(mem.id)]
            df2b=df2[df2["DiscordID"]==str(mem.id)]
            if len(df2b)==0:
                await mem.add_roles(nonmemrole)
                await mem.remove_roles(limmemrole)
                await post.send(f'{mem.display_name} is now a Non-Member')  
            else:
                if len(df1b)>0:
                    await mem.add_roles(memrole)
                    await mem.remove_roles(limmemrole)
                    await post.send(f'{mem.display_name} is now a member')  
        except:
            pass
    for mem in memrole.members:
        try:
            df1b=df1[df1["DiscordID"]==str(mem.id)]
            df2b=df2[df2["DiscordID"]==str(mem.id)]
            if len(df1b)==0:
                if len(df2b)==0:
                    await mem.add_roles(nonmemrole)
                    await mem.remove_roles(memrole)
                    await post.send(f'{mem.display_name} is now a a Non-Member')  
                else:
                    await mem.add_roles(limmemrole)
                    await mem.remove_roles(memrole)
                    await post.send(f'{mem.display_name} is now a Limited-Member') 
            else:
                pass
        except:
            pass



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} id {bot.user.id}')

bot.run(bottokens.base)
