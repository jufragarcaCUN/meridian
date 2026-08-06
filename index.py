# =============================================================================
# index.py - Archivo principal del Dashboard MMM Multi-Agente
# =============================================================================

import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# =============================================================================
# 1. CONFIGURACIÓN DE RUTAS E IMPORTACIÓN DE MÓDULOS LOCALES
# =============================================================================
DIRECTORIO_ACTUAL = Path(__file__).resolve().parent
CARPETA_PAGINAS = DIRECTORIO_ACTUAL / "paginas"

if str(DIRECTORIO_ACTUAL) not in sys.path:
    sys.path.insert(0, str(DIRECTORIO_ACTUAL))
if str(CARPETA_PAGINAS) not in sys.path:
    sys.path.insert(0, str(CARPETA_PAGINAS))

# IMPORTAR LOS MÓDULOS DE PÁGINAS
try:
    from paginas import presentacion
    from paginas import resultados
except ModuleNotFoundError as e:
    st.error(f"Error al importar módulos: {e}")
    st.info(
        "Asegúrate de que la carpeta 'paginas/' existe y contiene __init__.py, presentacion.py y resultados.py"
    )
    st.stop()

# =============================================================================
# 2. CONFIGURACIÓN DE LA PÁGINA DE STREAMLIT
# =============================================================================
st.set_page_config(
    page_title="Dashboard Marketing & MMM - CUN",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# 3. ESTILOS CSS GLOBALES
# =============================================================================
st.markdown(
    """
    <style>
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
        .seccion-contenedor { background: white; border-radius: 15px; padding: 25px; margin-bottom: 30px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08); }
        .seccion-contenedor h2 { color: #7FBC03; font-size: 28px; margin-bottom: 20px; border-bottom: 3px solid #7FBC03; padding-bottom: 12px; }
        .explicacion-tecnica {
            background: #f8fafc;
            border-left: 5px solid #7FBC03;
            padding: 20px 25px;
            border-radius: 10px;
            margin: 20px 0;
            font-size: 16px;
            line-height: 1.8;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# 4. CARGA DE DATOS
# =============================================================================
@st.cache_data
def cargar_datos():
    archivo = "reporte_master_mmm_proyecciones_2026(13).xlsx"
    try:
        df = pd.read_excel(
            archivo, sheet_name="Proyecciones_Campanas", engine="openpyxl"
        )
    except Exception as e:
        st.error(f"Error al leer el archivo Excel: {e}")
        return pd.DataFrame()

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


# =============================================================================
# 5. FUNCIÓN PARA MOSTRAR TABLA DE ANÁLISIS
# =============================================================================
def mostrar_tabla_analisis():
    st.markdown("## 📊 ANÁLISIS DE CONSULTAS SQL")
    st.markdown("---")

    data = [
        {
            "CONSULTA": "1. INGRESOS",
            "TABLA PRINCIPAL": "CUN_REPOSITORIO.CRM.Registros_CRM",
            "PROPÓSITO": "Extraer leads generados por Marketing (Meta y Google)",
            "COLUMNAS CLAVE": "id_base, número_de_documento, periodo, nombre_de_campaña_mercadeo, programalimpio, canal_fuente, modalidad, fec_crea",
            "FILTROS IMPORTANTES": "ingreso_lead='ingreso', creador_lead='MARKETING', fuerzacomercial='Contact', canal_fuente IN ('META','GADS')",
            "QUÉ APORTA": "Total de leads generados, segmentación por campaña, programa, canal y modalidad",
        },
        {
            "CONSULTA": "2. OPORTUNIDADES",
            "TABLA PRINCIPAL": "CUN_REPOSITORIO.CRM.Registros_CRM",
            "PROPÓSITO": "Identificar leads que avanzaron a oportunidad (más calificados)",
            "COLUMNAS CLAVE": "id_base, número_de_documento, periodo, nombre_de_campaña_mercadeo, programalimpio, canal_fuente, modalidad",
            "FILTROS IMPORTANTES": "tipo_registro='Oportunidad', creador_lead='MARKETING', fuerzacomercial='Contact', canal_fuente IN ('META','GADS')",
            "QUÉ APORTA": "Base para conversión Lead → Oportunidad",
        },
        {
            "CONSULTA": "3. MATRÍCULAS",
            "TABLA PRINCIPAL": "Registros_CRM + Zoho.Base_Personas (JOIN)",
            "PROPÓSITO": "Identificar estudiantes nuevos que pagaron (matrículas reales)",
            "COLUMNAS CLAVE": "id_base, periodo, programalimpio AS PROGRAMA, modalidad AS MODALIDA, Fuente_Aspirante, NUEVO, Estado_pago_data",
            "FILTROS IMPORTANTES": "bp.NUEVO='NUEVO', bp.Estado_pago_data='PAGO', bp.fuerza_comercial_data='CONTACT'",
            "QUÉ APORTA": "Matrículas reales y tasa de conversión",
        },
        {
            "CONSULTA": "4. METAS",
            "TABLA PRINCIPAL": "financiera.metas + Periodos_Calendario (JOIN)",
            "PROPÓSITO": "Obtener metas oficiales de estudiantes y calcular leads necesarios",
            "COLUMNAS CLAVE": "PROGRAMA_ACADEMICO, MODALIDAD, PERIODO, META (suma), META_LEADS (META/0.15)",
            "FILTROS IMPORTANTES": "FUERZA_COMERCIAL='CONTACT', fec_inicio BETWEEN '2026-06-01' AND '2026-12-31'",
            "QUÉ APORTA": "Metas de estudiantes y leads",
        },
        {
            "CONSULTA": "5. INVERSIÓN",
            "TABLA PRINCIPAL": "METAADS + GoogleAds (UNION) + Registros_CRM (LEFT JOIN)",
            "PROPÓSITO": "Calcular inversión por campaña y costo por lead",
            "COLUMNAS CLAVE": "canal_fuente, CAMPAÑA, INVERSION_1, TOTAL_LEADS, periodo, EJECUTADO_DISTRIBUIDO",
            "FILTROS IMPORTANTES": "Fechas 2025-2026, tipo_registro='POSIBLE_CLIENTE'",
            "QUÉ APORTA": "Costo por lead (CPL) y eficiencia",
        },
    ]

    df_analisis = pd.DataFrame(data)

    st.dataframe(
        df_analisis,
        use_container_width=True,
        height=400,
        column_config={
            "CONSULTA": st.column_config.TextColumn("CONSULTA", width="small"),
            "TABLA PRINCIPAL": st.column_config.TextColumn(
                "TABLA PRINCIPAL", width="medium"
            ),
            "PROPÓSITO": st.column_config.TextColumn("PROPÓSITO", width="medium"),
            "COLUMNAS CLAVE": st.column_config.TextColumn(
                "COLUMNAS CLAVE", width="large"
            ),
            "FILTROS IMPORTANTES": st.column_config.TextColumn(
                "FILTROS IMPORTANTES", width="large"
            ),
            "QUÉ APORTA": st.column_config.TextColumn("QUÉ APORTA", width="large"),
        },
    )

    st.markdown("---")
    st.markdown("### 🔗 RELACIÓN ENTRE CONSULTAS")


# =============================================================================
# 6. MAIN - PUNTO DE ENTRADA PRINCIPAL
# =============================================================================
def main():
    df_raw = cargar_datos()

    # ===== SIDEBAR =====
    st.sidebar.markdown(
        '<div style="background-color: #7FBC03; padding: 10px; text-align: center; border-radius: 8px; margin-bottom: 15px;">'
        '<h2 style="color: white; margin: 0; font-weight: bold;">🏫 CUN</h2>'
        '<p style="color: white; margin: 5px 0 0 0; font-size: 11px;">Pipeline Multi-Agente MMM</p>'
        "</div>",
        unsafe_allow_html=True,
    )

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

    # ===== FILTROS =====
    if pagina != "📋 Análisis de Consultas":
        st.sidebar.header("🎯 Filtros Dependientes")
        df_filtrado = df_raw.copy() if not df_raw.empty else pd.DataFrame()

        if not df_raw.empty:
            # Filtro Periodo
            if "Periodo Meta" in df_filtrado.columns:
                periodos = ["Todos"] + sorted(
                    [str(p) for p in df_filtrado["Periodo Meta"].dropna().unique()]
                )
                periodo_sel = st.sidebar.selectbox("📅 Periodo Meta:", periodos)
                if periodo_sel != "Todos":
                    df_filtrado = df_filtrado[
                        df_filtrado["Periodo Meta"].astype(str) == periodo_sel
                    ]

            # Filtro Programa
            if "Programa Academico" in df_filtrado.columns:
                programas = ["Todos"] + sorted(
                    [
                        str(p)
                        for p in df_filtrado["Programa Academico"].dropna().unique()
                    ]
                )
                programa_sel = st.sidebar.selectbox("🎓 Programa Académico:", programas)
                if programa_sel != "Todos":
                    df_filtrado = df_filtrado[
                        df_filtrado["Programa Academico"].astype(str) == programa_sel
                    ]

            # Filtro Fuente
            if "Fuente Clasificada" in df_filtrado.columns:
                fuentes = ["Todos"] + sorted(
                    [
                        str(f)
                        for f in df_filtrado["Fuente Clasificada"].dropna().unique()
                    ]
                )
                fuente_sel = st.sidebar.selectbox("📢 Fuente Clasificada:", fuentes)
                if fuente_sel != "Todos":
                    df_filtrado = df_filtrado[
                        df_filtrado["Fuente Clasificada"].astype(str) == fuente_sel
                    ]
    else:
        df_filtrado = pd.DataFrame()

    # ===== HEADER =====
    fecha_actual = pd.Timestamp.now().strftime("%d de %B de %Y")
    st.markdown(f'<div class="fecha">📅 {fecha_actual}</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="main-title">🏫 Dashboard MMM & Proyecciones de Cierre - Multi-Agente</p>',
        unsafe_allow_html=True,
    )
    st.write("---")

    # ===== RENDERIZADO DE PÁGINAS =====
    try:
        if pagina == "📊 Presentación y Modelo":
            if not df_raw.empty:
                presentacion.render(df_raw)
            else:
                st.warning("No hay datos para mostrar.")

        elif pagina == "📈 Resultados Ejecutivos":
            if not df_raw.empty:
                resultados.render(df_filtrado, df_raw)
            else:
                st.warning("No hay datos para mostrar.")

        else:  # Análisis de Consultas
            mostrar_tabla_analisis()

    except AttributeError as e:
        st.error(f"Error: {e}")
        st.info("""
        **Posibles causas:**
        1. Los archivos en `paginas/` no tienen la función `render()`
        2. La función `render()` tiene parámetros incorrectos
        3. El archivo `paginas/__init__.py` no existe
        """)
    except Exception as e:
        st.error(f"Error al renderizar la página: {e}")

    # ===== FOOTER =====
    st.markdown(
        """
        <div class="footer">
            <p>📊 Dashboard MMM - CUN &nbsp;|&nbsp; Versión 3.0 &nbsp;|&nbsp; 
            <span style="color: #7FBC03;">Datos actualizados al corte de julio 2026</span></p>
            <p style="font-size: 10px; color: #999;">Desarrollado por el equipo de Data & Analytics - CUN</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
