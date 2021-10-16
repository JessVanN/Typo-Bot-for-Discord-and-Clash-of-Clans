#updatebot
import pandas as pd
from pandas.io.json import json_normalize
import requests
import asyncio
import bdGX
import json
import aiohttp
import time
from tabulate import tabulate
pd.set_option('mode.chained_assignment', None)
pd.set_option('precision',18)
pd.set_option('display.float_format', lambda x: '%18.f' % x)
from discord import Webhook, RequestsWebhookAdapter
import os
import APIkeys
import logging
import logging.handlers
handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE", "./tpyolog.log"))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
log = logging.getLogger()
log.setLevel(os.environ.get("LOGLEVEL", "INFO"))
log.addHandler(handler)

webhook = Webhook.from_url("https://discordapp.com/api/webhooks/655146873212108821/2lTgSZC0TnWAgscVLZtip5YBSPZeCsJd0UQb111HqFGINxpozdEAkc_-iCW5MjMfYg-w", adapter=RequestsWebhookAdapter())

ipaddressforkey = requests.get('https://api.ipify.org').text
def fix_clashtag(tag):
    tag=str(tag)
    if tag[0] == '#':
        fixedtag = '%23' + tag[1:].upper()
    elif tag[0] == '%':
        fixedtag = tag.upper()
    else:
        fixedtag = '%23' + tag.upper()
    return fixedtag

async def get_players_info(inputtag, session):
    mykey = APIkeys.get_bearer_key(ipaddressforkey)
    fixedtag = fix_clashtag(inputtag)
    url = 'https://api.clashofclans.com/v1/players/' + fixedtag
    headers = {"Accept": "application/json", "authorization": mykey}
    async with session.get(url,headers=headers) as response:
    #response = requests.get(url, headers=headers)
        try:
            if response.status == 200:  # 200 response is success
                player_data = await response.json()
                return player_data
            else:
                async with session.get(url,headers=headers) as response:
                #response = requests.get(url, headers=headers)
                    try:
                        if response.status == 200:  # 200 response is success
                            player_data = await response.json()
                            return player_data
                        else:
                            webhook.send(f'Oh No: API error: new ban? {inputtag}', username='TypoUpdate')
                    except:
                        pass
        except:
            pass

async def get_clan_info(inputtag,session):
    mykey = APIkeys.get_bearer_key(ipaddressforkey)
    fixedtag = fix_clashtag(inputtag)
    url = 'https://api.clashofclans.com/v1/clans/' + fixedtag
    headers = {"Accept": "application/json", "authorization": mykey}
    async with session.get(url,headers=headers) as response:
        try:
            assert response.status == 200  # 200 response is success
            clan_data = await response.json()
            return clan_data
        except: 
            pass

async def update():
    dfmaster = pd.read_excel("MemberDatabase GX tpyo.xlsx")
    async with aiohttp.TCPConnector(limit=40) as connector:
        async with aiohttp.ClientSession(connector=connector) as session:
            ctl2=pd.read_excel("GXclans.xlsx")
            clanjson=[]
            clanlist=ctl2["ID"].tolist()
            for x in clanlist:
               try:
                    data = await get_clan_info(x, session)
                    if len(data)>1:
                        clanjson.append(data)
               except:
                    pass
    df= json_normalize(clanjson)
    memdf= json_normalize(clanjson, record_path='memberList', meta= ['tag'], record_prefix="mem_")
    df.drop(labels = ["badgeUrls.large", "badgeUrls.medium", "badgeUrls.small"], axis= 'columns', inplace= True)
    df.reset_index()
    memdf.reset_index()
    mems = memdf["mem_tag"]
    DFadd=dfmaster.loc[dfmaster['STATUS'] == "Current"]
    mems=mems.append(DFadd.Tag)
    mems.drop_duplicates(inplace=True) 
    memjson=[]
    async with aiohttp.TCPConnector(limit=47) as connector:
        async with aiohttp.ClientSession(connector=connector) as session:
            for row in mems:
                try:
                    data= await get_players_info(row,session) 
                    if len(data)>1:
                        memjson.append(data)
                except:
                    pass
    playdf= json_normalize(memjson)
    playdf=playdf.rename(columns={"tag":"mem_tag"})
    
    heroesdf= json_normalize(memjson, record_path='heroes', meta= ['tag'], record_prefix="hero_")
    heroesdf=  heroesdf.pivot(index="tag", columns="hero_name", values="hero_level")
    memdf= playdf.merge(heroesdf, how="left", left_on="mem_tag", right_index=True, sort=True)
    
    spellsdf= json_normalize(memjson, record_path='spells', meta= ['tag'], record_prefix="spell_")
    spellsdf=  spellsdf.pivot(index="tag", columns="spell_name", values="spell_level")
    memdf= memdf.merge(spellsdf, how="left", left_on="mem_tag", right_index=True, sort=True)
    
    troopsdf= json_normalize(memjson, record_path='troops', meta= ['tag'], record_prefix="troop_")
    def duptroop(row):
        if row["troop_village"]=="builderBase":
            return f"{row['troop_name']} BB"
        else:
            return f"{row['troop_name']}"
    troopsdf["troop_name"]=troopsdf.apply(duptroop, axis = 1)
    troopsdf=  troopsdf.pivot(index="tag", columns="troop_name", values="troop_level")
    memdf= memdf.merge(troopsdf, how="left", left_on="mem_tag", right_index=True, sort=True)
    
    achievementsdf= json_normalize(memjson, record_path='achievements', meta= ['tag'], record_prefix="achievement_")
    achievementsdf=achievementsdf[achievementsdf["achievement_name"]!="Keep your village safe"]
    achievementsdf=achievementsdf[achievementsdf["achievement_name"]!="Keep Your Account Safe!"] #duplicated in api th14 updatwe
    achievementsdf=  achievementsdf.pivot(index="tag", columns="achievement_name", values="achievement_value")

    memdf= memdf.merge(achievementsdf, how="left", left_on="mem_tag", right_index=True, sort=True)
    
