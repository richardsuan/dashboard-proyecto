from dash import dcc, html
from services.data_service import get_clients
from dash import dcc, html, Input, Output, callback
import pandas as pd 

def render():
    # Obtenemos los datos de clientes desde el DataFrame
    df = get_clients()
    clientes = df['Clientes'].unique()

    cliente_options = [{'label': cliente, 'value': cliente} for cliente in clientes]    
    return html.Div([
        html.H3('Filtros'),
        html.Div([
            html.Label('Cliente:'),
            dcc.Dropdown(
                id='client-dropdown',
                options=cliente_options,
                value=cliente_options[0]['value'] if cliente_options else None
            ),
            html.Label('Rango de Fechas:'),
            dcc.DatePickerRange(
                id='date-picker-range',
                min_date_allowed=None,
                max_date_allowed=None,
                start_date=None,
                end_date=None,
                display_format='YYYY-MM-DD',
                className='custom-date-picker'
            ),
        ])
    ])


@callback(
    [Output('date-picker-range', 'min_date_allowed'),
     Output('date-picker-range', 'max_date_allowed'),
     Output('date-picker-range', 'start_date'),
     Output('date-picker-range', 'end_date')],
    Input('client-data', 'data')
)
def update_date_range(client_data):
    if not client_data:
        return None, None, None, None

    try:
        df = pd.DataFrame(client_data)
        if 'Fecha' not in df.columns:
            return None, None, None, None

        df['Fecha'] = pd.to_datetime(df['Fecha'])

        min_date = df['Fecha'].min().date()
        max_date = df['Fecha'].max().date()

        return min_date, max_date, min_date, max_date
    except Exception as e:
        print(f"Error al procesar fechas: {e}")
        return None, None, None, None