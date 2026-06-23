import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Dashboard Marketing CUN", layout="wide")

st.markdown(
    """
<style>
    [data-testid="stHeader"] {background: rgba(0,0,0,0); height: 0rem;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    
    .main-title { font-size: 34px; font-weight: bold; color: #1d2939; margin-bottom: 5px; }
    .fecha { background: #f8fafc; padding: 12px 20px; border-radius: 10px; font-weight: bold; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08); color: #1d2939; display: inline-block; float: right; font-size: 14px;}
    
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
    .explicacion-tecnica strong {
        color: #1d2939;
    }
    .explicacion-tecnica code {
        background: #e2e8f0;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 14px;
    }
    
    .diagrama-relacional { display: flex; flex-wrap: wrap; gap: 25px; justify-content: center; padding: 20px 0; }
    .tabla { background: #f8fafc; border: 2px solid #7FBC03; border-radius: 12px; min-width: 240px; padding: 10px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.05); }
    .tabla-nombre { background: #7FBC03; color: white; font-weight: bold; padding: 10px 15px; text-align: center; border-radius: 10px 10px 0 0; margin-bottom: 8px; }
    .tabla-columna { padding: 6px 15px; font-size: 14px; color: #1d2939; border-bottom: 1px solid #e2e8f0; display: flex; gap: 6px; }
    .tabla-columna:last-child { border-bottom: none; }
    .pk { background: #000103; color: white; font-weight: bold; padding: 0 6px; border-radius: 4px; font-size: 11px; display: inline-block; }
    .fk { background: #E8997A; color: white; font-weight: bold; padding: 0 6px; border-radius: 4px; font-size: 11px; display: inline-block; }
    .pk-fk { background: #7FBC03; color: white; font-weight: bold; padding: 0 6px; border-radius: 4px; font-size: 11px; display: inline-block; }
    .nota { margin-top: 20px; font-size: 14px; color: #475569; background: #f1f5f9; padding: 12px; border-radius: 8px; }
    
    .paso-container {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 2px solid #e8f0fe;
    }
    .paso-container h4 {
        color: #7FBC03;
        font-size: 20px;
        margin-bottom: 10px;
    }
    .paso-container .numero-paso {
        background: #7FBC03;
        color: white;
        border-radius: 50%;
        width: 35px;
        height: 35px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 12px;
    }
    
    .embudo-container {
        background: white;
        border-radius: 15px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border: 2px solid #e8f0fe;
    }
    .embudo-paso {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 20px;
        margin: 8px 0;
        border-radius: 8px;
        background: #f8fafc;
        border-left: 4px solid #7FBC03;
    }
    .embudo-paso .porcentaje {
        font-weight: bold;
        color: #7FBC03;
        font-size: 18px;
    }
    .embudo-paso .perdida {
        color: #e74c3c;
        font-size: 14px;
        font-weight: 500;
    }
    
    .modelo-container {
        background: #f0f7ff;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        border: 2px solid #dbeafe;
    }
    .modelo-container h4 {
        color: #1d2939;
        margin-bottom: 15px;
    }
    .modelo-container .feature {
        background: white;
        padding: 8px 15px;
        border-radius: 6px;
        margin: 5px 0;
        border: 1px solid #e2e8f0;
        display: inline-block;
        margin-right: 10px;
    }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def cargar_datos_unificados():
    archivo = "reporte_master_mmm_proyecciones_2026.xlsx"
    df_inv = pd.read_excel(archivo, sheet_name="Inversion_Por_Periodos")
    df_inv.columns = df_inv.columns.str.strip()
    df_proy = pd.read_excel(archivo, sheet_name="Proyecciones_Campanas")
    df_proy.columns = df_proy.columns.str.strip()
    return df_inv, df_proy


try:
    df_inv, df_proy = cargar_datos_unificados()

    st.sidebar.markdown(
        '<div style="background-color: #7FBC03; padding: 15px; text-align: center; border-radius: 8px; margin-bottom: 20px;">'
        '<h2 style="color: white; margin: 0; font-weight: bold; letter-spacing: 2px;">🏫 CUN</h2>'
        "</div>",
        unsafe_allow_html=True,
    )

    st.sidebar.header("🗺️ Navegación")
    seccion_activa = st.sidebar.radio(
        "Seleccionar sección:",
        [
            "📊 Datos de entrada",
            "🔬 Modelo y Procesamiento",
            "📈 Resultados Ejecutivos",
        ],
    )

    st.sidebar.write("---")
    st.sidebar.header("🎯 Filtros de control")

    df_dinamico = df_proy.copy()

    lista_periodos = ["Todos"] + sorted(
        df_dinamico["Periodo Meta"].dropna().unique().astype(str).tolist()
    )
    periodo_sel = st.sidebar.selectbox("📅 Periodo Meta:", lista_periodos)
    if periodo_sel != "Todos":
        df_dinamico = df_dinamico[df_dinamico["Periodo Meta"] == periodo_sel]

    lista_programas = ["Todos"] + sorted(
        df_dinamico["Programa Academico"].dropna().unique().astype(str).tolist()
    )
    programa_sel = st.sidebar.selectbox("🎓 Programa Académico:", lista_programas)
    if programa_sel != "Todos":
        df_dinamico = df_dinamico[df_dinamico["Programa Academico"] == programa_sel]

    lista_fuentes = ["Todos"] + sorted(
        df_dinamico["Fuente Clasificada"].dropna().unique().astype(str).tolist()
    )
    fuente_sel = st.sidebar.selectbox("📢 Fuente Clasificada:", lista_fuentes)
    if fuente_sel != "Todos":
        df_dinamico = df_dinamico[df_dinamico["Fuente Clasificada"] == fuente_sel]

    lista_campanas = ["Todos"] + sorted(
        df_dinamico["Campana Mercadeo"].dropna().unique().astype(str).tolist()
    )
    campana_sel = st.sidebar.selectbox("🎯 Campaña Mercadeo:", lista_campanas)

    df_proy_filtrado = df_dinamico.copy()
    if campana_sel != "Todos":
        df_proy_filtrado = df_proy_filtrado[
            df_proy_filtrado["Campana Mercadeo"] == campana_sel
        ]

    df_inv_filtrado = df_inv.copy()
    if periodo_sel != "Todos":
        df_inv_filtrado = df_inv_filtrado[
            df_inv_filtrado["Periodo Meta"] == periodo_sel
        ]

    fecha_hoy = pd.Timestamp.now().strftime("%A, %d de %B de %Y")
    st.markdown(f'<div class="fecha">📅 {fecha_hoy}</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="main-title">🏫 Dashboard Marketing CUN</p>', unsafe_allow_html=True
    )
    st.write("---")

    # =========================================================================
    # SECCIÓN 1: DATOS DE ENTRADA
    # =========================================================================
    if seccion_activa == "📊 Datos de entrada":

        st.title("📊 Arquitectura de Datos del Pipeline MMM")

        st.markdown(
            """
        <div class="explicacion-tecnica">
            <strong>📌 Visión general:</strong> El pipeline integra datos transaccionales de CRM, 
            gastos de marketing y metas académicas para construir un modelo de atribución 
            multicanal. La arquitectura se basa en 4 fuentes principales que se relacionan 
            mediante el campo <code>id_base</code> como conector universal.
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        st.markdown("### 🔹 Capa 1: Ingreso de Leads (CRM)")
        st.caption(
            "Tabla: `crm.Registros_CRM` - Registro de todos los prospectos atraídos por marketing"
        )

        with st.container(border=True):
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.error("**🔑 Llave primaria**")
                st.markdown("- `id_base` *(Identificador único del prospecto)*")

            with col2:
                st.info("**📋 Campos relevantes**")
                st.markdown("- `número_de_documento` (Cédula)")
                st.markdown("- `correo_electrónico`")
                st.markdown("- `nombre_de_campaña_mercadeo`")
                st.markdown("- `canal_fuente`")
                st.markdown("- `programa_de_interes`")
                st.markdown("- `convertido`")

            with col3:
                st.warning("**⏱️ Marcas temporales**")
                st.markdown("- `fec_crea`")
                st.markdown("- `fechamodificacionhorahis`")

            with col4:
                st.success("**🎯 Filtros aplicados**")
                st.markdown("- `ingreso_lead = 'ingreso'`")
                st.markdown("- `creador_lead = 'MARKETING'`")
                st.markdown("- `fuerzacomercial = 'Contact'`")
                st.markdown("- Periodos: 2025-2026")

        st.markdown("### 🔹 Capa 2: Oportunidades Calificadas (CRM)")
        st.caption(
            "Tabla: `crm.Registros_CRM` - Prospectos que avanzan en el embudo comercial"
        )

        with st.container(border=True):
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.error("**🔑 Llave primaria**")
                st.markdown("- `id_base`")

            with col2:
                st.info("**📋 Campos relevantes**")
                st.markdown("- `número_de_documento`")
                st.markdown("- `correo_electrónico`")
                st.markdown("- `nombre_de_campaña_mercadeo`")
                st.markdown("- `canal_fuente`")
                st.markdown("- `programalimpio` **(AS PROGRAMA)**")
                st.markdown("- `convertido`")

            with col3:
                st.warning("**⏱️ Marcas temporales**")
                st.markdown("- `fec_crea`")
                st.markdown("- `fechamodificacionhorahis`")

            with col4:
                st.success("**🎯 Filtros aplicados**")
                st.markdown("- `tipo_registro = 'Oportunidad'`")
                st.markdown("- `creador_lead = 'MARKETING'`")
                st.markdown("- `fuerzacomercial = 'Contact'`")
                st.markdown("- Periodos: 2025-2026")

        st.markdown("### 🔹 Capa 3: Ventas Efectivas (CRM)")
        st.caption(
            "Tabla: `crm.Registros_CRM` - Registros con matrícula y pago efectivo"
        )

        with st.container(border=True):
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.error("**🔑 Llave primaria**")
                st.markdown("- `id_base`")

            with col2:
                st.info("**💰 Campos de cierre**")
                st.markdown("- `número_de_documento`")
                st.markdown("- `nombre_de_campaña_mercadeo`")
                st.markdown("- `canal_fuente`")
                st.markdown("- `programalimpio` **(AS PROGRAMA)**")
                st.markdown("- `modalidad` **(AS MODALIDA)**")

            with col3:
                st.warning("**⏱️ Fecha de cierre**")
                st.markdown("- `fec_crea` **(AS FEC_PAGO_LIQ)**")

            with col4:
                st.success("**🎯 Filtros aplicados**")
                st.markdown("- `tipo_registro = 'Oportunidad'`")
                st.markdown("- `creador_lead = 'MARKETING'`")
                st.markdown("- `fuerzacomercial = 'Contact'`")
                st.markdown("- `convertido = 'VENTA'`")
                st.markdown("- Periodos: 2025-2026")

        st.markdown("---")

        st.markdown("### 🔹 Capa 4: Metas Académicas")
        st.caption(
            "Tabla: `financiera.metas` - Objetivos de matrícula por programa y periodo"
        )

        with st.container(border=True):
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.error("**🔑 Llave primaria**")
                st.markdown("- `PROGRAMA_ACADEMICO`")
                st.markdown("- `MODALIDAD`")
                st.markdown("- `PERIODO`")

            with col2:
                st.info("**📋 Campos**")
                st.markdown("- `FUERZA_COMERCIAL`")
                st.markdown("- `META_EN_ESTUDIANTES`")

            with col3:
                st.warning("**🔗 Relación**")
                st.markdown("- `PERIODO` → `dbo.Periodos_Calendario.cod_periodo`")

            with col4:
                st.success("**🎯 Filtros**")
                st.markdown("- `FUERZA_COMERCIAL = 'CONTACT'`")
                st.markdown("- Periodos: 2025-2026")

        st.markdown("### 🔹 Capa 5: Gastos de Marketing")
        st.caption(
            "Tabla: `financiera.Leads_campaña_gasto` - Inversión por campaña y programa"
        )

        with st.container(border=True):
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.error("**🔑 Llave primaria**")
                st.markdown("- `Campana`")
                st.markdown("- `Programa`")
                st.markdown("- `Periodo_Año_Mes`")

            with col2:
                st.info("**📋 Campos**")
                st.markdown("- `Inversion_Gasto`")

            with col3:
                st.warning("**🔗 Relación**")
                st.markdown(
                    "- `Periodo_Año_Mes` → `dbo.Periodos_Calendario.cod_periodo`"
                )

            with col4:
                st.success("**🎯 Filtros**")
                st.markdown("- Año: 2026")

        st.write("---")
        st.subheader("🔄 Flujo de datos y embudo de conversión")
        st.write(
            "**Trazabilidad del viaje del prospecto desde el contacto inicial hasta la matrícula:**"
        )

        col_emb1, col_emb2, col_emb3, col_emb4 = st.columns(4)

        with col_emb1:
            st.metric(
                label="1. LEADS GENERADOS",
                value="100%",
                delta="Punto de entrada",
                delta_color="off",
            )
            st.caption("📥 `ingreso_lead = 'ingreso'`")

        with col_emb2:
            st.metric(
                label="2. OPORTUNIDADES",
                value="~60%",
                delta="-40%",
                delta_color="inverse",
            )
            st.caption("📋 `tipo_registro = 'Oportunidad'`")

        with col_emb3:
            st.metric(
                label="3. PRE-MATRÍCULAS",
                value="~30%",
                delta="-50%",
                delta_color="inverse",
            )
            st.caption("📝 Avance en el proceso comercial")

        with col_emb4:
            st.metric(
                label="4. MATRÍCULAS", value="~20%", delta="-33%", delta_color="inverse"
            )
            st.caption("💰 `convertido = 'VENTA'`")

        st.info(
            "💡 **Interpretación:** De cada 100 leads que entran, aproximadamente 60 avanzan a oportunidad, 30 llegan a pre-matrícula y 20 se convierten en matrículas efectivas. Este embudo nos permite identificar cuellos de botella y optimizar cada etapa."
        )

        st.write("---")

        st.markdown(
            """
        <div class="seccion-contenedor">
            <h2>🗂️ Modelo Entidad-Relación (MER)</h2>
            <div class="diagrama-relacional">
                <div class="tabla">
                    <div class="tabla-nombre">financiera.metas</div>
                    <div class="tabla-columna"><span class="pk">PK</span> PROGRAMA_ACADEMICO : varchar</div>
                    <div class="tabla-columna"><span class="pk">PK</span> MODALIDAD : varchar</div>
                    <div class="tabla-columna"><span class="pk pk-fk">PK, FK</span> PERIODO : varchar</div>
                    <div class="tabla-columna">FUERZA_COMERCIAL : varchar</div>
                    <div class="tabla-columna">META_EN_ESTUDIANTES : int</div>
                </div>
                <div class="tabla">
                    <div class="tabla-nombre">dbo.Periodos_Calendario</div>
                    <div class="tabla-columna"><span class="pk">PK</span> cod_periodo : varchar</div>
                    <div class="tabla-columna">fec_inicio : date</div>
                </div>
                <div class="tabla">
                    <div class="tabla-nombre">financiera.Leads_campaña_gasto</div>
                    <div class="tabla-columna"><span class="pk">PK</span> Campana : varchar</div>
                    <div class="tabla-columna"><span class="pk">PK</span> Programa : varchar</div>
                    <div class="tabla-columna"><span class="pk pk-fk">PK, FK</span> Periodo_Año_Mes : varchar</div>
                    <div class="tabla-columna">Inversion_Gasto : float</div>
                </div>
                <div class="tabla">
                    <div class="tabla-nombre">crm.Registros_CRM</div>
                    <div class="tabla-columna"><span class="pk">PK</span> id_base : varchar</div>
                    <div class="tabla-columna"><span class="fk">FK</span> periodo : varchar</div>
                    <div class="tabla-columna">programalimpio : varchar</div>
                    <div class="tabla-columna">convertido : varchar</div>
                    <div class="tabla-columna">canal_fuente : varchar</div>
                </div>
            </div>
            <p class="nota"><span class="pk">PK</span> = Llave Primaria | <span class="fk">FK</span> = Llave Foránea | Las flechas indican relaciones lógicas entre tablas</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.subheader("📋 Resumen de inversión por periodos")
        st.dataframe(df_inv_filtrado, use_container_width=True)

    # =========================================================================
    # SECCIÓN 2: MODELO Y PROCESAMIENTO
    # =========================================================================
    elif seccion_activa == "🔬 Modelo y Procesamiento":

        st.title("🔬 Pipeline de Machine Learning y Procesamiento")

        st.markdown(
            """
        <div class="explicacion-tecnica">
            <strong>🎯 Objetivo:</strong> El pipeline utiliza un modelo híbrido de <strong>Wavelet Denoising</strong> + 
            <strong>LSTM (Long Short-Term Memory)</strong> para proyectar el cierre de matrículas 
            y optimizar la asignación presupuestal en marketing.
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        col_texto, col_svg = st.columns([60, 40])
        with col_texto:
            st.markdown(
                """
            <div style="background: #f8fafc; padding: 20px; border-radius: 12px; height: 100%;">
                <h3 style="color: #1d2939;">1. Wavelet Denoising (Daubechies 4)</h3>
                <p style="font-size: 15px; line-height: 1.8;">
                    <strong>Función:</strong> <code>aplicar_wavelet_denoising(serie, wavelet='db4')</code>
                </p>
                <p style="font-size: 15px; line-height: 1.8;">
                    La transformada Wavelet descompone la serie temporal en diferentes escalas de frecuencia, 
                    permitiendo aislar el <strong>ruido operativo</strong> de la <strong>señal subyacente</strong>.
                </p>
                <p style="font-size: 15px; line-height: 1.8;">
                    <strong>Proceso:</strong>
                    <ul>
                        <li>Descomposición en coeficientes wavelet</li>
                        <li>Cálculo del umbral de ruido usando MAD (Median Absolute Deviation)</li>
                        <li>Aplicación de <strong>soft thresholding</strong> para eliminar el ruido</li>
                        <li>Reconstrucción de la señal limpia</li>
                    </ul>
                </p>
                <p style="font-size: 15px; line-height: 1.8; background: #e8f0fe; padding: 10px; border-radius: 8px;">
                    <strong>📊 Aplicación:</strong> Se aplica a <code>Inversion Gasto Distribuido</code> y 
                    <code>Oportunidades Totales (Leads)</code> para eliminar variaciones atípicas.
                </p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col_svg:
            st.markdown(
                """
            <div style="background: #f8fafc; padding: 20px; border-radius: 12px; text-align: center;">
                <h3 style="color: #1d2939;">📈 Señal vs Ruido</h3>
                <svg viewBox="0 0 300 150" xmlns="http://www.w3.org/2000/svg">
                    <text x="10" y="20" fill="#7FBC03" font-size="12" font-weight="bold">Señal original (con ruido)</text>
                    <polyline points="0,120 30,100 60,110 90,80 120,90 150,60 180,70 210,50 240,60 270,40 300,50" stroke="#94a3b8" stroke-width="2" stroke-dasharray="4,4" fill="none" />
                    <text x="10" y="60" fill="#7FBC03" font-size="12" font-weight="bold">Señal limpia (Wavelet)</text>
                    <polyline points="0,120 30,105 60,105 90,85 120,85 150,65 180,65 210,55 240,55 270,45 300,45" stroke="#7FBC03" stroke-width="3" fill="none" />
                    <line x1="0" y1="140" x2="300" y2="140" stroke="#000" stroke-width="1" />
                    <text x="0" y="155" fill="#94a3b8" font-size="8">Tiempo →</text>
                </svg>
                <p style="font-size: 12px; color: #64748b;">La señal limpia (verde) conserva la tendencia principal eliminando el ruido (gris punteado)</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("---")

        st.markdown(
            """
        <div style="background: #f0f7ff; padding: 25px; border-radius: 15px; margin: 20px 0; border: 2px solid #dbeafe;">
            <h3 style="color: #1d2939;">2. Red Neuronal LSTM (Long Short-Term Memory)</h3>
            <p style="font-size: 15px; line-height: 1.8;">
                <strong>Arquitectura:</strong> Red neuronal recurrente especializada en series temporales.
            </p>
            <div style="display: flex; flex-wrap: wrap; gap: 15px; margin: 15px 0;">
                <div style="background: white; padding: 12px 20px; border-radius: 8px; border: 1px solid #e2e8f0;">
                    <strong>🔹 Capa LSTM 1:</strong> 64 neuronas (return_sequences=True)
                </div>
                <div style="background: white; padding: 12px 20px; border-radius: 8px; border: 1px solid #e2e8f0;">
                    <strong>🔹 Dropout:</strong> 10%
                </div>
                <div style="background: white; padding: 12px 20px; border-radius: 8px; border: 1px solid #e2e8f0;">
                    <strong>🔹 Capa LSTM 2:</strong> 32 neuronas
                </div>
                <div style="background: white; padding: 12px 20px; border-radius: 8px; border: 1px solid #e2e8f0;">
                    <strong>🔹 Capa Densa:</strong> 16 neuronas (ReLU)
                </div>
                <div style="background: white; padding: 12px 20px; border-radius: 8px; border: 1px solid #e2e8f0;">
                    <strong>🔹 Capa Salida:</strong> 1 neurona (lineal)
                </div>
            </div>
            <p style="font-size: 15px; line-height: 1.8;">
                <strong>Features de entrada (X):</strong>
                <span class="feature">💰 Inversión_Limpia</span>
                <span class="feature">👥 Leads_Limpios</span>
                <span class="feature">🎯 Meta_Estudiantes</span>
            </p>
            <p style="font-size: 15px; line-height: 1.8;">
                <strong>Target (y):</strong> <span class="feature">📊 Matriculas_Reales</span>
            </p>
            <p style="font-size: 15px; line-height: 1.8; background: #e8f0fe; padding: 12px; border-radius: 8px; margin-top: 10px;">
                <strong>⚙️ Hiperparámetros:</strong> 
                Optimizador: <code>Adam (lr=0.002)</code> | 
                Pérdida: <code>Huber</code> | 
                Épocas: <code>40</code> | 
                Batch Size: <code>4</code>
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        st.markdown(
            """
        <div style="background: white; padding: 25px; border-radius: 15px; margin: 20px 0; border: 2px solid #e8f0fe;">
            <h3 style="color: #1d2939;">3. Pipeline de Procesamiento</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin: 15px 0;">
                <div style="background: #f8fafc; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #7FBC03;">
                    <div style="font-size: 28px;">🧹</div>
                    <h4 style="color: #1d2939; margin: 5px 0;">Limpieza</h4>
                    <p style="font-size: 13px; color: #475569;">Normalización de textos y clasificación de fuentes</p>
                </div>
                <div style="background: #f8fafc; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #7FBC03;">
                    <div style="font-size: 28px;">📊</div>
                    <h4 style="color: #1d2939; margin: 5px 0;">Escalado</h4>
                    <p style="font-size: 13px; color: #475569;">MinMaxScaler para normalizar features y target</p>
                </div>
                <div style="background: #f8fafc; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #7FBC03;">
                    <div style="font-size: 28px;">🧠</div>
                    <h4 style="color: #1d2939; margin: 5px 0;">Predicción</h4>
                    <p style="font-size: 13px; color: #475569;">LSTM + Wavelet para proyección de cierre</p>
                </div>
                <div style="background: #f8fafc; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #7FBC03;">
                    <div style="font-size: 28px;">💰</div>
                    <h4 style="color: #1d2939; margin: 5px 0;">Asignación</h4>
                    <p style="font-size: 13px; color: #475569;">Dispersión controlada del presupuesto</p>
                </div>
                <div style="background: #f8fafc; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #7FBC03;">
                    <div style="font-size: 28px;">🛡️</div>
                    <h4 style="color: #1d2939; margin: 5px 0;">Control</h4>
                    <p style="font-size: 13px; color: #475569;">Techo de cumplimiento: 116% - 122%</p>
                </div>
                <div style="background: #f8fafc; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #7FBC03;">
                    <div style="font-size: 28px;">📊</div>
                    <h4 style="color: #1d2939; margin: 5px 0;">Reporte</h4>
                    <p style="font-size: 13px; color: #475569;">5 vistas jerárquicas en Excel</p>
                </div>
            </div>
            <p style="font-size: 14px; color: #475569; text-align: center; background: #f8fafc; padding: 10px; border-radius: 8px;">
                <strong>💰 Presupuesto objetivo:</strong> $800,000,000 COP | 
                <strong>💰 CPA técnico:</strong> $5,500 por lead
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        st.subheader("📊 Serie Temporal - Proyección de Demanda")
        st.write(
            "**Tendencia histórica y proyección futura basada en el modelo LSTM:**"
        )

        # Crear datos de ejemplo para la gráfica
        meses = [
            "Ene",
            "Feb",
            "Mar",
            "Abr",
            "May",
            "Jun",
            "Jul",
            "Ago",
            "Sep",
            "Oct",
            "Nov",
            "Dic",
        ]
        historico = [120, 135, 110, 145, 130, 150, 140, 160, 155, 170, 165, 180]
        proyeccion = [180, 195, 190, 210, 205, 220]

        fig_serie = go.Figure()

        # Datos históricos
        fig_serie.add_trace(
            go.Scatter(
                x=meses[:12],
                y=historico,
                mode="lines+markers",
                name="📊 Histórico",
                line=dict(color="#7FBC03", width=3),
                marker=dict(size=8, color="#7FBC03"),
            )
        )

        # Proyección
        meses_proy = meses[6 : 6 + 6]  # Jul a Dic
        fig_serie.add_trace(
            go.Scatter(
                x=meses_proy,
                y=proyeccion,
                mode="lines+markers",
                name="🔮 Proyección LSTM",
                line=dict(color="#E8997A", width=3, dash="dash"),
                marker=dict(size=8, color="#E8997A"),
            )
        )

        fig_serie.update_layout(
            plot_bgcolor="white",
            margin=dict(l=20, r=20, t=10, b=10),
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
            yaxis_title="Estudiantes",
            xaxis_title="Periodo",
        )

        st.plotly_chart(fig_serie, use_container_width=True)
        st.caption(
            "📌 La línea sólida muestra el comportamiento histórico. La línea punteada muestra la proyección estimada por el modelo LSTM."
        )

    # =========================================================================
    # SECCIÓN 3: RESULTADOS EJECUTIVOS
    # =========================================================================
    elif seccion_activa == "📈 Resultados Ejecutivos":
        st.markdown(
            '<div class="seccion-contenedor"><h2>📊 Resultados Ejecutivos y Proyecciones</h2>',
            unsafe_allow_html=True,
        )

        st.subheader("1. Brecha de Estudiantes: Proyección vs Meta")
        st.write(
            "Comparativa entre la meta académica y la proyección estimada por el modelo."
        )

        df_agrup_proy = (
            df_proy_filtrado.groupby("Periodo Meta")["Proyeccion Cierre (Modelada)"]
            .sum()
            .reset_index()
        )
        meta_col = (
            "Meta Estudiantes"
            if "Meta Estudiantes" in df_inv.columns
            else "Meta Estudiantes Asignada"
        )
        df_agrup_inv = (
            df_inv_filtrado.groupby("Periodo Meta")[meta_col].sum().reset_index()
        )

        meta_map = dict(zip(df_agrup_inv["Periodo Meta"], df_agrup_inv[meta_col]))
        df_agrup_proy["Meta_Estudiantes"] = (
            df_agrup_proy["Periodo Meta"].map(meta_map).fillna(0)
        )
        df_brecha = df_agrup_proy.sort_values(by="Periodo Meta")

        if not df_brecha.empty:
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
                    text=[
                        f"{int(c):,}" for c in df_brecha["Proyeccion Cierre (Modelada)"]
                    ],
                    textposition="auto",
                )
            )
            fig_brechas.update_layout(
                barmode="group",
                plot_bgcolor="white",
                margin=dict(l=20, r=20, t=10, b=10),
            )
            st.plotly_chart(fig_brechas, use_container_width=True)

            st.caption(
                "🟢 Verde = Cumplimiento >= 100% | 🟡 Amarillo = 65% - 99% | 🔴 Rojo = < 65%"
            )
        else:
            st.info("No hay datos suficientes para mostrar las metas.")

        st.write("---")
        st.subheader("2. Distribución de Gasto y Top Campañas")
        col_g1, col_g2 = st.columns([40, 60])

        with col_g1:
            df_gasto_canal = (
                df_proy_filtrado.groupby("Fuente Clasificada")[
                    "Inversion Gasto Distribuido"
                ]
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
                df_proy_filtrado.groupby("Campana Mercadeo")[
                    "Proyeccion Cierre (Modelada)"
                ]
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

        st.write("---")
        st.subheader("3. Volumen de Leads por Fuente")
        df_grafico = (
            df_proy_filtrado.groupby("Fuente Clasificada")
            .agg(Total_Leads=("Oportunidades Totales (Leads)", "sum"))
            .reset_index()
            .sort_values(by="Total_Leads", ascending=True)
        )

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

        st.write("---")
        st.subheader("📋 Matriz Detallada de Proyecciones")
        st.dataframe(df_proy_filtrado, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

except FileNotFoundError:
    st.error("❌ Archivo 'reporte_master_mmm_proyecciones_2026.xlsx' no encontrado")
    st.info(
        "💡 Asegúrate de que el archivo Excel esté en la misma carpeta que este script."
    )
except Exception as e:
    st.error(f"⚠️ Error: {e}")
