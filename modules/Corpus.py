# from modules.Singleton import singleton
import re
import string
import math
import numpy as np
from pandas import DataFrame
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
#import nltk
# nltk.download('stopwords')


class Corpus:

    def __init__(self, nom, dicAuthor, dicDoc, ndoc, nauth):
        self.nom = nom
        self.dicAuthor = dicAuthor
        self.dicDoc = dicDoc
        self.ndoc = ndoc
        self.nauth = nauth

    def __repr__(self):
        rep = 'Corpus : ' + self.nom + '\n'
        for i in self.dicAuthor.values():
            rep += i.__str__()

        for i in self.dicDoc.values():
            rep += 'Source : '
            rep += 'Reddit \n' if i.getType() == 'reddit' else 'Arxiv \n'
            rep += i.__str__()
        rep += '\nNombre de docs : ' + str(self.ndoc) + '\n'
        rep += 'Nombre de Autheurs : ' + str(self.nauth) + '\n'
        return rep

    def getDicDoc(self):
        return self.dicDoc

    def setDicDoc(self, newDic):
        self.dicDoc = newDic

    def addDocument(self, doc):
        nbDoc = len(self.dicDoc)
        self.dicDoc[nbDoc] = doc

    def sortByTitle(self):
        dic = dict(sorted(self.dicDoc.items(), key=lambda item: item[1].titre))
        return dic

    def sortByDate(self):
        dic = dict(sorted(self.dicDoc.items(), key=lambda item: item[1].date))
        return dic

    def search(self, motif):
        filtered = {}
        for i, j in self.dicDoc.items():
            if re.search(motif, j.text):
                filtered[i] = j
        return filtered

    def concorde(self, motif, limit=20):
        data = {
            "contexte gauche": [],
            "motif trouve": [],
            "contexte droit": []
        }

        filtered = self.search(motif)

        for i in filtered.values():
            left, right = "...", ""
            words = i.text.partition(motif)
            for j in range(0, limit):
                if j < len(words[0]):
                    left += words[0][j]
            for j in range(0, limit):
                if j < len(words[2]):
                    right += words[2][j]
            right += "..."
            data["contexte gauche"].append(left)
            data["motif trouve"].append(motif)
            data["contexte droit"].append(right)

        df = DataFrame(data)
        return df

    def nettoyer_texte(self):
        cleaned = ""
        for i, j in self.dicDoc.items():
            cleaned += re.sub('[^a-zA-Z  ]+', '', j.text.lower())
        cleaned = re.sub('\t', '', cleaned)
        parsed = cleaned.split(' ')
        filtered = list(dict.fromkeys(parsed))
        for i in list(filtered):
            if len(i) <= 1:
                filtered.remove(i)
        filtered.sort()
        return filtered

    # Ah-Pine version
    def clean_doc(self):
        text = ""

        for i in self.dicDoc.values():
            text += i.text

        tokens = word_tokenize(text)
        tokens = [w.lower() for w in tokens]
        tokens = [word for word in tokens if len(word) > 1]

        re_punc = re.compile('[%s]' % re.escape(string.punctuation))

        stripped = [re_punc.sub('', w) for w in tokens]
        words = [word for word in stripped if word.isalpha()]

        stop_words = set(stopwords.words('english'))
        words = [w for w in words if not w in stop_words]

        # Racinisation
        # stemmer = SnowballStemmer(language='english')
        # stemmed = [stemmer.stem(word) for word in words]

        final = list(dict.fromkeys(words))

        return final

    def wordFrequency(self, limit=0):
        dictionary = self.clean_doc()
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
            freq = round(wordCount/len(dictionary)*100, 2)
            data["frequency"].append(str(freq) + " %")
            data["document frequency"].append(docFreq)
        df = DataFrame(data)
        df = df.sort_values("counts", ascending=False)

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
                "id": cpt,
                "nb total occurence": wordCount
            }
        #print(json.dumps(vocab, indent=4))
        return vocab

    def createTF(self):
        vocab = self.createVocab()
        matrix = np.zeros((len(self.dicDoc), len(vocab)))
        index = 0
        for i in vocab.keys():
            for j, k in self.dicDoc.items():
                wordCount = k.text.count(i)
                matrix[j][index] = wordCount
            index += 1

        #mat_TF = csr_matrix(matrix)
        return matrix

    def createIDF(self):
        vocab = self.clean_doc()
        IDF = np.empty(len(vocab))

        for i in range(0, len(vocab)):
            wordCount = 0
            for j, k in self.dicDoc.items():
                if k.text.count(vocab[i]) > 0:
                    wordCount += 1
            if wordCount == 0:
                wordCount = 1
            IDF[i] = math.log(len(self.dicDoc)/wordCount)

        return IDF

    def createMatTF_IDF(self):
        TF = self.createTF()
        IDF = self.createIDF()
        mat_TFxIDF = []
        for i in TF:
            mat_TFxIDF.append(i * IDF)
        return mat_TFxIDF

    def create_BM25(self, words):
        avgdl = 0
        for i in self.dicDoc.values():
            avgdl += len(i.text.split())
        avgdl = avgdl/len(self.dicDoc)
        k = 1.2
        b = 0.75
        vecScore = [0] * len(self.dicDoc)
        for i in words:
            for k, j in self.dicDoc.items():
                f = 0
                D = len(j.text.split())
                if i in j.text:
                    f = j.text.count(i) / D
                deno = (f + k * (1 - b + b * (D/avgdl)))
                if deno:
                    idf = f*(k+1) / deno
                    vecScore[k] = idf
        df = DataFrame(vecScore, columns=['score'])
        return df

    def searchEngine(self, motif, methode='TF'):
        keywords = motif.split()
        if methode == 'BM25':
            df = self.create_BM25(keywords)
            return df

        vocab = self.createVocab()
        if methode == 'TF':
            mat_TF = self.createTF()
        if methode == 'TF-IDF':
            mat_TF = self.createMatTF_IDF()

        vecKeyword = [0] * len(vocab)
        vecScore = []

        for i in keywords:
            if i in vocab:
                index = list(vocab).index(i)
                vecKeyword[index] = 1

        for i in mat_TF:
            row = np.array(i, int)
            score = np.dot(row, vecKeyword)
            vecScore.append(score)

        df = DataFrame(vecScore, columns=['score'])
        return df
