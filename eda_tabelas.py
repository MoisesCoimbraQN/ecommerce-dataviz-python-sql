import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# 1. Carrega as variáveis do .env
load_dotenv()

USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')
DATABASE = os.getenv('DB_NAME')  # <-- Esta linha define a variável DATABASE!

engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

# 2. Mapeamento das tabelas e chaves
tabelas_chaves = {
    "olist_customers_dataset": "customer_id",
    "olist_orders_dataset": "order_id",
    "olist_products_dataset": "product_id",
    "olist_sellers_dataset": "seller_id",
    "olist_order_payments_dataset": "order_id",
    "olist_order_items_dataset": "order_item_id",
    "olist_order_reviews_dataset": "review_id",
    "olist_geolocation_dataset": "geolocation_zip_code_prefix",
    "product_category_name_translation": "product_category_name"
}


print("\n" + "="*80)
print("👀 ETAPA 1: VISUALIZAÇÃO DAS AMOSTRAS DOS DADOS (TOP 5 LINHAS)")
print("="*80)

for tabela in tabelas_chaves.keys():
    print(f"\n📋 TABELA: {tabela.upper()}")
    q_sample = f"SELECT * FROM {tabela} LIMIT 5;"
    df_sample = pd.read_sql(q_sample, con=engine)
    print(df_sample.to_string(index=False))
    print("-" * 80)

# 3. Laço de varredura
for tabela, col_chave in tabelas_chaves.items():
    print(f"\n{'='*65}")
    print(f" ANALISANDO TABELA: {tabela.upper()}")
    print(f"{'='*65}")

    q_unicidade = f"""
    SELECT 
        COUNT(*) AS total_linhas,
        COUNT({col_chave}) AS total_ids_preenchidos,
        COUNT(DISTINCT {col_chave}) AS ids_unicos
    FROM {tabela};
    """

    q_estrutura = f"""
    SELECT 
        COLUMN_NAME AS coluna,
        DATA_TYPE AS tipo_dado,
        IS_NULLABLE AS aceita_null
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = '{DATABASE}' 
      AND TABLE_NAME = '{tabela}';
    """

    df_unicidade = pd.read_sql(q_unicidade, con=engine)
    df_estrutura = pd.read_sql(q_estrutura, con=engine)

    print(f" 1. UNICIDADE DA CHAVE CANDIDATA (`{col_chave}`):")
    print(df_unicidade.to_string(index=False))

    print("\n 2. ESTRUTURA DAS COLUNAS:")
    print(df_estrutura.to_string(index=False))
    print("\n")