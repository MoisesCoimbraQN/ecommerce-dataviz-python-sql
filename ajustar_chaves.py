import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

engine = create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)



"""
Script de DDL para otimização e governança do banco de dados MySQL 'db_olist'.
Converte tipos de dados de texto para DATETIME/INT e define Primary Keys (simples e compostas).
Garante integridade referencial, previne duplicidades e otimiza a performance de JOINs.
"""

# DDLs de otimização de tipos de dados nas tabelas, Primary Keys e definição de restrições NOT NULL
comandos_ddl = [
    # 1. Clientes
    "ALTER TABLE olist_customers_dataset MODIFY customer_id VARCHAR(50) NOT NULL, ADD PRIMARY KEY (customer_id);",
    
    # 2. Pedidos
    "ALTER TABLE olist_orders_dataset MODIFY order_id VARCHAR(50) NOT NULL, ADD PRIMARY KEY (order_id);",
    "ALTER TABLE olist_orders_dataset MODIFY order_purchase_timestamp DATETIME, MODIFY order_approved_at DATETIME, MODIFY order_delivered_carrier_date DATETIME, MODIFY order_delivered_customer_date DATETIME, MODIFY order_estimated_delivery_date DATETIME;",
    
    # 3. Produtos
    "ALTER TABLE olist_products_dataset MODIFY product_id VARCHAR(50) NOT NULL, ADD PRIMARY KEY (product_id);",
    
    # 4. Vendedores
    "ALTER TABLE olist_sellers_dataset MODIFY seller_id VARCHAR(50) NOT NULL, ADD PRIMARY KEY (seller_id);",
    
    # 5. Itens do Pedido (Chave Composta)
    "ALTER TABLE olist_order_items_dataset MODIFY order_id VARCHAR(50) NOT NULL, MODIFY order_item_id INT NOT NULL, ADD PRIMARY KEY (order_id, order_item_id);",
    "ALTER TABLE olist_order_items_dataset MODIFY shipping_limit_date DATETIME;",

    # 6. Pagamentos (Chave Composta)
    "ALTER TABLE olist_order_payments_dataset MODIFY order_id VARCHAR(50) NOT NULL, MODIFY payment_sequential INT NOT NULL, ADD PRIMARY KEY (order_id, payment_sequential);",

    # 7. Tradução de Categorias
    "ALTER TABLE product_category_name_translation MODIFY product_category_name VARCHAR(100) NOT NULL, ADD PRIMARY KEY (product_category_name);"
]

print(" Aplicando Primary Keys e Ajustes de Tipos de Dados no MySQL...")

with engine.begin() as conn:
    for sql in comandos_ddl:
        try:
            conn.execute(text(sql))
            print(f" Sucesso: {sql[:60]}...")
        except Exception as e:
            print(f" Erro/Aviso ao executar: {sql[:60]}... -> {e}")

print("\n Alterações concluídas! Atualize (F5) a visualização no DBeaver.")