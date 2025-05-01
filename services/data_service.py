import pandas as pd

# Datos de ejemplo (simulando una fuente de datos externa)
data = {
    'Fecha': pd.date_range(start='2023-04-01', periods=35, freq='D'),
    'Volumen': [200 + i + (i % 5) * 10 for i in range(35)],
    'Presion': [30 + (i % 10) for i in range(35)],
    'Temperatura': [20 + (i % 7) for i in range(35)]
}
df = pd.DataFrame(data)

def get_data():
    """Simula la obtención de datos."""
    return df.copy()  # Devuelve una copia para evitar modificaciones accidentales

def get_data_columns():
    """Simula la obtención de los nombres de las columnas de los datos."""
    return df.columns.tolist()
