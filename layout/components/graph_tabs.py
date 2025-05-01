from dash import dcc

def render():
    return dcc.Tabs(id='tabs', value='Volumen', children=[
        dcc.Tab(label='Volumen', value='Volumen'),
        dcc.Tab(label='Presion', value='Presion'),
        dcc.Tab(label='Temperatura', value='Temperatura'),
    ])
