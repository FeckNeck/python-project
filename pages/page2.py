import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import dash
from dash import html, dcc, callback, Input, Output, dash_table 
from Json import Json
from Corpus import Corpus
from Request import Request
import json, jsonpickle

request = Request()
request.fetchReddit()
request.fecthArxiv()

dicDoc = request.getDicDoc()
dicAuthor = request.getDicAuthor()

corpus = Corpus('corpus 2',dicAuthor,dicDoc,len(dicDoc),len(dicAuthor))
json = Json()
json.saveCorpus(corpus)

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.Div([
        html.Img(src='./assets/images/search.svg',className="svg"),
        dcc.Input(id="search", type="text", placeholder="search..."),
    ],
        className="input_container"
        ),
    # html.Div(
    #     dcc.Dropdown(
    #         ['5', '10', '15', '20', '30'],
    #         placeholder="concordancer limit",
    #         searchable=False,
    #         clearable=False,
    #     ),
    #     style={'width':'11%'}
    # ),

    html.Div(id='output'),
])

@callback(
    Output("output", "children"),
    Input("search", "value")
)
def update_city_selected(input_value):
    
    return f'You selected: {input_value}'