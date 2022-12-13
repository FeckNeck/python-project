import dash
from dash import html, dcc, callback, Input, Output, dash_table
import plotly.express as px
import pandas as pd
from modules.Json import Json
from wordcloud import WordCloud
import matplotlib.pyplot as plt


json = Json()
corpus = json.loadCorpus()
dicDoc = corpus.getDicDoc()
dicDoc = corpus.sortByTitle()
# words = corpus.clean_doc()
# text = ' '.join(words)

# wordcloud = WordCloud(background_color = 'white',max_words = 50).generate(text)
# plt.imshow(wordcloud)
# plt.axis("off")
# plt.savefig('assets/Images/wordCloud.png')
# plt.show();

documents = {
    'Author': [],
    'Title': [],
    'Text': [],
    'Date': []
}

concordancer = {
    "contexte gauche": [],
    "motif trouve": [],
    "contexte droit": []
}

for i, j in dicDoc.items():
    documents['Author'].append(j.auteur)
    documents['Title'].append(j.titre)
    documents['Text'].append(j.text)
    documents['Date'].append(j.date)

df = pd.DataFrame(documents)
dc = pd.DataFrame(concordancer)

dash.register_page(__name__, path='/')

fig = px.bar(labels={
    'index': 'documents', 'value': 'score'}, color_discrete_map={'score': '#2dd4bf'})
fig.update_layout(paper_bgcolor="#102D44",
                  plot_bgcolor='#102D44', font_color='white')


layout = html.Section([
    html.Div([  # -- Filter Container -- #
        html.Div([  # -- Input Search -- #
            html.Img(src='./assets/images/search.svg', className="svg"),
            dcc.Input(id="search", type="search", placeholder="search..."),
        ],
            className="input_container"
        ),
        dcc.Input(id="limit", type="number", value=10,
                  placeholder="Limit", min="10", max="30")
    ],
        className='filters_container'
    ),
    html.Div(  # -- Table Documents -- #
        dash_table.DataTable(
            fill_width=True,
            virtualization=True,
            data=df.to_dict('records'),
            style_header={
                'backgroundColor': '#1E3851',
                'border': '2px solid #102D44',
                'color': 'white',
                'textAlign': 'left',
            },
            style_data={
                'backgroundColor': '#102D44',
                'border': '2px solid #1E3851',
                'color': 'white',
                'textAlign': 'left'
            },

        ),
    ),
    html.Div([  # -- Container Concordancer -- #
        html.Div([
            dash_table.DataTable(
                id='concord',
                columns=[{"name": i, "id": i} for i in dc.columns],
                style_header={
                    'backgroundColor': '#1E3851',
                    'border': '2px solid #102D44',
                    'color': 'white',
                    'textAlign': 'left',
                },
                style_cell={
                    'backgroundColor': '#102D44',
                    'border': '2px solid #1E3851',
                    'color': 'white',
                    'textAlign': 'left'
                },
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'motif trouve'},
                        'textAlign': 'center'
                    }
                ]
            ),
            html.Img(src='./assets/images/wordCloud.png',style={'padding':'1rem 0'}),
        ]),
        dcc.Graph(id='graph', figure=fig)
    ],
        className='concorde_container'
    ),
],
    className="container")


# @callback(
#     Output("concord", "data"),
#     Output("graph", "figure"),
#     Input("search", "value"),
#     Input("limit", "value"),
# )

@callback(Output('concord', 'data'), Input('search', 'value'), Input("limit", "value"))
def updateTable(input_value, limit):
    if input_value == '':
        df = pd.DataFrame()
        return df.to_dict('records')
    df = corpus.concorde(input_value, limit)
    return df.to_dict('records')

@callback(Output("graph", "figure"), Input('search', 'value'))
def updateGraph(input_value):
    graph = corpus.searchEngine(input_value)
    fig = px.bar(graph, labels={
        'index': 'documents', 'value': 'score'}, color_discrete_map={'score': '#2dd4bf'})
    fig.update_layout(paper_bgcolor="#102D44",
                      plot_bgcolor='#102D44',
                      font_color='white',
                      hoverlabel={
                          'bgcolor': '#1E3851'
                      })
    return fig