# README - GERADOR DE DADOS DE TESTE 

Essa task teve como objetivo rodar um script de inserção de dados falsos para facilitar alguns testes específicos. Consiste em criar cadastros de funcionários e empresas, marcações de ponto, variações de batidas de ponto.

O gerador cria e insere automaticamente dados falsos de:
* Empresas (com Nome e CNPJ )
* Funcionários (com Nome, CPF e vínculo com a empresa)
* Horários de trabalho (padrão)
* Marcações de ponto (para um período de dias)

O código usa Python, Faker e mysql-connector.

---

## 1. COMO FUNCIONA (VISÃO GERAL)

### 1.1. Configuração (`config.py`)
O arquivo `config.py` define as quantidades padrão de dados a serem gerados:
* `qtd_empresas` (Quantidade de empresas)
* `qtd_funcionarios` (Quantidade de funcionários por empresa)
* `dias_marcacoes` (Quantos dias de marcações serão gerados)
O usuário pode alterar esses valores.

### 1.2. Banco de Dados (Estrutura)
O projeto requer um banco de dados **MySQL** chamado *`base_teste`* com as seguintes tabelas já criadas (e configuradas com `AUTO_INCREMENT` e chaves estrangeiras):
* `empresas`
* `funcionarios`
* `horarios`
* `marcacoes`

A conexão com o MySQL está centralizada no arquivo `database.py`.

### 1.3. Geração de Dados (`generators/`)
A pasta `generators/` contém a lógica de criação dos dados falsos:
* `empresas.py`: Gera nome e CNPJ (usando Faker).
* `funcionarios.py`: Cria nome, CPF e associa ao `empresa_id`.
* `horarios.py`: Cria um horário de trabalho fixo (Ex: 08:00 a 17:00).
* `marcacoes.py`: Gera 4 marcações por dia (Entrada, Saída Intervalo, Retorno Intervalo, Saída).

### 1.4. Inserção no Banco (`database.py`)
O `database.py` utiliza duas funções importantes:
* `insert_many`: Insere vários registros de uma vez que não possuem dependência de IDs.
* `insert_and_get_first_id`: Usada para Empresas e Funcionários. Insere os dados e captura o primeiro ID real gerado pelo banco (`AUTO_INCREMENT`). Isso garante que o Python atribua corretamente os IDs para os registros relacionados (chaves estrangeiras).

---

## 2. ARQUIVO PRINCIPAL (`main.py`)
O `main.py` é o arquivo de execução que "manda" nas seguintes etapas, garantindo a integridade dos dados:
1.  Lê os argumentos de linha de comando.
2.  Gera e insere Empresas, capturando o ID inicial.
3.  Atribui os IDs reais das Empresas aos funcionários.
4.  Gera e insere Funcionários, capturando o ID inicial.
5.  Atribui os IDs reais dos Funcionários aos horários e marcações.
6.  Gera e insere Horários.
7.  Gera e insere Marcações.
8.  Exibe: “Processo concluído!”.

---

## 3. COMO RODAR O PROJETO

### 3.1. Dependências
Instale as bibliotecas necessárias usando `pip`:

No terminal use:
pip install faker
pip install mysql-connector-python

### 3.2. Execução
Execute o script main.py no terminal, dentro da pasta do projeto:
*** python main.py ***

4. OBSERVAÇÕES IMPORTANTES
MySQL Ativo: O servidor MySQL deve estar rodando para a conexão funcionar.

Credenciais (Erro 1045): O usuário e senha configurados no database.py devem ser válidos e ter privilégios de acesso total ao banco base_teste. Se houver erros, verifique se a conta root usa o plug-in de autenticação mysql_native_password no seu MySQL.
