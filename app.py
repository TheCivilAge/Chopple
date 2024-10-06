from flask import Flask, render_template,request,url_for
import sqlite3, random, datetime,db
from models import Character
from PIL import Image, ImageFilter
from base64 import b64decode
import urllib.request


"""To Do:
 How to play page type

 form vailator for name entry

 remove daily character from data

 Fix guess table no picture
 save previous games as obj 
 Dark mode - browser preferneces
 session cookies?
"""

db.connect()

def initialize():
    data={}
    gameCondition= 0
    guesses=[]
    lives=6
    values={}

    characterList=db.view()
    characterNames=[]
    dailyCharacter=dailyCharacterSelect()

    for character in characterList:
        characterNames.append(character.Name)
    characterNames.sort()
    data={
         "characterNames": characterNames,
         "gameCondition":   gameCondition,
         "guesses": guesses,
         "numGuesses":0,
         "lives": lives,
         "correctCharacter": dailyCharacter,
         "values":values,
         "errorMsg":""
    }
    #hint(data['correctCharacter'])

    print("initialized")
    print(dailyCharacter)
    return data
     

def dailyCharacterSelect():
    #radnomly selects a character from database
    randomCharacter=random.choice(db.view())
    return randomCharacter

def getCharacter(guessedCharacter):
    #Finds a character in database based of character ID / Name
    character=db.getItem(guessedCharacter)
    return character

def compare(character, dailyCharacter):
    values=[False, False,False]
    if character.Name<dailyCharacter.Name:
        values[0]=True
    if character.Saga==dailyCharacter.Saga:
        values[1]=True
    if character.Affiliation==dailyCharacter.Affiliation:
        values[2]=True

    return values

def guess(guessedCharacter):
    """
    if the correct character is guess the user wins
    if the incorrect character is guessed
        -check if it already exists in previous guesses
        -if not add this character to guessed characters
        -compare characters
        -take a life off
    """
    if guessedCharacter == data['correctCharacter']:
        data['gameCondition']=1
        data['numGuesses']=len(data['guesses'])
    else:
        if guessedCharacter in data['guesses']:
            data['errorMsg']="This character was already guessed."
        else:
            if data['lives']==0:
                data['gameCondition']=-1
            else:
                data['guesses'].append(guessedCharacter)
                data['values'][guessedCharacter.Name]=compare(guessedCharacter,data['correctCharacter'])
                data['lives']-=1
                data["errorMsg"]=""

def hint(dailyCharacter):
    #No hint image blur is not good enough and and cropping doesn't work as there are other charcaters in the shot
    url=dailyCharacter.Pic
    urllib.request.urlretrieve(url,"dailyCharacter.png")
    im=Image.open(r"dailyCharacter.png")
    newIm = im.filter(ImageFilter.BLUR)    
    newIm.show()
    newIm.save("hint.png")
    print("hint working")
         
app=Flask(__name__)
data=initialize()

@app.route("/", methods=['GET','POST'])
def index():
    if(request.method=='GET'):
        # Stops unboundlocal variable error
        global data
        data['characterNames']
        newdata=initialize()
        data=newdata.copy()
        print(data)

    if(request.method=='POST'):
        guessedCharacter=request.form['Guess']
        try:
            guess(getCharacter(guessedCharacter))
            print(data)
        except:
            data['errorMsg']="This is not a valid character"
    
    return render_template('index.html',data=data,characterNames=data['characterNames'])

@app.route("/how to play")
def howToPlay():
    return render_template('how to play.html')

@app.route("/Previous Days")
def previousDays():
    return render_template('Previous Days.html')

if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)
