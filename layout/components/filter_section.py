from dash import dcc, html, Input, Output, callback
from services.data_service import get_clients

def render():
    # Obtenemos los datos de clientes desde el DataFrame
    df = get_clients()
    clientes = df['Clientes'].unique()  # Obtenemos los clientes únicos

    # Creamos las opciones para el Dropdown
    cliente_options = [{'label': cliente, 'value': cliente} for cliente in clientes]

    return html.Div([
        html.H3('Filtros'),
        html.Div([
            html.Label('Cliente:'),
            dcc.Dropdown(
                id='client-dropdown',  # ID del Dropdown
                options=cliente_options,  # Usamos las opciones generadas dinámicamente
                value=cliente_options[0]['value'] if cliente_options else None  # Valor por defecto
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

# Callback para almacenar el cliente seleccionado
@callback(
    Output('selected-client', 'data'),
    Input('client-dropdown', 'value')
)
def update_selected_client(selected_client):
    return selected_client