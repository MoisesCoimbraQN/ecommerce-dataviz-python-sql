import os
import glob
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# 1. Carrega as variáveis do .env
load_dotenv()

USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')
DATABASE = os.getenv('DB_NAME')

# 2. Conexão com o MySQL no Docker
connection_url = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(connection_url)

# 3. Caminho da pasta onde estão os CSVs
PASTA_DATA = "./data"

# Busca todos os arquivos .csv na pasta
arquivos_csv = glob.glob(os.path.join(PASTA_DATA, "*.csv"))

if not arquivos_csv:
    print(" Nenhum arquivo CSV encontrado na pasta './data'. Verifique o caminho!")
else:
    print(f" Encontrados {len(arquivos_csv)} arquivos CSV para importação.\n")

    for caminho_arquivo in arquivos_csv:
        # Extrai o nome do arquivo sem extensão para usar como nome da tabela
        nome_tabela = os.path.basename(caminho_arquivo).replace('.csv', '')
        
        print(f" Processando: {nome_tabela}...")
        
        # Lê o CSV com Pandas
        df = pd.read_csv(caminho_arquivo)
        
        # Envia para o MySQL (substitui a tabela se já existir)
        df.to_sql(
            name=nome_tabela,
            con=engine,
            if_exists='replace',
            index=False,
            chunksize=5000  # Envia em lotes otimizados
        )
        
        print(f" Tabela `{nome_tabela}` criada/atualizada com sucesso! ({len(df):,} linhas)\n")

    print(" Toda a base da Olist foi carregada com sucesso no MySQL do Docker!")