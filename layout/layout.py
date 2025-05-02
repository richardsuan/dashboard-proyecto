from layout.components import filter_section, anomaly_section, graph_tabs
from services import data_service
from dash import dcc, html, Input, Output, callback

df_columns = data_service.get_data_columns()

app_layout = html.Div([
    # Almacenamiento del cliente seleccionado
    dcc.Store(id='selected-client', storage_type='memory'),

    # Encabezado 
    html.Div([
        html.Div([
            html.H1('Contugas - Sistema de Detección de Anomalías', className='header-title'),
            html.Button('CONTUGAS', className='header-button')
        ], className='header-content')
    ], className='header'),

    # Cuerpo Principal
    html.Div(className='main-body', children=[
        # Columna izquierda - Filtros y Anomalías
        html.Div(className='left-column', children=[
            filter_section.render(),
            anomaly_section.render()
        ]),

        # Columna central
        html.Div(className='right-column', children=[
            # Fila 1 - Gráfico Principal
            html.Div(className='main-graph-section', children=[
                html.H3(id='main-title', children='Comportamiento y Predicción - Cliente 0790'),
                graph_tabs.render(),
                html.Div(id='main-graph-output', className='main-graph')
            ]),

            # Fila 2 - Relación entre variables y resumen
            html.Div(className='bottom-section', children=[
                html.Div(className='variables-section', children=[
                    html.H3('Relación entre Variables'),
                    html.Label('Eje X:'),
                    dcc.Dropdown(
                        id='x-axis',
                        options=[{'label': i, 'value': i} for i in df_columns],
                        value='Temperatura'
                    ),
                    html.Label('Eje Y:'),
                    dcc.Dropdown(
                        id='y-axis',
                        options=[{'label': i, 'value': i} for i in df_columns],
                        value='Presion'
                    ),
                    dcc.Graph(id='scatter-graph')
                ]),

                html.Div(className='summary-section', children=[
                    html.H3('Resumen Estadístico'),
                    html.Div(id='summary-output'),
                    html.H3('Detalle de Anomalía Predicha'),
                    html.Div(id='anomaly-detail-output'),
                ])
            ])
        ])
    ])
])

# Callback para actualizar el título dinámicamente
@callback(
    Output('main-title', 'children'),
    Input('selected-client', 'data')
)
def update_title(selected_client):
    if selected_client:
        return f'Comportamiento y Predicción - Cliente {selected_client}'
    return 'Comportamiento y Predicción'
