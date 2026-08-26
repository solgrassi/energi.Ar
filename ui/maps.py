import folium
from streamlit_folium import st_folium

def mostrar_mapa_centrales(df):
    """Genera un mapa interactivo usando Folium y la capa oficial del IGN."""
    
    # Textos y URL oficial del Instituto Geográfico Nacional
    attr = '&copy; <a href="https://www.ign.gob.ar">Instituto Geográfico Nacional</a>'
    tiles = 'https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/capabaseargenmap@EPSG%3A3857@png/{z}/{x}/{-y}.png'
    
    # Creacion del mapa centrado en Argentina
    m = folium.Map(
        location=(-38.4161, -63.6167),
        zoom_start=4,
        tiles=tiles,
        attr=attr,
        control_scale=True
    )
    
    # Agregado de los puntos iterando sobre el DataFrame
    for idx, row in df.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=4,
            color="#8B0000", 
            fill=True,
            fill_color="#FF4500",
            fill_opacity=0.8,
            # El tooltip es lo que aparece al pasar el mouse
            tooltip=f"<b>{row['nombre']}</b><br>Tecnología: {row['tecnologia_etiqueta']}<br>Potencia: {row['potencia_instalada_mw']} MW"
        ).add_to(m)
        
    st_folium(m, use_container_width=True, height=600)