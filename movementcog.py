import discord
import pandas as pd
from discord.ext import commands
from datetime import date, datetime
from tabulate import tabulate

pd.set_option('mode.chained_assignment', None)
pd.set_option('precision',18)
pd.set_option('display.float_format', lambda x: '%18.f' % x)

def kicknote(df, member, reason, typenote):
    if df['DiscordID']==str(member.id):
        if not pd.isnull(df['Note']):
            note= f"{df['Note']}, {typenote} on {str(date.today())} reason: {reason} "
            return note
        else:
            note= f"{typenote} on {str(date.today())} reason: {reason}" 
            return note
    else:
        note= df['Note']
        return note

class movement(commands.Cog,name="08. Track Joins, Apps, and Kicks"):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id==273261767801569281: #gx server
            try:
                df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
                memberid=member.id
                df2= df.loc[df.DiscordID.astype(str)==(str(memberid))]
                df2.sort_values(['TH'], axis=0, ascending=False, inplace=True, na_position='last') 
                if not df2.empty:
                    df2=df2[["CurrentName", "TH", "Tag", "Note"]]
                    dfsend=tabulate(df2,  headers="keys",showindex="never")
                    guild=member.guild
                    channel= guild.get_channel(623976231125385216)
                    await channel.send(f"The Discord ID for {member.display_name} already exists in the database with the following accounts linked")        
                    await channel.send(f"```{dfsend}```")
                else:
                    pass
            except:
                pass
            serv=member.guild
            role= serv.get_role(622145519417950238)
            role2= serv.get_role(779449130128113664)
            overwrites = {serv.default_role:discord.PermissionOverwrite(read_messages=False), role:discord.PermissionOverwrite(read_messages=True), 
                          member:discord.PermissionOverwrite(read_messages=True), role2:discord.PermissionOverwrite(read_messages=True)}
            gen= serv.get_channel(557640629912469513).category
            text=f"App {member.display_name}"
            chan2=await gen.create_text_channel(text, overwrites=overwrites)
            embed=discord.Embed(title=f"Welcome to Golden X! - Please read the following:",  color=0xeacf11)
            embed.set_author(name="TypoBot")
            embed.add_field(name="\u200b", value=f"""Golden X is a North American based competitive Clash of Clans organziation
To apply, you must be of highest townhall level in game and follow the steps listed below:
*If you do not wish to join, please let us know why you are here.
If you find you are unable to type in the server, then you haven’t verified your email associated with your discord account, please DM a leader or co-leader.*                      

:one: Post the following information:
•Profile Screenshot
•Village Screenshot
•Account Tag

:two: Answer the following questions:
•Where did you hear about us?
•How old are you?
•What Country do you reside in?
•Are you looking to play competitively?
•Why did you leave your last clan?

Thank-you for applying and please standby until someone is able to assist you further. :beers:""", inline=True)
            await chan2.send(member.mention,embed=embed)
        else:
            pass
        
        
    @commands.command(brief="Create an app channel for tagged member",help= "ACreates an app cahnnel and add member, gatekeepers, and maniacs to the channel", aliases=['startapp'])
    @commands.has_role("Gatekeeper")
    async def createapp(self, ctx, member: discord.Member):        
        if ctx.guild.id==273261767801569281:
            serv=ctx.guild
            role= serv.get_role(622145519417950238)
            role2= serv.get_role(779449130128113664)
            overwrites = {serv.default_role:discord.PermissionOverwrite(read_messages=False), role:discord.PermissionOverwrite(read_messages=True), 
                          member:discord.PermissionOverwrite(read_messages=True), role2:discord.PermissionOverwrite(read_messages=True)}
            gen= serv.get_channel(557640629912469513).category
            text=f"App {member.display_name}"
            chan2=await gen.create_text_channel(text, overwrites=overwrites)
            embed=discord.Embed(title=f"Welcome to Golden X! - Please read the following:",  color=0xeacf11)
            embed.set_author(name="TypoBot")
            embed.add_field(name="\u200b", value=f"""Golden X is a North American based competitive Clash of Clans organziation
To apply, you must be of highest townhall level in game and follow the steps listed below:
*If you do not wish to join, please let us know why you are here.
If you find you are unable to type in the server, then you haven’t verified your email associated with your discord account, please DM a leader or co-leader.*                      

:one: Post the following information:
•Profile Screenshot
•Village Screenshot
•Account Tag

:two: Answer the following questions:
•Where did you hear about us?
•How old are you?
•What Country do you reside in?
•Are you looking to play competitively?
•Why did you leave your last clan?

Thank-you for applying and please standby until someone is able to assist you further. :beers:""", inline=True)
            await chan2.send(member.mention,embed=embed)
        else:
            pass

    @commands.command(brief="Copies all text and files in channel to #apphistory", aliases=['copy'])
    @commands.has_role("Gatekeeper")
    async def copyapp(self, ctx):
        if ctx.channel.category.id==555136462329348106:#if in app category
            if ctx.channel.id!=557640629912469513: #if not app history
                post=ctx.guild.get_channel(557640629912469513)  #copy to app history
                gxchan=ctx.channel
                date1 = datetime(2020, 8,1)
                async for message in gxchan.history(limit=500, after=date1):
                    try:
                        try:
                            if len(message.attachments)==0:
                                await post.send(f"`{message.author.display_name} {message.created_at}`{message.content}")
                        except:
                            pass
                        if len(message.attachments)>0:
                            for item in message.attachments:
                                await item.save(fp=item.filename)
                                myfile = discord.File(item.filename)
                                await post.send(f"`{message.author.display_name} {message.created_at}` {message.content}")
                                await post.send(file=myfile)
                    except:
                        await post.send(f"`{message.author.display_name} {message.created_at} ERROR to many charaters or file to big")
            
    @commands.command(brief="Prompts to confirm delet channel")
    @commands.has_role("Gatekeeper")
    async def delete(self, ctx):
        if ctx.channel.category.id==555136462329348106:#if in app category
            if ctx.channel.id!=557640629912469513: #if not app history
                post=ctx.guild.get_channel(557640629912469513)  #copy to app history
                msg=await ctx.send("Are you sure your are ready to delete this channel")
        emoyes='✅'
        emono ='❌'
        await msg.add_reaction(emoyes)
        await msg.add_reaction(emono)
        def check(reaction, user):
            return  str(reaction.emoji) in ['✅', '❌'] and user == ctx.author
        emoawait, authmsg = await self.bot.wait_for('reaction_add', check=check, timeout=30.0)
        if emoawait.emoji in ['✅'] :
            await post.send(f"Channel {ctx.channel.name} has been deleted by {ctx.author.display_name}")
            await ctx.channel.delete()
        else:
            pass
 
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        bot_text = f'{member} walked the plank, Argh. Swimming with the fishes {member.mention} is. '
        guild= member.guild
        await guild.system_channel.send(bot_text)
        
    @commands.command(brief="Text describing base builders channel")
    @commands.has_role("Gatekeeper")
    async def basebuilder(self, ctx):
        text=f"""Hey Base Builders!,
We have a channel that we will allow any __vetted__ base builder to post a 1 time link to their discord server, as well as a description of there services and prices. 
We will give you access to post **1 time** in our base-builder-links channel. You will then be able to edit this post within the 2000 character limit to update the description if your services and prices changes. Minimally we would like you to include what services you sell (within Terms of services ONLY), a list of costs, a link to your server, if you bases are sold to more than 1 person per base, and any info on reviews you have received (sold 100 bases last month etc etc).

Please keep in mind you will only be allowed to post 1 time and edit as you go so pictures should keep in mind they cant be updated if prices change. The reason for the 1 time post policy is that we dont want emoji recomendations to get when an original is deleted and reposted,

We will then allow our members to vote your ad up and down to mark that they have purchased from you, your base held well, delivered timely etc.
:white_check_mark: Purchased
:fire: Bases held well
:alarm_clock: Bases delivered timely
:smiley:  Good Customer Service and Professionalism
:thumbsup: :thumbsdown: Recommended

To get started Leaders here need to vet you first. Please provide a rough version of the info from above including a link to your server."""
        await ctx.send(text)
        
               
    @commands.command(brief="Add to clan a tagged member",help= "Adds applicant to server either by listing a clan shortcut,the word guest or clash(for member access with no specific clan) and then Tagging them")
    @commands.has_role("Gatekeeper")
    async def add(self, ctx, shortcut:str, member: discord.Member):
        regrole= pd.read_excel("GXclans.xlsx")
        regroles=regrole[['Shortcut','DiscordRole']].dropna().set_index("Shortcut")['DiscordRole'].to_dict()
        roleassign=regroles.get(str.upper(shortcut))
        role = discord.utils.get(ctx.message.guild.roles, name=roleassign)
        role2 = discord.utils.get(ctx.message.guild.roles, name="Member")
        role3 = discord.utils.get(ctx.message.guild.roles, name="Approved App")
        role4 = discord.utils.get(ctx.message.guild.roles, name="Guest")
        if shortcut in ['Guest','guest','cv','CV']:
            await member.add_roles(role4)
            try:
                await member.remove_roles(role3)
            except:
                pass
            await ctx.send(f"{role4} added for {member.name}")
            socchan=ctx.guild.get_channel(680866869166604292)
            embed=discord.Embed(title=f"{member.display_name}, Welcome to Golden X 🍺 🎉",  color=0xeacf11) #add url="https://forms.gle/wVAE4XxwnU67tips7",
            embed.set_author(name="TypoBot")
            embed.add_field(name="\u200b", value="You are currently in our guest social chat, where you can interact with our Golden X community members!", inline=True)
            await socchan.send(member.mention,embed=embed)
        elif shortcut in ['Clash','clash','CoC','coc']:
            await member.add_roles(role2)
            try:
                await member.remove_roles(role3)
            except:
                pass
            try:
                await member.remove_roles(role4)
            except:
                pass
            await ctx.send(f"{role2} added for {member.name}")
            socchan=ctx.guild.get_channel(273261767801569281)
            embed=discord.Embed(title=f"{member.display_name}, Welcome to Golden X 🍺 🎉",  color=0xeacf11) #add url="https://forms.gle/wVAE4XxwnU67tips7",
            embed.set_author(name="TypoBot")
            embed.add_field(name="\u200b", value="You are currently in our member chat channel. Please tell us about yourself and read about your team-mates in <#752318724878630923>", inline=False)
            embed.add_field(name="\u200b", value="Important messages, our schedule, and SCCWL signup can be found in <#682263814854410272> <#623959328050905131> and <#678427726109081639>", inline=True)
            await socchan.send(member.mention,embed=embed)
        elif roleassign:
            await member.add_roles(role)
            await member.add_roles(role2)
            try:
                await member.remove_roles(role3)
            except:
                pass
            try:
                await member.remove_roles(role4)
            except:
                pass
            await ctx.send(f"{roleassign} added for {member.name}")
            socchan=ctx.guild.get_channel(273261767801569281)
            embed=discord.Embed(title=f"{member.display_name}, Welcome to Golden X as a new member of {roleassign} 🍺 🎉",  color=0xeacf11) #add url="https://forms.gle/wVAE4XxwnU67tips7",
            embed.set_author(name="TypoBot")
            embed.add_field(name="\u200b", value="You are currently in our member chat channel. Look for another tag in your clan’s channel. Please tell us about yourself and read about your team-mates in <#752318724878630923>", inline=False)
            embed.add_field(name="\u200b", value="Important messages, our schedule, and SCCWL signup can be found in <#682263814854410272> <#623959328050905131> and <#678427726109081639>", inline=True)
            clanlist=regrole[['Shortcut','ID']].set_index("Shortcut")['ID'].to_dict()
            clantag=clanlist.get(str.upper(shortcut))
            bot_text = 'https://link.clashofclans.com/?action=OpenClanProfile&tag='+clantag[1:]
            embed.add_field(name="\u200b", value=f"Click here for a link to your clan {bot_text} and say '{ctx.author.display_name} sent you' in your join message", inline=True)
            await socchan.send(member.mention,embed=embed)
        else:
            ctx.send("Please type ^add shortcut @tagmember, if they are not being assigned to a clan you may use guest or clash instead of a shortcut")
    
    @commands.command(brief="Kick member for reasons",help="To remove a server member ^kick @tag and type your reason why. Once done it will make of note of the reason on every account row in the database",aliases=['bye'])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.top_role.position > member.top_role.position:
            reason= f"by {ctx.author.name}: {reason}"
            await ctx.guild.kick(member, reason=reason)
            df=pd.read_excel("MemberDatabase GX tpyo.xlsx")
            df2=df[df.DiscordID==(str(member.id))]
            if df2.empty:
                pass
            else:
                df["Note"]= df.apply(lambda x:kicknote(x, member, reason, "Kicked"), axis=1)
                df.to_excel("MemberDatabase GX tpyo.xlsx")
                
    @commands.command(brief="App Approved but on hold",help="Approve an app, give guest, post notification and welcome")
    @commands.has_role("Gatekeeper")
    async def Approve(self, ctx, member: discord.Member):
        socchan=ctx.guild.get_channel(273261767801569281)
        await ctx.channel.edit(name=f"✅ {ctx.channel.name}")
        embed=discord.Embed(title=f"Congratulations {member.display_name} on being accepted to Golden X",  color=0xeacf11) #add url="https://forms.gle/wVAE4XxwnU67tips7",
        embed.set_author(name="TypoBot")
        embed.add_field(name="\u200b", value="""You can run the command *!wars* and decide if you would like to be tagged for friendly wars: click the green checkmark to give yourself the role or Red X to remove it. You will be tagged when a relevant war is available.
----------------------""", inline=True)
        embed.add_field(name="\u200b", value="""To sign up for the next Supercell CWL (SCCWL), please type *!signup* and then follow the prompts.
----------------------""", inline=True)
        embed.add_field(name="\u200b", value="""You now have roles for Member and are able to see the server, you have also been tagged in our member channel, please check that out to meet your clanmates
----------------------""", inline=True)
        embed.add_field(name="\u200b", value="""Important messages, our schedule, and SCCWL signup can be found in <#682263814854410272> and <#687833890211364887>
----------------------""", inline=True)
        embed.add_field(name="\u200b", value=f"""Click here for a link to the main clan
GX: https://link.clashofclans.com/?action=OpenClanProfile&tag=2Q9YRQY8
and say '{ctx.author.display_name} sent you' in your join message
----------------------""", inline=True)
        embed.add_field(name="\u200b", value="We will leave this channel open for a few more days so you can ask questions as you get to know us. Welcome!", inline=True)
        await ctx.send(member.mention,embed=embed)
        role2 = discord.utils.get(ctx.message.guild.roles, name="Member")
        role4 = discord.utils.get(ctx.message.guild.roles, name="Guest")
        await member.add_roles(role2)
        try:
            await member.remove_roles(role4)
        except:
            pass
        await ctx.send(f"Member added for {member.name}")
        socchan=ctx.guild.get_channel(273261767801569281)
        embed=discord.Embed(title=f"{member.display_name}, Welcome to Golden X's Newest Member 🍺 🎉",  color=0xeacf11) #add url="https://forms.gle/wVAE4XxwnU67tips7",
        embed.set_author(name="TypoBot")
        embed.add_field(name="\u200b", value="You are currently in our member chat channel. Please, feel free to tell us about yourself and read about your team-mates in <#752318724878630923>, also go to <#750778909221716108> and type !myinfo if you want to add your birthday to our calendar and be on our clan 'where are you from?' map", inline=False)
        await socchan.send(member.mention,embed=embed)
        gxchan=ctx.guild.get_channel(712782721448935496)
        df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        memberid=member.id
        df2= df.loc[df.DiscordID.astype(str)==(str(memberid))]
        df2.sort_values(['TH'], axis=0, ascending=False, inplace=True, na_position='last') 
        if not df2.empty:
            df2=df2[["CurrentName", "Tag"]]
            dfsend=tabulate(df2,  headers="keys",showindex="never")
            await gxchan.send(f"New approved app {member.display_name}: Please accept the new succesful app to GX in game when he/she applies")        
            await gxchan.send(f"```{dfsend}```")
        else:
            pass

        
      
        
    @commands.command(brief="add yellow emoji to channel name saying app is on hold", aliases=['holdapp','apphold'])
    @commands.has_role("Gatekeeper")
    async def hold(self, ctx):        
        if ctx.channel.category.id==ctx.guild.get_channel(557640629912469513).category.id:
            await ctx.channel.edit(name=f"🟡 {ctx.channel.name}")


    @commands.command(brief="Ban member for reasons",help="To remove a server member and prevent them from ever rejoining ^ban @tag and type your reason why. Once done it will make of note of the reason on every account row in the database",aliases=['byeforever'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.top_role.position > member.top_role.position:
            reason= f"by {ctx.author.name}: {reason}"
            guild=member.guild
            await guild.ban(member, reason=reason, delete_message_days=0)
            df=pd.read_excel("MemberDatabase GX tpyo.xlsx")
            df2=df[df.DiscordID==(str(member.id))]
            if df2.empty:
                pass
            else:
                df["Note"]= df.apply(lambda x:kicknote(x, member, reason, "Banned"), axis=1)
                df.to_excel("MemberDatabase GX tpyo.xlsx")
    
    #add print to log 
         
def setup(bot):
    bot.add_cog(movement(bot))