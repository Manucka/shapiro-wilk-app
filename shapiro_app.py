# -*- coding: utf-8 -*-
"""
Aplicativo Streamlit para Teste de Normalidade Shapiro-Wilk

Este script cria um aplicativo web interativo usando Streamlit.
O usuário pode inserir uma lista de números para realizar o teste de
Shapiro-Wilk e visualizar estatísticas descritivas, resultados e gráficos.
"""

import streamlit as st
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================================================================
# 1. Configuração da Página do Streamlit
# ==============================================================================
st.set_page_config(
    page_title="Teste de Normalidade Shapiro-Wilk",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Estilo CSS customizado para compactar a visualização e alinhar texto
st.markdown("""
    <style>
    .report-table {
        width: 100%;
        font-family: sans-serif;
    }
    .report-label {
        font-weight: bold;
        text-align: left;
        padding-right: 20px;
        width: 40%;
    }
    .report-value {
        text-align: left;
    }
    .conclusion-box {
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Teste de Normalidade Shapiro-Wilk")
st.markdown("""
    Verificação de normalidade com estatísticas descritivas, W, p-valor e gráficos.
""")

# ==============================================================================
# 2. Entrada de Dados do Usuário
# ==============================================================================
st.header("🔢 Insira Seus Números")

input_numbers_str = st.text_area(
    "Valores (entre 10 e 30 números)",
    value="",
    height=120,
    help="Cole ou digite seus números aqui. Use vírgulas ou quebras de linha."
)

analyze_button = st.button("Analisar Dados")

# ==============================================================================
# 3. Lógica de Análise
# ==============================================================================
if analyze_button:
    try:
        # Processamento da entrada
        numbers_raw = input_numbers_str.replace(' ', '').replace(',', '.').replace('\n', ',').split(',')
        dados = [float(num) for num in numbers_raw if num.strip()]

        num_dados = len(dados)

        if num_dados < 10 or num_dados > 30:
            st.error(f"❌ Erro: O número de dados fornecido ({num_dados}) está fora do intervalo permitido (10 a 30).")
        elif num_dados == 0:
            st.error("❌ Erro: Nenhum dado válido foi inserido.")
        else:
            # Cálculos Estatísticos
            media = np.mean(dados)
            desvio_padrao = np.std(dados, ddof=1)
            statistic, p_value = stats.shapiro(dados)
            alpha = 0.05

            st.write("---")
            st.header("📝 Normality test (SHAPIRO-WILK Method)")
            
            # Layout estilo tabela (Labels à esquerda, valores à direita)
            def table_row(label, value):
                st.markdown(f"""
                    <div style="display: flex; justify-content: flex-start; border-bottom: 1px solid #f0f2f6; padding: 5px 0;">
                        <div style="width: 200px; font-weight: bold;">{label}</div>
                        <div>{value}</div>
                    </div>
                """, unsafe_allow_html=True)

            table_row("Average", f"{media:.7f}")
            table_row("Standard deviation", f"{desvio_padrao:.7f}")
            table_row("Observations", f"{num_dados}")
            table_row("W", f"{statistic:.6f}")
            table_row("P-Value", f"{p_value:.7f}")

            # Conclusão
            if p_value > alpha:
                st.markdown(f"<div style='color: #2e7d32; font-weight: bold; margin-top: 15px;'>CONCLUSION: The normality is accepted with an alpha risk of {int(alpha*100)}%</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='color: #c62828; font-weight: bold; margin-top: 15px;'>CONCLUSION: The normality is rejected with an alpha risk of {int(alpha*100)}%</div>", unsafe_allow_html=True)

            st.write("---")

            # ==============================================================================
            # 4. Gráficos (Compactados)
            # ==============================================================================
            st.header("📈 Visualização Gráfica")
            plt.style.use('seaborn-v0_8-darkgrid')
            fig, axes = plt.subplots(1, 2, figsize=(12, 4)) # Altura reduzida para caber na tela

            # Histograma
            sns.histplot(dados, kde=True, bins='auto', color='royalblue', edgecolor='black', ax=axes[0])
            axes[0].set_title('Histograma', fontsize=10)
            axes[0].tick_params(labelsize=8)

            # Q-Q Plot
            stats.probplot(dados, dist="norm", plot=axes[1])
            axes[1].set_title('Gráfico Q-Q', fontsize=10)
            axes[1].tick_params(labelsize=8)

            plt.tight_layout()
            st.pyplot(fig)

    except ValueError:
        st.error("❌ Erro: Insira apenas números válidos.")
    except Exception as e:
        st.error(f"❌ Ocorreu um erro: {e}")

# Sidebar
with st.sidebar:
    st.header("Info")
    st.markdown("""
        Relatório simplificado conforme padrão de análise de precisão.
        
        **Nível Alpha:** 5%
    """)
    st.write("---")
    st.caption("v2.0 - Layout Compacto")
