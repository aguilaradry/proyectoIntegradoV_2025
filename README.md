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
│       └── update_data.yml             # Automatización con GitHub Actions
├── src/
│   └── <indicador_economico>/
│       ├── static/
│       │   ├── data/
│       │   │   ├── historical.csv      # Dataset generado
│       │   │   
│       │   └── models/
│       ├── collector.py                # Clase principal de recolección
│       └── logger.py                   # Configuración de logs
|       └── main.py                     # Punto de entrada del programa
├── docs/
│   └── report_entrega1.pdf             # Documentación
├── logs/
│   └── dolar_analysis_20250508.log     # Registros de ejecución
├── setup.py
└── README.md

## Automatización con GitHub Actions
Se creó un workflow en .github/workflows/update_data.yml que ejecuta el script principal (main.py) automáticamente al hacer push en la rama main. Además, realiza commit y push si se detectan cambios en los archivos generados. Esto garantiza que el historial de datos se mantenga actualizado sin intervención manual.

## Requisitos
- Python 3.8+
- Pandas 2.2.3
- Requests 2.32.3
- BeautifulSoup4
- SQLite3

Los datos recolectados se guardarán en src/proyecto/static/data/historical.csv y se registrarán eventos en la carpeta logs.