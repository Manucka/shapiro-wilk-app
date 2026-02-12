# -*- coding: utf-8 -*-
"""
Aplicativo Streamlit para Teste de Normalidade Shapiro-Wilk

Este script cria um aplicativo web interativo usando Streamlit.
O usuário pode inserir uma lista de números para realizar o teste de
Shapiro-Wilk e visualizar estatísticas descritivas, resultados e gráficos.
Inclui suporte para logo da empresa no topo.
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

# Estilo CSS para garantir que a tabela seja visível e limpa
st.markdown("""
    <style>
    table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
    }
    th, td {
        text-align: left;
        padding: 10px;
        border-bottom: 1px solid #f0f2f6;
    }
    .table-title {
        font-size: 1.2em;
        font-weight: bold;
        background-color: #f8f9fb;
    }
    .conclusion-cell {
        font-weight: bold;
        padding-top: 15px;
    }
    /* Estilo para centralizar a logo */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 2. Logo da Empresa
# ==============================================================================
# OPÇÃO A: Se você tiver a imagem no GitHub, use: st.image("logo.png", width=200)
# OPÇÃO B: Usando uma URL (substitua pela URL da logo da sua empresa)
# Abaixo usamos colunas para centralizar a imagem
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    # Substitua o link abaixo pelo link da logo da sua empresa
    # Se quiser usar um arquivo local que subiu no GitHub, use apenas o nome do arquivo: st.image("logo.png")
    st.image("https://logodownload.org/wp-content/uploads/2014/11/michelin-logo-0.png", width=150)

st.title("📊 Teste de Normalidade Shapiro-Wilk")
st.markdown("""
    Verificação de normalidade com estatísticas descritivas, W, p-valor e gráficos integrados.
""")

# ==============================================================================
# 3. Entrada de Dados do Usuário
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
# 4. Lógica de Análise
# ==============================================================================
if analyze_button:
    try:
        # Processamento da entrada (normaliza para ponto internamente)
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

            # Função auxiliar para formatar números com vírgula decimal
            def fmt(valor, casas=7):
                return f"{valor:.{casas}f}".replace('.', ',')

            # Definição da conclusão
            if p_value > alpha:
                conc_text = f"CONCLUSÃO: A normalidade é aceita com um risco alfa de {int(alpha*100)}%"
                conc_color = "#2e7d32" # Verde
            else:
                conc_text = f"CONCLUSÃO: A normalidade é rejeitada com um risco alfa de {int(alpha*100)}%"
                conc_color = "#c62828" # Vermelho

            st.write("---")
            
            # Construindo a tabela HTML unificada
            html_table = f"""
            <table>
                <tr>
                    <td colspan="2" class="table-title">📝 Teste de Normalidade (Método SHAPIRO-WILK)</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; width: 250px;">Média</td>
                    <td>{fmt(media)}</td>
                </tr>
                <tr>
                    <td style="font-weight: bold;">Desvio padrão</td>
                    <td>{fmt(desvio_padrao)}</td>
                </tr>
                <tr>
                    <td style="font-weight: bold;">Observações</td>
                    <td>{num_dados}</td>
                </tr>
                <tr>
                    <td style="font-weight: bold;">W</td>
                    <td>{fmt(statistic, 6)}</td>
                </tr>
                <tr>
                    <td style="font-weight: bold;">Valor-P</td>
                    <td>{fmt(p_value)}</td>
                </tr>
                <tr>
                    <td colspan="2" class="conclusion-cell" style="color: {conc_color}; border-bottom: none;">
                        {conc_text}
                    </td>
                </tr>
            </table>
            """
            st.markdown(html_table, unsafe_allow_html=True)

            # ==============================================================================
            # 5. Gráficos (Logo abaixo da tabela)
            # ==============================================================================
            plt.style.use('seaborn-v0_8-darkgrid')
            fig, axes = plt.subplots(1, 2, figsize=(12, 4)) 

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
    st.header("Informações")
    st.markdown("""
        Relatório integrado para cópia direta.
        
        Ao selecionar a tabela e colar no Excel, o título e a conclusão serão incluídos automaticamente.
    """)
    st.write("---")
    st.caption("v2.4 - Com Logo Corporativa")
