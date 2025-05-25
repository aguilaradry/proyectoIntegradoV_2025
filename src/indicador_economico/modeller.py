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
                        'RMSE': round(rmse, 4),
                        'MAE': round(mae, 4),
                        'R2': round(r2, 4),
                        'Directional_Accuracy': round(da, 2)
                    }
                }, f)
            
            # Guardar justificación de métricas
            report_dir = os.path.join('src', 'indicador_economico', 'static', 'reports')
            os.makedirs(report_dir, exist_ok=True)
            
            with open(os.path.join(report_dir, 'metricas.txt'), 'w') as f:
                f.write("JUSTIFICACIÓN DE LA MÉTRICA - RMSE (Root Mean Square Error):\n\n")
                f.write("1. SENSIBILIDAD A OUTLIERS: RMSE penaliza más fuertemente los errores grandes,\n")
                f.write("   lo cual es crucial en mercados financieros donde errores grandes pueden\n")
                f.write("   representar pérdidas significativas.\n\n")
                f.write("2. INTERPRETABILIDAD: RMSE está en las mismas unidades que la variable objetivo,\n")
                f.write("   facilitando la interpretación del error en términos del precio del activo.\n\n")
                f.write("3. OPTIMIZACIÓN: Muchos algoritmos de ML optimizan MSE/RMSE por defecto,\n")
                f.write("   lo que hace que sea consistente con el proceso de entrenamiento.\n\n")
                f.write("4. COMPARABILIDAD: RMSE es ampliamente usado en finanzas cuantitativas,\n")
                f.write("   permitiendo comparar nuestro modelo con benchmarks de la industria.\n\n")
                f.write("MÉTRICAS COMPLEMENTARIAS:\n")
                f.write("   MAE: Menos sensible a outliers, da una idea del error típico.\n\n")
                f.write("   R²: Indica qué proporción de la varianza explica el modelo.\n\n")
                f.write("   Directional_Accuracy: Mide si el modelo predice correctamente la dirección del movimiento.\n\n")                
                f.write("MÉTRICAS DEL MODELO:\n")
                f.write(f" - RMSE: {rmse:.4f}\n")
                f.write(f"   En promedio, el modelo se equivoca por ± {rmse:.4f} unidades monetarias (ej: pesos o dólares) en sus predicciones.\n")   
                f.write(f" - MAE : {mae:.4f}\n")
                f.write(f"   El error promedio absoluto del modelo es de {mae:.4f} unidades monetarias.\n")   
                f.write(f" - R²  : {r2:.4f}\n")
                f.write(f"   El modelo explica el {r2:.2%} de la variabilidad del precio observado.\n")   
                f.write(f" - Directional Accuracy: {da:.2f}%\n")
                f.write(f"   Un Directional Accuracy del {da:.2f}% significa que el modelo predice correctamente la dirección del movimiento en aproximadamente 3 de cada 4 casos.\n")   

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
            y_true = np.array(y_true)
            y_pred = np.array(y_pred)

            true_diff = np.diff(y_true)
            pred_diff = np.diff(y_pred)

            if len(true_diff) != len(pred_diff):
                min_len = min(len(true_diff), len(pred_diff))
                true_diff = true_diff[:min_len]
                pred_diff = pred_diff[:min_len]

            true_dir = true_diff > 0
            pred_dir = pred_diff > 0
            da = np.mean(true_dir == pred_dir) * 100
            return da
        except Exception as e:
            if self.logger:
                self.logger.error('Modeller', 'calcular_directional_accuracy', f'Error en DA: {e}')
            return np.nan
