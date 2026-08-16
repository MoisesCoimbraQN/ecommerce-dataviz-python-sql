"""
Analise Exploratoria de Negocio - Volumetria e Janela Temporal.
Executa consultas SQL para entender o comportamento de vendas e status dos pedidos.
"""

import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

load_dotenv()

USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')
DATABASE = os.getenv('DB_NAME')

engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

# 1. Janela Temporal do Dataset
q_janela = """
SELECT 
    MIN(order_purchase_timestamp) AS primeira_compra,
    MAX(order_purchase_timestamp) AS ultima_compra,
    DATEDIFF(MAX(order_purchase_timestamp), MIN(order_purchase_timestamp)) AS total_dias_historico
FROM olist_orders_dataset;
"""

# 2. Distribuição por Status de Pedido
q_status = """
SELECT 
    order_status,
    COUNT(*) AS total_pedidos,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM olist_orders_dataset), 2) AS pct_total
FROM olist_orders_dataset
GROUP BY order_status
ORDER BY total_pedidos DESC;
"""


# 3. Evolucao Mensal de Pedidos (Apenas Pedidos Validos)
q_evolucao_mensal = """
SELECT 
    DATE_FORMAT(order_purchase_timestamp, '%%Y-%%m') AS ano_mes,
    COUNT(*) AS total_pedidos
FROM olist_orders_dataset
WHERE order_status NOT IN ('canceled', 'unavailable')
GROUP BY ano_mes
ORDER BY ano_mes ASC;
"""


print("=== 1. JANELA TEMPORAL DO DATASET ===")
print(pd.read_sql(q_janela, con=engine).to_string(index=False))
print("\n")

print("=== 2. DISTRIBUICAO DE STATUS DOS PEDIDOS ===")
print(pd.read_sql(q_status, con=engine).to_string(index=False))
print("\n")

print("=== 3. EVOLUCAO MENSAL DE PEDIDOS ===")
print(pd.read_sql(q_evolucao_mensal, con=engine).to_string(index=False))

# 4. Faturamento Geral e Ticket Medio
q_financeiro = """
SELECT 
    ROUND(SUM(price), 2) AS receita_produtos,
    ROUND(SUM(freight_value), 2) AS receita_frete,
    ROUND(SUM(price + freight_value), 2) AS faturamento_total,
    ROUND(SUM(price) / COUNT(DISTINCT order_id), 2) AS ticket_medio_produto,
    ROUND(SUM(price + freight_value) / COUNT(DISTINCT order_id), 2) AS ticket_medio_total
FROM olist_order_items_dataset;
"""

# 5. Metodos de Pagamento e Parcelamento
q_pagamentos = """
SELECT 
    payment_type,
    COUNT(*) AS total_transacoes,
    ROUND(SUM(payment_value), 2) AS valor_total,
    ROUND(AVG(payment_installments), 1) AS media_parcelas
FROM olist_order_payments_dataset
GROUP BY payment_type
ORDER BY total_transacoes DESC;
"""

print("=== 4. RESUMO FINANCEIRO E TICKET MEDIO ===")
print(pd.read_sql(q_financeiro, con=engine).to_string(index=False))
print("\n")

print("=== 5. METODOS DE PAGAMENTO E PARCELAMENTO ===")
print(pd.read_sql(q_pagamentos, con=engine).to_string(index=False))

# 6. Top 10 Categorias por Faturamento
q_top_categorias = """
SELECT 
    COALESCE(t.product_category_name_english, p.product_category_name, 'nao_informado') AS categoria,
    COUNT(DISTINCT i.order_id) AS total_pedidos,
    ROUND(SUM(i.price), 2) AS faturamento_produtos
FROM olist_order_items_dataset i
JOIN olist_products_dataset p ON i.product_id = p.product_id
LEFT JOIN product_category_name_translation t ON p.product_category_name = t.product_category_name
GROUP BY categoria
ORDER BY faturamento_produtos DESC
LIMIT 10;
"""

# 7. Performance Logistica (Prazos de Entrega)
q_logistica = """
SELECT 
    ROUND(AVG(DATEDIFF(order_delivered_customer_date, order_purchase_timestamp)), 1) AS media_dias_entrega_real,
    ROUND(AVG(DATEDIFF(order_estimated_delivery_date, order_purchase_timestamp)), 1) AS media_dias_estimados,
    ROUND(AVG(DATEDIFF(order_estimated_delivery_date, order_delivered_customer_date)), 1) AS folga_media_dias,
    ROUND(SUM(CASE WHEN order_delivered_customer_date > order_estimated_delivery_date THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pct_pedidos_atrasados
FROM olist_orders_dataset
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL;
"""

print("=== 6. TOP 10 CATEGORIAS DE PRODUTOS POR FATURAMENTO ===")
print(pd.read_sql(q_top_categorias, con=engine).to_string(index=False))
print("\n")

print("=== 7. PERFORMANCE LOGISTICA E PRAZOS DE ENTREGA ===")
print(pd.read_sql(q_logistica, con=engine).to_string(index=False))


# 8. Analise Geografica por Estado
q_geografia = """
SELECT 
    c.customer_state AS uf,
    COUNT(DISTINCT o.order_id) AS total_pedidos,
    ROUND(SUM(i.price), 2) AS receita_produtos,
    ROUND(AVG(i.freight_value), 2) AS frete_medio,
    ROUND(AVG(DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp)), 1) AS dias_entrega_medio,
    ROUND(SUM(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pct_atraso
FROM olist_orders_dataset o
JOIN olist_customers_dataset c ON o.customer_id = c.customer_id
JOIN olist_order_items_dataset i ON o.order_id = i.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY c.customer_state
ORDER BY total_pedidos DESC;
"""

print("=== 8. TOP 10 ESTADOS (VOLUME, FRETE E ATRASO) ===")
print(pd.read_sql(q_geografia, con=engine).to_string(index=False))
print("\n")

# 9. Recorrencia de Compras por Cliente 
q_recorrencia = """
WITH compras_cliente AS (
    SELECT 
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS total_compras
    FROM olist_orders_dataset o
    JOIN olist_customers_dataset c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
)
SELECT 
    CASE WHEN total_compras = 1 THEN '1 compra' ELSE '2+ compras (recorrente)' END AS perfil_cliente,
    COUNT(*) AS quantidade_clientes,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM compras_cliente), 2) AS pct_clientes
FROM compras_cliente
GROUP BY perfil_cliente;
"""

print("=== 9. RECORRENCIA DE CLIENTES ===")
print(pd.read_sql(q_recorrencia, con=engine).to_string(index=False))
print("\n")

# 10. Impacto do Atraso na Nota de Avaliacao
q_reviews_atraso = """
SELECT 
    CASE 
        WHEN o.order_delivered_customer_date <= o.order_estimated_delivery_date THEN 'No Prazo'
        ELSE 'Com Atraso'
    END AS status_entrega,
    COUNT(DISTINCT r.review_id) AS total_avaliacoes,
    ROUND(AVG(r.review_score), 2) AS nota_media,
    ROUND(SUM(CASE WHEN r.review_score = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pct_nota_1
FROM olist_orders_dataset o
JOIN olist_order_reviews_dataset r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY status_entrega;
"""

print("=== 10. NOTA MEDIA DE AVALIACAO: NO PRAZO VS ATRASADO ===")
print(pd.read_sql(q_reviews_atraso, con=engine).to_string(index=False))

#adicionar outras consultas que faltarem para os demais... 