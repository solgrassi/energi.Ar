import streamlit as st
from ui.maps import mostrar_mapa_centrales
from ui.charts import mostrar_grafico_caudales, mostrar_grafico_emisiones, mostrar_grafico_torta
import streamlit.components.v1 as components

# --- CSS Y ESTÉTICA GLOBAL ---
def aplicar_estilos():
    js_scroll = '''
    <script>
        var body = window.parent.document.querySelector(".main");
        if (body) {
            body.scrollTop = 0;
        }
        window.parent.scrollTo(0, 0);
    </script>
    '''
    components.html(js_scroll, height=0)
    
    st.markdown("""
    <style>
    /*tipografía de Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

    /* Forzar la tipografía en toda la app */
    html, body, .stApp, .stMarkdown, p, h1, h2, h3, h4, li, a {
        font-family: 'Poppins', sans-serif !important;
    }

    /* Estilo de Botones */
    div.stButton > button {
        font-family: 'Poppins', sans-serif !important; 
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

    /* Títulos del Hero */
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
    .stat-card {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stat-card .stat-number {
        font-size: 2.2rem;
        font-weight: 800;
        color: #111827;
        display: block;
    }
    .stat-card .stat-label {
        font-size: 0.95rem;
        color: #4b5563;
        font-weight: 400;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE NAVEGACIÓN ---
def avanzar():
    st.session_state.paso += 1

def retroceder():
    st.session_state.paso -= 1

def mostrar_progreso(paso_actual, total=5):
    st.progress(paso_actual / (total - 1))
    st.caption(f"Paso {paso_actual + 1} de {total}")

# --- VISTAS ---
def vista_introduccion():
    aplicar_estilos()
    mostrar_progreso(0)
    st.markdown("<h1 class='hero-title'>⚡ energi.Ar</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='hero-subtitle'>La paradoja climática de nuestra matriz energética</h2>", unsafe_allow_html=True)
    
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
        
    st.markdown("<div style='margin-top: 2.5rem;'></div>", unsafe_allow_html=True)
    
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        st.button("Comenzar recorrido interactivo", on_click=avanzar, type="primary", use_container_width=True)

def vista_mapa(df_centrales):
    aplicar_estilos()
    df_centrales.loc[df_centrales['nombre'].str.contains('URUGUA', na=False, case=False), 'nombre'] = 'URUGUA-Í'
    st.title("1. La red de emergencia fósil")
    st.markdown("### ¿Quién nos salva cuando falla el clima?")
    
    st.write("""
    Antes de analizar la crisis, miremos nuestra infraestructura de respaldo. 
    En este mapa oficial podés ver la enorme red de **centrales térmicas** (los puntos rojos) distribuidas a lo largo y ancho del país. 
    
    Estas instalaciones, que generan electricidad quemando gas y fueloil, son el histórico "Plan B" de nuestra matriz energética. Usualmente funcionan para complementar los picos de demanda pero... **¿qué pasa cuando nuestra fuente limpia principal desaparece y este ejército fósil tiene que encenderse a máxima capacidad?**
    """)
    
    mostrar_mapa_centrales(df_centrales)

    with st.expander("📋 Ver listado de centrales en formato tabla (alternativa accesible)"):
        # Seleccion de las columnas útiles
        df_tabla = df_centrales[['nombre', 'tecnologia_etiqueta', 'provincia']].copy()
        
        df_tabla = df_tabla.rename(columns={
            'nombre': 'Nombre de la Central',
            'tecnologia_etiqueta': 'Tecnología',
            'provincia': 'Provincia'
        })
        df_tabla = df_tabla.sort_values(by='Nombre de la Central')
        df_tabla = df_tabla.reset_index(drop=True)
        df_tabla.index = df_tabla.index + 1
        
        st.dataframe(df_tabla, use_container_width=True)
    
    st.write("") 
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("⬅️ Atrás", on_click=retroceder, use_container_width=True)
    with col2:
        st.button("Siguiente: El impacto de la sequía ➡️", on_click=avanzar, type="primary", use_container_width=True)

def vista_graficos(df_caudales):
    aplicar_estilos()
    mostrar_progreso(2)
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
    mostrar_progreso(3)
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
    mostrar_progreso(4)
    st.title("4. El círculo vicioso... y cómo romperlo")
    st.markdown("### Resumen del impacto en nuestra matriz")
    
    st.write("Al observar los datos en conjunto, se revela un ciclo peligroso: el cambio climático genera sequías, lo que nos quita energía limpia, obligándonos a quemar más fósiles, lo que a su vez agrava el cambio climático.")
    
    promedio_nacional = df_lluvias.groupby('Anio')['Precipitacion_mm'].mean().mean()
    lluvia_2022 = df_lluvias[df_lluvias['Anio'] == 2022]['Precipitacion_mm'].mean()
    caida_lluvia = ((promedio_nacional - lluvia_2022) / promedio_nacional) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        caida_formateada = f"{caida_lluvia:.1f}".replace(".", ",")
        lluvia_formateada = f"{lluvia_2022:,.0f}".replace(",", ".")
        st.markdown(f"""
        <div class='stat-card'>
            <span class='stat-number'>-{caida_formateada}%</span>
            <span class='stat-label'>📉 Las precipitaciones nacionales cayeron a {lluvia_formateada} mm</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='stat-card'>
            <span class='stat-number'>-Caudales</span>
            <span class='stat-label'>💧 El Paraná y otros afluentes clave registraron sus caudales más bajos en 50 años</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='stat-card'>
            <span class='stat-number'>9.6M</span>
            <span class='stat-label'>🏭 Toneladas de CO2 emitidas para evitar apagones masivos</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    col_grafico, col_texto = st.columns([1, 1], gap="large")
    with col_grafico:
        mostrar_grafico_torta(df_combustibles)
    with col_texto:
        st.markdown("### El futuro es la diversificación")
        st.write("La crisis hídrica de 2022 nos dejó una lección clara: depender de un solo factor climático para generar energía limpia es un riesgo sistémico.")
        st.markdown("""
        Para no repetir esta historia, la transición energética debe acelerarse. No alcanza con esperar que vuelva a llover. El verdadero camino es invertir fuertemente en el aprovechamiento integral de nuestro territorio: 
        - 🌬️ **Potenciar** los parques eólicos en la Patagonia
        - ☀️ **Expandir** la matriz solar en el norte argentino
        - 🔌 **Modernizar** la red de transmisión nacional
        """)
        st.write("El desafío ya no es solo apagar las térmicas, sino construir una infraestructura resiliente que no dependa del cielo.")
        st.write("")
        st.button("🔄 Volver a explorar los datos", on_click=lambda: st.session_state.update(paso=0), type="primary", use_container_width=True)