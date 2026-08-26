import streamlit as st
from src.data_cleaning import limpiar_centrales, limpiar_caudales, limpiar_emisiones, limpiar_lluvias, limpiar_emisiones_combustibles
from ui.views import vista_introduccion, vista_mapa, vista_graficos, vista_emisiones, vista_conclusion

def inicializar_estado():
    st.set_page_config(page_title="energi.Ar", page_icon="⚡", layout="wide")
    if 'paso' not in st.session_state:
        st.session_state.paso = 0

@st.cache_data
def cargar_datos():
    df_cent = limpiar_centrales("data/generacin-elctrica-centrales-de-generacin (1).csv")
    df_caud = limpiar_caudales("data/agd_caudales_medios.csv")
    df_emis = limpiar_emisiones("data/factor_de_emision_2013_a_2023(4 c) Despacho OM 2022).csv")
    df_lluv = limpiar_lluvias("data/agd_i_ppt_pais_por_prov_2010_2024.csv")
    df_comb = limpiar_emisiones_combustibles("data/factor_de_emision_2013_a_2023(4 c) Despacho OM 2022).csv")
    return df_cent, df_caud, df_emis, df_lluv, df_comb

def main():
    inicializar_estado()
    df_centrales, df_caudales, df_emisiones, df_lluvias, df_combustibles = cargar_datos()

    # Router súper limpio
    if st.session_state.paso == 0:
        vista_introduccion()
    elif st.session_state.paso == 1:
        vista_mapa(df_centrales)
    elif st.session_state.paso == 2:
        vista_graficos(df_caudales)
    elif st.session_state.paso == 3:
        vista_emisiones(df_emisiones)
    elif st.session_state.paso == 4:
        vista_conclusion(df_lluvias, df_combustibles)

if __name__ == "__main__":
    main()