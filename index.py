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
.modelo-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 20px;
    margin: 8px 0;
    border: 1px solid #e8ecf0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    transition: all 0.3s ease;
    height: 100%;
}
.modelo-card:hover {
    box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    transform: translateY(-2px);
}
.modelo-card h4 {
    color: #7FBC03;
    margin-top: 0;
    margin-bottom: 10px;
    font-size: 17px;
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}
.modelo-card .badge {
    background: #7FBC03;
    color: white;
    font-size: 10px;
    padding: 2px 12px;
    border-radius: 20px;
    font-weight: bold;
}
.modelo-card .badge-google {
    background: #4285F4;
    color: white;
    font-size: 10px;
    padding: 2px 12px;
    border-radius: 20px;
    font-weight: bold;
}
.modelo-card .badge-meta {
    background: #1877F2;
    color: white;
    font-size: 10px;
    padding: 2px 12px;
    border-radius: 20px;
    font-weight: bold;
}
.modelo-card .badge-prediction {
    background: #E37400;
    color: white;
    font-size: 10px;
    padding: 2px 12px;
    border-radius: 20px;
    font-weight: bold;
}
.modelo-card .badge-efficiency {
    background: #00A86B;
    color: white;
    font-size: 10px;
    padding: 2px 12px;
    border-radius: 20px;
    font-weight: bold;
}
.modelo-card .badge-segmentation {
    background: #8B5CF6;
    color: white;
    font-size: 10px;
    padding: 2px 12px;
    border-radius: 20px;
    font-weight: bold;
}
.modelo-card .detalle {
    color: #555;
    font-size: 14px;
    line-height: 1.7;
}
.modelo-card .formula {
    background: #f0f4f8;
    padding: 10px 16px;
    border-radius: 8px;
    font-family: 'Courier New', monospace;
    font-size: 13px;
    margin: 10px 0;
    color: #1d2939;
    border: 1px solid #e2e8f0;
}
.modelo-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
    margin: 15px 0;
}
@media (max-width: 768px) {
    .modelo-grid {
        grid-template-columns: 1fr;
    }
}
.resena-general {
    background: linear-gradient(135deg, #f0f7f0 0%, #e8f0e8 100%);
    border-radius: 15px;
    padding: 25px 30px;
    margin-bottom: 30px;
    border-left: 6px solid #7FBC03;
}
.resena-general h3 {
    color: #2d5a2d;
    margin-top: 0;
}
.resena-general ul {
    margin-bottom: 0;
    line-height: 1.8;
}
.resena-general li {
    margin-bottom: 8px;
}
.metrica-item {
    background: #f8fafc;
    padding: 12px 16px;
    border-radius: 8px;
    margin: 10px 0;
    border-left: 4px solid #7FBC03;
}
.metrica-item .formula {
    font-size: 13px;
    margin: 6px 0;
}
.metrica-item .explicacion {
    margin: 4px 0;
    font-size: 13px;
    color: #444;
}
.metrica-item .interpretacion {
    margin: 4px 0;
    font-size: 13px;
    color: #555;
    background: #e8f0fe;
    padding: 4px 10px;
    border-radius: 6px;
    display: inline-block;
}
</style>""",
    unsafe_allow_html=True,
)


# =============================================================================
# 4. CARGA DE DATOS CON SELECTOR DE ARCHIVOS
# =============================================================================
@st.cache_data
def cargar_datos(ruta_archivo):
    """
    Carga datos desde un archivo Excel especificado.

    Args:
        ruta_archivo (str): Ruta completa al archivo Excel

    Returns:
        pd.DataFrame: DataFrame con los datos cargados
    """
    try:
        # Intentar cargar con la pestaña específica "Proyecciones_Campanas"
        try:
            df = pd.read_excel(
                ruta_archivo, sheet_name="Proyecciones_Campanas", engine="openpyxl"
            )
        except Exception as e:
            # Si no existe esa pestaña, cargar la primera hoja
            st.warning(
                f"No se encontró la pestaña 'Proyecciones_Campanas'. Cargando la primera hoja disponible."
            )
            df = pd.read_excel(ruta_archivo, engine="openpyxl")

        # Limpiar nombres de columnas (eliminar espacios al inicio y final)
        df.columns = df.columns.str.strip()

        # Convertir columnas numéricas a tipo float
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
# 5. FUNCIÓN PARA MOSTRAR RESEÑA DE MODELOS Y MÉTRICAS
# =============================================================================
def mostrar_resena_modelos():
    """Muestra una reseña completa de los modelos utilizados y sus métricas en grid de 2 columnas"""

    st.markdown("## 🧠 MODELOS UTILIZADOS Y MÉTRICAS")

    # ===== RESEÑA GENERAL =====
    st.markdown(
        """<div class="resena-general">
<h3>📖 ¿Cómo funciona este dashboard?</h3>
<p>Este dashboard integra <strong>4 modelos analíticos</strong> que trabajan en conjunto para predecir y optimizar 
el rendimiento de las campañas de marketing. Cada modelo aporta una perspectiva única:</p>
<ul>
    <li><strong>1. Modelo de Atribución Multi-Touch (MMM):</strong> Distribuye el crédito de conversión entre todos los puntos de contacto</li>
    <li><strong>2. Modelo de Proyección de Cierre:</strong> Predice el número de estudiantes que se matricularán al final del período</li>
    <li><strong>3. Modelo de Eficiencia de Campañas:</strong> Calcula el ROI y costo por lead de cada campaña</li>
    <li><strong>4. Modelo de Segmentación de Audiencia:</strong> Identifica perfiles de estudiantes con mayor probabilidad de conversión</li>
</ul>
<p style="margin-top: 12px;"><strong>🎯 Objetivo:</strong> Proporcionar una visión integral del desempeño de marketing para la toma de decisiones estratégicas.</p>
</div>""",
        unsafe_allow_html=True,
    )

    # ===== MODELOS EN GRID DE 2 EN 2 =====
    st.markdown("### 📊 Detalle de Modelos y Métricas")

    modelos = [
        {
            "nombre": "Modelo de Atribución Multi-Touch (MMM)",
            "badge": "ATTRIBUTION",
            "badge_class": "badge",
            "emoji": "🎯",
            "descripcion": "Distribuye el crédito de conversión entre todos los puntos de contacto del cliente (Meta Ads, Google Ads, etc.) basado en su contribución real al funnel de ventas.",
            "metricas": [
                {
                    "nombre": "Oportunidades Totales (Leads)",
                    "formula": "SUM(leads_generados) - SUM(leads_duplicados)",
                    "explicacion": "Total de leads únicos generados por todas las campañas, sin duplicados.",
                    "interpretacion": "Alto = Mayor alcance y captación de interés",
                },
                {
                    "nombre": "Inversión Gasto Distribuido",
                    "formula": "Σ(Gasto_Campaña_i × Peso_Atribución_i)",
                    "explicacion": "Gasto total distribuido proporcionalmente según la contribución de cada campaña.",
                    "interpretacion": "Permite identificar campañas con mejor relación costo-beneficio",
                },
                {
                    "nombre": "Costo por Lead (CPL)",
                    "formula": "Inversión Total / Leads Totales",
                    "explicacion": "Costo promedio de adquirir un lead.",
                    "interpretacion": "Menor = Mayor eficiencia en la captación",
                },
            ],
        },
        {
            "nombre": "Modelo de Proyección de Cierre",
            "badge": "PREDICTION",
            "badge_class": "badge-prediction",
            "emoji": "🔮",
            "descripcion": "Predice el número de estudiantes que se matricularán al final del período basándose en el comportamiento histórico y la tasa de conversión actual.",
            "metricas": [
                {
                    "nombre": "Proyección Cierre (Modelada)",
                    "formula": "Leads_Actuales × Tasa_Conversión_Histórica × Factor_Estacionalidad",
                    "explicacion": "Estimación del número de estudiantes que se matricularán al final del período.",
                    "interpretacion": "Permite planificar recursos y metas",
                },
                {
                    "nombre": "Tasa de Conversión Lead → Matrícula",
                    "formula": "(Matrículas / Leads) × 100",
                    "explicacion": "Porcentaje de leads que se convierten en matrículas.",
                    "interpretacion": "Alto = Mayor calidad de leads y efectividad comercial",
                },
            ],
        },
        {
            "nombre": "Modelo de Eficiencia de Campañas",
            "badge": "EFFICIENCY",
            "badge_class": "badge-efficiency",
            "emoji": "📈",
            "descripcion": "Evalúa el rendimiento de cada campaña calculando el ROI (Retorno de Inversión) y el costo por lead, permitiendo optimizar la asignación de presupuesto.",
            "metricas": [
                {
                    "nombre": "Matrículas Reales",
                    "formula": "COUNT(matriculas_confirmadas)",
                    "explicacion": "Número total de estudiantes que se matricularon efectivamente.",
                    "interpretacion": "Mide el impacto real en el negocio",
                },
                {
                    "nombre": "Meta Estudiantes vs Meta Leads",
                    "formula": "Meta_Estudiantes = Meta_Leads × 0.15",
                    "explicacion": "La meta de leads se calcula dividiendo la meta de estudiantes entre la tasa de conversión esperada (15%).",
                    "interpretacion": "Permite establecer metas realistas basadas en la eficiencia histórica",
                },
                {
                    "nombre": "ROI Estimado",
                    "formula": "((Matrículas × Valor_Matrícula) - Inversión) / Inversión",
                    "explicacion": "Retorno de inversión proyectado.",
                    "interpretacion": "Mayor = Mejor rentabilidad de la campaña",
                },
            ],
        },
        {
            "nombre": "Modelo de Segmentación de Audiencia",
            "badge": "SEGMENTATION",
            "badge_class": "badge-segmentation",
            "emoji": "👥",
            "descripcion": "Identifica perfiles de estudiantes con mayor probabilidad de conversión, segmentando por programa académico, modalidad y comportamiento de navegación.",
            "metricas": [
                {
                    "nombre": "Segmentación por Programa",
                    "formula": "GROUP BY(Programa_Academico, Modalidad)",
                    "explicacion": "Agrupa los leads por programa académico y modalidad para identificar qué segmentos generan más conversiones.",
                    "interpretacion": "Permite enfocar recursos en los programas más rentables",
                },
                {
                    "nombre": "Tasa de Conversión por Segmento",
                    "formula": "(Matrículas_Segmento / Leads_Segmento) × 100",
                    "explicacion": "Porcentaje de conversión específico para cada segmento de audiencia.",
                    "interpretacion": "Identifica segmentos con mejor y peor rendimiento",
                },
            ],
        },
    ]

    # Mostrar modelos en grid de 2 en 2
    for i in range(0, len(modelos), 2):
        par_modelos = modelos[i : i + 2]
        cols = st.columns(2)

        for idx, modelo in enumerate(par_modelos):
            with cols[idx]:
                modelo_html = f"""<div class="modelo-card">
<h4>
    {modelo['emoji']} {modelo['nombre']}
    <span class="{modelo['badge_class']}">{modelo['badge']}</span>
</h4>
<p class="detalle">{modelo['descripcion']}</p>"""

                for metrica in modelo["metricas"]:
                    modelo_html += f"""
<div class="metrica-item">
    <strong style="color: #1d2939; font-size: 14px;">📌 {metrica['nombre']}</strong>
    <div class="formula">
        <strong>Fórmula:</strong> {metrica['formula']}
    </div>
    <p class="explicacion">
        <strong>📖 Explicación:</strong> {metrica['explicacion']}
    </p>
    <span class="interpretacion">
        💡 {metrica['interpretacion']}
    </span>
</div>"""

                modelo_html += "\n</div>"
                st.markdown(modelo_html, unsafe_allow_html=True)

    # ===== RESUMEN DE FUENTES =====
    st.markdown("---")
    st.markdown("### 🔗 Fuentes de Datos por Modelo")

    fuentes_data = [
        {
            "Modelo": "Atribución Multi-Touch",
            "Fuente Principal": "Registros_CRM (CUN_REPOSITORIO.CRM)",
            "Tablas Relacionadas": "METAADS, GoogleAds, Base_Personas (Zoho)",
            "Periodicidad": "Diaria",
        },
        {
            "Modelo": "Proyección de Cierre",
            "Fuente Principal": "Registros_CRM + Periodos_Calendario",
            "Tablas Relacionadas": "financiera.metas, Base_Personas",
            "Periodicidad": "Semanal",
        },
        {
            "Modelo": "Eficiencia de Campañas",
            "Fuente Principal": "METAADS + GoogleAds",
            "Tablas Relacionadas": "Registros_CRM (JOIN), financiera.metas",
            "Periodicidad": "Diaria",
        },
        {
            "Modelo": "Segmentación de Audiencia",
            "Fuente Principal": "Registros_CRM",
            "Tablas Relacionadas": "Base_Personas, financiera.metas",
            "Periodicidad": "Semanal",
        },
    ]

    df_fuentes = pd.DataFrame(fuentes_data)
    st.dataframe(
        df_fuentes,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Modelo": st.column_config.TextColumn("🧠 Modelo", width="medium"),
            "Fuente Principal": st.column_config.TextColumn(
                "📂 Fuente Principal", width="large"
            ),
            "Tablas Relacionadas": st.column_config.TextColumn(
                "🔗 Tablas Relacionadas", width="large"
            ),
            "Periodicidad": st.column_config.TextColumn(
                "🔄 Periodicidad", width="small"
            ),
        },
    )


# =============================================================================
# 6. FUNCIÓN PARA MOSTRAR TABLA DE ANÁLISIS
# =============================================================================
def mostrar_tabla_analisis():
    """Muestra la tabla de análisis de consultas SQL"""

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
    st.info("""
    **Relación entre las consultas:**
    1. **INGRESOS** → Obtiene todos los leads generados por marketing
    2. **OPORTUNIDADES** → Filtra los leads que avanzaron en el funnel
    3. **MATRÍCULAS** → Identifica los leads que se convirtieron en estudiantes
    4. **METAS** → Proporciona los objetivos a alcanzar
    5. **INVERSIÓN** → Calcula el costo por lead y eficiencia
    """)


# =============================================================================
# 7. MAIN - PUNTO DE ENTRADA PRINCIPAL
# =============================================================================
def main():
    """
    Función principal del dashboard.
    Controla la navegación, carga de datos y renderizado de páginas.
    """

    # ===== SIDEBAR - CONFIGURACIÓN =====
    # Encabezado del sidebar con logo de CUN
    st.sidebar.markdown(
        """<div style="background-color: #7FBC03; padding: 10px; text-align: center; border-radius: 8px; margin-bottom: 15px;">
<h2 style="color: white; margin: 0; font-weight: bold;">🏫 CUN</h2>
<p style="color: white; margin: 5px 0 0 0; font-size: 11px;">Pipeline Multi-Agente MMM</p>
</div>""",
        unsafe_allow_html=True,
    )

    # ===== SELECTOR DE ARCHIVOS EXCEL (PRIMERO Y MÁS IMPORTANTE) =====
    st.sidebar.header("📂 Seleccionar Datos")

    # Diccionario con las rutas de los archivos disponibles
    archivos_disponibles = {
        "📊 Datos 3500M": r"C:\Users\juan_garnicac\Documents\ProyectosVisual\Meridian\presentacion\3500M.xlsx",
        "📊 Datos 4250": r"C:\Users\juan_garnicac\Documents\ProyectosVisual\Meridian\presentacion\4250.xlsx",
        "📊 Datos 5000M": r"C:\Users\juan_garnicac\Documents\ProyectosVisual\Meridian\presentacion\5000M.xlsx",
    }

    # Selector de archivo - PRIMER ELEMENTO DEL SIDEBAR
    archivo_seleccionado = st.sidebar.selectbox(
        "📁 Seleccionar archivo de datos:",
        options=list(archivos_disponibles.keys()),
        index=0,  # Selecciona "Datos 3500M" por defecto
        help="Selecciona el archivo Excel con los datos de MMM que deseas analizar",
    )

    # Obtener la ruta del archivo seleccionado
    ruta_archivo = archivos_disponibles[archivo_seleccionado]

    # Mostrar información del archivo seleccionado
    st.sidebar.info(f"📁 Cargando: {archivo_seleccionado}")

    # ===== CARGA DE DATOS =====
    # Mostrar spinner mientras se cargan los datos
    with st.spinner(f"Cargando {archivo_seleccionado}..."):
        df_base = cargar_datos(ruta_archivo)

    # Verificar si los datos se cargaron correctamente
    if df_base.empty:
        st.sidebar.error(
            "❌ Error al cargar los datos. Verifica que el archivo exista y tenga el formato correcto."
        )
        st.error(
            "No se pudieron cargar los datos. Por favor, verifica la ruta del archivo."
        )
        st.stop()

    # Mostrar confirmación de carga exitosa
    st.sidebar.success(f"✅ {len(df_base):,} filas cargadas correctamente")

    # Separador visual
    st.sidebar.write("---")

    # ===== NAVEGACIÓN =====
    st.sidebar.header("🗺️ Navegación")
    pagina = st.sidebar.radio(
        "Seleccionar Vista:",
        [
            "📊 Presentación y Modelo",
            "📈 Resultados Ejecutivos",
            "📋 Análisis de Consultas",
        ],
        help="Selecciona la vista que deseas explorar",
    )
    st.sidebar.write("---")

    # ===== FILTROS DEPENDIENTES (SOLO PARA CIERTAS PÁGINAS) =====
    # Inicializar df_filtrado
    df_filtrado = pd.DataFrame()

    # Solo mostrar filtros si no estamos en la página de análisis de consultas
    if pagina != "📋 Análisis de Consultas":
        st.sidebar.header("🎯 Filtros Dependientes")
        df_filtrado = df_base.copy() if not df_base.empty else pd.DataFrame()

        if not df_base.empty:
            # ===== FILTRO POR PERIODO =====
            if "Periodo Meta" in df_filtrado.columns:
                # Obtener periodos únicos
                periodos_unicos = sorted(
                    [str(p) for p in df_filtrado["Periodo Meta"].dropna().unique()]
                )
                periodos = ["Todos"] + periodos_unicos

                # Selector de periodo
                periodo_sel = st.sidebar.selectbox(
                    "📅 Periodo Meta:",
                    periodos,
                    help="Filtra los datos por periodo académico",
                )

                # Aplicar filtro
                if periodo_sel != "Todos":
                    df_filtrado = df_filtrado[
                        df_filtrado["Periodo Meta"].astype(str) == periodo_sel
                    ]

            # ===== FILTRO POR PROGRAMA ACADÉMICO =====
            if "Programa Academico" in df_filtrado.columns:
                # Obtener programas únicos
                programas_unicos = sorted(
                    [
                        str(p)
                        for p in df_filtrado["Programa Academico"].dropna().unique()
                    ]
                )
                programas = ["Todos"] + programas_unicos

                # Selector de programa
                programa_sel = st.sidebar.selectbox(
                    "🎓 Programa Académico:",
                    programas,
                    help="Filtra los datos por programa académico",
                )

                # Aplicar filtro
                if programa_sel != "Todos":
                    df_filtrado = df_filtrado[
                        df_filtrado["Programa Academico"].astype(str) == programa_sel
                    ]

            # ===== FILTRO POR FUENTE =====
            if "Fuente Clasificada" in df_filtrado.columns:
                # Obtener fuentes únicas
                fuentes_unicas = sorted(
                    [
                        str(f)
                        for f in df_filtrado["Fuente Clasificada"].dropna().unique()
                    ]
                )
                fuentes = ["Todos"] + fuentes_unicas

                # Selector de fuente
                fuente_sel = st.sidebar.selectbox(
                    "📢 Fuente Clasificada:",
                    fuentes,
                    help="Filtra los datos por fuente de marketing (Meta, Google, etc.)",
                )

                # Aplicar filtro
                if fuente_sel != "Todos":
                    df_filtrado = df_filtrado[
                        df_filtrado["Fuente Clasificada"].astype(str) == fuente_sel
                    ]

    # ===== HEADER PRINCIPAL =====
    # Mostrar fecha actual
    fecha_actual = pd.Timestamp.now().strftime("%d de %B de %Y")
    st.markdown(f'<div class="fecha">📅 {fecha_actual}</div>', unsafe_allow_html=True)

    # Título principal
    st.markdown(
        '<p class="main-title">🏫 Dashboard MMM & Proyecciones de Cierre - Multi-Agente</p>',
        unsafe_allow_html=True,
    )
    st.write("---")

    # ===== RENDERIZADO DE PÁGINAS =====
    try:
        # ===== PÁGINA 1: PRESENTACIÓN Y MODELO =====
        if pagina == "📊 Presentación y Modelo":
            if not df_base.empty:
                # Mostrar reseña de modelos
                mostrar_resena_modelos()
                st.markdown("---")
                # Renderizar página de presentación
                presentacion.render(df_base)
            else:
                st.warning(
                    "⚠️ No hay datos para mostrar. Verifica que el archivo seleccionado sea válido."
                )

        # ===== PÁGINA 2: RESULTADOS EJECUTIVOS =====
        elif pagina == "📈 Resultados Ejecutivos":
            if not df_base.empty:
                # Renderizar página de resultados con datos filtrados y completos
                resultados.render(df_filtrado, df_base)
            else:
                st.warning(
                    "⚠️ No hay datos para mostrar. Verifica que el archivo seleccionado sea válido."
                )

        # ===== PÁGINA 3: ANÁLISIS DE CONSULTAS =====
        else:  # "📋 Análisis de Consultas"
            mostrar_tabla_analisis()

    except AttributeError as e:
        # Error específico para funciones de páginas
        st.error(f"Error al renderizar la página: {e}")
        st.info("""
        **Posibles causas:**
        1. Los archivos en `paginas/` no tienen la función `render()`
        2. La función `render()` tiene parámetros incorrectos
        3. El archivo `paginas/__init__.py` no existe
        """)
    except Exception as e:
        # Error genérico
        st.error(f"Error al renderizar la página: {e}")

    # ===== FOOTER =====
    st.markdown(
        f"""<div class="footer">
    <p>📊 Dashboard MMM - CUN &nbsp;|&nbsp; Versión 3.0 &nbsp;|&nbsp; 
    <span style="color: #7FBC03;">Datos actualizados al corte de julio 2026</span></p>
    <p style="font-size: 10px; color: #999;">Desarrollado por el equipo de Data & Analytics - CUN</p>
    <p style="font-size: 10px; color: #999;">📁 Archivo activo: {archivo_seleccionado}</p>
</div>""",
        unsafe_allow_html=True,
    )


# =============================================================================
# 8. PUNTO DE ENTRADA
# =============================================================================
if __name__ == "__main__":
    main()
