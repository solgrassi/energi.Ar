import pandas as pd
import json

def limpiar_generacion(ruta):
    """Recibe una ruta de un csv de generacion electrica, extrae la columna anio y renombra las columnas"""
    df = pd.read_csv(ruta)
    # Extraccion del anio
    df['anio'] = pd.to_datetime(df['anio']).dt.year
    df = df.rename(columns={'generacion_bruta_asociada_a_redes': 'Generacion_GWh', 'anio': 'Anio'})
    return df

def limpiar_caudales(ruta):
    """Recibe una ruta de un csv de caudales, y renombra sus columnas"""
    df = pd.read_csv(ruta, sep=';', encoding='utf-8')
    # Renombre para estandarizar columnas
    df = df.rename(columns={'año': 'Anio', 'caudal_medio_anual': 'Caudal_m3s'})
    return df

def limpiar_centrales(ruta):
    """Limpia el archivo de centrales y extrae latitud y longitud"""
    df = pd.read_csv(ruta)
    
    # Extraer lat y lon del texto geojson
    def extraer_coord(geo_str, indice):
        try:
            # Convierte el string '{"type":"Point","coordinates":[-65,-24]}' en diccionario
            dicc = json.loads(geo_str)
            return dicc['coordinates'][indice]
        except:
            return None

    # Las coordenadas vienen en [longitud, latitud]
    df['lon'] = df['geojson'].apply(lambda x: extraer_coord(x, 0))
    df['lat'] = df['geojson'].apply(lambda x: extraer_coord(x, 1))
    
    # Obtencion de columnas de interes
    columnas_utiles = ['nombre', 'tecnologia_etiqueta', 'potencia_instalada_mw', 'provincia', 'lat', 'lon']
    return df[columnas_utiles].dropna(subset=['lat', 'lon'])

def limpiar_emisiones(ruta):
    """Limpia el dataset de emisiones que viene con el encabezado roto"""
    df = pd.read_csv(ruta, sep=';', skiprows=6, encoding='latin1', low_memory=False)
    
    # La columna 'Unnamed: 19' tiene el total, y 'tCO2/MWh' el factor
    df = df.rename(columns={
        'Unnamed: 19': 'Emisiones_Totales_tCO2',
        'tCO2/MWh': 'Factor_Emision'
    })
    
    # Arreglo de números (cambio coma por punto)
    df['Factor_Emision'] = df['Factor_Emision'].astype(str).str.replace(',', '.').astype(float)
    df['Emisiones_Totales_tCO2'] = pd.to_numeric(df['Emisiones_Totales_tCO2'], errors='coerce')
    
    # Agrupacion por mes
    df_mensual = df.groupby('mes').agg({
        'Emisiones_Totales_tCO2': 'sum',
        'Factor_Emision': 'mean'
    }).reset_index()
    
    return df_mensual

def limpiar_lluvias(ruta):
    """Limpia el dataset de precipitaciones y lo formatea para análisis temporal"""
    df = pd.read_csv(ruta, sep=';', encoding='utf-8')

    df_melted = pd.melt(
        df, 
        id_vars=['estación_meteorológica'], 
        var_name='Anio', 
        value_name='Precipitacion_mm'
    )
    
    df_melted['Anio'] = df_melted['Anio'].str.replace('año_', '').astype(int)
    df_melted['estación_meteorológica'] = df_melted['estación_meteorológica'].str.strip()
    
    return df_melted

def limpiar_emisiones_combustibles(ruta):
    """Extrae el total de emisiones divididas por tipo de combustible."""
    df = pd.read_csv(ruta, sep=';', skiprows=6, encoding='latin1', low_memory=False)
    
    datos = {
        'Combustible': ['Carbón Mineral', 'Fuel Oil', 'Gas Natural', 'Gas Oil'],
        'Emisiones_tCO2': [
            pd.to_numeric(df['CM.2'], errors='coerce').sum(),
            pd.to_numeric(df['FO.2'], errors='coerce').sum(),
            pd.to_numeric(df['GN.2'], errors='coerce').sum(),
            pd.to_numeric(df['GO.2'], errors='coerce').sum()
        ]
    }
    return pd.DataFrame(datos)