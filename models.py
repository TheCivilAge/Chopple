
class Character:
    
    def __init__(self,Id,Name,Pic, Saga, Affiliation):
        self.Id=Id
        self.Name=Name
        self.Pic=Pic
        self.Saga=Saga
        self.Affiliation=Affiliation

    def getID(self):
        return self.Id
    
    def __str__(self):
      return str(self.Id)+" "+self.Name+" "+self.Saga+" "+self.Affiliation 

    def __eq__(self, other):
         
         return self.Id==other.Id
class Game:
    def __init__(self,Id,Date,CorrectCharacter,Win):
        self.Id=Id
        self.Date=Date
        self.CorrectCharacter=CorrectCharacter
        self.Win=Win