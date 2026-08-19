# =============================================================================
# index.py - Archivo principal del Dashboard MMM Multi-Agente
# =============================================================================

import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os

DIRECTORIO_ACTUAL = Path(__file__).resolve().parent
CARPETA_PAGINAS = DIRECTORIO_ACTUAL / "paginas"

if str(DIRECTORIO_ACTUAL) not in sys.path:
    sys.path.insert(0, str(DIRECTORIO_ACTUAL))
if str(CARPETA_PAGINAS) not in sys.path:
    sys.path.insert(0, str(CARPETA_PAGINAS))

# =============================================================================
# CONFIGURACIÓN DE LA PÁGINA DE STREAMLIT
# =============================================================================
st.set_page_config(
    page_title="Dashboard Marketing & MMM - CUN",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# ESTILOS CSS GLOBALES
# =============================================================================
st.markdown(
    """<style>
[data-testid="stHeader"] {background: rgba(0,0,0,0); height: 0rem;}
.block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
.main-title { font-size: 28px; font-weight: bold; color: #1d2939; margin-bottom: 5px; }
.fecha { background: #f8fafc; padding: 8px 15px; border-radius: 8px; font-weight: bold; 
         box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05); color: #1d2939; float: right; font-size: 13px;}
.footer {
    margin-top: 3rem;
    padding: 1rem;
    text-align: center;
    font-size: 12px;
    color: #666;
    border-top: 1px solid #ddd;
}
</style>""",
    unsafe_allow_html=True,
)


# =============================================================================
# FUNCIÓN PARA OBTENER ARCHIVOS DISPONIBLES
# =============================================================================
def obtener_archivos_disponibles():
    archivos = {}
    carpeta_datos = DIRECTORIO_ACTUAL / "data"
    if carpeta_datos.exists():
        for archivo in carpeta_datos.glob("*.xlsx"):
            archivos[archivo.stem] = str(archivo)
    for archivo in DIRECTORIO_ACTUAL.glob("*.xlsx"):
        if archivo.stem not in archivos:
            archivos[archivo.stem] = str(archivo)
    carpeta_presentacion = DIRECTORIO_ACTUAL / "presentacion"
    if carpeta_presentacion.exists():
        for archivo in carpeta_presentacion.glob("*.xlsx"):
            if archivo.stem not in archivos:
                archivos[archivo.stem] = str(archivo)
    if not archivos:
        archivos = {"📤 Subir archivo manual": "manual_upload"}
    return archivos


# =============================================================================
# CARGA DE DATOS
# =============================================================================
@st.cache_data
def cargar_datos(ruta_archivo):
    try:
        try:
            df = pd.read_excel(
                ruta_archivo, sheet_name="Proyecciones_Campanas", engine="openpyxl"
            )
        except:
            st.warning(
                "No se encontró la pestaña 'Proyecciones_Campanas'. Cargando la primera hoja."
            )
            df = pd.read_excel(ruta_archivo, engine="openpyxl")
        df.columns = df.columns.str.strip()
        cols_numericas = [
            "Oportunidades Totales (Leads)",
            "Matriculas Reales",
            "Meta Estudiantes",
            "Inversion Gasto Distribuido",
            "Proyeccion Cierre (Modelada)",
            "Meta Leads",
        ]
        for col in cols_numericas:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        return df
    except Exception as e:
        st.error(f"Error al leer el archivo Excel: {e}")
        return pd.DataFrame()


# =============================================================================
# FUNCIÓN RENDER - DIBUJA LOS GRÁFICOS DE RESULTADOS
# =============================================================================
def render_resultados(df_filtrado, df_raw):
    """
    FUNCIÓN RENDER: Recibe el DataFrame filtrado y el completo, y dibuja los gráficos.

    PARÁMETROS:
    - df_filtrado: Datos con los filtros aplicados (periodo, programa, fuente)
    - df_raw: Todos los datos sin filtrar (para metas totales)

    QUÉ HACE:
    1. Muestra gráfico de barras: Proyección vs Meta por periodo
    2. Muestra gráfico de gasto por canal
    3. Muestra top 10 campañas por cierre modelado
    4. Muestra volumen de leads por fuente
    5. Muestra tabla detallada de datos
    """

    st.markdown(
        '<div style="background: white; border-radius: 15px; padding: 25px; margin-bottom: 30px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);">'
        '<h2 style="color: #7FBC03; font-size: 28px; margin-bottom: 20px; border-bottom: 3px solid #7FBC03; padding-bottom: 12px;">📊 Resultados Ejecutivos y Proyecciones</h2>',
        unsafe_allow_html=True,
    )

    # Si no hay datos filtrados, mostrar advertencia
    if df_filtrado.empty:
        st.warning("⚠️ No hay datos para mostrar con los filtros seleccionados.")
        return

    # ===== GRÁFICO 1: Brecha de Estudiantes =====
    st.subheader("1. Brecha de Estudiantes: Proyección vs Meta")

    df_agrup_proy = (
        df_filtrado.groupby("Periodo Meta")["Proyeccion Cierre (Modelada)"]
        .sum()
        .reset_index()
    )

    if not df_raw.empty:
        meta_col = (
            "Meta Estudiantes"
            if "Meta Estudiantes" in df_raw.columns
            else "Meta Estudiantes Asignada"
        )
        df_agrup_inv = df_raw.groupby("Periodo Meta")[meta_col].sum().reset_index()
        meta_map = dict(zip(df_agrup_inv["Periodo Meta"], df_agrup_inv[meta_col]))
        df_agrup_proy["Meta_Estudiantes"] = (
            df_agrup_proy["Periodo Meta"].map(meta_map).fillna(0)
        )
    else:
        df_agrup_proy["Meta_Estudiantes"] = 0

    df_brecha = df_agrup_proy.sort_values(by="Periodo Meta")

    if not df_brecha.empty and df_brecha["Meta_Estudiantes"].sum() > 0:
        df_brecha["Cumplimiento"] = (
            df_brecha["Proyeccion Cierre (Modelada)"]
            / df_brecha["Meta_Estudiantes"].replace(0, 1)
        ) * 100

        fig_brechas = go.Figure()
        fig_brechas.add_trace(
            go.Bar(
                x=df_brecha["Periodo Meta"],
                y=df_brecha["Meta_Estudiantes"],
                name="🎯 Meta Académica",
                marker_color="#A3B1C6",
                text=[f"{int(m):,}" for m in df_brecha["Meta_Estudiantes"]],
                textposition="auto",
            )
        )

        colores_cierre = [
            "#2E7D32" if pct >= 100 else "#F5A623" if pct >= 65 else "#C02424"
            for pct in df_brecha["Cumplimiento"]
        ]
        fig_brechas.add_trace(
            go.Bar(
                x=df_brecha["Periodo Meta"],
                y=df_brecha["Proyeccion Cierre (Modelada)"],
                name="📈 Proyección Modelada",
                marker_color=colores_cierre,
                text=[f"{int(c):,}" for c in df_brecha["Proyeccion Cierre (Modelada)"]],
                textposition="auto",
            )
        )
        fig_brechas.update_layout(
            barmode="group", plot_bgcolor="white", margin=dict(l=20, r=20, t=10, b=10)
        )
        st.plotly_chart(fig_brechas, use_container_width=True)
        st.caption(
            "🟢 Verde = Cumplimiento >= 100% | 🟡 Amarillo = 65% - 99% | 🔴 Rojo = < 65%"
        )
    else:
        st.info("ℹ️ No hay datos suficientes para mostrar las metas.")

    # ===== GRÁFICO 2: Distribución de Gasto y Top Campañas =====
    st.write("---")
    st.subheader("2. Distribución de Gasto y Top Campañas")

    col_g1, col_g2 = st.columns([40, 60])

    with col_g1:
        if "Fuente Clasificada" in df_filtrado.columns:
            df_gasto_canal = (
                df_filtrado.groupby("Fuente Clasificada")["Inversion Gasto Distribuido"]
                .sum()
                .reset_index()
            )
            fig_gasto = px.bar(
                df_gasto_canal,
                x="Fuente Clasificada",
                y="Inversion Gasto Distribuido",
                color="Fuente Clasificada",
                title="💰 Presupuesto por Canal",
                text_auto=".2s",
                color_discrete_sequence=px.colors.qualitative.Safe,
            )
            st.plotly_chart(fig_gasto, use_container_width=True)

    with col_g2:
        df_cierres_campana = (
            df_filtrado.groupby("Campana Mercadeo")["Proyeccion Cierre (Modelada)"]
            .sum()
            .reset_index()
        )
        df_cierres_campana = df_cierres_campana.sort_values(
            by="Proyeccion Cierre (Modelada)", ascending=False
        ).head(10)
        fig_cierres_cam = px.bar(
            df_cierres_campana,
            y="Campana Mercadeo",
            x="Proyeccion Cierre (Modelada)",
            orientation="h",
            title="🏆 Top 10 Campañas por Cierre Modelado",
            text_auto=".1f",
            color="Proyeccion Cierre (Modelada)",
            color_continuous_scale=px.colors.sequential.Magenta,
        )
        st.plotly_chart(fig_cierres_cam, use_container_width=True)

    # ===== GRÁFICO 3: Volumen de Leads por Fuente =====
    st.write("---")
    st.subheader("3. Volumen de Leads por Fuente")

    if "Fuente Clasificada" in df_filtrado.columns:
        df_grafico = (
            df_filtrado.groupby("Fuente Clasificada")
            .agg(Total_Leads=("Oportunidades Totales (Leads)", "sum"))
            .reset_index()
            .sort_values(by="Total_Leads", ascending=True)
        )
        if not df_grafico.empty:
            fig_canales = px.bar(
                df_grafico,
                y="Fuente Clasificada",
                x="Total_Leads",
                orientation="h",
                color="Total_Leads",
                color_continuous_scale=px.colors.sequential.Blugrn,
                text_auto=".s",
                title="👥 Volumen de Leads por Fuente",
            )
            st.plotly_chart(fig_canales, use_container_width=True)

    # ===== TABLA DETALLADA =====
    st.write("---")
    st.subheader("📋 Matriz Detallada de Proyecciones")
    st.dataframe(df_filtrado, use_container_width=True)


# =============================================================================
# FUNCIÓN PARA MOSTRAR RESEÑA DE MODELOS
# =============================================================================
def mostrar_resena_modelos():
    st.markdown("## 🧠 MODELOS UTILIZADOS Y MÉTRICAS")
    st.markdown(
        """
    <div style="background: #f8fafc; border-radius: 10px; padding: 20px; border-left: 5px solid #7FBC03;">
    <h4>📖 Resumen de Modelos</h4>
    <p>Este dashboard integra 4 modelos analíticos:</p>
    <ul>
        <li><strong>1. MMM (Atribución Multi-Touch):</strong> Distribuye el crédito de conversión entre todos los puntos de contacto</li>
        <li><strong>2. Proyección de Cierre:</strong> Predice estudiantes que se matricularán al final del período</li>
        <li><strong>3. Eficiencia de Campañas:</strong> Calcula ROI y costo por lead</li>
        <li><strong>4. Segmentación de Audiencia:</strong> Identifica perfiles con mayor conversión</li>
    </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )


# =============================================================================
# FUNCIÓN PARA MOSTRAR ANÁLISIS DE CONSULTAS
# =============================================================================
def mostrar_tabla_analisis():
    st.markdown("## 📊 ANÁLISIS DE CONSULTAS SQL")
    data = [
        {
            "CONSULTA": "1. INGRESOS",
            "PROPÓSITO": "Extraer leads generados por Marketing",
        },
        {"CONSULTA": "2. OPORTUNIDADES", "PROPÓSITO": "Identificar leads calificados"},
        {
            "CONSULTA": "3. MATRÍCULAS",
            "PROPÓSITO": "Identificar estudiantes nuevos con pago",
        },
        {"CONSULTA": "4. METAS", "PROPÓSITO": "Obtener metas oficiales de estudiantes"},
        {
            "CONSULTA": "5. INVERSIÓN",
            "PROPÓSITO": "Calcular inversión por campaña y CPL",
        },
    ]
    st.dataframe(pd.DataFrame(data), use_container_width=True)


# =============================================================================
# MAIN
# =============================================================================
def main():

    # SIDEBAR
    st.sidebar.markdown(
        """<div style="background-color:#7FBC03;padding:10px;text-align:center;border-radius:8px;margin-bottom:15px;">
    <h2 style="color:white;margin:0;">🏫 CUN</h2>
    <p style="color:white;margin:5px 0 0 0;font-size:11px;">Pipeline Multi-Agente MMM</p>
    </div>""",
        unsafe_allow_html=True,
    )

    # SELECTOR DE ARCHIVOS
    st.sidebar.header("📂 Seleccionar Datos")
    archivos_disponibles = obtener_archivos_disponibles()

    if len(archivos_disponibles) > 1:
        opciones = list(archivos_disponibles.keys())
        archivo_seleccionado = st.sidebar.selectbox(
            "📁 Seleccionar archivo:", options=opciones
        )
        ruta_archivo = archivos_disponibles[archivo_seleccionado]
        if ruta_archivo != "manual_upload":
            st.sidebar.info(f"📁 Cargando: {archivo_seleccionado}")
        else:
            ruta_archivo = None
    else:
        st.sidebar.warning("⚠️ No se encontraron archivos Excel")
        archivo_seleccionado = "📤 Subir archivo manual"
        ruta_archivo = None

    # SUBIDA MANUAL
    if ruta_archivo is None or archivo_seleccionado == "📤 Subir archivo manual":
        uploaded_file = st.sidebar.file_uploader(
            "📤 Subir archivo Excel", type=["xlsx", "xls"]
        )
        if uploaded_file is not None:
            temp_path = DIRECTORIO_ACTUAL / "temp_upload.xlsx"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            ruta_archivo = str(temp_path)
            st.sidebar.success("✅ Archivo subido correctamente")
        else:
            st.sidebar.warning("📤 Por favor, sube un archivo")
            st.stop()

    # CARGA DE DATOS
    if ruta_archivo and ruta_archivo != "manual_upload":
        with st.spinner(f"Cargando {archivo_seleccionado}..."):
            df_base = cargar_datos(ruta_archivo)
    else:
        df_base = pd.DataFrame()

    # VERIFICAR DATOS
    if df_base.empty:
        st.sidebar.error("❌ Error al cargar los datos")
        st.error("No se pudieron cargar los datos.")
        st.stop()

    st.sidebar.success(f"✅ {len(df_base):,} filas cargadas")

    # NAVEGACIÓN
    st.sidebar.write("---")
    st.sidebar.header("🗺️ Navegación")
    pagina = st.sidebar.radio(
        "Seleccionar Vista:",
        [
            "📊 Presentación y Modelo",
            "📈 Resultados Ejecutivos",
            "📋 Análisis de Consultas",
        ],
    )
    st.sidebar.write("---")

    # FILTROS
    df_filtrado = pd.DataFrame()
    if pagina != "📋 Análisis de Consultas":
        st.sidebar.header("🎯 Filtros")
        df_filtrado = df_base.copy()

        if "Periodo Meta" in df_filtrado.columns:
            periodos = ["Todos"] + sorted(
                [str(p) for p in df_filtrado["Periodo Meta"].dropna().unique()]
            )
            periodo_sel = st.sidebar.selectbox("📅 Periodo Meta:", periodos)
            if periodo_sel != "Todos":
                df_filtrado = df_filtrado[
                    df_filtrado["Periodo Meta"].astype(str) == periodo_sel
                ]

        if "Programa Academico" in df_filtrado.columns:
            programas = ["Todos"] + sorted(
                [str(p) for p in df_filtrado["Programa Academico"].dropna().unique()]
            )
            programa_sel = st.sidebar.selectbox("🎓 Programa:", programas)
            if programa_sel != "Todos":
                df_filtrado = df_filtrado[
                    df_filtrado["Programa Academico"].astype(str) == programa_sel
                ]

        if "Fuente Clasificada" in df_filtrado.columns:
            fuentes = ["Todos"] + sorted(
                [str(f) for f in df_filtrado["Fuente Clasificada"].dropna().unique()]
            )
            fuente_sel = st.sidebar.selectbox("📢 Fuente:", fuentes)
            if fuente_sel != "Todos":
                df_filtrado = df_filtrado[
                    df_filtrado["Fuente Clasificada"].astype(str) == fuente_sel
                ]

    # HEADER PRINCIPAL
    fecha_actual = datetime.now().strftime("%d de %B de %Y")
    st.markdown(f'<div class="fecha">📅 {fecha_actual}</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="main-title">🏫 Dashboard MMM & Proyecciones de Cierre - Multi-Agente</p>',
        unsafe_allow_html=True,
    )
    st.write("---")

    # RENDERIZADO DE PÁGINAS
    try:
        if pagina == "📊 Presentación y Modelo":
            mostrar_resena_modelos()
            st.write("---")
            st.dataframe(df_base, use_container_width=True)

        elif pagina == "📈 Resultados Ejecutivos":
            # AQUÍ SE LLAMA A LA FUNCIÓN RENDER
            render_resultados(df_filtrado, df_base)

        else:
            mostrar_tabla_analisis()

    except Exception as e:
        st.error(f"Error al renderizar: {e}")

    # FOOTER
    st.markdown(
        f"""
    <div class="footer">
        <p>📊 Dashboard MMM - CUN | Versión 3.0 | Datos actualizados julio 2026</p>
        <p style="font-size:10px;color:#999;">📁 Archivo: {archivo_seleccionado}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
