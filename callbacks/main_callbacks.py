from dash import Output, Input, dcc
import plotly.express as px
from services import data_service  # Importa el servicio de datos

def register_callbacks(app):
    @app.callback(
        Output('main-graph-output', 'children'),
        Input('tabs', 'value')
    )
    def update_main_graph(tab):
        df = data_service.get_data()
        fig = px.line(df, x='Fecha', y=tab.capitalize(), title=f'{tab.capitalize()} en el tiempo')
        return dcc.Graph(figure=fig)


def construir_entrenar_modelo(X_train, y_train, X_test, y_test, dropout1=0.4, dropout2=0.3, dropout3=0.2, l2_reg=0.001, learning_rate=0.0005, patience=15):
    model = Sequential()
    model.add(Dense(128, input_dim=X_train.shape[1], kernel_regularizer=regularizers.l2(l2_reg)))
    model.add(BatchNormalization())
    model.add(LeakyReLU(alpha=0.1))
    model.add(Dropout(dropout1))

    model.add(Dense(64, kernel_regularizer=regularizers.l2(l2_reg)))
    model.add(BatchNormalization())
    model.add(LeakyReLU(alpha=0.1))
    model.add(Dropout(dropout2))

    model.add(Dense(32, kernel_regularizer=regularizers.l2(l2_reg)))
    model.add(BatchNormalization())
    model.add(LeakyReLU(alpha=0.1))
    model.add(Dropout(dropout3))

    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer=Adam(learning_rate=learning_rate), loss='binary_crossentropy', metrics=['AUC'])

    early_stop = EarlyStopping(monitor='val_auc', patience=patience, mode='max', restore_best_weights=True)

    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=300,
        batch_size=32,
        class_weight={0: 1, 1: 50},
        callbacks=[early_stop],
        verbose=1
    )

    return model, history