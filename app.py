import dash
from dash import Dash, html, dcc

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
    'background-color': '#0D2438',
    'color': 'white'
},
)

if __name__ == '__main__':
    app.run_server(debug=True)
