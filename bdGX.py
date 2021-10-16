import pandas as pd
import requests
from pandas.io.json import json_normalize
from datetime import date, datetime, timedelta
import csv
import time
import datetime
import APIkeys
from requests import get
pd.set_option('precision',18)
pd.set_option('display.float_format', lambda x: '%18.f' % x)
            
def fix_bottag(tag):
    tag=tag.replace('O','0')
    if tag[0] == '#':
        fixedtag = tag[0] + tag[1:].upper()
    elif tag[0] != '#':
        fixedtag = "#"+ tag[0:].upper()
    return fixedtag

def fix_clashtag(tag):
    tag=str(tag)
    if tag[0] == '#':
        fixedtag = '%23' + tag[1:].upper()
    elif tag[0] == '%':
        fixedtag = tag.upper()
    else:
        fixedtag = '%23' + tag.upper()
    return fixedtag

ipaddressforkey = requests.get('https://api.ipify.org').text
def get_clan_info(inputtag):
    mykey = APIkeys.get_bearer_key(ipaddressforkey)
    fixedtag = fix_clashtag(inputtag)
    url = 'https://api.clashofclans.com/v1/clans/' + fixedtag
    headers = {"Accept": "application/json", "authorization": mykey}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:  # 200 response is success
        clan_data = response.json()
        df1= json_normalize(clan_data)
        memdf= json_normalize(clan_data, record_path='memberList', meta= ['tag'], record_prefix="mem_")
        return df1, memdf
    else: 
        pass

def get_player_info(inputtag):
    mykey = APIkeys.get_bearer_key(ipaddressforkey)
    fixedtag = fix_clashtag(inputtag)
    url = 'https://api.clashofclans.com/v1/players/' + fixedtag
    headers = {"Accept": "application/json", "authorization": mykey}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:  # 200 response is success
        player_data = response.json()
        playdf= json_normalize(player_data)
        heroesdf=pd.DataFrame()
        heroesdf= json_normalize(player_data, record_path='heroes', meta= ['tag'], record_prefix="hero_")
        if heroesdf.empty:
            heroesdf=pd.DataFrame(columns=["tag",'Archer Queen', 'Battle Machine', 'Barbarian King', 'Grand Warden', "Royal Champion"])
            heroesdf['tag']=playdf['tag']
            heroesdf.set_index('tag', inplace=True)
        else:
            heroesdf= heroesdf[["tag", "hero_name", "hero_level", ]]
            heroesdf=  heroesdf.pivot(index="tag", columns="hero_name", values="hero_level")
        return playdf, heroesdf

def moveact(df):
    if df.startclan == df.clan_tag and (not pd.isnull(df['name'])):
        return 'No Change'
    elif pd.isnull(df['name']):
        return 'Unknown'
    elif (not pd.isnull(df.startclan)) and (pd.isnull(df.clan_tag)):
        return ' moved to the void'
    elif (pd.isnull(df.startclan)) and (not pd.isnull(df.clan_tag)):
        return ' is a new/returning join to '
    elif (df.STATUS in ['Applicant','Alt']) and (not pd.isnull(df.clan_tag)):
        return ' is a new/returning join to '
    elif df.startclan != df.clan_tag:
        return ' moved to '
    else:
        return "Unknown"

def addtagvalues(row):
    tag= row[0]
    mem_tag = row[6]
    if pd.isnull(tag):
        return mem_tag
    elif not pd.isnull(tag):
        return tag 

def updateStatus(df, clanlist):
    if (df.clan_tag not in clanlist):
        return 'Gone'
    elif (df.clan_tag in clanlist):
        return 'Current'
    else:
        return df.STATUS
    
def updatefd(df):
    datenow = time.strftime("%Y-%m-%d")
    if pd.isnull(df.FirstDate):
        return datenow
    else:
        return df.FirstDate

def updateld(df,clanlist):
    datenow = datetime.datetime.today()
    date1000 = datetime.datetime.today() + timedelta(1000)
    if (not df.clan_tag in clanlist):
        if datenow<=df.LastDate:
            return datenow
        else:
            return df.LastDate 
    elif (df.clan_tag in clanlist):
        return date1000
    elif df['STATUS'] in ['Kicked']:
        return df.LastDate 
    else:
        return df.LastDate 
    
def updateprevname(df):
    if df['name'] != df['CurrentName']:
        return df.CurrentName
    else:
        return df.PreviousName

def updatecurrentname(df):
    if df['name'] != df['CurrentName']:
        return df['name']
    else:
        return df['CurrentName']


