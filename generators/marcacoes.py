from datetime import datetime, timedelta
import random

# Gera marcações de ponto com alguns erros e variações, para testar o sistema
def gerar_marcacoes(funcionarios, dias_gerar, variacao_minutos=5):

    todas_marcacoes = []

    # horários base de trabalho
    horarios_padrao = ["08:00", "12:00", "13:00", "17:00"]

    # porcentagens simples de situações "reais"
    chance_faltar_um_horario = 10       # 10%
    chance_dia_sem_marcacao = 5         # 5%
    chance_duplicar_marcacao = 5        # 5%
    chance_horario_invertido = 3        # 3%

    # loop para cada funcionário
    for func in funcionarios:

        # gerar marcações para a quantidade de dias
        for dia_contador in range(dias_gerar):

            # pega a data (dias passados até hoje)
            data_marcacao = (datetime.now() - timedelta(days=dia_contador)).date()

            # verifica se o dia será totalmente sem marcações
            if random.randint(1, 100) <= chance_dia_sem_marcacao:
                # pula esse dia (funcionário faltou)
                continue

            # começa com a lista padrão
            horarios_hoje = horarios_padrao.copy()

            # chance de remover uma marcação (ex: faltou saída para almoço)
            if random.randint(1, 100) <= chance_faltar_um_horario:
                indice_remover = random.randint(0, len(horarios_hoje) - 1)
                horarios_hoje.pop(indice_remover)

            # chance de inverter horários (erro de relógio)
            if random.randint(1, 100) <= chance_horario_invertido and len(horarios_hoje) >= 2:
                random.shuffle(horarios_hoje)

            # agora gera cada horário
            for horario in horarios_hoje:

                # aplica variação aleatória de minutos
                base_time = datetime.strptime(horario, "%H:%M")
                minutos_extra = random.randint(-variacao_minutos, variacao_minutos)
                horario_real = (base_time + timedelta(minutes=minutos_extra)).time()

                todas_marcacoes.append({
                    "funcionario_id": func["id"],
                    "data": data_marcacao,
                    "hora": horario_real
                })

                # chance de duplicar a batida
                if random.randint(1, 100) <= chance_duplicar_marcacao:
                    todas_marcacoes.append({
                        "funcionario_id": func["id"],
                        "data": data_marcacao,
                        "hora": horario_real
                    })

    return todas_marcacoes


# gera query e valores para inserir no MySQL
def insert_marcacoes(lista_marcacoes):
    query = "INSERT INTO marcacoes (funcionario_id, data, hora) VALUES (%s, %s, %s)"
    valores = []

    for m in lista_marcacoes:
        valores.append((
            m["funcionario_id"],
            m["data"],
            m["hora"]
        ))

    return query, valores
