from logger import Logger
from collector import Collector
from enricher import Enricher
import pandas as pd
import os


def main():
    logger = Logger()
    df = pd.DataFrame()
    logger.info('Main','main','Inicializar clase Logger')
    collector = Collector(logger=logger)
    df = collector.collector_data()
    if not df.empty:
        enricher = Enricher(logger=logger)
        df_enriched = enricher.calcular_informacion_kpi(df)

        # Guardar enriquecido adicional como dolar_data_enricher.csv
        save_enriched_path = os.path.join('src', 'indicador_economico', 'static', 'data', 'dolar_data_enricher.csv')
        df_enriched.to_csv(save_enriched_path, index=False)

        save_path = os.path.join('src', 'indicador_economico', 'static', 'data', 'historical.csv')
        df.to_csv(save_path, index=False)
        
        logger.info('Main', 'main', f'Datos guardados exitosamente en {save_path}')
    else:
        logger.warning('Main', 'main', 'El DataFrame está vacío. No se guardó el archivo.')


if __name__ == "__main__":
    main()