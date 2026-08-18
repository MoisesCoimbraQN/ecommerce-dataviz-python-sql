# Brazilian E-Commerce Data Analysis & Insights

Este repositório contém uma Análise Exploratória de Dados (EDA) aplicada a um ecossistema de E-Commerce no Brasil. O objetivo do projeto é mapear o comportamento de compras, identificar gargalos logísticos, avaliar a satisfação do cliente (CSAT) e analisar a performance por categoria e região.

---

## Fonte dos Dados

* Dataset: Brazilian E-Commerce Public Dataset by Olist
* Origem: Kaggle (dados reais e anonimizados do e-commerce brasileiro)
* Período de Extração/Cobertura dos Dados: Pedidos realizados entre 2016 e 2018

---

## Estrutura do Projeto

* data/: Conjunto de dados estruturados e processados.
* notebooks/: Notebooks Jupyter contendo o pipeline de análise exploratória.
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

* Linguagem: Python 3.x
* Manipulação de Dados: Pandas, NumPy
* Visualização Estática: Matplotlib, Seaborn
* Visualização Interativa: Plotly Express / Graph Objects

---

## Como Executar o Projeto

1. Clone o repositório:
   git clone https://github.com/seu-usuario/Brazilian_E_Commerce.git
   cd Brazilian_E_Commerce

2. Crie e ative o ambiente virtual:
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate

3. Instale as dependências:
   pip install -r requirements.txt

4. Execute o Jupyter Notebook:
   jupyter notebook