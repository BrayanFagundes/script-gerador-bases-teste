"""Compatibilidade: wrapper para o gerador/insert de `marcacao`.

Este módulo aceita chamadas antigas que passavam 'funcionarios' e/ou usavam nomes/pluralizações diferentes.
Ele normaliza entradas para `generators.marcacao` (singular) que gera `marcacao` com timestamps (epoch).
"""
from .marcacao import gerar_marcacoes as gerar_marcacoes_new, insert_marcacoes as insert_marcacoes_new


def gerar_marcacoes(funcionarios_or_registros, dias_gerar, variacao_minutos=5):
    """Se receber `funcionarios`, tenta extrair `registro_id` ou `id` e monta uma lista de registros mínima.

    Retorna a mesma estrutura que `gerar_marcacoes` do módulo novo.
    """
    registros = []

    # Se itens já aparentam ser registros (possuem 'idRegistroFuncionario' ou 'id'), adaptamos
    for f in funcionarios_or_registros:
        if isinstance(f, dict):
            if "idRegistroFuncionario" in f:
                registros.append({"id": f["idRegistroFuncionario"]})
            elif "registro_id" in f:
                registros.append({"id": f["registro_id"]})
            elif "id" in f and ("idEmpresa" in f or "empresa_id" in f or "cpf" in f):
                # é provavelmente um funcionário sem registro; usar id como idRegistroFuncionario
                registros.append({"id": f.get("registro_id", f.get("id"))})
            else:
                # último recurso: gerar um id temporário
                registros.append({"id": f.get("id", 0)})
        else:
            registros.append({"id": getattr(f, "id", 0)})

    return gerar_marcacoes_new(registros, dias_gerar, variacao_minutos)


def insert_marcacoes(marcacoes):
    # delega ao inserter novo, mantendo a assinatura compatível
    return insert_marcacoes_new(marcacoes)
