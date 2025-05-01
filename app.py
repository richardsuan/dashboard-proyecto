import dash

from layout import layout
from callbacks import main_callbacks, scatter_callbacks

app = dash.Dash(__name__)
app.title = 'Contugas - Sistema de Detección de Anomalías'
app.layout = layout.app_layout

# Inicializar los callbacks
main_callbacks.register_callbacks(app)
scatter_callbacks.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
