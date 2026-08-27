import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

COLORES_TECNOLOGIA = {
    'Térmica': '#DC2626',                       
    'Hidroeléctrica (Menor a 50 Mw)': '#3b82f6' 
}

def color_por_tecnologia(tecnologia):
    return COLORES_TECNOLOGIA.get(tecnologia, '#6B7280')  # gris para lo que no matchee

def crear_popup(row):
    """Popup HTML estructurado con toda la info relevante de la central."""
    html = f"""
    <div style="font-family: 'Poppins', sans-serif; min-width: 190px;">
        <h4 style="margin:0 0 6px 0; color:#111827;">{row['nombre']}</h4>
        <p style="margin:2px 0; color:#374151;"><b>Tecnología:</b> {row['tecnologia_etiqueta']}</p>
        <p style="margin:2px 0; color:#374151;"><b>Provincia:</b> {row['provincia']}</p>
    </div>
    """
    return folium.Popup(html, max_width=250)

def agregar_leyenda(m):
    """Inyecta una leyenda fija con los colores por tecnología."""
    items_html = "".join(
        f'<span style="color:{color};">●</span> {tec}<br>'
        for tec, color in COLORES_TECNOLOGIA.items()
    )
    leyenda_html = f"""
    <div style="position: fixed; bottom: 30px; left: 30px; z-index:9999;
                background-color: white; padding: 10px 14px; border-radius: 10px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.15);
                font-family: 'Poppins', sans-serif; font-size: 13px; color:#374151;">
        <b>Tecnología</b><br>
        {items_html}
    </div>
    """
    m.get_root().html.add_child(folium.Element(leyenda_html))

def mostrar_mapa_centrales(df):
    """Genera un mapa interactivo usando Folium y la capa oficial del IGN."""
    
    attr = '&copy; <a href="https://www.ign.gob.ar">Instituto Geográfico Nacional</a>'
    tiles = 'https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/capabaseargenmap@EPSG%3A3857@png/{z}/{x}/{-y}.png'
    
    m = folium.Map(
        location=(-38.4161, -63.6167),
        zoom_start=4,
        tiles=tiles,
        attr=attr,
        control_scale=True
    )

    
    for idx, row in df.iterrows():
        color = color_por_tecnologia(row['tecnologia_etiqueta'])
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
            popup=crear_popup(row),
            tooltip=row['nombre']
        ).add_to(m)
    
    agregar_leyenda(m)
    
    st_folium(m, use_container_width=True, height=600)