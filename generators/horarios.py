def gerar_horarios(funcionarios):
    # gera uma lista de horários padrão para cada funcionário
    return [{
        "funcionario_id": f["id"],   # pega o id do funcionário
        "entrada": "08:00",          # horário fixo de entrada
        "intervalo_saida": "12:00",  # horário de saída pro almoço
        "intervalo_retorno": "13:00",# volta do almoço
        "saida": "17:00"             # fim do expediente
    } for f in funcionarios]         # repete isso pra cada funcionário


def insert_horarios(horarios):
    # query SQL para inserir os horários no banco
    query = """INSERT INTO horarios 
    (funcionario_id, entrada, intervalo_saida, intervalo_retorno, saida)
    VALUES (%s, %s, %s, %s, %s)"""

    # monta a lista de valores na ordem exata que o SQL precisa
    values = [(h["funcionario_id"], h["entrada"], h["intervalo_saida"], h["intervalo_retorno"], h["saida"]) 
              for h in horarios]

    return query, values   # envia a query e os valores pro insert
