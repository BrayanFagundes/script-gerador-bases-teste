from faker import Faker
faker = Faker("pt_BR")

# Usa faker para gerar dados fake de empresas
def gerar_empresas(qtd):
    empresas = []
    for _ in range(qtd):
        empresas.append({
            "razaoSocial": faker.company(),          # nome da empresa
            "documento": faker.cnpj(),               # cnpj fake
            "endereco": faker.street_name(),         # endereço simples
            "cidade": faker.city(),                  # cidade fake
            "idTipoDocumentoCadastro": 1,          
            "idSitEmpresa": 1                    
        })
    return empresas

# Monta a query e os valores para inserção em massa de empresas
def insert_empresas(empresas):
    query = """
        INSERT INTO empresa 
        (razaoSocial, documento, endereco, cidade, idTipoDocumentoCadastro, idSitEmpresa)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = [
        (
            e.get("razaoSocial", e.get("nome")),
            e.get("documento", e.get("cnpj")),
            e.get("endereco", ""),
            e.get("cidade", ""),
            e.get("idTipoDocumentoCadastro", 1),
            e.get("idSitEmpresa", 1)
        )
        for e in empresas
    ]

    return query, values
