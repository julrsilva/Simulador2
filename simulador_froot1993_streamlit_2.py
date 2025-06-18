import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Simulador VPL com Hedge (Froot 1993)", layout="centered")

# Título
st.title("💹 Simulador de Gestão de Risco Corporativo")
st.caption("Baseado em Froot, Scharfstein e Stein (1993)")

# Entradas do usuário
investimento = st.slider("Investimento total (I)", 50, 200, 100)
a = st.slider("Parâmetro a (retorno marginal inicial)", 0.5, 5.0, 2.0)
b = st.slider("Parâmetro b (retorno decrescente)", 0.001, 0.05, 0.01)
r_base = st.slider("Custo base do capital externo (%)", 0.0, 0.3, 0.10, step=0.01)
lambda_sens = st.slider("Sensibilidade do custo ao financiamento externo (λ)", 0.000, 0.010, 0.001, step=0.0005)
custo_hedge_pct = st.slider("Custo do hedge (% do investimento)", 0.0, 0.05, 0.01)

# Fluxos de caixa simulados
cf_vals = np.array([100, 80, 60, 40, 20])
npv_sem_hedge = []
npv_com_hedge = []

# Função de retorno do investimento
def retorno(I):
    return a * I - b * I**2

for cf in cf_vals:
    # --- Sem hedge ---
    f1 = max(0, investimento - cf)
    r1 = r_base + lambda_sens * f1
    custo1 = cf + f1 * (1 + r1)
    npv1 = retorno(investimento) - custo1
    npv_sem_hedge.append(npv1)

    # --- Com hedge ---
    cf_hedge = cf * 1.1
    f2 = max(0, investimento - cf_hedge)
    r2 = r_base + lambda_sens * f2
    custo2 = cf_hedge + f2 * (1 + r2) + custo_hedge_pct * investimento
    npv2 = retorno(investimento) - custo2
    npv_com_hedge.append(npv2)

# Resultado em gráfico
st.subheader("📈 Comparação do Valor Presente Líquido (NPV)")

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(cf_vals, npv_sem_hedge, marker='o', label='Sem Hedge', color='blue')
ax.plot(cf_vals, npv_com_hedge, marker='s', label='Com Hedge', color='orange')
ax.set_xlabel("Fluxo de Caixa Interno")
ax.set_ylabel("NPV")
ax.set_title("Impacto da Gestão de Risco no Valor do Projeto")
ax.legend()
ax.grid(True)
ax.invert_xaxis()
st.pyplot(fig)

# Resultado em tabela
df_result = pd.DataFrame({
    "Fluxo de Caixa": cf_vals,
    "Financiamento Sem Hedge": investimento - cf_vals,
    "NPV Sem Hedge": npv_sem_hedge,
    "Financiamento Com Hedge": investimento - (cf_vals * 1.1),
    "NPV Com Hedge": npv_com_hedge,
    "Ganho com Hedge": np.array(npv_com_hedge) - np.array(npv_sem_hedge)
})
st.dataframe(df_result.round(2), use_container_width=True)
