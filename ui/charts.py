import streamlit as st
import pandas as pd
import plotly.express as px

def mostrar_grafico_caudales(df_caudales):
    """Genera un gráfico de líneas y calcula la caída porcentual."""
    
    st.write("Seleccioná un río clave para ver cómo fluctuó su nivel de agua a lo largo de los años.")
    
    rios_limpios = df_caudales['rio'].dropna().astype(str).str.strip()
    rios_disponibles = sorted(rios_limpios.unique())
    rio_seleccionado = st.selectbox(
        "Río a analizar:", 
        rios_disponibles, 
        index=rios_disponibles.index('PARANA') if 'PARANA' in rios_disponibles else 0
    )
    
    df_filtrado = df_caudales[df_caudales['rio'] == rio_seleccionado]
    
    # Agrupacion por anio y promedio
    df_grafico = df_filtrado.groupby('Anio')['Caudal_m3s'].mean()
    
    st.line_chart(df_grafico)
    
    # calculo dinamico de impacto
    if not df_grafico.empty:
        promedio_historico = df_grafico.mean()
        ultimo_anio = df_grafico.index[-1]
        ultimo_caudal = df_grafico.iloc[-1]
        
        if ultimo_caudal < promedio_historico:
            caida = ((promedio_historico - ultimo_caudal) / promedio_historico) * 100
            st.error(f"⚠️ **Impacto:** En el año {ultimo_anio}, el río {rio_seleccionado} registró un caudal de **{ultimo_caudal:,.0f} m³/s**. Esto representa un desplome del **{caida:.1f}%** respecto a su promedio histórico.")
        else:
            st.success(f"💧 En el año {ultimo_anio}, el río {rio_seleccionado} se mantuvo estable o por encima de su promedio histórico.")

def mostrar_grafico_emisiones(df_emisiones):
    """Genera un gráfico de área con las emisiones de CO2 y calcula el total."""
    
    st.write("Evolución mensual de las emisiones producidas por quemar combustibles fósiles para generar electricidad.")
    
    meses = {1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun', 
             7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'}
    df_emisiones['Mes_Nombre'] = df_emisiones['mes'].map(meses) + " 2022"
    
    df_grafico = df_emisiones.set_index('Mes_Nombre')['Emisiones_Totales_tCO2']

    st.area_chart(df_grafico)
    
    # calculo dinamico
    total_anual = df_emisiones['Emisiones_Totales_tCO2'].sum()
    
    st.warning(f"**Impacto ambiental:** Durante 2022, las centrales térmicas emitieron un volumen acumulado de **{f'{total_anual:,.0f}'.replace(',', '.')} toneladas de CO2** a la atmósfera.")
    st.info("**¿Qué significa este número en la realidad?**\n\nEsta cantidad de contaminación equivale a las emisiones generadas por **más de 2.100.000 autos** circulando ininterrumpidamente durante todo un año.")

def mostrar_grafico_torta(df_combustibles):
    """Genera un gráfico de dona interactivo con la composición de las emisiones."""
    
    st.markdown("#### Composición de las emisiones por combustible (2022)")
    

    # Configuracion de grafico
    fig = px.pie(
        df_combustibles, 
        values='Emisiones_tCO2', 
        names='Combustible',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.YlOrRd[::-1] # Paleta de colores fuego/alerta
    )
    
    fig.update_traces(textposition='outside', textinfo='percent+label')

    fig.update_layout(margin=dict(t=20, b=20, l=0, r=0))
    
    st.plotly_chart(fig, use_container_width=True)