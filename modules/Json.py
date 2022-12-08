import json, jsonpickle

class Json:
    
    def __init__(self):
        self.corpus = {}
        
    def saveCorpus(self,corpus):
        jsonCorpus = jsonpickle.encode(corpus,indent=4,make_refs=False)
        with open('json_data.json', 'w') as outfile:
            json.dump(jsonCorpus, outfile)
            
    def loadCorpus(self):
        with open('json_data.json', 'r') as f:
            j = json.load(f)
            self.corpus = jsonpickle.decode(j)

    def getCorpus(self):
        return self.corpus