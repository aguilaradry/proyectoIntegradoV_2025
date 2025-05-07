from logger import Logger
from collector import Collector
import pandas as pd
import os


def main():
    logger = Logger()
    df = pd.DataFrame()
    logger.info('Main','main','Inicializar clase Logger')
    collector = Collector(logger=logger)
    df = collector.collector_data()
    if not df.empty:
        save_path = os.path.join('src', 'proyecto', 'static', 'data', 'dolar_australiano_data.csv')
        df.to_csv(save_path, index=False)
        logger.info('Main', 'main', f'Datos guardados exitosamente en {save_path}')
    else:
        logger.warning('Main', 'main', 'El DataFrame está vacío. No se guardó el archivo.')


if __name__ == "__main__":
    main()