from dash import dcc, html

def render():
    return html.Div([
        html.H3('Filtros'),
        html.Div([
            html.Label('Cliente:'),
            dcc.Dropdown(
                options=[{'label': 'Cliente Industrial 078', 'value': '078'}],
                value='078'
            ),
            html.Label('Periodo:'),
            dcc.Dropdown(
                options=[
                    {'label': 'Últimos 30 días + 15 de predicción', 'value': '30dias'}
                ],
                value='30dias'
            ),
        ])
    ])
