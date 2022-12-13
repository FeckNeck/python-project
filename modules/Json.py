import json, jsonpickle,pickle

class Json:
        
    def saveCorpus(self,corpus):
        # jsonCorpus = jsonpickle.encode(corpus,indent=4,make_refs=False)
        # with open('data/json_data.json', 'w') as outfile:
        #     json.dump(jsonCorpus, outfile)
        with open("corpus.pkl", "wb") as f:
            pickle.dump(corpus, f)
            
    def loadCorpus(self):
        # Ouverture du fichier, puis lecture avec pickle
        with open("corpus.pkl", "rb") as f:
            corpus = pickle.load(f)
            return corpus