"""
Página de Análisis Profundo - 6 Gráficas Interactivas
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
from pathlib import Path
import os

warnings.filterwarnings("ignore")

# ================================================================
# CONFIGURACIÓN DE MÉTRICAS
# ================================================================

METRICAS_CONFIG = {
    "DME_s": {
        "nombre": "Duración del monólogo",
        "columna": "DME_s",
        "unidad": "segundos",
        "formato": "{:.1f}s",
        "tipo": "menor",
        "meta": 3.5,
        "limite_cumple": 3.5,
        "condicion": "menor",
    },
    "DTE_ratio": {
        "nombre": "Porcentaje de habla",
        "columna": "DTE_ratio",
        "unidad": "",
        "formato": "{:.3f}",
        "tipo": "rango",
        "min": 0.0,
        "max": 0.50,
        "limite_cumple": 0.50,
        "condicion": "menor_igual",
    },
    "Jitter_Score": {
        "nombre": "Estabilidad técnica",
        "columna": "Jitter_Score",
        "unidad": "",
        "formato": "{:.3f}",
        "tipo": "mayor",
        "meta": 0.40,
        "limite_cumple": 0.4,
        "condicion": "mayor",
    },
    "IMP_promedio": {
        "nombre": "Movimiento promedio",
        "columna": "IMP_promedio",
        "unidad": "",
        "formato": "{:.3f}",
        "tipo": "mayor",
        "meta": 4.0,
        "limite_cumple": 4.0,
        "condicion": "mayor",
    },
    "sigma2_IM": {
        "nombre": "Cambios de movimiento",
        "columna": "sigma2_IM",
        "unidad": "",
        "formato": "{:.3f}",
        "tipo": "mayor",
        "meta": 8.5,
        "limite_cumple": 8.5,
        "condicion": "mayor",
    },
    "Tone_CoV": {
        "nombre": "Variación de la voz",
        "columna": "Tone_CoV",
        "unidad": "",
        "formato": "{:.3f}",
        "tipo": "mayor",
        "meta": 0.32,
        "limite_cumple": 0.32,
        "condicion": "mayor",
    },
    "Enthusiasm_Score": {
        "nombre": "Nivel de energía",
        "columna": "Enthusiasm_Score",
        "unidad": "",
        "formato": "{:.3f}",
        "tipo": "mayor",
        "meta": 0.15,
        "limite_cumple": 0.15,
        "condicion": "mayor",
    },
}

# ================================================================
# FUNCIONES AUXILIARES
# ================================================================


@st.cache_data
def load_data():
    """Carga los datos desde el archivo Excel"""
    try:
        from pathlib import Path

        excel_path = Path(
            "C:/Users/juan_garnicac/Documents/ProyectosVisual/Videos/presentaciones/exel_entrada.xlsx"
        )

        if not excel_path.exists():
            st.error(f"❌ No se encontró el archivo Excel en: {excel_path}")
            return None

        df = pd.read_excel(excel_path)

        # Convertir columnas numéricas
        numeric_columns = [
            "sigma2_IM",
            "Jitter_Score",
            "IMP_promedio",
            "CPM",
            "DME_s",
            "DTE_ratio",
            "Enthusiasm_Score",
            "Tone_CoV",
        ]
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        return df

    except Exception as e:
        st.error(f"❌ Error al cargar los datos: {str(e)}")
        return None


def calcular_cumplimiento(valor, config):
    """Calcula el porcentaje de cumplimiento"""
    if pd.isna(valor):
        return 0.0

    tipo = config.get("tipo")
    meta = config.get("meta")

    if meta is None:
        return 0.0

    try:
        if tipo == "mayor":
            if meta == 0:
                return 0.0
            return min((valor / meta) * 100, 100.0)
        elif tipo == "menor":
            if meta == 0:
                return 0.0
            if valor <= meta:
                return 100.0
            return max(0.0, min((meta / valor) * 100, 100.0))
        elif tipo == "rango":
            min_val = config.get("min", 0)
            max_val = config.get("max", float("inf"))
            return 100.0 if min_val <= valor <= max_val else 0.0
        return 0.0
    except:
        return 0.0


def obtener_estado(pct):
    if pct >= 100:
        return "✅ Cumple"
    elif pct >= 70:
        return "⚠️ Parcial"
    else:
        return "❌ Requiere mejora"


@st.cache_data
def agregar_columnas_cumplimiento(_df, metricas_disp):
    """Agrega columnas de cumplimiento al DataFrame"""
    df_resultado = _df.copy()
    for col in metricas_disp:
        config = METRICAS_CONFIG[col]
        col_cumplimiento = f"{col}_cumplimiento"
        if col in df_resultado.columns and col_cumplimiento not in df_resultado.columns:
            df_resultado[col_cumplimiento] = df_resultado[col].apply(
                lambda x: calcular_cumplimiento(x, config)
            )
    return df_resultado


def mostrar_leyenda_grafica(titulo, pregunta, interpretacion):
    st.markdown(
        f"""
    <div style="background: #f0f2f6; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 5px solid #2e7d32;">
        <h4 style="margin: 0; color: #1a1a1a;">📊 {titulo}</h4>
        <p style="margin: 5px 0 0 0; font-size: 0.9rem;">
            <strong>❓ ¿Qué pregunta responde?</strong> {pregunta}
        </p>
        <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #555;">
            <strong>📖 ¿Cómo interpretarlo?</strong> {interpretacion}
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def mostrar_interpretacion_grafica(titulo, que_muestra, como_leer, que_buscar):
    with st.container():
        st.markdown("---")
        st.markdown(f"### 📖 {titulo}")
        st.info(que_muestra)
        st.success(como_leer)
        st.warning(que_buscar)
        st.markdown("---")


