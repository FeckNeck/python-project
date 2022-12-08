import dash
from dash import Dash, html, dcc

# request = Request()
# request.fetchReddit()
# request.fecthArxiv()

# dicDoc = request.getDicDoc()
# dicAuthor = request.getDicAuthor()

# corpus = Corpus('corpus 2',dicAuthor,dicDoc,len(dicDoc),len(dicAuthor))


app = Dash(__name__, use_pages=True)

# app.layout = html.Div([

#     html.Div(
#         [
#             html.Div(
#                 dcc.Link(
#                     f"{page['name']}", href=page["relative_path"],
#                 ),
#                 className='link',
#             )
#             for page in dash.page_registry.values()
#         ],
#         className="header",
#     ),

#  	dash.page_container,
# ],
#     style={"height": "100vh",
#             'background-color':'#0D2438',
#             'color':'white'
#             },
# )

# if __name__ == '__main__':
#  	app.run_server(debug=True)