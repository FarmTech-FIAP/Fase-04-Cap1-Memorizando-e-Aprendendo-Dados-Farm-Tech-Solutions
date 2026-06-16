import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import oracledb
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Configuração da página Streamlit
st.set_page_config(page_title="FarmTech Solutions - Assistente Inteligente", layout="wide")

st.title("🌱 FarmTech Solutions - Agricultura Cognitiva")
st.markdown("Dashboard Analítico de Machine Learning para Previsão de Safra e Irrigação")

# 1. Conexão e Ingestão de Dados do Banco SQL (Oracle no Docker)
@st.cache_data
def carregar_dados():
    usuario = "system"
    senha = "fiap"
    dsn_string = "localhost:1521/XE" 
    
    conn = oracledb.connect(user=usuario, password=senha, dsn=dsn_string)
    
    # IMPORTANTE: Aspas duplas para o Oracle respeitar o nome da tabela
    query = "SELECT * FROM HISTORICO_AGRICOLA"
    
    df = pd.read_sql_query(query, conn)
    
    # Garante que os nomes das colunas fiquem em minúsculo no DataFrame do Pandas,
    # mesmo se o Oracle tiver retornado em maiúsculo.
    df.columns = df.columns.str.lower()
    
    conn.close()
    return df

try:
    dados = carregar_dados()
except Exception as e:
    st.error(f"Erro ao conectar no Oracle do Docker: {e}")
    st.info("💡 Verifique se o container do Docker está ligado e se rodou o script de ingestão antes.")
    st.stop() 

# 2. Pipeline de Machine Learning (Treinamento)
X = dados[['umidade_solo', 'ph_solo', 'nivel_n', 'nivel_p', 'nivel_k']]
y_produtividade = dados['produtividade_kg']
y_irrigacao = dados['volume_irrigacao_litros']

# Divisão de treino e teste
X_train, X_test, y_prod_train, y_prod_test = train_test_split(X, y_produtividade, test_size=0.2, random_state=42)
_, _, y_irr_train, y_irr_test = train_test_split(X, y_irrigacao, test_size=0.2, random_state=42)

# Modelos de Regressão Múltipla
modelo_prod = LinearRegression().fit(X_train, y_prod_train)
modelo_irr = LinearRegression().fit(X_train, y_irr_train)

# Previsões para as métricas
pred_prod = modelo_prod.predict(X_test)

# 3. Interface: Métricas de Avaliação do Modelo
st.header("📊 Desempenho do Modelo Preditivo (Produtividade)")
col1, col2, col3, col4 = st.columns(4)
col1.metric("MAE", round(mean_absolute_error(y_prod_test, pred_prod), 2))
col2.metric("MSE", round(mean_squared_error(y_prod_test, pred_prod), 2))
col3.metric("RMSE", round(np.sqrt(mean_squared_error(y_prod_test, pred_prod)), 2))
col4.metric("R² Score", round(r2_score(y_prod_test, pred_prod), 2))

st.divider()

# 4. Interface: Gráficos de Correlação
st.header("📈 Análise de Correlação de Dados")
fig, ax = plt.subplots(figsize=(8, 4))
# Seleciona apenas colunas numéricas para a correlação
sns.heatmap(dados.select_dtypes(include=[np.number]).corr(), annot=True, cmap="YlGnBu", ax=ax)
st.pyplot(fig)

st.divider()

# 5. Interface: Previsões e Ações de Manejo Interativas
st.header("🔮 Simulador de Ações Futuras (Dados dos Sensores)")
st.markdown("Insira os dados lidos pelos sensores (Wokwi) para obter a recomendação de IA.")

c1, c2, c3 = st.columns(3)
with c1:
    in_umidade = st.slider("Umidade do Solo (%)", 0.0, 100.0, 50.0)
with c2:
    in_ph = st.slider("pH do Solo", 0.0, 14.0, 6.5)
with c3:
    in_n = st.selectbox("Nitrogênio (N)", [0, 1])
    in_p = st.selectbox("Fósforo (P)", [0, 1])
    in_k = st.selectbox("Potássio (K)", [0, 1])

# Executando Previsão
entrada_usuario = pd.DataFrame([[in_umidade, in_ph, in_n, in_p, in_k]], 
                               columns=['umidade_solo', 'ph_solo', 'nivel_n', 'nivel_p', 'nivel_k'])

prev_produtividade = modelo_prod.predict(entrada_usuario)[0]
prev_irrigacao = modelo_irr.predict(entrada_usuario)[0]

st.subheader("💡 Recomendações do Assistente Inteligente")
st.success(f"**Estimativa de Produtividade:** {prev_produtividade:.2f} kg esperados.")

if prev_irrigacao > 10:
    st.warning(f"**Ação de Irrigação:** LIGAR BOMBA. Necessário aplicar aproximadamente {prev_irrigacao:.2f} litros de água.")
else:
    st.info(f"**Ação de Irrigação:** MANTER DESLIGADA. O solo possui umidade suficiente.")

if in_ph < 5.5 or in_ph > 7.5:
    st.error("**Ação de Manejo:** Alerta de pH fora do limite para o milho. Sugere-se correção do solo imediata.")