def mostrar_diccionario_metricas():
    """Muestra el diccionario completo de métricas con explicaciones"""
    st.markdown("### 📊 Diccionario de Métricas - ¿Qué estamos midiendo?")

    metricas_data = [
        {
            "Métrica": "Duración del monólogo (DME_s)",
            "Qué mide": "Tiempo que el docente habla sin interrupción. Mide su capacidad de mantener la atención y fluidez.",
            "Meta": "< 3.5 segundos",
            "Interpretación": "Valores bajos indican que el docente habla en segmentos cortos, manteniendo la atención del estudiante.",
        },
        {
            "Métrica": "Porcentaje de habla (DTE_ratio)",
            "Qué mide": "Relación entre el tiempo que habla el docente y el tiempo total de la clase.",
            "Meta": "≤ 0.5 (máximo 50%)",
            "Interpretación": "Valores bajos indican que el docente no domina la conversación, permitiendo participación del estudiante.",
        },
        {
            "Métrica": "Estabilidad técnica (Jitter_Score)",
            "Qué mide": "Estabilidad y naturalidad de la voz del docente. Fluidez del discurso.",
            "Meta": "> 0.4",
            "Interpretación": "Valores altos indican una voz estable y natural, sin tartamudeos ni vacilaciones.",
        },
        {
            "Métrica": "Movimiento promedio (IMP_promedio)",
            "Qué mide": "Cantidad de movimiento corporal del docente durante la clase.",
            "Meta": "> 4.0",
            "Interpretación": "Valores altos indican un docente dinámico que usa el espacio y el movimiento para mantener la atención.",
        },
        {
            "Métrica": "Cambios de movimiento (sigma2_IM)",
            "Qué mide": "Variación y consistencia del movimiento corporal del docente.",
            "Meta": "> 8.5",
            "Interpretación": "Valores altos indican variedad en los movimientos, evitando la monotonía.",
        },
        {
            "Métrica": "Variación de la voz (Tone_CoV)",
            "Qué mide": "Variación del tono y expresividad vocal del docente.",
            "Meta": "> 0.32",
            "Interpretación": "Valores altos indican una voz expresiva que mantiene el interés del estudiante.",
        },
        {
            "Métrica": "Nivel de energía (Enthusiasm_Score)",
            "Qué mide": "Nivel de entusiasmo y energía vocal del docente.",
            "Meta": "> 0.15",
            "Interpretación": "Valores altos indican un docente energético que transmite pasión por el tema.",
        },
        {
            "Métrica": "Clase Predicha",
            "Qué mide": "Clasificación de la clase como ENTRETENIDO o ABURRIDO.",
            "Meta": "ENTRETENIDO",
            "Interpretación": "Clases clasificadas como ENTRETENIDO son las que tienen mejor desempeño en todas las métricas.",
        },
    ]

    df_metricas = pd.DataFrame(metricas_data)
    st.dataframe(
        df_metricas,
        column_config={
            "Métrica": st.column_config.TextColumn("📊 Métrica", width="medium"),
            "Qué mide": st.column_config.TextColumn("🔍 ¿Qué mide?", width="large"),
            "Meta": st.column_config.TextColumn("🎯 Meta", width="small"),
            "Interpretación": st.column_config.TextColumn(
                "💡 Interpretación", width="large"
            ),
        },
        hide_index=True,
        use_container_width=True,
    )
    st.markdown("---")


