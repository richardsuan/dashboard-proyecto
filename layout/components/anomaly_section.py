from dash import html

def render():
    return html.Div([
        html.H3('Anomalías'),
        html.Div([
            html.Div('Cliente 078 - Alta', style={'backgroundColor': '#FFCCCC', 'padding': '10px'}),
            html.Div('Cliente 078 - Media', style={'backgroundColor': '#CCCCFF', 'padding': '10px'}),
            html.Div('Cliente 078 - Alta', style={'backgroundColor': '#CCCCFF', 'padding': '10px'})
        ]),
        html.Button('Ver todas las anomalías')
    ])
