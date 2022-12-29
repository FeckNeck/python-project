from modules.Api import Api
from modules.Corpus import Corpus
import matplotlib.pyplot as plt
import time

api = Api()
limit = [5, 10, 15, 20, 30, 50, 75, 100]

dic = {
    'TF': [],
    'TF-IDF': [],
    'BM25': [],
}


for i in limit:
    api.fetchReddit(i)
    api.fetchArxiv(i)
    dicDoc = api.getDicDoc()
    dicAuth = api.getDicAuthor()

    corpus = Corpus('Corpus Arxiv/Reddit', dicAuth,
                    dicDoc, len(dicDoc), len(dicAuth))

    for j in dic.keys():
        start = time.time()
        corpus.searchEngine('electron', j)
        end = time.time()
        duration = end - start
        dic[j].append(duration)

for i in dic.keys():
    plt.plot(limit, dic[i], label=i)

plt.legend()
plt.title("calculation time per method")
plt.xlabel("Nb documents")
plt.ylabel("Time execution (s)")
plt.show()
