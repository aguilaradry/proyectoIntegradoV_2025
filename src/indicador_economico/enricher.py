import pandas as pd
import numpy as np
import os

class Enricher:
    def __init__(self, logger):
        self.logger = logger

    # KPI (Precio promedio mensual/anual de cierre, Volatilidad histórica mensual, Tendencia interanual (YoY),
    # Máximo y mínimo histórico, Volumen promedio de negociación por trimestre, Días con cambios extremos (+/-5%)).
    def calcular_informacion_kpi(self, df):
        if df.empty:
            self.logger.warning('Enricher', 'calcular_informacion_kpi', 'DataFrame vacío. No se puede enriquecer.')
            return df

        # Copiar el DataFrame para no modificar el original
        df = df.copy()

        # Limpiar y convertir columnas numéricas
        for col in ['abrir', 'max', 'min', 'cerrar', 'cierre_ajustado','volumen']:
            df[col] = df[col].astype(str).str.replace(',', '.', regex=False).str.replace(' ', '', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Convertir fechas
        df['trimestre'] = 'Q' + df['fecha'].dt.quarter.astype(str)

        # KPI Precio promedio mensual/anual de cierre
        df['promedio_mensual_cierre'] = df.groupby(['año', 'mes'])['cerrar'].transform('mean')
        df['promedio_anual_cierre'] = df.groupby(['año'])['cerrar'].transform('mean')

        # KPI Volatilidad mensual
        df['retorno'] = df['cerrar'].pct_change()
        df['volatilidad_mensual'] = df.groupby(['año', 'mes'])['retorno'].transform('std')

        # KPI Tendencia interanual YoY
        try:
            df['cerrar_yoy'] = df.groupby('mes')['cerrar'].transform(lambda x: x.pct_change(1))
        except Exception as e:
            self.logger.warning('Enricher', 'calcular_informacion_kpi', f'Error al calcular YoY: {e}')
            df['cerrar_yoy'] = np.nan

        # KPI Máximo y mínimo histórico
        df['maximo_historico'] = df['cerrar'].cummax()
        df['minimo_historico'] = df['cerrar'].cummin()

        # KPI Volumen promedio de negociación por trimestre
        df['volumen_promedio_trimestral'] = df.groupby(['año', 'trimestre'])['volumen'].transform('mean')

        # KPI Días con cambios extremos (+/-5%)
        df['dias_extremo'] = df['retorno'].abs() >= 0.05

        # Guardar CSV enriquecido
        enriched_path = os.path.join('src', 'indicador_economico', 'static', 'data')
        os.makedirs(enriched_path, exist_ok=True)
        final_path = os.path.join(enriched_path, 'dolar_data_enricher.csv')
        df.to_csv(final_path, index=False)
        self.logger.info('Enricher', 'calcular_informacion_kpi', f'Archivo enriquecido guardado en {final_path}')

        return df
