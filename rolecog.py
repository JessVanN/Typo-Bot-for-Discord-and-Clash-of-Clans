import gspread
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g
import discord
import pandas as pd
from discord.ext import commands
from datetime import datetime

pd.set_option('mode.chained_assignment', None)
pd.set_option('precision',18)
pd.set_option('display.float_format', lambda x: '%18.f' % x)

# guest_role_map = {"AQ": "Clash Applicant",
#     'cod':"CallOfDuty",
#     'pubg':"PUBG Mobile",
#     "🎥": "Guest Content Creator", 
#     "🔨": "Base Builder", 
#     "🎵": "Music", 
#     "📣": "VoiceSquad", 
#     "⚔️":'FRIENDLY War PLS'}

class role(commands.Cog,name="09. Discord Role Assignment"):
    def __init__(self,bot):
        self.bot = bot
           
#     @commands.Cog.listener()
#     async def on_raw_reaction_add(self, payload):
#         if payload.message_id == 680953059777708080:
#             guild=self.bot.get_guild(payload.guild_id)
#             member=guild.get_member(payload.user_id)
#             role_name = guest_role_map.get(payload.emoji.name)
#             if role_name:
#                 role = discord.utils.get(guild.roles, name=role_name)
#                 await member.add_roles(role) 
#             if payload.emoji.name== "AQ":
#                 chapp=guild.get_channel(557640629912469513)
#                 embed=discord.Embed(title=f"Welcome to Golden X Exports 🍺 🎉 To apply:",  color=0xeacf11)
#                 embed.set_author(name="TypoBot")
#                 embed.add_field(name="\u200b", value=f"""Post the following information then, wait for a notification from the recruitment team.:
# •Clash Profile Screenshot
# •Clash Village Screenshot
# •Account Tag
# •The name of the clan you would like to join (if specific) See <#680891205843812362> for a detailed list. 

# Thanks for looking into our awesome squad. Good luck getting accepted and we hope you will enjoy your stay.""", inline=True)
#                 await chapp.send(member.mention,embed=embed)
# #                await chapp.send(messagesend)
#  #               try:
#  #                   channel = await member.create_dm()
#                    # await channel.send("""Welcome to Golden X server, thank you for applying to join, in the server #applications channel please complete the following to apply to join. 
# # *This is an automatic bot message and any responses here will not be seen.*
 
# # If you find you are unable to type in the server it is because our server requires your discord email be verified, if you can not get this to work, DM an admin (blue name)                                      

# # :one: Post the following information:
# # •Profile Screenshot
# # •Village Screenshot
# # •Account Tag
# # •The name of the clan you would like to join (if specific) See #clan-descriptions for a detailed list. 

# # :two: Answer the following questions:
# # •Where did you hear about us?
# # •How old are you?
# # •What Country do you reside in?
# # •What style of game play are you looking for? (Competitive, Semi-competitive, Casual)
# # •Why did you leave your last clan?

# # :three: Wait for a notification from the recruitment team.

