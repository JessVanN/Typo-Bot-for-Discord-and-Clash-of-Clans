import csv
import requests
import operator
import pandas as pd
from pandas.io.json import json_normalize
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import bdGX as bd
import discord
from discord import Webhook, RequestsWebhookAdapter
import time

clantaglist = "GXclans.xlsx"

webhook = Webhook.from_url("https://discordapp.com/api/webhooks/653629653310898187/XAfwTgd7Mkl8FUHMFCiYcGbD4KdSDNvw4TiDDHeLdQuOc-QCQqBtHC-wnusZg95KrCEN", adapter=RequestsWebhookAdapter())

def runstats():
    ctl2=pd.read_excel("GXclans.xlsx")
    clanlist=ctl2["ID"].tolist()

    datenow= date.today()
    dateminus28 = (date.today() + relativedelta(months=-1)).replace(day=1)
    dateplus28 = (date.today() + relativedelta(months=+1)).replace(day=1)
    datenow= datenow.strftime("%m-%d-%Y")
    dateminus28= dateminus28.strftime("%m-%d-%Y")
    print1= "Delta Stats for "+ datenow+' compared to '+ dateminus28
    webhook.send(print1, username='C3PO')
       
    claninfolist = []
    #Read current clan members via API for provided clan tag(s) and generate output stats for them
    for row in clanlist:
        clan_member_list = bd.get_clan_list(row)
        for players in clan_member_list['memberList']:
            try:
                newinfo = bd.get_player_stats(players['tag'])
                claninfolist.append(newinfo)
            except:
                pass
          
    outputXCLdate = "GXRAW_STATS_" + datenow + ".xlsx"
    NewerStatsXCL = "GXRAW_STATS_" + datenow + ".xlsx"
    OlderStatsXCL = "GXRAW_STATS_" + dateminus28 + ".xlsx"
    outputXCL = datenow + '_delta.xlsx'
    NewerStatsXCLdf= json_normalize(claninfolist)
    NewerStatsXCLdf.to_excel(outputXCLdate)
    
    #begin pandas analysis and comparison
    OlderStatsXCLdf= pd.read_excel(OlderStatsXCL)
    NewerStatsXCLdf.set_index("Tag", inplace=True)
    OlderStatsXCLdf.set_index("Tag", inplace=True)
    newnames=NewerStatsXCLdf[['Clan','Name','League','Gold']]
    newnames= newnames.rename(columns={'Gold':'GoldCap'})
    NewerStatsXCLdf=NewerStatsXCLdf.drop(labels=['Clan','Name','League'], axis='columns')
    OlderStatsXCLdf=OlderStatsXCLdf.drop(labels=['Clan','Name','League'], axis='columns')
    DeltaDF=NewerStatsXCLdf.subtract(OlderStatsXCLdf)#subtracts all values providing difference
    
    DeltaDF=DeltaDF.merge(newnames, how="left", on="Tag")
    DeltaDF=DeltaDF[DeltaDF['TH']>=0]
    DeltaDF.drop(labels=['LegendCups', 'TH'], axis=1, inplace=True)
    
    DeltaDF["Activity"]=DeltaDF.apply(bd.activity, axis=1)
    DeltaDF.to_excel(outputXCL)
    
    recordDE=DeltaDF[DeltaDF['DE']>=2487907 ] #Corbin
    recordAttacks=DeltaDF[DeltaDF['Attacks']>=1400] #jess 2 week record set Apr 7, 2018
    recordDefenses=DeltaDF[DeltaDF['Defenses']>=5630] #twodown 2 week record set 
    recordDonations=DeltaDF[DeltaDF['Donations']>=50492] #joan
    recordActivity=DeltaDF[DeltaDF['Activity']>=320.0 ] #kp
    
    DeltaDF.sort_values(by='Donations', ascending=False)
    donations10=DeltaDF.nlargest(10, 'Donations')
    donations10.reset_index(inplace=True)
    df_lines = [f'{row.Index:<3}{row.Donations:<9}{row.Name}' for row in donations10.itertuples()]
    donations10send = "```\n"
    for line in df_lines:
        new_df_send = f'{donations10send}{line}\n'
        donations10send = new_df_send
    
    DeltaDF.sort_values(by='CHL', ascending=False)
    CHL10=DeltaDF.nlargest(10, 'CHL')
    CHL10.reset_index(inplace=True)
    df_lines = [f'{row.Index:<3}{row.CHL:<4}{row.Name}' for row in CHL10.itertuples()]
    CHL10send = "```\n"
    for line in df_lines:
        new_df_send = f'{CHL10send}{line}\n'
        CHL10send = new_df_send
       
    DeltaDF.sort_values(by='Defenses', ascending=False)
    Defenses10=DeltaDF.nlargest(10, 'Defenses')
    Defenses10.reset_index(inplace=True)    
    df_lines = [f'{row.Index:<3}{row.Defenses:<6}{row.Name}' for row in Defenses10.itertuples()]
    Defenses10send = "```\n"
    for line in df_lines:
        new_df_send = f'{Defenses10send}{line}\n'
        Defenses10send = new_df_send
    
    DeltaDF.sort_values(by='WarStars', ascending=False)
    WarStars10=DeltaDF.nlargest(10, 'WarStars')
    WarStars10.reset_index(inplace=True)
    df_lines = [f'{row.Index:<3}{row.WarStars:<5}{row.Name}' for row in WarStars10.itertuples()]
    WarStars10send = "```\n"
    for line in df_lines:
        new_df_send = f'{WarStars10send}{line}\n'
        WarStars10send = new_df_send
    
    DeltaDF.sort_values(by='Attacks', ascending=False)
    Attacks10=DeltaDF.nlargest(10, 'Attacks')
    Attacks10.reset_index(inplace=True)
    df_lines = [f'{row.Index:<3}{row.Attacks:<5}{row.Name}' for row in Attacks10.itertuples()]
    Attacks10send = "```\n"
    for line in df_lines:
        new_df_send = f'{Attacks10send}{line}\n'
        Attacks10send = new_df_send
    
    DeltaDF.sort_values(by='DE', ascending=False)
    DE10=DeltaDF.nlargest(10, 'DE')
    DE10.reset_index(inplace=True)
    df_lines = [f'{row.Index:<3}{row.DE:<11}{row.Name}' for row in DE10.itertuples()]
    DE10send = "```\n"
    for line in df_lines:
        new_df_send = f'{DE10send}{line}\n'
        DE10send = new_df_send
    
    DeltaDF.sort_values(by='ClanGames', ascending=False)
    ClanGames10=DeltaDF.nlargest(10, 'ClanGames')
    ClanGames10=ClanGames10[ClanGames10['ClanGames']>0]
    ClanGames10.reset_index(inplace=True)
    df_lines = [f'{row.Index:<3}{row.ClanGames:<8}{row.Name}' for row in ClanGames10.itertuples()]
    ClanGames10send = "```\n"
    for line in df_lines:
        new_df_send = f'{ClanGames10send}{line}\n'
        ClanGames10send = new_df_send
    
    Activity2=DeltaDF.nlargest(30, 'Activity')
    Activity2.reset_index(inplace=True)
    Activity2.sort_values(by='Activity', ascending=False, inplace=True)
    df_lines = [f'{row.Index:<3}{row.Activity:<6}{row.Name}' for row in Activity2.itertuples()]
    Activitysend = "```\n"
    for line in df_lines:
        new_Activity = f'{Activitysend}{line}\n'
        Activitysend = new_Activity
    #print to discord and run every 2 weeks, with additional text
    print4= "Older File:" + OlderStatsXCL
    print5= "Newer File:" + NewerStatsXCL
    webhook.send(print4, username='C3PO')
    time.sleep(1)
    webhook.send(print5, username='C3PO')
    time.sleep(1)
    webhook.send("__**Top Ten Donators**__", username='C3PO')
    webhook.send(f'{donations10send}```', username='C3PO')
    time.sleep(2)
    webhook.send("__**Top Ten # of Heros Upgraded**__", username='C3PO')
    webhook.send(f'{CHL10send}```', username='C3PO')
    time.sleep(2)
    webhook.send("__**Top Ten Defenses**__", username='C3PO')
    webhook.send(f'{Defenses10send}```', username='C3PO')
    time.sleep(2)
    webhook.send("__**Top Ten WarStars**__", username='C3PO')
    webhook.send(f'{WarStars10send}```', username='C3PO')
    time.sleep(2)
    webhook.send("__**Top Ten # of Successful Attacks**__", username='C3PO')
    webhook.send(f'{Attacks10send}```', username='C3PO')
    time.sleep(2)
    webhook.send("__**Top Ten DE Collected**__", username='C3PO')
    webhook.send(f'{DE10send}```', username='C3PO')
    time.sleep(2)
    webhook.send("__**Top Ten Clan Games Points**__", username='C3PO')
    webhook.send(f'{ClanGames10send}```', username='C3PO')
    time.sleep(2)
    webhook.send("__**Top 30 Members Activity Score**__", username='C3PO')
    webhook.send("Please note: an activity score of 10 represents minimal daily activity", username='C3PO')
    webhook.send(f'{Activitysend}```', username='C3PO')
    time.sleep(2)
    webhook.send(f"The 4 weeks stats are complete. Please run again on {dateplus28}" , username='C3PO')
    if recordDonations.empty:
        pass
    else:
        df_lines = [f'{row.Name} has broken the Donation record: {row.Donations:<7} ' for row in recordDonations.itertuples()]
        Donationsrec = "```\n"
        for line in df_lines:
            new_df_send = f'{Donationsrec}{line}\n'
            Donationsrec = new_df_send
        webhook.send(f'{Donationsrec}```', username='C3PO')
        time.sleep(2)
    if recordDE.empty:
        pass
    else:
        df_lines = [f'{row.Name} has broken the DE record: {row.DE:<7} ' for row in recordDE.itertuples()]
        DErec = "```\n"
        for line in df_lines:
            new_df_send = f'{DErec}{line}\n'
            DErec = new_df_send
        webhook.send(f'{DErec}```', username='C3PO')
        time.sleep(2)
    if recordAttacks.empty:
        pass
    else:
        df_lines = [f'{row.Name} has broken the Attacks record: {row.Attacks:<7} ' for row in recordAttacks.itertuples()]
        Attacksrec = "```\n"
        for line in df_lines:
            new_df_send = f'{Attacksrec}{line}\n'
            Attacksrec = new_df_send
        webhook.send(f'{Attacksrec}```', username='C3PO')
        time.sleep(2)
    if recordActivity.empty:
        pass
    else:
        df_lines = [f'{row.Name} has broken the Activity record: {row.Activity:<7} ' for row in recordActivity.itertuples()]
        Activityrec = "```\n"
        for line in df_lines:
            new_df_send = f'{Activityrec}{line}\n'
            Activityrec = new_df_send
        webhook.send(f'{Activityrec}```', username='C3PO')
        time.sleep(2)
    if recordDefenses.empty:
        pass
    else:
        df_lines = [f'{row.Name} has broken the Defenses record: {row.Defenses:<7} ' for row in recordDefenses.itertuples()]
        Defensesrec = "```\n"
        for line in df_lines:
            new_df_send = f'{Defensesrec}{line}\n'
            Defensesrec = new_df_send
        webhook.send(f'{Defensesrec}```', username='C3PO')
    uploadfile=discord.File(outputXCL)
    webhook.send(file=uploadfile)

while __name__=='__main__':
    try:
        if date.today().day ==1:
            runstats()
    except Exception as ex:
        webhook.send(ex)
        time.sleep(86300) 
        if date.today().day ==1:
            runstats()
    time.sleep(86300)