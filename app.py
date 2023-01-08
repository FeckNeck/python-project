import dash
from dash import Dash, html, dcc

# ----- # - Create Corpus file - # ----- #

#from modules.Corpus import Corpus
#from modules.Api import Api
#
#api = Api()
#api.fetchReddit()
#api.fetchArxiv()
#
#dicDoc = api.getDicDoc()
#dicAuth = api.getDicAuthor()
#
#corpus = Corpus('Corpus Arxiv/Reddit', dicAuth,
#                dicDoc, len(dicDoc), len(dicAuth))
#
#api.saveCorpus(corpus)
#
## ----- # - Create WordCloud - # ----- #
#import matplotlib.pyplot as plt
#from wordcloud import WordCloud
#words = corpus.clean_doc()
#text = ' '.join(words)
#
#wordcloud = WordCloud(background_color='white', max_words=50).generate(text)
#plt.imshow(wordcloud)
#plt.axis("off")
#plt.savefig('assets/images/wordCloud.png')


app = Dash(__name__, suppress_callback_exceptions=True, use_pages=True)

app.layout = html.Div([

    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']}", href=page["relative_path"],
                ),
                className='link',
            )
            for page in dash.page_registry.values()
        ],
        className="header",
    ),

    dash.page_container,
],
    style={
    'min-height': '100vh',
    'background-color': '#0D2438',
    'color': 'white'
},
)

if __name__ == '__main__':
    app.run_server(debug=True)
