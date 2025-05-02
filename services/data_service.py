import pandas as pd
import requests
# Datos de ejemplo (simulando una fuente de datos externa)
data = {
    'Fecha': pd.date_range(start='2023-04-01', periods=35, freq='D'),
    'Volumen': [200 + i + (i % 5) * 10 for i in range(35)],
    'Presion': [30 + (i % 10) for i in range(35)],
    'Temperatura': [20 + (i % 7) for i in range(35)]
}
df = pd.DataFrame(data)

def get_data():
    # modi
    """Simula la obtención de datos."""
    return df.copy()  # Devuelve una copia para evitar modificaciones accidentales

def get_clients():
    """Obtiene los datos de clientes desde un endpoint remoto."""
    try:
        response = requests.get("http://localhost:8080/clients")
        response.raise_for_status()  # Lanza una excepción si la respuesta tiene un error HTTP
        clients = response.json()  # Parseamos la respuesta JSON
        
        # Ajustamos la longitud de la lista de clientes para que coincida con el DataFrame
        if len(clients) < len(df):
            clients.extend(['Desconocido'] * (len(df) - len(clients)))  # Rellenamos con 'Desconocido'
        else:
            clients = clients[:len(df)]  # Cortamos la lista si es más larga que el DataFrame
        
        df['Clientes'] = clients  # Agregamos los clientes al DataFrame
    except requests.RequestException as e:
        print(f"Error al obtener los datos: {e}")
        df['Clientes'] = ['Desconocido'] * len(df)  # En caso de error, rellenamos con valores por defecto
    return df.copy()  # Devuelve una copia para evitar modificaciones accidentales

def get_data_columns(client_name, variable):
    """
    Obtiene los datos de una variable específica para un cliente desde un endpoint remoto.
    """
    try:
        # Definimos la URL del endpoint y el payload
        url = "http://localhost:8080/clients/data"
        payload = {
            "client_name": client_name,
            "variable": variable
        }
        headers = {"Content-Type": "application/json"}

        # Realizamos la solicitud POST
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Lanza una excepción si la respuesta tiene un error HTTP

        # Parseamos la respuesta JSON
        data = response.json()

        # Extraemos las columnas de los datos obtenidos
        if data and isinstance(data, list):
            return list(data[0].keys())  # Retorna las claves del primer elemento como columnas
        else:
            return []  # Retorna una lista vacía si no hay datos
    except requests.RequestException as e:
        print(f"Error al obtener los datos: {e}")
        return []  # En caso de error, retorna una lista vacía
