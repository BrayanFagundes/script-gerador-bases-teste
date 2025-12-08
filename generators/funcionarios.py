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
                "empresa_id": e["id"]      # liga o funcionário à empresa certa
            })

    return funcionarios  # volta a lista final

def insert_funcionarios(funcionarios):
    # comando SQL pra inserir no banco
    query = "INSERT INTO funcionarios (nome, cpf, empresa_id) VALUES (%s, %s, %s)"

    # montar os valores do insert (na mesma ordem da query)
    values = [(f["nome"], f["cpf"], f["empresa_id"]) for f in funcionarios]

    return query, values  # devolve query + valores pro executemany
