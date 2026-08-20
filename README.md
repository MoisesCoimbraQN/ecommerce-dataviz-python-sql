# Brazilian E-Commerce Data Analysis & Insights

Este repositório contém um projeto ponta a ponta de Análise e Engenharia de Dados aplicado a um ecossistema de E-Commerce no Brasil. O projeto abrange desde o provisionamento do banco de dados relacional em ambiente containerizado até a execução de consultas SQL e a criação de painéis analíticos interativos.

---

## Fonte dos Dados

* Dataset: Brazilian E-Commerce Public Dataset by Olist
* Origem: Kaggle (dados reais e anonimizados do e-commerce brasileiro)
* Período de Cobertura: Pedidos realizados entre 2016 e 2018

---

## Arquitetura e Engenharia de Dados

### 1. Ambiente e Banco de Dados (Docker & DBeaver)
* Containerização: Provisionamento do banco de dados relacional PostgreSQL via Docker e Docker Compose.
* Gestão do Banco: Conexão, modelagem e administração das tabelas realizadas via DBeaver.
* Ingestão de Dados: Carga dos arquivos CSV originais para as tabelas relacionais mantendo as chaves primárias e estrangeiras (PK/FK).

### 2. Consultas e Extração via SQL
* Agregações e Joins complexos para consolidar dados de clientes, pedidos, pagamentos e avaliações.
* Criação de visões (Views) e consultas otimizadas para servir de base direta para as análises em Python.

---

## Estrutura do Projeto

* docker/: Arquivos de configuração do container (docker-compose.yml e scripts de inicialização).
* sql/: Scripts SQL para criação de esquemas, tabelas e consultas analíticas.
* data/: Arquivos de dados e exportações processadas.
* notebooks/: Notebooks Jupyter com o pipeline de análise exploratória em Python.
* assets/: Arquivos .html interativos exportados para integração com dashboards e sites.

---

## Seções da Análise Exploratória (EDA)

### 1. Visualizações Estáticas Executivas (Matplotlib & Seaborn)
* Evolução Temporal: Tendência de volume e receita de pedidos ao longo do tempo.
* Gargalo Logístico: Taxa de atraso nas entregas segmentada por Estado (UF).
* Satisfação (CSAT): Relação entre tempo de entrega e notas de avaliação dos clientes.

### 2. Painel Interativo para Exploração de Dados (Plotly)
> Esta seção apresenta gráficos interativos em Plotly, permitindo a exploração detalhada dos dados via hover e zoom. Essa abordagem viabiliza a exportação nativa em HTML, facilitando a incorporação das visualizações em websites, dashboards e relatórios executivos.

* 01. Evolução Mensal: Gráfico de linha interativo com métricas ao passar o mouse.
* 02. Atraso por UF: Barras com gradiente térmico de criticidade de atrasos.
* 03. CSAT vs. Atraso: Distribuição de notas (1 a 5) entre entregas no prazo e em atraso.
* 04. Concentração Geográfica: Subplots pareados (Volume de Pedidos vs. Receita R$).
* 05. Top Categorias por Região: Gráfico de barras empilhadas 100% com distribuição percentual.
* 06. Formas de Pagamento: Donut chart com apontadores externos e participação das transações.
* 07. Lead Time por UF: Tempo médio de entrega (dias) ordenado por estado.

---

## Tecnologias Utilizadas

* Infraestrutura & Banco de Dados: Docker, PostgreSQL, DBeaver, SQL
* Linguagem: Python 3.x
* Manipulação de Dados: Pandas, NumPy, SQLAlchemy / psycopg2
* Visualização Estática: Matplotlib, Seaborn
* Visualização Interativa: Plotly Express / Graph Objects

---

## Como Executar o Projeto

1. Clone o repositório:
   git clone https://github.com/seu-usuario/Brazilian_E_Commerce.git
   cd Brazilian_E_Commerce

2. Suba o ambiente Docker do Banco de Dados:
   docker-compose up -d

3. Crie e ative o ambiente virtual Python:
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate

4. Instale as dependências:
   pip install -r requirements.txt

5. Execute o Jupyter Notebook:
   jupyter notebook