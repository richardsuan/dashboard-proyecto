from layout.components import filter_section, anomaly_section, graph_tabs
from services import data_service  # Importa el servicio de datos si es necesario para el layout
from dash import dcc, html
# Datos de ejemplo (podrías obtenerlos del servicio aquí si es necesario para la inicialización del layout)
df_columns = data_service.get_data_columns()

app_layout = html.Div([
    # Encabezado Principal
    html.Div([
        html.H1('Contugas - Sistema de Detección de Anomalías', style={'color': 'white'}),
        html.Button('CONTUGAS', style={'float': 'right', 'backgroundColor': '#004080', 'color': 'white'})
    ], style={'backgroundColor': '#004080', 'padding': '10px'}),

    # Contenido Principal en Filas y Columnas
    html.Div(style={'display': 'flex'}, children=[
        # Columna Izquierda - Filtros y Anomalías
        html.Div(style={'width': '20%', 'padding': '10px'}, children=[
            filter_section.render(),
            anomaly_section.render()
        ]),

        # Columna Central - Gráfico Principal
        html.Div(style={'width': '55%', 'padding': '10px'}, children=[
            html.H3('Comportamiento y Predicción - Cliente 078'),
            graph_tabs.render(),
            html.Div(id='main-graph-output') # Contenedor para el gráfico principal
        ]),

        # Columna Derecha - Relación entre Variables y Resumen
        html.Div(style={'width': '25%', 'padding': '10px'}, children=[
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
            dcc.Graph(id='scatter-graph'),
            html.H3('Resumen Estadístico'),
            html.Div(id='summary-output'),
            html.H3('Detalle de Anomalía Predicha'),
            html.Div(id='anomaly-detail-output'),
        ]),
    ])
])