# # Thanks for looking into our awesome squad. Good luck getting accepted and we hope you will enjoy your stay. :beers:""")
#                # except:
#                  #   pass
                    
    
#     @commands.Cog.listener()
#     async def on_raw_reaction_remove(self, payload):
#         if payload.message_id == 680953059777708080:
#             guild=self.bot.get_guild(payload.guild_id)
#             member=guild.get_member(payload.user_id)
#             role_name = guest_role_map.get(payload.emoji.name)
#             if role_name:
#                 role = discord.utils.get(guild.roles, name=role_name)
#                 await member.remove_roles(role) 
#             if payload.emoji.name== "AQ":
#                 chgate=guild.get_channel(623976231125385216)
#                 await chgate.send(f"{member.display_name} Removed their own Applicant role")
    
    @commands.command(brief="Give based based on in game location",help= "Assign Role based on main family clans, if accounts are linked in discord", aliases=['giveroles'])
    @commands.has_role("Co-Leader")
    async def give_roles(self, ctx):
        df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        df= df.loc[df['STATUS']=='Current']
        df2=df[df.DiscordID.astype('int64') >1]
        guild=ctx.guild
        regrole= pd.read_excel("GXclans.xlsx")
        regroles=regrole[['ID','DiscordRole']].dropna().set_index("ID")['DiscordRole'].to_dict()
        for index, row in df2.iterrows():
            try:
                member=ctx.message.guild.get_member(int(row["DiscordID"]))
                role_name = regroles.get(row["clan_tag"])
                role = discord.utils.get(guild.roles, name=role_name)
                if role not in member.roles:
                    if role_name:
                        await member.add_roles(role)
                        await ctx.send(f"{role_name} added for {member.name} with account {row['CurrentName']} in {row['clan_name']}")
            except:
                pass
        sendtxt=str(regroles)
        await ctx.send(f"Complete {sendtxt}")
    
    @commands.command(brief="Assign members to clan shortcut then tag each",help= "Tag a role and then all the members you want to add to that role",aliases=['manualroles'])
    @commands.has_role("Co-Leader")
    async def manualrole(self, ctx, shortcut, *DiscordMembers: discord.Member):
        try:
            await ctx.send("This command is based on the Roster Spreedsheet in google, clans tab, and will only work for roles with a value in the Manual CWL column (spelled correctly), to update the list type `^loadsheets`")
            regrole= pd.read_excel("GXclans.xlsx")
            regroles=regrole[['Shortcut','CWLRole']].dropna().set_index("Shortcut")['CWLRole'].to_dict()
            roleassign=regroles.get(str.upper(shortcut))
            for memarg in DiscordMembers:
                try:
                    mem=memarg
                    role = discord.utils.get(ctx.message.guild.roles, name=roleassign)
                    if roleassign:
                        await mem.add_roles(role)
                        await ctx.send(f"{roleassign} added for {mem.name} ")
                except Exception as ex:
                    print(ex)
            await ctx.send(f"Complete")
        except Exception as ex:
            print(ex)
   
    @commands.command(brief="give SCCWL roles by roster spreadsheet assignment",help= "Assign SCCWL Roles based on Google roster spreadsheet assignment, based on the CWLRole column in the Planning Google sheet", aliases=['givesccwl'])
    @commands.has_role("Co-Leader")
    async def give_sccwl(self, ctx):
        df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
                 'credentials.json', scope) # Your json file here
        gc = gspread.authorize(credentials)
        wks = gc.open_by_key("1AB3hksv3WlAH0om-GBgjVcWZoIhCR6o4K6UDTWDvQWk").worksheet("roster tag export")
        data = wks.get_all_values()
        headers = data.pop(0)
        rosteredtags = pd.DataFrame(data, columns=headers)
        rosteredtags=rosteredtags[rosteredtags["Tag"]!="??"]
        rosteredtags=rosteredtags[rosteredtags["Tag"]!=""]
        rosteredtags=rosteredtags.set_index("Tag",drop=True)
        rtlist=rosteredtags["Rostered Team"].to_dict()
        cwlrole= pd.read_excel("GXclans.xlsx")
        cwlroles=cwlrole[['Name','CWLRole']].dropna().set_index("Name")['CWLRole'].to_dict()
        discordids=df[['Tag','DiscordID']].dropna().set_index("Tag")['DiscordID'].to_dict()
        for x in rtlist:
            try:
                clan=rtlist.get(x)
                rolename=cwlroles.get(clan)
                role = discord.utils.get(ctx.guild.roles, name=rolename)
                disid=discordids.get(x)
                member=ctx.message.guild.get_member(int(disid))
                if role not in member.roles:
                    if rolename:
                        await member.add_roles(role)
                        await ctx.send(f"{member.display_name} given role :arrow_forward: {rolename}")
            except Exception as ex:
                await ctx.send(f"{disid} is broken")
        sendtxt=str(cwlroles)
        await ctx.send(f"Complete {sendtxt}")
    
    @commands.command(brief="List people with no roles",help='List all members of the server who have not been given a role',aliases=['noroles','withoutrole'])
    async def withoutroles(self,ctx):
        for member in ctx.guild.members:
            if len(member.roles)==1:
                memtime= datetime.now() -member.joined_at 
                await ctx.send(f"{member.name} has been in the server for {'%d days %d hours' % (memtime.days, memtime.seconds/3600)}")
        await ctx.send("complete")

    # @commands.has_role("Discord Server Admin")        
    # @commands.command()
    # async def theend(self,ctx):
    #     ids= pd.read_excel("discordremovelist.xlsx")
    #     ids=ids["DiscordID"].tolist()
    #     for memid in ids:
    #         try:
    #             member=ctx.message.guild.get_member(int(memid))
    #             for role in member.roles:
    #                 try:
    #                     if role.name!="ThunderRepublic":
    #                         if role.is_default()==False:
    #                             await member.remove_roles(role) 
    #                             await ctx.send(f"{member.name} remove {role.name}")
    #                 except:
    #                     pass
    #         except:
    #             pass
    #     await ctx.send("complete")
    
    @commands.has_role("Co-Leader")
    @commands.command(brief="Remove C1 C2 roles",help= "Remove list of roles from every server member", aliases=['removesccwl'])
    async def remove_sccwl(self, ctx):
        regrole= pd.read_excel("GXclans.xlsx")
        remove_sccwl_list=regrole['CWLRole'].dropna().to_list()
        await ctx.send("Ok give me a couple minutes")
        guild=ctx.guild
        for member in guild.members:
            for rle in remove_sccwl_list:
                roleremove = discord.utils.find(lambda r: r.name == rle, ctx.message.guild.roles)
                if roleremove in member.roles:
                    await member.remove_roles(roleremove) 
        await ctx.send("complete")
    
    # @commands.command(brief="Give Th roles",help="Give @TH13 etc roles to every linked member", aliases=['give_th','giveth'])
    # @commands.has_role("Co-Leader")
    # async def giveTHroles(self, ctx):
    #     df = pd.read_excel("MemberDatabase GX tpyo.xlsx")
    #     df= df.loc[df['STATUS']=='Current']
    #     df2=df[df.DiscordID.astype('int64') >1]
    #     guild=ctx.guild
    #     for index, row in df2.iterrows():
    #         try:
    #             member=ctx.message.guild.get_member(int(row["DiscordID"]))
    #             role_name = f"TH{int(row['TH'])}"
    #             role = discord.utils.get(guild.roles, name=role_name)
    #             if role not in member.roles:
    #                 if role_name:
    #                    await member.add_roles(role)
    #                    await ctx.send(f"{role_name} added for {member.display_name} with account {row['CurrentName']}")
    #         except:
    #             pass
    #     await ctx.send(f"Complete")    
        
    @commands.command(brief="Add Friendly war Role")
    async def friendlywars(self, ctx):
        msg=await ctx.send("Do you want the role for @FriendlyWars to be tagged when a FW is being scheduled and looking for more participants?")
        emoyes='✅'
        emono ='❌'
        await msg.add_reaction(emoyes)
        await msg.add_reaction(emono)
        def check(reaction, user):
            return  str(reaction.emoji) in ['✅', '❌'] and user == ctx.author
        emoawait, authmsg = await self.bot.wait_for('reaction_add', check=check, timeout=100.0)
        if emoawait.emoji in ['✅'] :
            role = discord.utils.get(ctx.guild.roles, name="Friendly Wars")
            await ctx.author.add_roles(role) 
            await ctx.send(f"{role.name} has been added for {ctx.author.display_name}")
        elif emoawait.emoji in ['❌'] :
            role = discord.utils.get(ctx.guild.roles, name="Friendly Wars")
            await ctx.author.remove_roles(role) 
            await ctx.send(f"{role.name} has been removed for {ctx.author.display_name}")
        else:
            pass
        
    @commands.command(brief="Add Classic war Role", aliases=['war','wars'])
    async def classicwars(self, ctx):
        msg=await ctx.send("Do you want the role for @ClassicWars to be tagged when a tradition war is about to be spun?")
        emoyes='✅'
        emono ='❌'
        await msg.add_reaction(emoyes)
        await msg.add_reaction(emono)
        def check(reaction, user):
            return  str(reaction.emoji) in ['✅', '❌'] and user == ctx.author
        emoawait, authmsg = await self.bot.wait_for('reaction_add', check=check, timeout=100.0)
        if emoawait.emoji in ['✅'] :
            role = discord.utils.get(ctx.guild.roles, name="Classic Wars")
            await ctx.author.add_roles(role) 
            await ctx.send(f"{role.name} has been added for {ctx.author.display_name}")
        elif emoawait.emoji in ['❌'] :
            role = discord.utils.get(ctx.guild.roles, name="Classic Wars")
            await ctx.author.remove_roles(role) 
            await ctx.send(f"{role.name} has been removed for {ctx.author.display_name}")
        else:
            pass
        msg=await ctx.send("Do you want the role for @FriendlyWars to be tagged when a FW is being scheduled and looking for more participants?")
        emoyes='✅'
        emono ='❌'
        await msg.add_reaction(emoyes)
        await msg.add_reaction(emono)
        def check(reaction, user):
            return  str(reaction.emoji) in ['✅', '❌'] and user == ctx.author
        emoawait, authmsg = await self.bot.wait_for('reaction_add', check=check, timeout=100.0)
        if emoawait.emoji in ['✅'] :
            role = discord.utils.get(ctx.guild.roles, name="Friendly Wars")
            await ctx.author.add_roles(role) 
            await ctx.send(f"{role.name} has been added for {ctx.author.display_name}")
        elif emoawait.emoji in ['❌'] :
            role = discord.utils.get(ctx.guild.roles, name="Friendly Wars")
            await ctx.author.remove_roles(role) 
            await ctx.send(f"{role.name} has been removed for {ctx.author.display_name}")
        else:
            pass

def setup(bot):
    bot.add_cog(role(bot))               