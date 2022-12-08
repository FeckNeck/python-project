class Author:
    
    def __init__(self,name):
        self.name = name
        self.production = []
    
    def add(self,doc):
        self.production.append(doc)
    
    def __str__(self):
        nbdoc = len(self.production)
        ch = 'Author : ' + self.name + '\n ndoc : ' + str(nbdoc) + '\n docs : ' + '\n'
        for i in self.production:
            ch += i.__str__();
        ch += '\n'
        return ch

    def stats(self):
        ch = 'Nb docs : ' + str(len(self.production)) + '\n'
        somme = 0
        for i in self.production:
            somme = somme + len(i.getText())
        moyenne = somme/len(self.production)
        ch += 'Taille moyenne : ' + str(moyenne)
        print(ch)