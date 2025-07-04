# -*- coding: utf-8 -*-
"""
Aplicativo Streamlit para Teste de Normalidade Shapiro-Wilk

Este script cria um aplicativo web interativo usando Streamlit.
O usuário pode inserir uma lista de números para realizar o teste de
Shapiro-Wilk e visualizar os resultados e gráficos de normalidade.
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
    Este aplicativo permite que você verifique se um conjunto de dados segue uma distribuição normal
    usando o teste de Shapiro-Wilk.
    Você pode inserir seus números, e o aplicativo fornecerá a estatística do teste,
    o valor-p e gráficos para visualização.
""")

# ==============================================================================
# 2. Entrada de Dados do Usuário
# ==============================================================================
st.header("🔢 Insira Seus Números")
st.info("Por favor, insira seus números separados por vírgulas (ex: 1.2, 3.4, 5.6) ou um por linha.")

# Área de texto para entrada de números
# O usuário pode colar ou digitar os números aqui
input_numbers_str = st.text_area(
    "Valores (entre 10 e 30 números)",
    value="18.66667, 18.95, 17.85, 15.73333, 16.41667, 14.5, 15.91667, 15.3, 15.41667, 15.91667, 16.41667, 16.66667, 18.95, 17.85, 15.73333",
    height=150,
    help="Cole ou digite seus números aqui. Use vírgulas ou quebras de linha para separar os valores."
)

# Botão para iniciar a análise
analyze_button = st.button("Analisar Dados")

# ==============================================================================
# 3. Lógica de Análise (executada ao clicar no botão)
# ==============================================================================
if analyze_button:
    try:
        # Processa a string de entrada para obter uma lista de números
        # Remove espaços em branco, substitui vírgulas por pontos (para decimal),
        # divide por vírgulas ou quebras de linha, filtra vazios e converte para float.
        numbers_raw = input_numbers_str.replace(' ', '').replace(',', '.').replace('\n', ',').split(',')
        dados = [float(num) for num in numbers_raw if num.strip()]

        num_dados = len(dados)

        # Validação do número de dados
        if num_dados < 10 or num_dados > 30:
            st.error(f"❌ Erro: O número de dados fornecido ({num_dados}) está fora do intervalo permitido (10 a 30).")
            st.warning("Por favor, insira entre 10 e 30 números.")
        elif num_dados == 0:
            st.error("❌ Erro: Nenhum dado válido foi inserido. Por favor, digite ou cole seus números.")
        else:
            st.success(f"✅ Dados carregados com sucesso: {num_dados} valores.")
            st.write("---")

            # Realiza o teste de Shapiro-Wilk
            st.header("🔬 Resultados do Teste de Shapiro-Wilk")
            statistic, p_value = stats.shapiro(dados)

            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Estatística W", value=f"{statistic:.4f}")
            with col2:
                st.metric(label="Valor-p", value=f"{p_value:.4f}")

            # Interpretação do resultado
            alpha = 0.05 # Nível de significância padrão
            st.subheader("Conclusão:")
            if p_value > alpha:
                st.markdown(f"Com um nível de significância de **{alpha}**, o valor-p ({p_value:.4f}) é maior que {alpha}.")
                st.markdown("Portanto, **não há evidência estatística para rejeitar a hipótese nula de normalidade.**")
                st.success("Isso sugere que os dados **PARECEM seguir uma distribuição normal**.")
            else:
                st.markdown(f"Com um nível de significância de **{alpha}**, o valor-p ({p_value:.4f}) é menor ou igual a {alpha}.")
                st.markdown("Portanto, **rejeitamos a hipótese nula de normalidade.**")
                st.error("Isso sugere que os dados **NÃO PARECEM seguir uma distribuição normal**.")

            st.write("---")

            # ==============================================================================
            # 4. Geração de Gráficos para Visualização
            # ==============================================================================
            st.header("📈 Visualização da Distribuição")
            st.markdown("Os gráficos abaixo ajudam a visualizar a forma da distribuição dos seus dados.")

            # Configurações para os gráficos
            plt.style.use('seaborn-v0_8-darkgrid')
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))

            # --- Histograma ---
            sns.histplot(dados, kde=True, bins='auto', color='darkorange', edgecolor='black', ax=axes[0])
            axes[0].set_title('Histograma dos Dados', fontsize=14)
            axes[0].set_xlabel('Valores', fontsize=12)
            axes[0].set_ylabel('Frequência', fontsize=12)
            axes[0].grid(axis='y', alpha=0.75)

            # --- Q-Q Plot ---
            stats.probplot(dados, dist="norm", plot=axes[1])
            axes[1].set_title('Q-Q Plot (Distribuição Normal)', fontsize=14)
            axes[1].set_xlabel('Quantis Teóricos (Normal)', fontsize=12)
            axes[1].set_ylabel('Quantis Observados', fontsize=12)
            axes[1].grid(True)

            plt.tight_layout()
            st.pyplot(fig) # Exibe a figura no Streamlit

            st.markdown("""
            **Guia de Interpretação dos Gráficos:**
            1.  **Histograma:** Observe a forma da distribuição. Uma distribuição normal se assemelha a uma 'curva de sino' simétrica. Desvios dessa forma (assimetria, múltiplos picos, achatamento) sugerem não-normalidade.
            2.  **Q-Q Plot (Quantil-Quantil):** Compare a dispersão dos pontos com a linha reta diagonal. Se os pontos seguirem de perto a linha reta, os dados são aproximadamente normalmente distribuídos. Desvios significativos da linha indicam não-normalidade.
            """)
            st.info("Nota: Para amostras pequenas, a interpretação visual dos gráficos pode ser menos conclusiva do que o resultado do teste estatístico formal.")

    except ValueError:
        st.error("❌ Erro: Por favor, insira apenas números válidos. Verifique se não há caracteres estranhos.")
    except Exception as e:
        st.error(f"❌ Ocorreu um erro inesperado: {e}")

# ==============================================================================
# 5. Informações Adicionais (Sidebar)
# ==============================================================================
with st.sidebar:
    st.header("Sobre o Teste de Shapiro-Wilk")
    st.markdown("""
        O teste de Shapiro-Wilk é um teste de hipótese usado para verificar
        se uma amostra de dados foi retirada de uma população com distribuição normal.

        * **Hipótese Nula (H₀):** Os dados são normalmente distribuídos.
        * **Hipótese Alternativa (H₁):** Os dados não são normalmente distribuídos.

        **Interpretação do Valor-p:**
        * Se `p-valor > 0.05` (nível de significância comum): Não rejeitamos H₀. Os dados podem ser normais.
        * Se `p-valor ≤ 0.05`: Rejeitamos H₀. Os dados provavelmente não são normais.
    """)
