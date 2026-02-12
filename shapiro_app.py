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

st.title("📊 Teste de Normalidade Shapiro-Wilk")
st.markdown("""
    Este aplicativo permite verificar se um conjunto de dados segue uma distribuição normal.
    Ele fornece estatísticas descritivas, a estatística do teste (W), o valor-p e gráficos de visualização.
""")

# ==============================================================================
# 2. Entrada de Dados do Usuário
# ==============================================================================
st.header("🔢 Insira Seus Números")
st.info("Insira seus números separados por vírgulas (ex: 1.2, 3.4, 5.6) ou um por linha.")

input_numbers_str = st.text_area(
    "Valores (entre 10 e 30 números)",
    value="",
    height=150,
    help="Cole ou digite seus números aqui. Use vírgulas ou quebras de linha para separar os valores."
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
            st.success(f"✅ Análise concluída para {num_dados} valores.")
            st.write("---")

            # Cálculos Estatísticos
            media = np.mean(dados)
            desvio_padrao = np.std(dados, ddof=1) # ddof=1 para desvio padrão amostral
            statistic, p_value = stats.shapiro(dados)
            alpha = 0.05

            # Exibição das Informações (Estilo Relatório)
            st.header("📋 Resumo da Análise")
            
            # Criando colunas para as estatísticas descritivas
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Média", f"{media:.4f}")
            col_b.metric("Desvio Padrão", f"{desvio_padrao:.4f}")
            col_c.metric("Observações", f"{num_dados}")

            st.write("---")
            
            # Resultados do Teste de Shapiro-Wilk
            st.subheader("Resultados do Teste")
            col_w, col_p = st.columns(2)
            col_w.metric("Estatística W", f"{statistic:.6f}")
            col_p.metric("Valor-P", f"{p_value:.6f}")

            # Conclusão baseada no Alpha
            if p_value > alpha:
                st.success(f"**CONCLUSÃO:** A normalidade é **ACEITA** com um risco alfa de {int(alpha*100)}%")
                st.markdown("Os dados parecem seguir uma distribuição normal.")
            else:
                st.error(f"**CONCLUSÃO:** A normalidade é **REJEITADA** com um risco alfa de {int(alpha*100)}%")
                st.markdown("Os dados não parecem seguir uma distribuição normal.")

            st.write("---")

            # ==============================================================================
            # 4. Gráficos
            # ==============================================================================
            st.header("📈 Visualização Gráfica")
            plt.style.use('seaborn-v0_8-darkgrid')
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))

            # Histograma
            sns.histplot(dados, kde=True, bins='auto', color='royalblue', edgecolor='black', ax=axes[0])
            axes[0].set_title('Histograma e Curva de Densidade', fontsize=14)
            axes[0].set_xlabel('Valores', fontsize=12)
            axes[0].set_ylabel('Frequência', fontsize=12)

            # Q-Q Plot
            stats.probplot(dados, dist="norm", plot=axes[1])
            axes[1].set_title('Gráfico Q-Q (Quantil-Quantil)', fontsize=14)
            axes[1].set_xlabel('Quantis Teóricos', fontsize=12)
            axes[1].set_ylabel('Quantis Observados', fontsize=12)

            plt.tight_layout()
            st.pyplot(fig)

    except ValueError:
        st.error("❌ Erro: Certifique-se de inserir apenas números válidos.")
    except Exception as e:
        st.error(f"❌ Ocorreu um erro: {e}")

# Sidebar
with st.sidebar:
    st.header("Informações Técnicas")
    st.markdown("""
        **Média:** Soma de todos os valores dividida pela contagem.
        
        **Desvio Padrão:** Medida da dispersão dos dados em relação à média.
        
        **Estatística W:** Mede a proximidade dos dados a uma distribuição normal ideal (máximo 1).
        
        **Valor-P:** Se for maior que 0.05, aceitamos que os dados são normais.
    """)
    st.markdown("---")
    st.caption("Desenvolvido para análise de precisão.")
