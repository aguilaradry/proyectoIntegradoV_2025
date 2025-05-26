import streamlit as st
import pandas as pd
import numpy as np
import os

# Configuración de página
st.set_page_config(page_title="Dashboard Económico - AUD", layout="wide")

# Cargar datos
data_path = os.path.join('src', 'indicador_economico', 'static', 'data', 'dolar_data_enricher.csv')

@st.cache_data
def cargar_datos():
    return pd.read_csv(data_path, parse_dates=['fecha'])

df = cargar_datos()
df = df.sort_values('fecha')

# Cálculos adicionales
df['retorno'] = df['cerrar'].pct_change()
df['media_movil_30'] = df['cerrar'].rolling(window=30).mean()
df['retorno_acumulado'] = (1 + df['retorno']).cumprod() - 1
df['desviacion_mensual'] = df.groupby(['año', 'mes'])['retorno'].transform('std')

# Título del Dashboard
st.markdown("<h2 style='text-align: center;'>📊 Dashboard Económico - Tipo de Cambio Dólar Australiano</h2>", unsafe_allow_html=True)
st.markdown("---")

# KPIs
st.sidebar.header("Indicadores Clave")
ultima_fila = df.iloc[-1]
st.sidebar.markdown(f"""
<div style='font-size:15px; line-height: 1.6'>
<b>💵 Último Cierre:</b> ${ultima_fila['cerrar']:.2f}<br>
<b>📉 Volatilidad Actual:</b> {ultima_fila['volatilidad_mensual']:.4f}<br>
<b>📈 Retorno YTD:</b> {ultima_fila['retorno_acumulado']:.2%}<br>
<b>📆 Retorno YoY:</b> {ultima_fila.get('cerrar_yoy', np.nan):.2%}<br>
<b>📊 Volumen Prom. Trimestral:</b> {ultima_fila['volumen_promedio_trimestral']:.0f}
</div>
""", unsafe_allow_html=True)

#Filtros
st.sidebar.header("Filtros")
anio = st.sidebar.selectbox("Seleccionar año", options=sorted(df['año'].dropna().unique(), reverse=True))
df_filtrado = df[df['año'] == anio]


# 1. Precio cierre diario y media móvil
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"📈 Precio de Cierre Diario - {anio}")
    st.line_chart(df_filtrado.set_index('fecha')['cerrar'])

with col2:
    st.subheader("📉 Media Móvil de 30 Días")
    st.line_chart(df.set_index('fecha')[['cerrar', 'media_movil_30']].dropna())

# 2. Volatilidad mensual y retorno acumulado
col3, col4 = st.columns(2)

with col3:
    st.subheader("📊 Volatilidad Mensual")
    volatilidad = df.groupby(['año', 'mes'])['retorno'].std().reset_index()
    volatilidad['fecha'] = pd.to_datetime(volatilidad['año'].astype(str) + '-' + volatilidad['mes'].astype(str) + '-01')
    st.line_chart(volatilidad.set_index('fecha')['retorno'])

with col4:
    st.subheader("📈 Retorno Acumulado Desde el Inicio")
    st.line_chart(df.set_index('fecha')['retorno_acumulado'])

# 3. Desviación mensual
st.subheader("📉 Desviación Estándar Mensual")
desv_mensual = df.groupby(['año', 'mes'])['retorno'].std().reset_index()
desv_mensual['fecha'] = pd.to_datetime(desv_mensual['año'].astype(str) + '-' + desv_mensual['mes'].astype(str) + '-01')
st.line_chart(desv_mensual.set_index('fecha')['retorno'])

# 4. Tabla de días extremos
st.subheader("⚠️ Días con Variaciones Extremas (±5%)")
dias_extremos = df[df['dias_extremo'] == True]
st.write(f"Total de días extremos: **{len(dias_extremos)}**")
st.dataframe(dias_extremos[['fecha', 'cerrar', 'retorno']])