#    df.to_excel("clanfull data.xlsx")
#    memdf.to_excel("memfull data.xlsx")
    
    memdf2 = memdf[['mem_tag', 'clan.name', 'clan.tag', 'name', 'role', "townHallLevel", "townHallWeaponLevel",  'Archer Queen', 'Barbarian King', 'Grand Warden','Royal Champion']]
    memdf2= memdf2.rename(columns={"clan.tag":"clan_tag", "clan.name":"clan_name", "townHallLevel":"TH"})
    #up to this point have same API data as master now we need to compare and update
    
    #this section is who moved
    dfmaster2 = dfmaster[["Tag", "CurrentName", "STATUS", "LastDate",'clan_tag','clan_name']]
    dfmaster2=dfmaster2.rename(columns={"clan_tag":"startclan","clan_name":"startname"})
        
    merger1= dfmaster2.merge(memdf2, how="outer", left_on="Tag", right_on="mem_tag", sort=True)
    
    merger1['change'] = merger1.apply(bdGX.moveact, axis = 1)
    merger1.loc[merger1['change']==' moved to the void','clan_name']=' '
    merger1.loc[merger1['change']==' moved to the void','clan_tag']=' '
    merger2 = merger1.copy()
    merger2 = merger2.loc[merger2['change'] != "Unknown"]
    
    dfthhero= dfmaster[["Tag", "CurrentName", "STATUS", "LastDate", 'clan_tag','clan_name', 'TH',  'Archer Queen', 'Barbarian King', 'Grand Warden','Royal Champion',"AssgnClan"]]
    dfthhero=dfthhero.rename(columns={"clan_tag":"startclan","clan_name":"startname"})
    dfthhero2= dfthhero.merge(memdf2, how="outer", left_on="Tag", right_on="mem_tag", sort=True, suffixes=('_old','_new'))
    dfthhero2['change'] = dfthhero2.apply(bdGX.moveact, axis = 1)
    dfthhero3= dfthhero2.loc[dfthhero2['change'] != "Unknown"]
    dfthhero3= dfthhero3.loc[dfthhero2['TH_new'] >3]
    dfthhero3= dfthhero3.loc[dfthhero2['TH_old'] >3]
    dfth=dfthhero3.loc[dfthhero3['TH_new'] != dfthhero3['TH_old']]
    dfth = dfth[["Tag", "CurrentName", 'TH_new', 'TH_old']]
    
    merger2['Tag'] = merger2.apply(bdGX.addtagvalues, axis='columns')
    merger3=merger2[['Tag', 'clan_name', 'clan_tag',"startname", 'name', 'role', "TH", "townHallWeaponLevel",  'Archer Queen', 'Barbarian King', 'Grand Warden', "Royal Champion", 'change']]
    merger3=merger3.rename(columns={"mem_tag":"Tag"})
    merger3.set_index("Tag", inplace=True)
    dfmaster.set_index("Tag", inplace=True)
    update1=memdf2[['mem_tag', 'clan_name', 'clan_tag', 'name', 'role', "TH", "townHallWeaponLevel",  'Archer Queen', 'Barbarian King', 'Grand Warden', "Royal Champion"]]
    update1=update1.rename(columns={"mem_tag":"Tag"})
    update1.set_index("Tag", inplace=True)
    dfmaster.update(update1)
    dfmaster.update(merger3)
     
    merger4=merger3['change']
    dfmasterupdated=dfmaster.merge(merger4, how="outer", left_on='Tag', right_on='Tag')
    merger5=merger3['startname']
    dfmasterupdated=dfmasterupdated.merge(merger5, how="outer", left_on='Tag', right_on='Tag')
    dfmasterupdated.update(merger3)
    try:
        dfmasterupdated['STATUS'] = dfmasterupdated.apply(bdGX.updateStatus, args=([clanlist]), axis = 1)
    except KeyError:
        pass
    try:
        dfkicked=dfmasterupdated[dfmasterupdated['AssgnClan']=='KICK']
        dfkicked=dfkicked[dfkicked['STATUS']=='Current']
    except:
        pass
    try:
        dfmasterupdated['FirstDate'] = dfmasterupdated.apply(bdGX.updatefd, axis = 1)
        dfmasterupdated['FirstDate'] = pd.to_datetime(dfmasterupdated['FirstDate'], format = '%Y-%m-%d')
        dfmasterupdated['FirstDate'] = dfmasterupdated['FirstDate'].dt.date
    except KeyError:
        pass
    try:
        dfmasterupdated['LastDate'] = pd.to_datetime(dfmasterupdated['LastDate'], format = '%Y-%m-%d')
        dfmasterupdated['LastDate'] = dfmasterupdated.apply(bdGX.updateld,args=([clanlist]), axis = 1)
        dfmasterupdated['LastDate'] = pd.to_datetime(dfmasterupdated['LastDate'], format = '%Y-%m-%d')
    except KeyError:
        pass  
    try:    
        dfmasterupdated['PreviousName'] = dfmasterupdated.apply(bdGX.updateprevname, axis = 1) 
    except KeyError:
        pass 
    try:
        dfupdates2 = pd.DataFrame()
        dfupdates2= dfmasterupdated.dropna(subset=['CurrentName'])
        dfupdates2=dfupdates2.loc[dfupdates2['name'] != dfupdates2['CurrentName']]
        dfupdates2=dfupdates2[['CurrentName', 'name']]
    except KeyError:
        pass
    dfmasterupdated['CurrentName'] = dfmasterupdated.apply(bdGX.updatecurrentname, axis = 1)
    try:
        dfupdatesmove = pd.DataFrame()
        dfupdates= dfmasterupdated.dropna(subset=['change'])
        dfupdates= dfupdates.loc[dfupdates['change'] != "No Change"]
        dfupdatesmove=dfupdates[['CurrentName','TH','startname','change', 'clan_name']]
    except KeyError:
        pass
    dfmasterupdated['Grand Warden'].fillna(0, inplace=True)
    dfmasterupdated['Archer Queen'].fillna(0, inplace=True)
    dfmasterupdated['Barbarian King'].fillna(0, inplace=True)
    dfmasterupdated['Royal Champion'].fillna(0, inplace=True)
    dfmasterupdated['heroes']= dfmasterupdated['Barbarian King'].map(int).map(str)+'/'+dfmasterupdated['Archer Queen'].map(int).map(str) +'/'+dfmasterupdated['Grand Warden'].map(int).map(str)+'/'+dfmasterupdated['Royal Champion'].map(int).map(str)
    dfmasterupdated.drop(labels = ["change",'startname'], axis= 'columns', inplace= True)
    dfmasterupdated.DiscordID=dfmasterupdated.DiscordID.fillna(0).astype(str)
    dfmasterupdated.sort_values(['LastDate', "FirstDate","CurrentName"], axis=0, ascending=False, inplace=True, na_position='last')
    dfmasterupdated=dfmasterupdated[['CurrentName', 'PreviousName', 'DiscordID', 'FirstDate','LastDate', 'STATUS', 'IsElder', 'ReadRules', 'Note', 'clan_name', 'clan_tag', 'name', 'role', 'TH', 'townHallWeaponLevel', 'Archer Queen','Barbarian King', 'Grand Warden', 'Royal Champion', 'heroes','AssgnClan', 'DOB']]
    dfmasterupdated.to_excel("MemberDatabase GX tpyo.xlsx")
    try:
        if dfupdatesmove.empty:
            pass
        else:
            dfupdatesmove = dfupdatesmove.reset_index()
            df_lines = [f'{row.CurrentName:<10} {row.TH:<2} {row.Tag:<10}: {row.startname}{row.change}{row.clan_name}' for row in dfupdatesmove.itertuples()]
            webhook.send("**Members who have moved since last update**", username='TypoUpdate')
            df_send = "```\nName Moved to \n"
            for line in df_lines:
                new_df_send = f'{df_send}{line}\n'
                if len(new_df_send) > 1997:
                    webhook.send(f'{df_send}```', username='TypoUpdate')
                    df_send = f'```\n'
                else:
                    df_send = new_df_send
            time.sleep(1)
            webhook.send(f'{df_send}```', username='TypoUpdate')
    except KeyError:
        pass
    try:
        if dfupdates2.empty:
            pass
        else:
            webhook.send("**Members who have changed names since last update**", username='TypoUpdate')
            time.sleep(1)
            webhook.send(dfupdates2, username='TypoUpdate')
    except KeyError:
        pass
    try:
        if dfth.empty:
            pass
        else:
            webhook.send("**Members who have Upgraded TH levels**", username='TypoUpdate')
            time.sleep(1)
            webhook.send(tabulate(dfth, headers="keys")[0:1999], username='TypoUpdate')
    except KeyError:
        pass
    try:
        if len(dfkicked)>0:
            dfkicked=dfkicked[['CurrentName','TH','clan_name']]
            webhook.send("**WARNING THE FOLLOWING WAS MARKED AS KICKED (RECENTLY JOINED OR LEFT)**", username='TypoUpdate')
            time.sleep(1)
            webhook.send(tabulate(dfkicked, headers="keys"), username='TypoUpdate')
        else:
            pass
    except KeyError:
        pass

while __name__=='__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(update())
    except:
        time.sleep(3570)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(update())
    time.sleep(3570)                 
