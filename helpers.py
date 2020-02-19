from config import *
from globals import *
from models import *
import re
def isLoggedIn():
    if LOGIN in session and session[LOGIN]==TRUE:
        return True
    return False

def validateData(p1, p2, w):
    if p1 =='' or p2 =='' or w=='':
        return False
    #check if winner name doesnt match any player's name
    if (p1!=w and p2!=w): 
        return False

    #names should only be numberic or contain spaces
    regex = r'([a-zA-Z]+( )?)*'
    if re.match (regex, p1).group(0)!=p1 or re.search (regex, p2).group(0)!=p2:
        return False
    
    return True

def insertPlayer (p):
    exists = Player.query.filter_by(name=p).first()
    if exists is None:
        #player is not in Players db, add him to it and set wins = 0
        player = Player (p)
        db.session.add (player)
        db.session.commit ()

def updateWinCount(w):
    player = Player.query.filter_by (name=w).first()
    player.wins+=1
    db.session.add (player)
    db.session.commit ()

#to clean the input string
def clean (str):
    if str != '':
        str = str.split()[0]
        str = str.lower()
        #str = re.sub(r'[^a-zA-Z ]', '', str)
    return str