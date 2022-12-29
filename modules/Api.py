from modules.Document import Document
from modules.Author import Author
from datetime import datetime
from modules.DocumentGenerator import DocumentGenerator

import praw
import urllib
import urllib.request
import xmltodict
import pickle


class Api:

    def __init__(self):
        self.cpt = 0
        self.dicDoc = {}
        self.dicAuthor = {}

    def fetchReddit(self, limit=15):
        reddit = praw.Reddit(
            client_id="hlsFU3IkM2cOeG_rxaI7NQ",
            client_secret="51Lc0MLl9-4BzD3UCxD94yiOOwR_hg",
            user_agent="testscript by u/fakebot3",
            username="FeckNeck",
        )

        ml_subreddit = reddit.subreddit('MachineLearning')
        for post in ml_subreddit.hot(limit=limit):
            date = str(datetime.fromtimestamp(post.created_utc))
            date = date.split()[0]
            name = str(post.author)
            doc = DocumentGenerator.factory('reddit', post.title, name, str(
                date), post.url, post.selftext, score=post.score, nbComments=post.num_comments)
            self.dicDoc[self.cpt] = doc
            author = Author(name)
            if not(name in self.dicAuthor):
                self.dicAuthor[name] = author
            self.dicAuthor[name].add(doc)
            self.cpt = self.cpt + 1

    def fetchArxiv(self, limit=15):
        url = 'http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=' + \
            str(limit)
        data = urllib.request.urlopen(url)
        xml = xmltodict.parse(data.read().decode('utf-8'))

        for i in xml['feed']['entry']:
            listAuthor = []
            listLink = []
            if isinstance(i['author'], list):  # Multiple authors in one document
                primaryAuthor = i['author'][0]['name']
                for j in range(1, len(i['author'])):
                    name = i['author'][j]['name']
                    listAuthor.append(name)
                    author = Author(name)
                    doc = Document(i['title'], name, i['published'],
                                   listLink, i['summary'])
                    if not(name in self.dicAuthor):
                        self.dicAuthor[name] = author
                    self.dicAuthor[name].add(doc)
            else:
                primaryAuthor = i['author']['name']
            for j in i['link']:  # Multiple links in one document
                listLink.append(j['@href'])
            date = i['published'].replace('T', ' ')
            date = date.split()[0]
            doc = DocumentGenerator.factory(
                'arxiv', i['title'], primaryAuthor, date, listLink, i['summary'], coAuthors=listAuthor)
            self.dicDoc[self.cpt] = doc
            self.cpt = self.cpt + 1

    def saveCorpus(self, corpus):
        with open("data/corpus.pkl", "wb") as f:
            pickle.dump(corpus, f)

    def loadCorpus(self):
        with open("data/corpus.pkl", "rb") as f:
            corpus = pickle.load(f)
            return corpus

    def getDicDoc(self):
        return self.dicDoc

    def getDicAuthor(self):
        return self.dicAuthor
