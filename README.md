# Proyecto Integrado V - Automatización de Datos Económicos

## Descripción
Este proyecto implementa un sistema automatizado para la recolección continua de datos históricos de indicadores económicos desde Yahoo Finanzas. Utiliza GitHub Actions para mantener actualizada la base de datos sin intervención manual.

El indicador seleccionado corresponde al **dólar australiano (AUD/USD)**.

## Indicador Económico: Dólar Australiano (AUD/USD)
El tipo de cambio AUD/USD representa la cantidad de dólares estadounidenses necesarios para adquirir un dólar australiano. Este indicador es ampliamente utilizado en los mercados financieros internacionales, y su seguimiento permite:

Evaluar la fortaleza relativa entre las economías de Australia y Estados Unidos.

Analizar tendencias de comercio exterior, especialmente en sectores como minería y energía, donde Australia es un actor clave.

Tomar decisiones de inversión basadas en las políticas monetarias y económicas de ambos países.

Entender la evolución de los mercados de divisas y su impacto sobre precios, exportaciones e importaciones.

Este valor es seguido por inversores, economistas y empresas para anticipar movimientos del mercado y ajustar estrategias financieras.

## Características
- Descarga automatizada de datos históricos económicos.
- Persistencia de datos en formato CSV o SQLite.
- Actualización programada mediante GitHub Actions.
- Implementación basada en principios de Programación Orientada a Objetos.
- Sistema de logging para trazabilidad de operaciones.

## Estructura del proyecto

<PROYECTOINTEGRADOV_2025>/
├── .github/
│   └── workflows/
│       └── update_data.yml                     # Automatización con GitHub Actions
├── src/
│   └── <indicador_economico>/
│       ├── static/
│       │   ├── data/
│       │   │   ├── dolar_data_enricher.csv     # Dataset enriquecido
│       │   │   ├── historical.csv              # Dataset generado
│       │   │   ├── predicciones.csv            # Resultados de predicciones generadas
│       │   ├── models/
│       │   │   └── model.pkl                   # Modelo entrenado serializado
│       │   └── reports/
│       │       ├── Dashboard.pdf               # Reporte PDF con capturas de gráficos
│       │       └── metricas.txt                # Justificación de métricas del modelo
│       ├── collector.py                        # Clase principal para recolección de datos
│       ├── dashboard.py                        # Dashboard con visualización de datos históricos
│       ├── dashboard_prediccion.py             # Dashboard con visualización de predicciones
│       ├── enricher.py                         # Script para enriquecimiento y procesamiento de datos
│       ├── logger.py                           # Configuración y manejo de logs
|       ├── main.py                             # Punto de entrada del programa
│       └── modeller.py                         # Entrenamiento y evaluación del modelo predictivo

├── docs/
│   └── report_entrega1.pdf                    # Documentación y reporte de entrega
├── logs/
│   └── dolar_analysis_20250508.log            # Registros y logs de ejecución
├── setup.py                                   # Archivo de configuración e instalación
└── README.md                                  # Documentación principal del proyecto


## Automatización con GitHub Actions
Se creó un workflow en .github/workflows/update_data.yml que ejecuta el script principal (main.py) automáticamente al hacer push en la rama main. Además, realiza commit y push si se detectan cambios en los archivos generados. Esto garantiza que el historial de datos se mantenga actualizado sin intervención manual.

## Requisitos
- Python 3.8+
- Pandas 2.2.3
- Requests 2.32.3
- BeautifulSoup4
- SQLite3

## Ejecución del Dashboard
Para visualizar los dashboards interactivos, instalar las dependencias del setup.py y usar los siguientes comandos desde la raíz del proyecto:

**Dashboard de datos históricos:**
streamlit run src/indicador_economico/dashboard.py

**Dashboard de predicciones:**
streamlit run src/indicador_economico/dashboard_prediccion.py

Los datos recolectados se guardarán en src/proyecto/static/data/historical.csv y se registrarán eventos en la carpeta logs.