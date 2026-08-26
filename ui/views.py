import streamlit as st
from ui.maps import mostrar_mapa_centrales
from ui.charts import mostrar_grafico_caudales, mostrar_grafico_emisiones, mostrar_grafico_torta

# --- CSS Y ESTÉTICA GLOBAL ---
def aplicar_estilos():
    st.markdown("""
    <style>
    /* 1. Importar tipografía moderna de Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

    /* 2. Forzar la tipografía en toda la app */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
    }

    /* 3. Estilo de Botones Modernos (Tipo "Pill") */
    div.stButton > button {
        border-radius: 25px !important;
        font-weight: 600 !important;
        min-height: 50px !important;
        border: none !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
    }

    div.stButton > button[kind="secondary"] {
        background-color: #e5e7eb !important;
        color: #374151 !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #d1d5db !important;
    }

    /* 4. Títulos del Hero */
    .hero-title {
        text-align: center; 
        font-size: 3.8rem; 
        font-weight: 800; 
        color: #111827;
        margin-bottom: 0.2rem;
        letter-spacing: -1px;
    }
    .hero-subtitle {
        text-align: center; 
        color: #4b5563; 
        font-size: 1.4rem;
        font-weight: 400;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    .intro-text {
        text-align: center;
        font-size: 1.1rem;
        line-height: 1.6;
        max-width: 800px;
        margin: 0 auto 2rem auto;
        color: #374151;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE NAVEGACIÓN ---
def avanzar():
    st.session_state.paso += 1

def retroceder():
    st.session_state.paso -= 1

# --- VISTAS ---
def vista_introduccion():
    aplicar_estilos()
    
    st.markdown("<h1 class='hero-title'>⚡ energi.Ar</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='hero-subtitle'>La paradoja climática de nuestra matriz energética</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='intro-text'>
        Durante la última década, Argentina hizo un esfuerzo enorme por incorporar <b>energías limpias y renovables</b>. 
        Sin embargo, hay un factor externo que está poniendo en jaque este progreso: <b>el cambio climático y las sequías extremas</b>.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.info("💡 **Dato clave:**\n\nEl agua de nuestros ríos funciona como la batería natural más grande del país. Cuando baja su nivel por falta de lluvias, todo el sistema entra en crisis.")
    with col2:
        st.error("⚠️ **¿Qué pasa cuando no llueve?**\n\nAl secarse nuestras represas, debemos tomar decisiones drásticas para evitar cortes de luz masivos; medidas que impactan directamente en el medio ambiente.")
        
    st.write("<br><br>", unsafe_allow_html=True)
    
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        st.button("Comenzar recorrido interactivo", on_click=avanzar, type="primary", use_container_width=True)

def vista_mapa(df_centrales):
    aplicar_estilos()
    st.title("1. La red de generación eléctrica")
    st.markdown("### ¿De dónde sale nuestra energía hoy?")
    
    st.write("""
    Antes de entender el problema, miremos la infraestructura. 
    En este mapa oficial podés explorar todas las centrales de generación eléctrica del país. 
    Vas a notar que las grandes represas hidroeléctricas están concentradas en cuencas específicas, como la del Litoral o la del Comahue.
    """)
    
    mostrar_mapa_centrales(df_centrales)
    
    st.write("") 
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("⬅️ Atrás", on_click=retroceder, use_container_width=True)
    with col2:
        st.button("Siguiente: El impacto de la sequía ➡️", on_click=avanzar, type="primary", use_container_width=True)

def vista_graficos(df_caudales):
    aplicar_estilos()
    st.title("2. Cuando el agua no alcanza")
    st.markdown("### El desplome histórico de nuestros ríos")
    
    mostrar_grafico_caudales(df_caudales)
    
    st.write("")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("⬅️ Volver al mapa", on_click=retroceder, use_container_width=True)
    with col2:
        st.button("Siguiente: El costo ambiental ➡️", on_click=avanzar, type="primary", use_container_width=True)

def vista_emisiones(df_emisiones):
    aplicar_estilos()
    st.title("3. El costo ambiental")
    st.markdown("### El caso crítico de 2022")
    
    st.write("""
    **¿Por qué nos enfocamos en el año 2022?** 
    Durante ese año, Argentina atravesó el pico del fenómeno climático de "La Niña", provocando una de las sequías más severas de las que se tenga registro. 
    Al quedarse sin agua en las represas, el sistema eléctrico tuvo que encender a máxima capacidad las centrales térmicas que queman gas y fueloil para evitar apagones masivos.
    """)
    
    mostrar_grafico_emisiones(df_emisiones)
    
    st.write("")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("⬅️ Atrás", on_click=retroceder, use_container_width=True)
    with col2:
        st.button("Siguiente: Conclusión final ➡️", on_click=avanzar, type="primary", use_container_width=True)

def vista_conclusion(df_lluvias, df_combustibles):
    aplicar_estilos()
    st.title("4. El círculo vicioso... y cómo romperlo")
    st.markdown("### Resumen del impacto en nuestra matriz")
    
    st.write("Al observar los datos en conjunto, se revela un ciclo peligroso: el cambio climático genera sequías, lo que nos quita energía limpia, obligándonos a quemar más fósiles, lo que a su vez agrava el cambio climático.")
    
    promedio_nacional = df_lluvias.groupby('Anio')['Precipitacion_mm'].mean().mean()
    lluvia_2022 = df_lluvias[df_lluvias['Anio'] == 2022]['Precipitacion_mm'].mean()
    caida_lluvia = ((promedio_nacional - lluvia_2022) / promedio_nacional) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.error("📉 1. Causa Climática")
        st.write(f"Las precipitaciones nacionales cayeron a **{lluvia_2022:.0f} mm** (**-{caida_lluvia:.1f}%**).")
    with col2:
        st.warning("💧 2. Caída de Recursos")
        st.write("El Río Paraná y otros afluentes clave para las represas hidroeléctricas registraron sus caudales más bajos en 50 años.")
    with col3:
        st.error("🏭 3. Costo Ambiental")
        st.write("Se emitieron **9.6 millones de toneladas de CO2** para evitar apagones masivos.")
        
    st.markdown("---")
    
    col_grafico, col_texto = st.columns([1, 1], gap="large")
    with col_grafico:
        mostrar_grafico_torta(df_combustibles)
    with col_texto:
        st.markdown("### El futuro es la diversificación")
        st.write("""
        La crisis hídrica de 2022 nos dejó una lección ineludible: depender de un solo factor climático para generar energía limpia es un riesgo sistémico. El gráfico refleja cómo, ante la emergencia, el sistema se sostuvo a base de Gas Oil y Gas Natural, disparando nuestra huella de carbono.
        
        **Para no repetir esta historia, la transición energética debe acelerarse.** 
        No alcanza con esperar que vuelva a llover. El verdadero camino es invertir fuertemente en el aprovechamiento integral de nuestro territorio: potenciar los parques eólicos en la Patagonia, expandir la matriz solar en el norte argentino y, fundamentalmente, modernizar la red de transmisión nacional. 
        
        El desafío ya no es solo apagar las centrales térmicas, sino construir una infraestructura inteligente, resiliente y diversificada que no dependa del cielo para mantener nuestras luces encendidas.
        """)
        st.write("")
        st.button("🔄 Volver a explorar los datos", on_click=lambda: st.session_state.update(paso=0), type="primary", use_container_width=True)