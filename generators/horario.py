def gerar_horarios(empresas):
    # gera um horário padrão para cada empresa 
    return [{
        "descricao": f"Horário padrão da empresa {e['id']}",   # só uma descrição simples
        "idSituacaoCadastro": 1                                # campo obrigatório no banco
    } for e in empresas]   # repete isso para cada empresa


def insert_horarios(horarios):
    # query SQL para inserir os horários no banco (agora com os campos reais da tabela)
    query = """INSERT INTO horario 
    (descricao, idSituacaoCadastro)
    VALUES (%s, %s)"""

    # monta a lista de valores na ordem exata que o SQL precisa
    values = [(h["descricao"], h["idSituacaoCadastro"]) 
              for h in horarios]

    return query, values   # envia a query e os valores pro insert
