from Singleton import singleton 
import re, json, string, math
import numpy as np
from pandas import DataFrame
from matplotlib import pyplot
from scipy.sparse import csr_matrix
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
#import nltk
#nltk.download('stopwords')
from sklearn.feature_extraction.text import CountVectorizer

@singleton
class Corpus:
    
    def __init__(self,nom,dicAuthor,dicDoc,ndoc,nauth):
        self.nom = nom
        self.dicAuthor = dicAuthor
        self.dicDoc = dicDoc
        self.ndoc = ndoc
        self.nauth = nauth

    def __repr__(self):
        rep = 'Corpus : ' + self.nom + '\n'
        for i in self.dicAuthor.values():
            rep += i.__str__();
            

        for i in self.dicDoc.values():
            rep += 'Source : '
            rep += 'Reddit \n' if i.getType() == 'reddit' else 'Arxiv \n'
            rep += i.__str__();
        rep += '\nNombre de docs : ' + str(self.ndoc) + '\n'
        rep += 'Nombre de Autheurs : ' + str(self.nauth) + '\n'
        return rep
    
    def addDocument(self,doc):
        nbDoc = len(self.dicDoc)
        self.dicDoc[nbDoc] = doc
        
    def sortedTile(self, limit):
        dic = dict(sorted(self.dicDoc.items(), key=lambda item: item[1].titre))
        cpt = 1
        for i in dic.values():
            if cpt <= limit:
                print(i)
                cpt += 1

    def sortedDate(self, limit):
        dic = dict(sorted(self.dicDoc.items(), key=lambda item: item[1].date))
        cpt = 1
        for i in dic.values():
            if cpt <= limit:
                print(i)
                cpt += 1
                
    def search(self,motif):
        filtered = {}
        for i,j in self.dicDoc.items():
            if re.search(motif, j.text):
                filtered[i] = j
        return filtered

    def concorde(self,motif,limit = 10):
        data = {
            "contexte gauche" : [],
            "motif trouve" : [],
            "contexte droit" : []
        }
        
        filtered = self.search(motif)
        
        for i in filtered.values():
            txtLimit = limit
            left,right = "...",""
            splice = re.split(motif,i.text)
            if len(splice[0]) < txtLimit or len(splice[1]) < txtLimit:
                txtLimit = len(splice[0])
            for j in range(0,txtLimit):
                left += splice[0][j]
            for k in range(0,txtLimit):
                right += splice[1][k]
            right += "..."
            data["contexte gauche"].append(left)
            data["motif trouve"].append(motif)
            data["contexte droit"].append(right)
            
        df = DataFrame(data)
        return df
        
    def nettoyer_texte(self):
        cleaned = ""
        for i,j in self.dicDoc.items():
           cleaned += re.sub('[^a-zA-Z  ]+','', j.text.lower())
        cleaned = re.sub('\t','',cleaned)
        parsed = cleaned.split(' ')
        filtered = list(dict.fromkeys(parsed))
        for i in list(filtered):
           if len(i) <= 1:
               filtered.remove(i)
        filtered.sort()
        return filtered
    
    #Ah-Pine version
    def clean_doc(self):
        text = ""
        
        for i in self.dicDoc.values():
            text += i.text
        
        tokens = word_tokenize(text)
        tokens = [w.lower() for w in tokens]
        tokens = [word for word in tokens if len(word) > 1]
        
        re_punc = re.compile('[%s]' % re.escape(string.punctuation))
        
        stripped = [re_punc.sub('',w) for w in tokens]
        words = [word for word in stripped if word.isalpha()]
        
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if not w in stop_words]
        
        stemmer = SnowballStemmer(language='english')
        stemmed = [stemmer.stem(word) for word in words]
        stemmed = list(dict.fromkeys(stemmed))

        return stemmed
        
    def wordFrequency(self,limit = 0):
        dictionary = self.nettoyer_texte()
        #dictionary = self.clean_text_V2()
        #dictionary = list(dict.fromkeys(dictionary))
        
        data = {
            "word": [],
            "counts": [],
            "frequency": [],
            "document frequency": [],
        }
        
        for i in dictionary:
            data["word"].append(i)
            docFreq = 0
            wordCount = 0
            freq = 0
            for k in self.dicDoc.values():
                if k.text.count(i) > 0:
                    docFreq += 1
                wordCount += k.text.count(i)
            data["counts"].append(wordCount)
            freq = round(wordCount/len(dictionary)*100,2)
            data["frequency"].append(str(freq) + " %")
            data["document frequency"].append(docFreq)
        df = DataFrame(data)
        df = df.sort_values("counts",ascending=False);
        
        if limit > 0:
            print(df.head(limit))
        else:
            print(df)
    
    # -- TP 7 -- #
    def createVocab(self):
        #dictionary = self.nettoyer_texte()
        dictionary = self.clean_doc()
        vocab = {}
        cpt = 0
        for i in dictionary:
            wordCount = 0
            cpt += 1
            for k in self.dicDoc.values():
                wordCount += k.text.lower().count(i)
            vocab[i] = {
                    "id":cpt,
                    "nb total occurence":wordCount
                }
        #print(json.dumps(vocab, indent=4))
        return vocab
   
    def createTF(self):
        vocab = self.createVocab()
        matrix = np.zeros((len(self.dicDoc),len(vocab)))
        index = 0
        for i in vocab.keys():
            for j,k in self.dicDoc.items():
                wordCount = k.text.count(i)
                matrix[j][index] = wordCount
            index += 1
               
        #mat_TF = csr_matrix(matrix)
        return matrix
    
    def ceateIDF(self):
        vocab = self.nettoyer_texte()
        IDF = np.empty(len(vocab))
        
        for i in range(0,len(vocab)):
            wordCount = 0
            for j,k in self.dicDoc.items():
                if k.text.count(vocab[i]) > 0:
                    wordCount += 1
            if wordCount == 0: wordCount = 1
            IDF[i] = math.log(len(self.dicDoc)/wordCount)
            
        return IDF
    
    def createMatTF_IDF(self):
        TF = self.createTF()
        IDF = self.ceateIDF()
        mat_TFxIDF = []
        for i in TF: 
            mat_TFxIDF.append(i * IDF)
        return mat_TFxIDF
    
    def searchEngine(self):
        #keywords = input('Keywords : ').lower()
        keywords = 'poupette sky'
        keywords = keywords.split(' ')
        
        vocab = self.createVocab()
        
        mat_TF = self.createTF()

        vecKeyword = [0] * len(vocab)
        vecScore = []
        
        for i in keywords:
            if i in vocab:
                index = list(vocab).index(i)
                vecKeyword[index] = 1
        
        for i in mat_TF:
            row = np.array(i, int)
            score = np.dot(row,vecKeyword)
            vecScore.append(score)
        
        df = DataFrame(vecScore,columns=['Score'])
        df = df.sort_values(by='Score',ascending=False)
        bar = df.plot.bar()
        bar.set_xlabel("Documents")
    
    def getDicDoc(self):
        return self.dicDoc