# ================================================================
# MAIN
# ================================================================


def main():
    st.set_page_config(
        page_title="Análisis Profundo | CUN",
        page_icon="📈",
        layout="wide",
    )

    st.header("📈 Análisis Profundo - 6 Gráficas Interactivas")

    # ================================================================
    # CARGAR DATOS DESDE EXCEL
    # ================================================================
    df = load_data()
    if df is None:
        st.stop()

    # ================================================================
    # FILTROS EN LA BARRA LATERAL (PARA ESTA PÁGINA)
    # ================================================================
    st.sidebar.header("🎛️ Filtros")

    df_filtrado = df.copy()

    # Filtro por Clase Predicha (el que te interesa)
    if "Clase_Predicha" in df.columns:
        df["Clase_Normalizada"] = df["Clase_Predicha"].str.upper()
        clases = ["Todas"] + sorted(df["Clase_Normalizada"].dropna().unique().tolist())
        clase_seleccionada = st.sidebar.selectbox(
            "🎯 Clase Predicha", options=clases, key="filtro_clase_profundidad"
        )
        if clase_seleccionada != "Todas":
            df_filtrado = df_filtrado[
                df_filtrado["Clase_Normalizada"] == clase_seleccionada
            ]
            st.sidebar.success(f"✅ Filtro: {clase_seleccionada}")

    # Filtro por Área
    if "area" in df.columns:
        areas = ["Todas"] + sorted(df["area"].dropna().unique().tolist())
        area_seleccionada = st.sidebar.selectbox(
            "📚 Área", areas, key="filtro_area_profundidad"
        )
        if area_seleccionada != "Todas":
            df_filtrado = df_filtrado[df_filtrado["area"] == area_seleccionada]

    # Filtro por Docente
    if "nombres_apellidos" in df.columns:
        docentes = ["Todos"] + sorted(
            df["nombres_apellidos"].dropna().unique().tolist()
        )
        docente_seleccionado = st.sidebar.selectbox(
            "👨‍🏫 Docente", docentes, key="filtro_docente_profundidad"
        )
        if docente_seleccionado != "Todos":
            df_filtrado = df_filtrado[
                df_filtrado["nombres_apellidos"] == docente_seleccionado
            ]

    # Mostrar cantidad de registros
    st.sidebar.markdown("---")
    st.sidebar.metric("📊 Registros", len(df_filtrado))

    if df_filtrado.empty:
        st.warning("⚠️ No hay datos con los filtros seleccionados.")
        st.stop()

    # Mostrar filtro activo en la página
    if "Clase_Normalizada" in df_filtrado.columns:
        clases_presentes = df_filtrado["Clase_Normalizada"].dropna().unique()
        if len(clases_presentes) == 1:
            st.info(f"🎯 Filtro de clase activo: **{clases_presentes[0]}**")
        else:
            st.info(
                f"📊 Mostrando **{len(clases_presentes)}** clases: {', '.join(clases_presentes)}"
            )

    st.info(f"📊 Mostrando {len(df_filtrado)} registros")

    # ================================================================
    # Obtener métricas disponibles
    # ================================================================
    metricas_disp = [
        col for col in METRICAS_CONFIG.keys() if col in df_filtrado.columns
    ]

    if not metricas_disp:
        st.warning("⚠️ No hay métricas disponibles en el dataset.")
        st.stop()

    # Agregar columnas de cumplimiento
    with st.spinner("🔄 Calculando métricas de cumplimiento..."):
        df_filtrado = agregar_columnas_cumplimiento(df_filtrado, metricas_disp)

    # ================================================================
    # GRÁFICA 1: Radar Chart (PROMEDIO DEL GRUPO FILTRADO)
    # ================================================================
    with st.expander(
        "🕸️ Gráfica 1: Radar de Cumplimiento - Promedio del Grupo", expanded=True
    ):
        mostrar_leyenda_grafica(
            "Perfil de Cumplimiento del Grupo Filtrado",
            "¿Cuál es el perfil promedio del grupo seleccionado?",
            "🔹 Cada eje = % de cumplimiento. 100% = cumple la meta.",
        )

        if metricas_disp:
            nombres_metricas = []
            valores_cumplimiento = []

            for col in metricas_disp:
                if col in df_filtrado.columns:
                    valor_promedio = df_filtrado[col].mean()
                    config = METRICAS_CONFIG[col]
                    pct = calcular_cumplimiento(valor_promedio, config)
                    nombres_metricas.append(config["nombre"])
                    valores_cumplimiento.append(pct)

            if valores_cumplimiento:
                fig_radar = go.Figure()
                fig_radar.add_trace(
                    go.Scatterpolar(
                        r=valores_cumplimiento,
                        theta=nombres_metricas,
                        fill="toself",
                        name=f"Promedio Grupo ({len(df_filtrado)} registros)",
                        line_color="#2e7d32",
                    )
                )
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100],
                            tickvals=[0, 25, 50, 75, 100],
                            ticktext=["0%", "25%", "50%", "75%", "100%"],
                        )
                    ),
                    title=f"Perfil de Cumplimiento - Grupo Filtrado ({len(df_filtrado)} registros)",
                    height=550,
                    template="plotly_white",
                )
                st.plotly_chart(fig_radar, use_container_width=True)

    # ================================================================
    # GRÁFICA 2: Comparativa ENTRETENIDO vs ABURRIDO
    # ================================================================
    with st.expander(
        "📊 Gráfica 2: Comparativa ENTRETENIDO vs ABURRIDO", expanded=False
    ):
        mostrar_leyenda_grafica(
            "Comparativa de Cumplimiento entre ENTRETENIDO y ABURRIDO",
            "¿Qué métricas tienen mayor porcentaje de cumplimiento en cada clase?",
            "🔹 Barras verdes = ENTRETENIDO | Barras rojas = ABURRIDO",
        )

        if "Clase_Normalizada" in df_filtrado.columns and metricas_disp:
            clases_presentes = df_filtrado["Clase_Normalizada"].dropna().unique()

            if len(clases_presentes) >= 2:
                columnas_cumplimiento = [f"{col}_cumplimiento" for col in metricas_disp]
                columnas_existentes = [
                    col for col in columnas_cumplimiento if col in df_filtrado.columns
                ]

                if columnas_existentes:
                    df_promedios = (
                        df_filtrado.groupby("Clase_Normalizada")[columnas_existentes]
                        .mean()
                        .reset_index()
                    )
                    df_melt = df_promedios.melt(
                        id_vars="Clase_Normalizada",
                        var_name="Columna",
                        value_name="Cumplimiento_%",
                    )
                    df_melt["Nombre_Métrica"] = (
                        df_melt["Columna"]
                        .str.replace("_cumplimiento", "")
                        .map(
                            lambda x: (
                                METRICAS_CONFIG[x]["nombre"]
                                if x in METRICAS_CONFIG
                                else x
                            )
                        )
                    )

                    fig = px.bar(
                        df_melt,
                        x="Nombre_Métrica",
                        y="Cumplimiento_%",
                        color="Clase_Normalizada",
                        barmode="group",
                        color_discrete_map={
                            "ENTRETENIDO": "#2e7d32",
                            "ABURRIDO": "#c62828",
                        },
                        title="Comparativa de Cumplimiento",
                        text_auto=".1f",
                        range_y=[0, 100],
                    )
                    fig.update_layout(
                        template="plotly_white", height=450, xaxis_tickangle=-45
                    )
                    fig.update_traces(textposition="outside")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(
                    f"⚠️ Solo hay una clase disponible: **{clases_presentes[0]}**. Se necesitan ambas clases para esta comparativa."
                )

    # ================================================================
    # GRÁFICA 3: Top 10 Docentes - ENTRETENIDO vs ABURRIDO
    # ================================================================
    with st.expander(
        "🏆 Gráfica 3: Top 10 Docentes - ENTRETENIDO vs ABURRIDO", expanded=False
    ):
        mostrar_leyenda_grafica(
            "Top 10 Docentes con más Clases ENTRETENIDO",
            "¿Qué docentes tienen más clases ENTRETENIDO?",
            "🔹 Barras verdes = ENTRETENIDO | Barras rojas = ABURRIDO",
        )

        if (
            "nombres_apellidos" in df_filtrado.columns
            and "Clase_Normalizada" in df_filtrado.columns
        ):
            df_docente_clase = (
                df_filtrado.groupby(["nombres_apellidos", "Clase_Normalizada"])
                .size()
                .reset_index(name="count")
            )
            df_pivot = (
                df_docente_clase.pivot(
                    index="nombres_apellidos",
                    columns="Clase_Normalizada",
                    values="count",
                )
                .fillna(0)
                .reset_index()
            )

            for col in ["ENTRETENIDO", "ABURRIDO"]:
                if col not in df_pivot.columns:
                    df_pivot[col] = 0

            df_pivot["total"] = df_pivot["ENTRETENIDO"] + df_pivot["ABURRIDO"]
            df_pivot["pct_entretenido"] = (
                df_pivot["ENTRETENIDO"] / df_pivot["total"]
            ) * 100
            df_pivot = df_pivot[df_pivot["total"] >= 3]
            df_pivot = df_pivot.sort_values("pct_entretenido", ascending=False).head(10)

            if not df_pivot.empty:
                fig = go.Figure()
                fig.add_trace(
                    go.Bar(
                        y=df_pivot["nombres_apellidos"],
                        x=df_pivot["ENTRETENIDO"],
                        name="ENTRETENIDO",
                        orientation="h",
                        marker_color="#2e7d32",
                        text=df_pivot["ENTRETENIDO"].astype(int),
                        textposition="inside",
                    )
                )
                fig.add_trace(
                    go.Bar(
                        y=df_pivot["nombres_apellidos"],
                        x=df_pivot["ABURRIDO"],
                        name="ABURRIDO",
                        orientation="h",
                        marker_color="#c62828",
                        text=df_pivot["ABURRIDO"].astype(int),
                        textposition="inside",
                    )
                )
                fig.update_layout(
                    barmode="stack",
                    title="Top 10 Docentes - Clases ENTRETENIDO vs ABURRIDO",
                    template="plotly_white",
                    height=450,
                    xaxis_title="Número de Clases",
                    yaxis_title="Docente",
                )
                st.plotly_chart(fig, use_container_width=True)

    # ================================================================
    # DICCIONARIO DE MÉTRICAS
    # ================================================================
    st.markdown("---")
    mostrar_diccionario_metricas()

    # ================================================================
    # FOOTER
    # ================================================================
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #666; padding: 20px 0;">
            <p style="margin: 0; font-size: 0.9rem;">
                📊 Dashboard de Análisis Profundo - Todos los derechos reservados © 2024
            </p>
            <p style="margin: 0; font-size: 0.8rem; color: #999;">
                Análisis de métricas de desempeño docente con filtros interactivos
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
