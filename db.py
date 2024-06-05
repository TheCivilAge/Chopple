import sqlite3,random
from models import Character
from os import path

ROOT = path.dirname(path.realpath(__file__))

def createId():
    return random.getrandbits(28)

def connect():
    conn= sqlite3.connect(path.join(ROOT, "Characters.db"))
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Characters (Id INTEGER PRIMARY KEY, Name varchar(30), Pic varchar(255), Saga varchar(40), Affiliation varchar(255))")
    conn.commit()
    conn.close()

def insert(Character):
    conn= sqlite3.connect(path.join(ROOT, "Characters.db"))
    cur = conn.cursor()
    cur.execute("INSERT INTO Characters VALUES (?,?,?,?,?)", (
        Character.Id,
        Character.Name,
        Character.Pic,
        Character.Saga,
        Character.Affiliation
    ))
    conn.commit()
    conn.close()

def getItem(Id):
    conn= sqlite3.connect(path.join(ROOT, "Characters.db"))
    cur = conn.cursor()
    if isinstance(Id,int):
        cur.execute("SELECT * FROM Characters WHERE Id=?",[Id])
    else:
        cur.execute("SELECT * FROM Characters WHERE Name=?",[Id])
    rows = cur.fetchall()
    characterList=[]
    for i in rows:
        character = Character(i[0],i[1], i[2], i[3],i[4])
        characterList.append(character)
    conn.commit()
    conn.close()
    return characterList[0]

    
def view():
    conn= sqlite3.connect(path.join(ROOT, "Characters.db"))
    cur = conn.cursor()
    cur.execute("SELECT * FROM Characters")
    rows = cur.fetchall()
    characterList = []
    for i in rows:
        character = Character(i[0],i[1], i[2], i[3],i[4])
        characterList.append(character)
    conn.close()
    return characterList