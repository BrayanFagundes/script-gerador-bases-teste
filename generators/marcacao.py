from datetime import datetime, timedelta
import random

# Gera marcações reais pro banco (com erros e variações)
# OBS: agora usa registroFuncionario (e não funcionario), pq o banco exige isso
def gerar_marcacoes(registros, dias_gerar, variacao_minutos=5):

    todas = []  # lista final

    # horários base do expediente
    horarios_padrao = [
        ("08:00", 1),   # entrada
        ("12:00", 2),   # saída almoço
        ("13:00", 3),   # volta almoço
        ("17:00", 4)    # saída final
    ]

    # chances pra simular erros reais
    chance_faltar_um = 10         # 10%
    chance_dia_vazio = 5          # 5%
    chance_duplicada = 5          # 5%
    chance_bagunçar_ordem = 3     # 3%

    # loop pros registros (func vinculado à empresa + tipo + gmt)
    for reg in registros:

        # gera N dias
        for d in range(dias_gerar):

            data_atual = (datetime.now() - timedelta(days=d)).date()

            # chance do funcionário não marcar nada no dia
            if random.randint(1, 100) <= chance_dia_vazio:
                continue  # pula tudo

            # copia pra manipular sem estragar o original
            horarios_hoje = horarios_padrao.copy()

            # chance de sumir uma marcação do dia
            if random.randint(1, 100) <= chance_faltar_um:
                idx = random.randint(0, len(horarios_hoje) - 1)
                horarios_hoje.pop(idx)

            # chance de bagunçar ordem (erro comum de relógio)
            if random.randint(1, 100) <= chance_bagunçar_ordem and len(horarios_hoje) >= 2:
                random.shuffle(horarios_hoje)

            # gera todas as batidas do dia
            for hora_texto, numMarc in horarios_hoje:

                # variação aleatória
                base = datetime.strptime(hora_texto, "%H:%M")
                minutos = random.randint(-variacao_minutos, variacao_minutos)
                horario_real = base + timedelta(minutes=minutos)

                # timestamp só da data
                data_meia_noite = datetime(
                    data_atual.year,
                    data_atual.month,
                    data_atual.day
                )
                ts_data = int(data_meia_noite.timestamp())

                # timestamp só da hora
                ts_hora = int(datetime(1970, 1, 1, horario_real.hour, horario_real.minute).timestamp())

                # timestamp completo (data + hora)
                dt_completa = datetime(
                    data_atual.year,
                    data_atual.month,
                    data_atual.day,
                    horario_real.hour,
                    horario_real.minute
                )
                ts_data_hora = int(dt_completa.timestamp())

                todas.append({
                    "idRegistroFuncionario": reg["id"],  # agora usa o id do registroFuncionario
                    "dataMarcacao": ts_data_hora,        # data + hora
                    "data": ts_data,                     # só dia
                    "hora": ts_hora,                     # só hora
                    "idTpOrigemMarcacao": 1,             # origem padrão
                    "considerar": 1,                     # sempre válido
                    "numeroMarcacao": numMarc,           # 1,2,3,4
                    "descricao": "Fake"                  # só texto simples
                })

                # chance de duplicar batida
                if random.randint(1, 100) <= chance_duplicada:
                    todas.append({
                        "idRegistroFuncionario": reg["id"],
                        "dataMarcacao": ts_data_hora,
                        "data": ts_data,
                        "hora": ts_hora,
                        "idTpOrigemMarcacao": 1,
                        "considerar": 1,
                        "numeroMarcacao": numMarc,
                        "descricao": "Fake"
                    })

    return todas


# monta query + valores pra jogar no banco
def insert_marcacoes(marcacoes):

    query = """
        INSERT INTO marcacao 
        (idRegistroFuncionario, dataMarcacao, data, hora, idTpOrigemMarcacao, considerar, numeroMarcacao, descricao)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    valores = [
        (
            m["idRegistroFuncionario"],
            m["dataMarcacao"],
            m["data"],
            m["hora"],
            m["idTpOrigemMarcacao"],
            m["considerar"],
            m["numeroMarcacao"],
            m["descricao"]
        )
        for m in marcacoes
    ]

    return query, valores
