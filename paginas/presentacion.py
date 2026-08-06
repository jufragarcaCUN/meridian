# =============================================================================
# paginas/presentacion.py - Presentación y Modelo del Pipeline MMM
# =============================================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def render(df_raw):
    """Función render que llama index.py"""

    st.title("🔬 Pipeline Multi-Agente y Procesamiento MMM")

    st.markdown(
        """
    <div style="background: #f8fafc; border-left: 5px solid #7FBC03; padding: 20px 25px; border-radius: 10px; margin: 20px 0; font-size: 16px; line-height: 1.8;">
        <strong>🎯 Objetivo:</strong> El pipeline utiliza un sistema <strong>Multi-Agente</strong> 
        con <strong>5 agentes especializados</strong> que trabajan en conjunto para optimizar 
        la asignación presupuestal, evaluar el rendimiento y generar recomendaciones ejecutivas.
        El núcleo predictivo combina <strong>Wavelet Denoising</strong> + <strong>LSTM</strong>.
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Mostrar los 5 agentes
    st.markdown("### 🤖 Los 5 Agentes del Pipeline")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        <div style="background: #f8fafc; padding: 15px; border-radius: 12px; margin: 5px 0; border-left: 4px solid #7FBC03;">
            <strong>🧠 Agente Orquestador MMM</strong>
            <p style="font-size: 14px; margin: 5px 0;">Asigna y optimiza el presupuesto de marketing</p>
            <p style="font-size: 12px; color: #475569;">💰 $8.5B COP | Alpha: 2.1</p>
        </div>
        <div style="background: #f8fafc; padding: 15px; border-radius: 12px; margin: 5px 0; border-left: 4px solid #7FBC03;">
            <strong>📊 Agente de Oportunidades</strong>
            <p style="font-size: 14px; margin: 5px 0;">Evalúa eficiencia Top-of-Funnel (CPL)</p>
            <p style="font-size: 12px; color: #475569;">📈 Top 15 campañas con mejor CPL</p>
        </div>
        <div style="background: #f8fafc; padding: 15px; border-radius: 12px; margin: 5px 0; border-left: 4px solid #7FBC03;">
            <strong>🎯 Agente de Matrículas</strong>
            <p style="font-size: 14px; margin: 5px 0;">Evalúa eficiencia Bottom-of-Funnel (CAC)</p>
            <p style="font-size: 12px; color: #475569;">🎓 Top 15 campañas por tasa de conversión</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div style="background: #f8fafc; padding: 15px; border-radius: 12px; margin: 5px 0; border-left: 4px solid #7FBC03;">
            <strong>🔄 Agente Nurturing CRM</strong>
            <p style="font-size: 14px; margin: 5px 0;">Calcula potencial de reconversión de leads</p>
            <p style="font-size: 12px; color: #475569;">⚡ Factor: 76.5% | Mínimo: 20%</p>
        </div>
        <div style="background: #f8fafc; padding: 15px; border-radius: 12px; margin: 5px 0; border-left: 4px solid #7FBC03;">
            <strong>🤖 Agente Consultor Ollama</strong>
            <p style="font-size: 14px; margin: 5px 0;">Genera informe ejecutivo con IA Generativa</p>
            <p style="font-size: 12px; color: #475569;">🧠 Modelo: LLAMA3 | 📄 Informe estructurado</p>
        </div>
        <div style="background: #f0f7ff; padding: 15px; border-radius: 12px; margin: 5px 0; border: 2px solid #dbeafe;">
            <strong>⚙️ Pipeline Core</strong>
            <p style="font-size: 14px; margin: 5px 0;">Wavelet Denoising (DB4) + LSTM</p>
            <p style="font-size: 12px; color: #475569;">📊 Features: Inversión + Leads + Meta</p>
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
            <p style="font-size: 15px; line-height: 1.8; background: #e8f0fe; padding: 10px; border-radius: 8px;">
                <strong>📊 Aplicación:</strong> Se aplica a <code>Inversion Gasto Distribuido</code> y 
                <code>Oportunidades Totales (Leads)</code>.
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
            <p style="font-size: 12px; color: #64748b;">La señal limpia (verde) conserva la tendencia principal eliminando el ruido (gris)</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    st.markdown(
        """
    <div style="background: #f0f7ff; padding: 25px; border-radius: 15px; margin: 20px 0; border: 2px solid #dbeafe;">
        <h3 style="color: #1d2939;">2. Red Neuronal LSTM</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 15px; margin: 15px 0;">
            <div style="background: white; padding: 12px 20px; border-radius: 8px; border: 1px solid #e2e8f0;">
                <strong>🔹 LSTM 1:</strong> 64 neuronas
            </div>
            <div style="background: white; padding: 12px 20px; border-radius: 8px; border: 1px solid #e2e8f0;">
                <strong>🔹 Dropout:</strong> 10%
            </div>
            <div style="background: white; padding: 12px 20px; border-radius: 8px; border: 1px solid #e2e8f0;">
                <strong>🔹 LSTM 2:</strong> 32 neuronas
            </div>
            <div style="background: white; padding: 12px 20px; border-radius: 8px; border: 1px solid #e2e8f0;">
                <strong>🔹 Densa:</strong> 16 neuronas (ReLU)
            </div>
            <div style="background: white; padding: 12px 20px; border-radius: 8px; border: 1px solid #e2e8f0;">
                <strong>🔹 Salida:</strong> 1 neurona (lineal)
            </div>
        </div>
        <p style="font-size: 15px; line-height: 1.8; background: #e8f0fe; padding: 12px; border-radius: 8px; margin-top: 10px;">
            <strong>⚙️ Hiperparámetros:</strong> 
            Optimizador: <code>Adam (lr=0.002)</code> | 
            Pérdida: <code>Huber</code> | 
            Épocas: <code>50</code> | 
            Batch Size: <code>8</code>
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    st.error("Este archivo es un módulo de página y debe ser importado desde index.py")
