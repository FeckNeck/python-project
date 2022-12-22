import pickle


class Json:

    def saveCorpus(self, corpus):
        with open("data/corpus.pkl", "wb") as f:
            pickle.dump(corpus, f)

    def loadCorpus(self):
        with open("data/corpus.pkl", "rb") as f:
            corpus = pickle.load(f)
            return corpus
