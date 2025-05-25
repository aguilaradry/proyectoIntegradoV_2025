import os
import pandas as pd
import numpy as np
import pickle
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error, r2_score, mean_absolute_percentage_error, root_mean_squared_error
)
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split


class Modeller:
    def __init__(self, logger=None):
        self.logger = logger
        self.model = None
        self.scaler = None
        self.model_path = os.path.join('src', 'indicador_economico', 'static', 'models', 'model.pkl')
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)

    def entrenar_modelo(self, df: pd.DataFrame, target_col: str = 'cerrar'):
        try:
            # Columnas predictoras
            features = [
                'abrir', 'max', 'min', 'volumen', 'promedio_mensual_cierre',
                'promedio_anual_cierre', 'volatilidad_mensual', 'cerrar_yoy',
                'maximo_historico', 'minimo_historico', 'volumen_promedio_trimestral'
            ]
            df = df.dropna(subset=features + [target_col])
            X = df[features]
            y = df[target_col]

            # Escalamiento robusto
            self.scaler = RobustScaler()
            X_scaled = self.scaler.fit_transform(X)

            # División de datos (sin shuffle por series temporales)
            X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, shuffle=False)

            # Entrenamiento del modelo
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.model.fit(X_train, y_train)

            # Predicciones
            y_pred = self.model.predict(X_test)

            # Métricas
            rmse = root_mean_squared_error(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            da = self.calcular_directional_accuracy(y_test.values, y_pred)

            if self.logger:
                self.logger.info('Modeller', 'entrenar_modelo',
                                 f'Modelo entrenado. RMSE: {rmse:.2f}, MAE: {mae:.2f}, R2: {r2:.2f}, DA: {da:.2f}%')

            # Guardar modelo
            with open(self.model_path, 'wb') as f:
                pickle.dump({
                    'model': self.model,
                    'scaler': self.scaler,
                    'features': features,
                    'fecha_entrenamiento': datetime.now().isoformat(),
                    'metricas': {
                        'RMSE': rmse,
                        'MAE': mae,
                        'R2': r2,
                        'Directional_Accuracy': da
                    }
                }, f)

        except Exception as e:
            if self.logger:
                self.logger.error('Modeller', 'entrenar_modelo', f'Error durante el entrenamiento: {e}')
            raise

    def predecir(self, df: pd.DataFrame) -> pd.Series:
        try:
            with open(self.model_path, 'rb') as f:
                model_bundle = pickle.load(f)
                model = model_bundle['model']
                scaler = model_bundle['scaler']
                features = model_bundle['features']

            df = df.dropna(subset=features)
            X = df[features]
            X_scaled = scaler.transform(X)
            predictions = model.predict(X_scaled)

            return pd.Series(predictions, index=df.index)

        except Exception as e:
            if self.logger:
                self.logger.error('Modeller', 'predecir', f'Error al hacer predicciones: {e}')
            raise

    def calcular_directional_accuracy(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calcula la precisión direccional: % de veces que el modelo predice correctamente si sube o baja.
        """
        try:
            true_diff = np.diff(y_true)
            pred_diff = np.diff(y_pred)
            true_dir = true_diff > 0
            pred_dir = pred_diff > 0
            da = np.mean(true_dir == pred_dir) * 100
            return da
        except Exception as e:
            if self.logger:
                self.logger.error('Modeller', 'calcular_directional_accuracy', f'Error en DA: {e}')
            return np.nan
