# =============================================================================
# paginas/resultados.py - Resultados Ejecutivos
# =============================================================================

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def render(df_filtrado, df_raw):  # ← Acepta 2 argumentos
    """Función render que llama index.py"""

    st.markdown(
        '<div style="background: white; border-radius: 15px; padding: 25px; margin-bottom: 30px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);">'
        '<h2 style="color: #7FBC03; font-size: 28px; margin-bottom: 20px; border-bottom: 3px solid #7FBC03; padding-bottom: 12px;">📊 Resultados Ejecutivos y Proyecciones</h2>',
        unsafe_allow_html=True,
    )

    # ============ USAR df_filtrado PARA LOS DATOS FILTRADOS ============
    if df_filtrado.empty:
        st.warning("No hay datos para mostrar con los filtros seleccionados.")
        return

    st.subheader("1. Brecha de Estudiantes: Proyección vs Meta")

    df_agrup_proy = (
        df_filtrado.groupby("Periodo Meta")["Proyeccion Cierre (Modelada)"]
        .sum()
        .reset_index()
    )

    # Usar df_raw para los totales sin filtros
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

    st.write("---")
    st.subheader("📋 Matriz Detallada de Proyecciones")
    st.dataframe(df_filtrado, use_container_width=True)


if __name__ == "__main__":
    st.error("Este archivo es un módulo de página y debe ser importado desde index.py")
