#  Dicionário de Dados — E-Commerce Olist

Este documento descreve a estrutura, o significado e os tipos das colunas presentes no banco de dados relacional `db_olist`.

---

## 1. `olist_customers_dataset` (Clientes)
Armazena as informações dos clientes e suas localizações.

* **`customer_id`**: ID do cliente no contexto do pedido (chave única para cada pedido realizado).
* **`customer_unique_id`**: ID único do cliente (permite identificar compras recorrentes da mesma pessoa).
* **`customer_zip_code_prefix`**: Primeiros 5 dígitos do CEP do cliente.
* **`customer_city`**: Cidade do cliente.
* **`customer_state`**: Estado (UF) do cliente.

---

## 2. `olist_orders_dataset` (Pedidos)
Tabela central com os dados da transação e datas do ciclo de entrega.

* **`order_id`**: Identificador único do pedido.
* **`customer_id`**: Chave estrangeira que conecta ao cliente que fez o pedido.
* **`order_status`**: Status atual do pedido (`delivered`, `shipped`, `canceled`, etc.).
* **`order_purchase_timestamp`**: Data e hora em que a compra foi realizada.
* **`order_approved_at`**: Data e hora de aprovação do pagamento.
* **`order_delivered_carrier_date`**: Data e hora em que o pedido foi despachado para a transportadora.
* **`order_delivered_customer_date`**: Data e hora real da entrega ao cliente.
* **`order_estimated_delivery_date`**: Data estimada de entrega prometida no momento da compra.

---

## 3. `olist_products_dataset` (Produtos)
Informações do catálogo de produtos cadastrados.

* **`product_id`**: Identificador único do produto.
* **`product_category_name`**: Nome da categoria do produto (em português).
* **`product_name_lenght`**: Quantidade de caracteres do título do produto.
* **`product_description_lenght`**: Quantidade de caracteres da descrição do produto.
* **`product_photos_qty`**: Quantidade de fotos publicadas no anúncio do produto.
* **`product_weight_g`**: Peso do produto em gramas ($g$).
* **`product_length_cm`**: Comprimento do produto em centímetros ($cm$).
* **`product_height_cm`**: Altura do produto em centímetros ($cm$).
* **`product_width_cm`**: Largura do produto em centímetros ($cm$).

---

## 4. `olist_sellers_dataset` (Vendedores)
Lojistas e parceiros que vendem através do marketplace.

* **`seller_id`**: Identificador único do vendedor.
* **`seller_zip_code_prefix`**: Primeiros 5 dígitos do CEP do vendedor.
* **`seller_city`**: Cidade do vendedor.
* **`seller_state`**: Estado (UF) do vendedor.

---

## 5. `olist_order_payments_dataset` (Pagamentos)
Detalhes sobre a transação financeira de cada pedido.

* **`order_id`**: Identificador único do pedido.
* **`payment_sequential`**: Sequencial da forma de pagamento (ex: 1 para o 1º cartão, 2 para o 2º método/voucher).
* **`payment_type`**: Método de pagamento (`credit_card`, `boleto`, `voucher`, `debit_card`).
* **`payment_installments`**: Número de parcelas escolhidas.
* **`payment_value`**: Valor total pago naquela transação.

---

## 6. `olist_order_items_dataset` (Itens do Pedido)
Detalhamento de quais produtos foram comprados em cada pedido e por qual vendedor.

* **`order_id`**: Identificador único do pedido.
* **`order_item_id`**: Sequencial do item dentro do mesmo pedido (1, 2, 3...).
* **`product_id`**: Identificador do produto vendido.
* **`seller_id`**: Identificador do vendedor responsável pela oferta.
* **`shipping_limit_date`**: Data limite para o vendedor despachar o produto.
* **`price`**: Preço unitário do produto.
* **`freight_value`**: Valor do frete cobrado para aquele item.

---

## 7. `olist_order_reviews_dataset` (Avaliações)
Pesquisas de satisfação e comentários enviados pelos clientes.

* **`review_id`**: Identificador único da avaliação.
* **`order_id`**: Identificador único do pedido avaliado.
* **`review_score`**: Nota de satisfação dada pelo cliente (de 1 a 5).
* **`review_comment_title`**: Título da avaliação.
* **`review_comment_message`**: Texto/comentário deixado pelo cliente.
* **`review_creation_date`**: Data de envio da pesquisa de satisfação.
* **`review_answer_timestamp`**: Data e hora em que o cliente respondeu.

---

## 8. `olist_geolocation_dataset` (Geolocalização)
Mapeamento de CEPs brasileiros para coordenadas geográficas.

* **`geolocation_zip_code_prefix`**: Primeiros 5 dígitos do CEP.
* **`geolocation_lat`**: Latitude geográfica.
* **`geolocation_lng`**: Longitude geográfica.
* **`geolocation_city`**: Nome da cidade.
* **`geolocation_state`**: Estado (UF).

---

## 9. `product_category_name_translation` (Tradução de Categorias)
Tabela 'de-para' com a tradução dos nomes das categorias do português para o inglês.

* **`product_category_name`**: Nome da categoria em português.
* **`product_category_name_english`**: Nome da categoria traduzido para o inglês.