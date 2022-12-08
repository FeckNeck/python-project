from Document import RedditDocument, ArxivDocument

class DocumentGenerator:
    
    @staticmethod
    def factory(type,titre,auteur,date,url,text,score="",nbComments="",coAuthors=[]):
        if type == 'reddit': return RedditDocument(titre,auteur,date,url,text,score,nbComments)
        if type == 'arxiv': return ArxivDocument(titre,auteur,date,url,text,coAuthors)
        
        assert 0, "Erreur : " + type