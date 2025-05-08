# Proyecto Integrado V - Automatización de Datos Económicos

## Descripción
Este proyecto implementa un sistema automatizado para la recolección continua de datos históricos de indicadores económicos desde Yahoo Finanzas. Utiliza GitHub Actions para mantener actualizada la base de datos sin intervención manual.

El indicador seleccionado corresponde al **dólar australiano (AUD/USD)**.

## Características
- Descarga automatizada de datos históricos económicos
- Persistencia de datos en formato CSV y SQLite
- Actualización programada mediante GitHub Actions
- Implementación con principios de Programación Orientada a Objetos
- Logging completo para seguimiento de operaciones

## Estructura del proyecto
- src/<indicador_economico>/collector.py: Clase principal para descarga y persistencia de datos
- src/<indicador_economico>/logger.py: Configuración de logging para todo el proyecto
- src/<indicador_economico>/static/data/historical.csv: Dataset en formato CSV
- .github/workflows/update_data.yml: Workflow para actualizaciones automáticas


<PROYECTOINTEGRADOV_2025>/
├── .github/
│   └── workflows/
│       └── update_data.yml
├── src/
│   └── <indicador_economico>/
│       ├── static/
│       │   ├── data/
│       │   │   ├── historical.csv
│       │   │   
│       │   └── models/
│       ├── collector.py
│       └── logger.py
|       └── main.py
├── docs/
│   └── report_entrega1.pdf
├── setup.py
└── README.md

## Requisitos
- Python 3.8+
- Pandas 2.2.3
- Requests 2.32.3
- BeautifulSoup4
- SQLite3