import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = "127.0.0.1"  # força IPv4, evita o problema de localhost -> ::1
PORT = os.getenv("DB_PORT")
DATABASE = os.getenv("DB_NAME")

connection_url = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(connection_url)

try:
    query = "SHOW TABLES;"
    df_tables = pd.read_sql(query, con=engine)
    print("✅ Conexão bem-sucedida ao MySQL no Docker!")
    print("\nTabelas encontradas no banco 'db_olist':")
    print(df_tables)
except Exception as e:
    print(f"❌ Erro ao conectar no MySQL: {e}")