from database import get_connection


def main():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        tables = [
            'empresa',
            'funcionario',
            'registroFuncionario',
            'horario',
            'marcacao',
        ]

        print('\n=== Contagens por tabela ===')
        for t in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {t}")
                cnt = cursor.fetchone()[0]
                print(f"📊 {t}: {cnt}")
            except Exception as e:
                print(f"❌ Erro ao consultar {t}: {e}")

        print('\n=== Últimos registros (amostra) ===')
        samples = [
            ('funcionario', 'idFuncionario', 5),
            ('registroFuncionario', 'idRegistroFuncionario', 5),
            ('marcacao', 'idMarcacao', 10),
        ]
        for t, col, lim in samples:
            try:
                cursor.execute(f"SELECT * FROM {t} ORDER BY {col} DESC LIMIT {lim}")
                rows = cursor.fetchall()
                print(f"\nTabela {t} - {len(rows)} linhas retornadas:")
                for r in rows:
                    print(r)
            except Exception as e:
                print(f"❌ Erro ao listar {t}: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    main()
