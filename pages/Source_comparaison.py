import dash
from dash import html, dcc, callback, Input, Output, State, dash_table
import plotly.express as px
import pandas as pd
from modules.Json import Json
from datetime import datetime

json = Json()
corpus = json.loadCorpus()
dicDoc = corpus.getDicDoc()


def createDocuments(dicDoc):  # -- Ceate clean dataframe of documents -- #
    documents = {
        'ID': [],
        'Author': [],
        'Title': [],
        'Text': [],
        'Date': []
    }
    for j, i in dicDoc.items():
        documents['ID'].append(j)
        documents['Author'].append(i.auteur)
        documents['Title'].append(i.titre)
        documents['Text'].append(i.text)
        documents['Date'].append(i.date)

    df = pd.DataFrame(documents)
    return df


df = createDocuments(dicDoc)

# -- Dates for slider -- #
dicDates = {i: datetime.strptime(j, "%Y-%m-%d").date()
            for i, j in enumerate(df['Date'].sort_values())}
listDates = (list(dicDates.keys()))
minDate, maxDate = dicDates[0], dicDates[len(dicDates) - 1]
# ---------------------- #

dash.register_page(__name__)

layout = html.Section([
    html.Div([  # -- Filter Container -- #
        html.Div([  # -- Input Search -- #
            html.Img(src='./assets/images/search.svg', className="svg"),
            dcc.Input(id="search", type="search", placeholder="search..."),
        ],
            className="input_container"
        ),
        dcc.Dropdown(['Title', 'Date'], 'Sorter', id='sorter',
                     placeholder='Sort by', style={'width': '6rem'}),
        dcc.Dropdown(['Reddit', 'Arxiv'], 'Source', id='source',
                     placeholder='Source', style={'width': '7rem'}),
        dcc.Dropdown(df['Author'], id='author',
                     placeholder='Author', style={'width': '15rem'}),
    ],
        className='filters_container'
    ),
    html.Div(  # -- Slider -- #
        dcc.RangeSlider(id='slider',
                        min=listDates[0], max=listDates[-1], marks=dicDates, step=None, className='Slider'),
        style={'padding-bottom': '2rem'}
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
    # -- Graph -- #
    dcc.Graph(id='graph_TF', style={'padding': '2rem 0'}),
], className="container")


@callback(  # -- Filter Table  and Update Graph-- #
    Output('documents', 'data'),
    Output('graph_TF', 'figure'),
    Input('search', 'value'),
    State('search', 'value'),
    Input('sorter', 'value'),
    Input('source', 'value'),
    Input('author', 'value'),
    [Input('slider', 'value')]
)
def Filter(search_value, state, sort_value, source_value, author_value, dates):
    newDic = dicDoc.copy()

    global minDate, maxDate

    if dates:
        dates.sort()
        minDate = dicDates[dates[0]]
        maxDate = dicDates[dates[1]]

    if sort_value == 'Title':
        newDic = corpus.sortByTitle()
    elif sort_value == 'Date':
        newDic = corpus.sortByDate()

    if source_value == 'Reddit' or source_value == 'Arxiv':
        newDic = {i: j for i, j in newDic.items() if j.getType()
                  == source_value}
    if author_value:
        newDic = {i: j for i, j in newDic.items() if j.getAuthor()
                  == author_value}
    if search_value:
        newDic = {i: j for i, j in newDic.items(
        ) if search_value in j.getText().lower()}

    newDic = {i: j for i, j in newDic.items() if j.getDate() >=
              minDate and j.getDate() <= maxDate}

    newDf = createDocuments(newDic)

    if state:
        scores = corpus.searchEngine(state)
        scores = scores.filter(items=newDic.keys(), axis=0)
        dates = [x for x in newDf['Date']]
        scores['date'] = dates
        scores = scores.sort_values('date')
        fig = px.line(scores, x='date', y='score',
                      markers=True, color_discrete_sequence=["#2dd4bf"])
        update_fig(fig)
        return newDf.to_dict('records'), fig
    else:
        fig = px.line()
        update_fig(fig)

    return newDf.to_dict('records'), fig


def update_fig(fig):
    fig.update_layout(paper_bgcolor="#102D44",
                      plot_bgcolor='#102D44',
                      font_color='white',

                      hoverlabel={
                          'bgcolor': '#1E3851'
                      })
    fig.update_xaxes(showgrid=True, gridwidth=1,
                     gridcolor='#94a3b8', zeroline=False)
    fig.update_yaxes(showgrid=True, gridwidth=1,
                     gridcolor='#94a3b8', zeroline=False)