def get_clan_list(clantag):
    mykey = APIkeys.get_bearer_key(ipaddressforkey)
    fixedtag = fix_clashtag(clantag)
    url = 'https://api.clashofclans.com/v1/clans/' + fixedtag
    headers = {"Accept": "application/json", "authorization": mykey}
    # call get service with headers and params
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        clan_data = response.json()
    else:
        clan_data="0"
    return clan_data
         
def get_player_stats(inputtag):
    #Make sure we don't get player info too fast and get shut down
    time.sleep(.001)

    mykey = APIkeys.get_bearer_key(ipaddressforkey)
    fixedtag = fix_clashtag(inputtag)
    url = 'https://api.clashofclans.com/v1/players/' + fixedtag
    headers = {"Accept": "application/json", "authorization": mykey}

    response = requests.get(url, headers=headers)
    thisplayerinfo = {'LegendCups':0,'BestTrophies':0,'Name': '', 'Tag': '', 'TH':'','Gold': 0,'DE': 0,'WarStars': 0,'Attacks': 0,'Defenses': 0,'Donations': 0,'CHL': 0,'ClanGames': 0,'Elixir': 0, 'Clan': '', 'League':''}

    if response.status_code == 200:  # 200 response is success
        player_data = response.json()
        player_name_bytes = player_data['name'].encode(encoding="ascii",errors='replace')
        player_name = player_name_bytes.decode()
        thisplayerinfo['Name'] = player_name
        thisplayerinfo['Tag'] = player_data['tag']
        thisplayerinfo['TH'] = player_data['townHallLevel']
        thisplayerinfo['BestTrophies'] = player_data['bestTrophies']

        if 'legendStatistics' in player_data:
            thisplayerinfo['LegendCups'] = player_data['legendStatistics']['legendTrophies']

        if 'clan' in player_data:
            thisplayerinfo['Clan'] = player_data['clan']['name']

        if 'league' in player_data:
            thisplayerinfo['League'] = player_data['league']['name']

        for ach in player_data['achievements']:
            if ach['name'] == "Gold Grab":
                thisplayerinfo['Gold'] = int(ach['value'])
            elif ach['name'] == "Unbreakable":
                thisplayerinfo['Defenses'] = int(ach['value'])
            elif ach['name'] == "Heroic Heist":
                thisplayerinfo['DE'] = int(ach['value'])
            elif ach['name'] == "Conqueror":
                thisplayerinfo['Attacks'] = int(ach['value'])
            elif ach['name'] == "War Hero":
                thisplayerinfo['WarStars'] = int(ach['value'])
            elif ach['name'] == "Friend in Need":
                thisplayerinfo['Donations'] = int(ach['value'])
            elif ach['name'] == "Elixir Escapade":
                thisplayerinfo['Elixir'] = int(ach['value'])
            elif ach['name'] == "Games Champion":
                thisplayerinfo['ClanGames'] = int(ach['value'])

        for hero in player_data['heroes']:
            if(hero['village']=='home'):
                thisplayerinfo['CHL'] += hero['level']

        return thisplayerinfo
    else:
        pass

def activity(row):
    donation_denominator = 10000
    gold_denominator = 75000000
    attacks_denominator = 250
    de_denominator = 500000
    if row['GoldCap'] == 2000000000:
        Activitynum = (100 / 3) * ((row['Donations'] / donation_denominator) + (row['Attacks'] / attacks_denominator) + (row['DE'] / de_denominator))
    elif row['GoldCap'] < 2000000000:
        Activitynum = (100 / 4) * ((row['Gold'] / gold_denominator)+(row['Donations'] / donation_denominator) + (row['Attacks'] / attacks_denominator) + (row['DE'] / de_denominator))
    Actnum=float(str(round(Activitynum,1)))
    return Actnum

#def updates():
#
#    return dfupdatesmove, dfupdates2, dfth #move, name change, th change

#def combineids(df2):
#    if len(str(df2["DiscordID2"]))==9:
#        df2["DiscordID"]=str(df2.DiscordID1)+str(df2.DiscordID2)
#    else:
#        df2["DiscordID"]=str(df2.DiscordID1)+"0"+str(df2.DiscordID2)
#    return df2["DiscordID"]

def altsname(df2, guild, ctx):
    df2['DiscordName']= " NotAssigned"
    if int(df2['DiscordID']) >1:  #**
        try:
            df2['DiscordName'] = guild.get_member(int(df2["DiscordID"])).display_name
        except ValueError:
            df2['DiscordName'] = " ID-NotInServer"
        except AttributeError:
            df2['DiscordName'] = " ID-NotInServer"
    else:
        pass
    return  df2['DiscordName']
def removenames(df3):
    if df3["count"] > 1:
        df3['DiscordName'] = "\u200b"
    else:
        df3['DiscordName'] = df3['DiscordName'] 
    return  df3['DiscordName']