import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1", # Não consegui rodar localhost, coloquei o enderço do banco, verificar como usar localhost
        user="root",
        password="Pass1234@", # Em uma aplicação real não pdoeria aparecer a senha, ver um jeito de arrumar isso
        database="base_teste" # Nome banco que está sendo inserido
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