import requests
import pandas as pd
from bs4 import BeautifulSoup
from logger import Logger
import os

class Collector:
    def __init__(self, logger):
        self.url = 'https://es.finance.yahoo.com/quote/6A%3DF/history/?period1=973659600&period2=1746573611'
        self.logger = logger

        # Crear carpetas si no existen
        os.makedirs('src/proyecto/static/data', exist_ok=True)

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
            
            # Limpiar y convertir valores numéricos
            for col in ['abrir', 'max', 'min', 'cerrar', 'cierre_ajustado']:
                df[col] = df[col].str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
                df[col] = pd.to_numeric(df[col], errors='coerce')

            # Limpiar volumen
            df['volumen'] = df['volumen'].replace('-', '0')  # Si hay guiones que significan "sin volumen"

            # Convertir fecha y extraer año, mes, día
            df['fecha'] = pd.to_datetime(df['fecha'], format='%d %b %Y', errors='coerce')
            df = df.dropna(subset=['fecha'])  # Elimina las filas con fecha NaT
            df['año'] = df['fecha'].dt.year.astype(int)
            df['mes'] = df['fecha'].dt.month.astype(int)
            df['dia'] = df['fecha'].dt.day.astype(int)

            self.logger.info("Collector", "collector_data", f"Datos recolectados exitosamente: {df.shape[0]} filas.")
            return df
        
        except Exception as error:
            self.logger.error("Collector", "collector_data", f"Error al obtener los datos: {error}")
