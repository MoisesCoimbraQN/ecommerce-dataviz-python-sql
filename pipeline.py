import os
import datetime as dt
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# 1. Garante a criação da pasta data/ para armazenar os Parquets
os.makedirs("data", exist_ok=True)

# 2. Carrega as variáveis de ambiente do .env
load_dotenv()

USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')
DATABASE = os.getenv('DB_NAME')

engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

def run_pipeline():
    print("Iniciando Pipeline ETL com Geolocalizacao...")
    
    # --- 1. EXTRAÇÃO (EXTRACT) ---
    # Extrai pedidos, clientes e pagamentos
    query_orders = """
        SELECT 
            o.order_id, 
            o.customer_id, 
            o.order_status, 
            o.order_purchase_timestamp, 
            o.order_delivered_customer_date, 
            o.order_estimated_delivery_date,
            p.payment_type,
            p.payment_value,
            c.customer_unique_id, 
            c.customer_zip_code_prefix,
            c.customer_state,
            c.customer_city
        FROM olist_orders_dataset o
        JOIN olist_order_payments_dataset p ON o.order_id = p.order_id
        JOIN olist_customers_dataset c ON o.customer_id = c.customer_id
        WHERE o.order_status = 'delivered';
    """
    
    # Extrai coordenadas médias por prefixo de CEP (evita duplicações no JOIN com agregação dos prefixos dos CEPs dos clientes)
    query_geo = """
        SELECT 
            geolocation_zip_code_prefix AS customer_zip_code_prefix,
            AVG(geolocation_lat) AS latitude,
            AVG(geolocation_lng) AS longitude
        FROM olist_geolocation_dataset
        GROUP BY geolocation_zip_code_prefix;
    """
    
    try:
        df = pd.read_sql(query_orders, con=engine)
        df_geo = pd.read_sql(query_geo, con=engine)
        print(f"Extracao concluida: {len(df):,} registros de pedidos e {len(df_geo):,} localizacoes.")
    except Exception as e:
        print(f"Erro ao conectar ou extrair do MySQL: {e}")
        return

    # 2. TRANSFORMAÇÃO & INSIGHTS (TRANSFORM) 
    
    # A. Merge de dados geográficos
    df = df.merge(df_geo, on='customer_zip_code_prefix', how='left')
    
    # B. Converter colunas temporais
    date_cols = ['order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col])
        
    # C. SLAs Logísticos -- calculo de dias de entrega, atraso e flag de atraso
    df['dias_entrega_real'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.total_seconds() / 86400
    df['dias_estimados'] = (df['order_estimated_delivery_date'] - df['order_purchase_timestamp']).dt.total_seconds() / 86400
    df['atraso_dias'] = df['dias_entrega_real'] - df['dias_estimados']
    df['flag_atraso'] = np.where(df['atraso_dias'] > 0, 1, 0)
    
    # D. Modelagem RFM com Localização do Cliente
    max_date = df['order_purchase_timestamp'].max() + dt.timedelta(days=1)
    
    rfm = df.groupby('customer_unique_id').agg({
        'order_purchase_timestamp': lambda x: (max_date - x.max()).days,
        'order_id': 'nunique',
        'payment_value': 'sum',
        'customer_state': 'first',
        'customer_city': 'first',
        'latitude': 'first',
        'longitude': 'first'
    }).reset_index()
    
    rfm.columns = [
        'customer_unique_id', 'Recencia_Dias', 'Frequencia_Pedidos', 
        'ValorTotal_R$', 'Estado', 'Cidade', 'latitude', 'longitude'
    ]
    
    # Scores RFM (Quartis)
    rfm['R_Score'] = pd.qcut(rfm['Recencia_Dias'], 4, labels=[4, 3, 2, 1])
    rfm['F_Score'] = pd.Series(np.where(rfm['Frequencia_Pedidos'] > 1, 2, 1))
    rfm['M_Score'] = pd.qcut(rfm['ValorTotal_R$'], 4, labels=[1, 2, 3, 4])
    

# Regra de Segmentação de Clientes
    def definir_segmento(row):
        if row['R_Score'] == 4 and row['M_Score'] == 4:
            return 'Recente / Valioso'  # Ajustado de 'Cliente Campeao'
        elif row['R_Score'] <= 2 and row['M_Score'] >= 3:
            return 'Em Risco / Churn'
        elif row['R_Score'] >= 3:
            return 'Cliente Ativo / Recente'
        else:
            return 'Atencao Necessaria'
            
    rfm['Segmento_Cliente'] = rfm.apply(definir_segmento, axis=1)

    # --- 3. CARGA (LOAD) ---
    path_pedidos = "data/mart_pedidos_performance.parquet"
    path_rfm = "data/mart_rfm_clientes.parquet"
    
    df.to_parquet(path_pedidos, index=False)
    rfm.to_parquet(path_rfm, index=False)
    
    print(f"Data Mart de Pedidos com Geo salvo em: {path_pedidos}")
    print(f"Data Mart de RFM com Geo salvo em: {path_rfm}")
    print("Pipeline executado com sucesso!")

if __name__ == "__main__":
    run_pipeline()


# Verificando
"""
# 1. Carrega o Data Mart de RFM com dados de geolocalização
df_rfm = pd.read_parquet("data/mart_rfm_clientes.parquet")

# 2. Exibe as primeiras linhas da base
print("--- Primeiras Linhas do Data Mart ---")
print(df_rfm.head())

# 3. Contagem absoluta e percentual por segmento de cliente
print("\n--- Distribuição dos Segmentos de Clientes ---")
contagem = df_rfm['Segmento_Cliente'].value_counts()
percentual = df_rfm['Segmento_Cliente'].value_counts(normalize=True) * 100

df_resumo = pd.DataFrame({
    'Total_Clientes': contagem,
    'Percentual_%': percentual.round(2)
})
print(df_resumo)

# 4. Filtro para o segmento Recente / Valioso
recentes_valiosos = df_rfm[df_rfm['Segmento_Cliente'] == 'Recente / Valioso']
print(f"\nTotal de Clientes Recentes / Valiosos: {len(recentes_valiosos):,}")
"""