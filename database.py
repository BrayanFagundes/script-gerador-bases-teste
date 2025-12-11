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
    - DB_PORT (default: 3306)
    - DB_USER (default: 'root')
    - DB_PASSWORD (default: 'Pass1234@')
    - DB_NAME (default: 'base_teste')
    

    If your database runs on a non-standard port (e.g. 3305), set `DB_PORT=3305`.
    """
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "3306"))
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "Pass1234@")
    database = os.getenv("DB_NAME", "base_teste")

    conn = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
    )

    # DEBUG: informa qual database/ schema foi selecionado nessa conexão
    try:
        print(f"🔌 Conectado ao MySQL: host={host} port={port} database={conn.database}")
    except Exception:
        pass

    return conn
    

# Função para inserir dados que NÃO PRECISAM retornar o ID
def insert_many(query, values):
    if not values:
        print("⚠️ Nenhum registro para inserir. Pulando insert_many.")
        return

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # DEBUG: mostrar a query e um exemplo de valores para diagnóstico
        try:
            preview = values[0] if isinstance(values, (list, tuple)) and len(values) > 0 else None
        except Exception:
            preview = None
        print("-- Executando query:")
        print(query.strip())
        print("-- Exemplo de valores:", repr(preview))

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
    if not values:
        print("⚠️ Nenhum registro para inserir. insert_and_get_first_id retorna 0.")
        return 0

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.executemany(query, values)
        conn.commit()

        # cursor.lastrowid normalmente aponta para o último ID inserido
        # Para obter o primeiro ID quando usamos executemany, subtrai-se rowcount - 1
        try:
            rowcount = cursor.rowcount or len(values)
            primeiro_id = cursor.lastrowid - rowcount + 1
        except Exception:
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