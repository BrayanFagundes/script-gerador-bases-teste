from faker import Faker
faker = Faker("pt_BR")  # usar dados do Brasil (nome, cpf etc)

def gerar_funcionarios(empresas, qtd):
    funcionarios = []  # lista onde fica os funcionários

    for e in empresas:
        # gera X funcionarios para cada empresa
        for _ in range(qtd):
            funcionarios.append({
                "nome": faker.name(),      # nome aleatório
                "cpf": faker.cpf(),        # cpf aleatório
                "pis": faker.numerify('###########'),  # pis fake só pra preencher o campo obrigatório
                "empresa_id": e["id"],     # liga o funcionário à empresa certa (uso interno)
            })

    return funcionarios  # volta a lista final


def insert_funcionarios(funcionarios):
    # comando SQL pra inserir no banco
    # (agora ajustado para a tabela 'funcionario' real)
    query = """
        INSERT INTO funcionario 
        (nome, cpf, pis, idEstadoCivil, idSituacaoCadastro, verificaBiometria)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    # montar os valores do insert (na mesma ordem da query)
    values = [
        (
            f["nome"],
            f["cpf"],
            f["pis"],
            1,  # idEstadoCivil default
            1,  # idSituacaoCadastro default
            0   # verificaBiometria default
        )
        for f in funcionarios
    ]

    return query, values  # devolve query + valores pro executemany


def gerar_registros(funcionarios):
    """Gera registros para `registroFuncionario` a partir da lista de funcionários.

    Cada registro referencia um `idFuncionario` e `idEmpresa` (empresa_id gerado anteriormente).
    Os campos obrigatórios são preenchidos com valores plausíveis para testes.
    """
    from datetime import datetime
    ts_now = int(datetime.now().timestamp())

    registros = []
    for f in funcionarios:
        registros.append({
            "idFuncionario": f["id"],
            "idEmpresa": f["empresa_id"],
            "dataAdmissao": ts_now,
            "dataDemissao": -1,
            "inicioMarcacao": 0,
            "finalMarcacao": 0,
            "idTipoFuncionario": 1,
            "idGmt": 1,
            "idSituacaoCadastro": 1
        })

    return registros


def insert_registros(registros):
    query = """
        INSERT INTO registroFuncionario
        (idFuncionario, idEmpresa, dataAdmissao, dataDemissao, inicioMarcacao, finalMarcacao, idTipoFuncionario, idGmt, idSituacaoCadastro)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = [
        (
            r["idFuncionario"],
            r["idEmpresa"],
            r["dataAdmissao"],
            r["dataDemissao"],
            r["inicioMarcacao"],
            r["finalMarcacao"],
            r["idTipoFuncionario"],
            r["idGmt"],
            r["idSituacaoCadastro"]
        )
        for r in registros
    ]

    return query, values
