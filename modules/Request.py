from modules.Document import Document, RedditDocument, ArxivDocument
from modules.Author import Author
from datetime import datetime
from modules.Corpus import Corpus
from modules.DocumentGenerator import DocumentGenerator

import praw
import urllib, urllib.request, xmltodict

class Request:
    
    def __init__(self):
        self.cpt = 0
        self.dicDoc = {}
        self.dicAuthor = {}
    
    def fetchReddit(self):
        reddit = praw.Reddit(
             client_id="hlsFU3IkM2cOeG_rxaI7NQ",
             client_secret="51Lc0MLl9-4BzD3UCxD94yiOOwR_hg",
             user_agent="testscript by u/fakebot3",
             username="FeckNeck",
        )
        
        ml_subreddit = reddit.subreddit('MachineLearning')    
        for post in ml_subreddit.hot(limit=10):
            date = datetime.fromtimestamp(post.created_utc)
            name = str(post.author)
            doc = DocumentGenerator.factory('reddit',post.title,name,str(date),post.url,post.selftext,score=post.score,nbComments=post.num_comments)
            self.dicDoc[self.cpt] = doc
            author = Author(name)
            if not(name in self.dicAuthor):
                self.dicAuthor[name] = author
            self.dicAuthor[name].add(doc)
            self.cpt = self.cpt + 1
        
    def fecthArxiv(self):
        url = 'http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=5'
        data = urllib.request.urlopen(url)
        xml = xmltodict.parse(data.read().decode('utf-8'))
        
        for i in xml['feed']['entry']:
            listAuthor = []
            listLink = []
            primaryAuthor = i['author'][0]['name']
            for j in range(1,len(i['author'])): #Multiple authors in one document
                name = i['author'][j]['name']
                listAuthor.append(name)
                author = Author(name)
                doc = Document(i['title'],name,i['published'],listLink,i['summary'])
                if not(name in self.dicAuthor):
                    self.dicAuthor[name] = author
                self.dicAuthor[name].add(doc)
            for j in i['link']: #Multiple links in one document
                listLink.append(j['@href'])
            doc = DocumentGenerator.factory('arxiv',i['title'],primaryAuthor,i['published'],listLink,i['summary'],coAuthors=listAuthor)
            self.dicDoc[self.cpt] = doc
            self.cpt = self.cpt +1
    
    def getDicDoc(self):
        return self.dicDoc

    def getDicAuthor(self):
        return self.dicAuthor