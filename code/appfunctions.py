import random
import re
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
#filepath=''
filepath="/storage/emulated/0/Android/data/com.managepass/"

def saltprov(newsalt=0):
    saltlist=[]
    saltstr=b""
    saltcount=3
    if newsalt==2:
        saltcount=4
        newsalt=1
    if newsalt==1:
        for i in range(saltcount):
            saltlist.append(os.urandom(32))
            saltstr+=saltlist[i]+b"::"
        saltfile=open(".salt","wb")
        saltfile.write(saltstr[:-2])
    else:
        random.seed()
        saltfile=open(".salt","rb")
        saltstr=saltfile.read()
        saltfile.close()
        saltlist=saltstr.split(b"::")
        random.shuffle(saltlist)
        saltstr=b""
        for salt in saltlist:
            saltstr+=salt+b"::"
        saltfile=open(".salt","wb")
        saltfile.write(saltstr[:-2])
    saltfile.close()
    return saltlist

def keyderive(usrsalt, salt, encdatstr, iterindex=18):
    key=enckeyprov(usrsalt, salt, iterindex)
    encmech=Fernet(key)
    try:
        result=str(encmech.decrypt(encdatstr))[2:-1]
        return result+"::key::"+str(key)[2:-1]
    except:
        return "**error**"

def enckeyprov(usrsalt, savedsalt, iterindex):
    dbackend=default_backend()
    kdf = Scrypt(
    length=32,
     salt=savedsalt,
     n=2**iterindex, 
     r=8,
     p=1,
     backend=dbackend)
    key = base64.urlsafe_b64encode(kdf.derive(bytes(usrsalt,'ascii')))
    return key

def savedata(passwlist,key):
    datfile = open(".data","wb")
    finalstr=""
    usrsalt=""
    for passw in passwlist:
        finalstr+=passw+":"+passwlist[passw]+"##next##"
        if passwlist[passw][:7]=="**usr**":
            usrsalt=passwlist[passw][7:]
    finalstr=finalstr[:-8]
    encmech = Fernet(key)
    datfile.write(encmech.encrypt(bytes(finalstr,'ascii')))
    datfile.close()

def quickkeyderive(salt, mpassw):
    dbackend=default_backend()
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
     salt=salt,
     iterations=100000,
     backend=dbackend)
    return(base64.urlsafe_b64encode(kdf.derive(bytes(mpassw,'ascii'))))


def quicksavedata(site_name, passw, mpassw):
    saltfile=open(".tempsalt","rb")
    salt=saltfile.read()
    datstr=b""
    if salt==b"":
        datfile=open(".tempdata","wb")
        saltfile.close()
        saltfile=open(".tempsalt",'wb')
        salt=os.urandom(16)
        saltfile.write(salt)
        saltfile.close()
    else:
        datfile=open(".tempdata","rb")
        datstr=datfile.read()
        datfile.close()
        datfile=open(".tempdata","wb")
        
    key=quickkeyderive(salt, mpassw)
    encmech=Fernet(key)
    datstr+=encmech.encrypt(bytes(site_name+":"+passw,"ascii"))+b"::"
    datfile.write(datstr)
    datfile.close()
    

