import argparse
from config import CONFIG
from database import insert_many, insert_and_get_first_id # <-- IMPORT NOVO- função pega id inicial agora 

from generators.empresas import gerar_empresas, insert_empresas
from generators.funcionarios import gerar_funcionarios, insert_funcionarios
from generators.horarios import gerar_horarios, insert_horarios
from generators.marcacoes import gerar_marcacoes, insert_marcacoes

def main():
    parser = argparse.ArgumentParser() # Cria o parser que lê argumentos passados pelo terminal, perguuntar se tem outra maneira
    parser.add_argument("--qtd_empresas", type=int, default=CONFIG["qtd_empresas"]) # type=int garante que retorne um número, default usa a config
    parser.add_argument("--qtd_funcionarios", type=int, default=CONFIG["qtd_funcionarios"])
    parser.add_argument("--dias_marcacoes", type=int, default=CONFIG["dias_marcacoes"])
    args = parser.parse_args()

    # --- INSERÇÃO DE EMPRESAS ---
    empresas = gerar_empresas(args.qtd_empresas) # inserção de empresa fake
    q, v = insert_empresas(empresas) # monta query com valores
    
    # ALterei essa linha: Usa a nova função para obter o ID inicial
    primeiro_id_empresa = insert_and_get_first_id(q, v) 

    # alterei a linha: Atribui os IDs reais gerados pelo banco de dados
    for i, e in enumerate(empresas):
        e["id"] = primeiro_id_empresa + i

    # --- INSERÇÃO DE FUNCIONÁRIOS ---
    funcionarios = gerar_funcionarios(empresas, args.qtd_funcionarios)
    q, v = insert_funcionarios(funcionarios)
    
    # alterei a linha: Usa a nova função para obter o ID inicial
    primeiro_id_funcionario = insert_and_get_first_id(q, v)

    # alterei a linha: Atribui os IDs reais gerados pelo banco de dados
    for i, f in enumerate(funcionarios):
        f["id"] = primeiro_id_funcionario + i

    # --- INSERÇÃO DE HORÁRIOS ---
    horarios = gerar_horarios(funcionarios)
    q, v = insert_horarios(horarios)
    insert_many(q, v)

    # --- INSERÇÃO DE MARCAÇÕES ---
    marcacoes = gerar_marcacoes(funcionarios, args.dias_marcacoes)
    q, v = insert_marcacoes(marcacoes)
    insert_many(q, v)

    print("Processo concluído!")

if __name__ == "__main__":
    main()