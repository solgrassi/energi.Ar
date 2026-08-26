# ⚡ energi.Ar
**La paradoja climática de nuestra matriz energética**

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.20+-FF4B4B.svg)
![Accesibilidad](https://img.shields.io/badge/Accesibilidad-Nivel_AA-success.svg)
![Estado](https://img.shields.io/badge/Estado-Completado-brightgreen)

**energi.Ar** es una aplicación web interactiva de *Data Storytelling* desarrollada para concientizar sobre el impacto directo del cambio climático en la generación de energía en Argentina. 

A través de un recorrido guiado por datos oficiales, el proyecto demuestra cómo la sequía histórica de 2022 (Fenómeno La Niña) vació las represas hidroeléctricas del país, forzando al sistema a quemar reservas de combustibles fósiles y emitiendo más de 9.6 millones de toneladas de CO2 a la atmósfera.

---

## 🚀 Características Principales

* **Narrativa de Datos (Data Storytelling):** Flujo de navegación en 4 pasos que guía al usuario desde la infraestructura nacional hasta el impacto ambiental.
* **Mapas Interactivos:** Visualización geoespacial de la matriz de generación eléctrica nacional.
* **Cálculos en Tiempo Real:** Procesamiento dinámico del desplome histórico en el caudal de los ríos y las precipitaciones.
* **Diseño Accesible (WCAG AA):** Tipografía de alta legibilidad (Poppins), alto contraste de colores, y botones adaptados con áreas táctiles ampliadas para dispositivos móviles.
* **Arquitectura Modular:** Código limpio basado en la separación de responsabilidades (limpieza de datos, vistas de UI y controlador principal).

---

## 🛠️ Tecnologías Utilizadas

El proyecto fue construido íntegramente con Python y librerías de análisis de datos de código abierto:

* **[Streamlit](https://streamlit.io/):** Framework principal para la interfaz web y el enrutamiento.
* **[Pandas](https://pandas.pydata.org/):** Limpieza, transformación y agregación de datasets gubernamentales (manejo de formatos irregulares y delimitadores).
* **[Folium](https://python-visualization.github.io/folium/):** Renderizado del mapa interactivo de centrales eléctricas.
* **[Plotly Express](https://plotly.com/python/):** Gráficos interactivos de alta performance para el panel de conclusiones.

---

## 📂 Origen de los Datos

Los datos utilizados en este proyecto provienen de fuentes oficiales y de datos abiertos del Gobierno de la Nación Argentina:
1. **Centrales de Generación:** Coordenadas y tecnologías de la infraestructura eléctrica nacional.
2. **Caudales Medios:** Registros históricos del flujo de agua en los principales ríos y afluentes.
3. **Precipitaciones:** Registro meteorológico nacional de lluvias (2010 - 2024).
4. **Factores de Emisión:** Análisis detallado del despacho de combustibles (Gas Natural, Fuel Oil, Gas Oil, Carbón) y toneladas de CO2 emitidas en 2022.

---

## 💻 Cómo ejecutar el proyecto localmente

Si deseás correr esta aplicación en tu propia computadora, seguí estos pasos:

1. **Cloná el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/energi-ar.git](https://github.com/solgrassi/energi.Ar.git)
   cd energi-ar
   
Creá un entorno virtual (recomendado):

Bash
python -m venv venv
source venv/Scripts/activate  # En Windows

Instalá las dependencias:

Bash
pip install -r requirements.txt
Iniciá la aplicación:

Bash
streamlit run app.py
