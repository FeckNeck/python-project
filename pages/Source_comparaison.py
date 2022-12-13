import dash
from dash import html, dcc, callback, Input, Output, dash_table
import plotly.express as px
import pandas as pd
from modules.Json import Json

json = Json()
corpus = json.loadCorpus()
dicDoc = corpus.getDicDoc()
listAuthor = []

def createDocuments(dicDoc):
    documents = {
        'Author': [],
        'Title': [],
        'Text': [],
        'Date': []
    }
    for i in dicDoc.values():
        documents['Author'].append(i.auteur)
        listAuthor.append(i.auteur)
        documents['Title'].append(i.titre)
        documents['Text'].append(i.text)
        documents['Date'].append(i.date)

    df = pd.DataFrame(documents)
    return df

df = createDocuments(dicDoc)

dash.register_page(__name__)

layout = html.Section([
    html.Div([  # -- Filter Container -- #
        html.Div([  # -- Input Search -- #
            html.Img(src='./assets/images/search.svg', className="svg"),
            dcc.Input(id="search", type="search", placeholder="search..."),
        ],
            className="input_container"
        ),
        dcc.Dropdown(['Text', 'Date'], 'NYC', id='sorter',placeholder='Sort by',style={'width':'6rem'}),
        dcc.Dropdown(['Reddit', 'Arxiv'], 'NYC', id='source',placeholder='Source',style={'width':'6rem'}),
        dcc.Dropdown(listAuthor, 'NYC', id='author',placeholder='Author',style={'width':'15rem'}),
    ],
        className='filters_container'
    ),
    html.Div(  # -- Table Documents -- #
        dash_table.DataTable(
            id='documents',
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
       html.Div(id='xd')
], className="container")


@callback(
    Output(component_id='documents', component_property='data'),
    Input(component_id='sorter', component_property='value')
)
def sortBy(input_value):
    if input_value == 'Text':
        newDic = corpus.sortByTitle()
    elif input_value == 'Date':
        newDic = corpus.sortByDate()
    else:
        newDic = dicDoc
    newDf = createDocuments(newDic)
    return newDf.to_dict('records')