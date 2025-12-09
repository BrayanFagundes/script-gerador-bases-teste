import os

try:
    import mysql.connector
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "mysql-connector-python is not installed. Run: python -m pip install mysql-connector-python"
    )


def get_connection():
    """Create a MySQL connection using environment variables with sensible defaults.

    Set these environment variables to override defaults:
    - DB_HOST (default: 'localhost')
    - DB_PORT (default: 3305)
    - DB_USER (default: 'admin')
    - DB_PASSWORD (default: 'dix1bolt')
    - DB_NAME (default: 'desenvolvimento')

    If your database runs on a non-standard port (e.g. 3305), set `DB_PORT=3305`.
    """
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "3305"))
    user = os.getenv("DB_USER", "admin")
    password = os.getenv("DB_PASSWORD", "dix1bolt")
    database = os.getenv("DB_NAME", "desenvolvimento")

    return mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
    )

# Função para inserir dados que NÃO PRECISAM retornar o ID
def insert_many(query, values):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.executemany(query, values)
        conn.commit()
        print(f"✅ Inserção concluída para {cursor.rowcount} registros.")

    except mysql.connector.Error as err:
        print(f"❌ Erro de Banco de Dados: {err}")
        if conn:
            conn.rollback()
        raise # Levanta o erro para parar a execução do script

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Função para inserir dados (ex: empresas, funcionarios) e obter o ID inicial
def insert_and_get_first_id(query, values):
    conn = None
    cursor = None
    primeiro_id = 0
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.executemany(query, values)
        conn.commit()
        
        # Recupera o ID da primeira linha inserida (cursor.lastrowid)
        primeiro_id = cursor.lastrowid
        print(f"✅ Inserção concluída para {cursor.rowcount} registros. Primeiro ID: {primeiro_id}")
        return primeiro_id
        
    except mysql.connector.Error as err:
        print(f"❌ Erro de Banco de Dados: {err}")
        if conn:
            conn.rollback()
        raise # Levanta o erro para parar a execução do script
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()