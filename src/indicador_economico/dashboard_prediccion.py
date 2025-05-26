import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Configuración inicial
st.set_page_config(page_title="📊 Dashboard Económico - Dólar Australiano Futuro", layout="wide")

# Rutas de archivo
DATA_PATH = 'src/indicador_economico/static/data/dolar_data_enricher.csv'
PRED_PATH = 'src/indicador_economico/static/data/predicciones.csv'

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=['fecha'])
    df = df.sort_values('fecha')
    if os.path.exists(PRED_PATH):
        pred = pd.read_csv(PRED_PATH, parse_dates=['fecha'])
        df = pd.merge(df, pred[['fecha', 'prediccion']], on='fecha', how='left')
    return df

df = load_data()

# Título principal centrado y negrita
st.markdown(
    "<h1 style='text-align: center; font-weight: bold; font-size: 38px;'>📊 Dashboard Económico - Dólar Australiano Futuro</h1>",
    unsafe_allow_html=True
)

# Estilo común para gráficos con cuadrículas y sin bordes sólidos
layout_common = dict(
    hovermode='x unified',
    legend_title_text='',
    title_font=dict(size=28, family='Arial', color='black'),
    font=dict(size=20, family='Arial'),
    plot_bgcolor='rgba(230, 240, 250, 0.9)',  # Fondo suave dentro gráfico
    paper_bgcolor='white',  # Fondo fuera gráfico
    xaxis=dict(
        title_font=dict(size=22, family='Arial', color='black'),
        tickfont=dict(size=18, color='black'),
        showline=False,  # sin línea borde
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
    ),
    yaxis=dict(
        title_font=dict(size=22, family='Arial', color='black'),
        tickfont=dict(size=18, color='black'),
        showline=False,
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
    ),
    hoverlabel=dict(
        font_size=16,
        font_family='Arial',
        font_color='black',
        bgcolor='white',
        bordercolor='gray'
    ),
    legend=dict(
        x=0.02,
        y=0.98,
        bgcolor='rgba(255, 255, 255, 0.8)',
        bordercolor='black',
        borderwidth=1,
        font=dict(
            size=22,
            family='Arial',
            color='black'
        ),
        orientation='v',
        valign='top'
    )
)

# Data para gráfico general
df_long = df.melt(id_vars=['fecha'], value_vars=['cerrar', 'prediccion'], var_name='Tipo', value_name='Precio')
df_long = df_long.dropna(subset=['Precio'])
df_long['Tipo'] = df_long['Tipo'].map({'cerrar': 'Precio Real', 'prediccion': 'Predicción'})

# Gráfico Precio Real vs Predicción (completo)
fig_all = px.line(df_long, x='fecha', y='Precio', color='Tipo',
                  labels={'fecha': 'Fecha', 'Precio': 'Precio'},
                  title='Precio Real vs. Predicción (Completo)',
                  color_discrete_map={'Precio Real': 'blue', 'Predicción': 'orange'})

fig_all.update_layout(**layout_common)
fig_all.update_layout(height=600)

st.plotly_chart(fig_all, use_container_width=True)

# Filtrar solo año 2025
df_2025 = df[df['fecha'].dt.year == 2025]

if not df_2025.empty:
    df_2025_long = df_2025.melt(id_vars=['fecha'], value_vars=['cerrar', 'prediccion'], var_name='Tipo', value_name='Precio')
    df_2025_long = df_2025_long.dropna(subset=['Precio'])
    df_2025_long['Tipo'] = df_2025_long['Tipo'].map({'cerrar': 'Precio Real', 'prediccion': 'Predicción'})

    fig_2025 = px.line(
        df_2025_long, x='fecha', y='Precio', color='Tipo',
        labels={'fecha': 'Fecha', 'Precio': 'Precio'},
        title='Precio Real vs. Predicción (Año 2025)',
        color_discrete_map={'Precio Real': 'blue', 'Predicción': 'orange'},
        width=1000,
        height=600
    )

    fig_2025.update_layout(**layout_common)
    fig_2025.update_layout(xaxis_tickformat='%d %b')

    st.plotly_chart(fig_2025, use_container_width=False)
else:
    st.info("No hay datos para el año 2025.")
