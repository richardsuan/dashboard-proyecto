from layout.components import filter_section, anomaly_section, graph_tabs
from services import data_service
from dash import dcc, html, Input, Output, callback, callback_context
import pandas as pd
import plotly.express as px

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
                html.H3(id='main-title', children='Comportamiento y Predicción - Cliente'),
                graph_tabs.render(),
                dcc.Graph(id='scatter-graph')  # Gráfica que será actualizada dinámicamente
            ]),

            # Fila 2 - Relación entre variables y resumen
            html.Div(className='bottom-section', children=[
                html.Div(className='variables-section', children=[
                    html.H3('Relación entre Variables'),
                    html.Label('Eje X:'),
                    dcc.Dropdown(
                        id='x-axis',
                        options=[],  # Opciones dinámicas
                        value=None  # Valor por defecto
                    ),
                    html.Label('Eje Y:'),
                    dcc.Dropdown(
                        id='y-axis',
                        options=[],  # Opciones dinámicas
                        value=None  # Valor por defecto
                    ),
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

@callback(
    Output('main-title', 'children'),
    Input('selected-client', 'data')
)
def update_title(selected_client):
    if selected_client:
        return f'Comportamiento y Predicción - Cliente {selected_client}'
    return 'Comportamiento y Predicción'

@callback(
    [Output('x-axis', 'options'),
     Output('y-axis', 'options'),
     Output('scatter-graph', 'figure')],
    [Input('selected-client', 'data'),
     Input('graph-tabs', 'value'),
     Input('x-axis', 'value'),
     Input('y-axis', 'value')]
)
def update_graph_and_dropdowns(selected_client, selected_tab, x_axis_value, y_axis_value):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

    if not selected_client or not selected_tab:
        return [], [], {
            'data': [],
            'layout': {
                'title': 'Seleccione un cliente y una pestaña para visualizar la gráfica'
            }
        }

    data = data_service.get_data_columns(selected_client)
    df = pd.DataFrame(data)
    dropdown_options = [{'label': col, 'value': col} for col in df.columns]

    figure = {}

    if triggered_id == 'selected-client' or triggered_id == 'graph-tabs':
        # Inicializar la gráfica con los datos del cliente y la pestaña
        if not df.empty:
            figure = px.line(df, x='Fecha', y=selected_tab.capitalize(),
                             title=f'{selected_tab.capitalize()} para {selected_client}')
        else:
            figure = {"layout": {"title": f"No hay datos disponibles para {selected_client}"}}

    elif triggered_id == 'x-axis' or triggered_id == 'y-axis':
        # Actualizar la gráfica basado en los ejes seleccionados
        if df is not None and not df.empty and x_axis_value in df.columns and y_axis_value in df.columns:
            figure = px.scatter(df, x=x_axis_value, y=y_axis_value, trendline="ols",
                                 title=f'Gráfica de {y_axis_value} vs {x_axis_value} para {selected_client}')
        else:
            figure = {"layout": {"title": "Seleccione variables válidas para los ejes X e Y"}}

    return dropdown_options, dropdown_options, figure