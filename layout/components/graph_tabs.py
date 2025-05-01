from dash import dcc

def render():
    return dcc.Tabs(
        id='tabs',
        value='volumen',
        className='custom-tabs',
        children=[
            dcc.Tab(label='Volumen', value='volumen', className='custom-tab', selected_className='custom-tab--selected'),
            dcc.Tab(label='Presion', value='presion', className='custom-tab', selected_className='custom-tab--selected'),
            dcc.Tab(label='Temperatura', value='temperatura', className='custom-tab', selected_className='custom-tab--selected'),
        ]
    )