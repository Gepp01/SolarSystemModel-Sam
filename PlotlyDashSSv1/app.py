# app.py
from dash import Dash, html, dcc
import dash

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.H1("Solar System Explorer", style={'textAlign':'center'}),
    # Auto-generated nav links
    html.Div([
        dcc.Link(page['name'], href=page['path'], style={'margin':'0 1em'})
        for page in dash.page_registry.values()
    ], style={'textAlign':'center', 'padding':'10px'}),
    html.Hr(),
    dcc.PageContainer()
])