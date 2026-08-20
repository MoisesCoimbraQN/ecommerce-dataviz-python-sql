import pandas as pd

# 1. Carrega o Data Mart de RFM
df_rfm = pd.read_parquet("data/mart_rfm_clientes.parquet")

# 2. Exibe as primeiras linhas com a classificação dos clientes
print(df_rfm.head())

# 3. Conta quantos clientes ficaram em cada segmento
print(df_rfm['Segmento_Cliente'].value_counts())

# 4. Filtra apenas os Clientes Campeões
campeoes = df_rfm[df_rfm['Segmento_Cliente'] == 'Cliente Campeao']
print(f"Total de Clientes Campeões: {len(campeoes)}")