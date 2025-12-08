from faker import Faker
faker = Faker("pt_BR")  # gera dados brasileiros (cnpj, nome de empresa, etc)

def gerar_empresas(qtd):
    # cria uma lista com a quantidade de empresas pedida
    return [{"nome": faker.company(), "cnpj": faker.cnpj()} for _ in range(qtd)]

def insert_empresas(empresas):
    # query para inserir empresas no banco
    query = "INSERT INTO empresas (nome, cnpj) VALUES (%s, %s)"

    # monta os valores na ordem da query acima
    values = [(e["nome"], e["cnpj"]) for e in empresas]

    return query, values  # devolve a query e a lista de tuplas
