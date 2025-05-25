import requests
import pandas as pd
from bs4 import BeautifulSoup
from logger import Logger
import os
import time
from datetime import datetime, timedelta

class Collector:
    def __init__(self, logger):
        # Generar timestamps para fechas dinámicas (desde el 8 de noviembre de 2000 hasta hoy)
        fecha_inicio = datetime(2000, 11, 8)
        fecha_fin = datetime.now()
        period1 = int(time.mktime(fecha_inicio.timetuple()))
        period2 = int(time.mktime(fecha_fin.timetuple()))

        # Construir la URL con los timestamps actualizados
        self.url = f'https://es.finance.yahoo.com/quote/6A%3DF/history/?period1={period1}&period2={period2}'
        self.logger = logger

        # Crear carpetas si no existen
        os.makedirs('src/indicador_economico/static/data', exist_ok=True)

    def collector_data(self):
        try:
            df = pd.DataFrame()
            headers= {'User-Agent':'Mozilla/5.0'}
            response = requests.get(self.url,headers=headers)
            if response.status_code != 200:
                self.logger.error("Collector", "collector_data", f"Error al consultar la url : {response.status_code}")
                return df
            soup = BeautifulSoup(response.text,'html.parser')
            table = soup.select_one('div[data-testid="history-table"] table')
            if table is None:
                self.logger.error("Collector", "collector_data","Error al buscar la tabla data-testid=history-table")
                return df
            headers_list = [th.get_text(strip=True) for th in table.thead.find_all('th')]
            self.logger.info("Collector", "collector_data", f"Columnas obtenidas de la tabla: {headers_list}")

            rows=[]
            for tr in table.tbody.find_all('tr'):
                colums = [td.get_text(strip=True) for td in tr.find_all('td')]
                if len(colums) == len(headers_list):
                    rows.append(colums)
                    
            df = pd.DataFrame(rows,columns=headers_list).rename(columns={
                    'Fecha':'fecha',
                    'Abrir':'abrir',
                    'Máx.':'max',
                    'Mín.':'min',
                    'CerrarPrecio de cierre ajustado para splits.':'cerrar',
                    'Cierre ajustadoPrecio de cierre ajustado para splits y distribuciones de dividendos o plusvalías.':'cierre_ajustado',
                    'Volumen':'volumen'
                })
            
            # Limpiar volumen
            df['volumen'] = df['volumen'].replace('-', '0')  # Si hay guiones que significan "sin volumen"

            # Traducir meses en español a inglés para que datetime los entienda
            meses_esp_a_eng = {
                'ene': 'Jan', 'feb': 'Feb', 'mar': 'Mar', 'abr': 'Apr',
                'may': 'May', 'jun': 'Jun', 'jul': 'Jul', 'ago': 'Aug',
                'sept': 'Sep', 'oct': 'Oct', 'nov': 'Nov', 'dic': 'Dec'
            }
            df['fecha'] = df['fecha'].replace(meses_esp_a_eng, regex=True)

            # Convertir fecha
            df['fecha'] = pd.to_datetime(df['fecha'], format='%d %b %Y', errors='coerce')

            df['año'] = df['fecha'].dt.year.astype('Int64')
            df['mes'] = df['fecha'].dt.month.astype('Int64')
            df['dia'] = df['fecha'].dt.day.astype('Int64')

            self.logger.info("Collector", "collector_data", f"Datos recolectados exitosamente: {df.shape[0]} filas.")
            return df
        
        except Exception as error:
            self.logger.error("Collector", "collector_data", f"Error al obtener los datos: {error}")
