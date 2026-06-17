import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Numeric

# --- PASSO 1: CONEXÃO COM O ORACLE ---
string_conexao = "oracle+oracledb://system:fiap@localhost:1521/?service_name=XE"

print("Conectando ao banco de dados Oracle...")
engine = create_engine(string_conexao)

# --- PASSO 2: SIMULAR OS DADOS DOS SENSORES (IOT) ---
np.random.seed(42)

umidade = np.random.uniform(40, 80, 100)
ph = np.random.uniform(5.0, 7.5, 100)
n = np.random.randint(0, 2, 100)
p = np.random.randint(0, 2, 100)
k = np.random.randint(0, 2, 100)

irrigacao = 100 - umidade + np.random.normal(0, 5, 100)
produtividade = (umidade * 0.5) + (ph * 2) + (n * 15) + (p * 10) + (k * 10) + np.random.normal(0, 5, 100)

dados = pd.DataFrame({
    'umidade_solo': umidade,
    'ph_solo': ph,
    'nivel_n': n,
    'nivel_p': p,
    'nivel_k': k,
    'volume_irrigacao_litros': irrigacao,
    'produtividade_kg': produtividade
})

# --- PASSO 3: INGESTÃO DOS DADOS NO ORACLE ---
print("Criando tabela e inserindo dados...")

dados.to_sql('historico_agricola', engine, if_exists='replace', index=False,
             dtype={
                 'umidade_solo': Numeric(10, 2),
                 'ph_solo': Numeric(10, 2),
                 'nivel_n': Integer(),
                 'nivel_p': Integer(),
                 'nivel_k': Integer(),
                 'volume_irrigacao_litros': Numeric(10, 2),
                 'produtividade_kg': Numeric(10, 2)
             })

print("Ingestão concluída com sucesso! No SQL Developer faça um SELECT * FROM historico_agricola;")