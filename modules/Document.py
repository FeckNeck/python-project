class Document:
    
    def __init__(self,titre,auteur,date,url,text):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.text = text
    
    def affichage(self):
        print('titre : ', self.titre,'\n', 
              'auteur : ', self.auteur,'\n',
              'date : ', self.date,'\n',
              'url : ', self.url,'\n',
              'text : ', self.text,'\n',)
    
    def getText(self):
        return self.text;
    
    def getType(self):
        pass;

    def __str__(self):
        return 'auteur' + self.auteur + '\ntitre : ' + self.titre + '\n' + 'Date : ' + str(self.date) + '\n'
    
class RedditDocument(Document):
    
    def __init__(self,titre,auteur,date,url,text,score,nbComments):
        Document.__init__(self, titre, auteur, date, url, text)
        self.score = score
        self.nbComments = nbComments
    
    def __str__(self):
        ch = Document.__str__(self)
        ch += 'Score : ' + str(self.score) + '\nNb Comments : ' + str(self.nbComments) + '\n'
        return ch + '\n'
    
    def getType(self):
        return 'reddit'
    
class ArxivDocument(Document):
    
    def __init__(self,titre,auteur,date,url,text,coAuthors):
        Document.__init__(self, titre, auteur, date, url, text)
        self.coAuthors = coAuthors
    
    def __str__(self):
        ch = Document.__str__(self)
        ch += 'Co authors : \n'
        for i in self.coAuthors:
            ch += i + '\n'
        return ch + '\n'
    
    def getType(self):
        return 'arxiv'