# Instruções rápidas para agentes de codificação (projeto gerador)

Objetivo curto

- Gerar dados falsos (empresas, funcionários, horários, marcações) e inserir em um banco MySQL.

Arquitetura — visão rápida

- Entrypoint: `main.py` — orquestra geração e inserção em 7 etapas (empresas → funcionários → horários → marcações).
- Geração: pasta `generators/` contém um par de funções por entidade: `gerar_*` (lista de dicts) e `insert_*` (retorna `(query, values)`).
- Persistência: `database.py` centraliza a conexão e duas funções de inserção:
  - `insert_and_get_first_id(query, values)` — usada para entidades que precisam de IDs auto-increment (empresas, funcionários).
  - `insert_many(query, values)` — para inserções que não precisam retornar IDs (horários, marcações).
- Config: `config.py` contém valores default (`qtd_empresas`, `qtd_funcionarios`, `dias_marcacoes`, `variacao_minutos`) que podem ser sobrescritos por argumentos de linha de comando.

Padrões de implementação (siga estes ao editar/estender)

- Gerador de entidade: `gerar_X(...)` sempre retorna `List[dict]` com chaves usadas pelo `insert_X` (ex.: `{'nome': ..., 'cnpj': ...}` para empresas).
- Inserção: `insert_X` sempre retorna `(query, values)` para uso direto com `database.insert_many` ou `insert_and_get_first_id`.
- Atribuição de IDs: quando for preciso relacionar entidades (ex.: funcionário → empresa), o fluxo é:
  1. `empresas = gerar_empresas(...)`
  2. `q, v = insert_empresas(empresas)` → `primeiro_id = insert_and_get_first_id(q, v)`
  3. Atualizar `empresas[i]['id'] = primeiro_id + i` antes de gerar funcionários.

Conveções e inconsistências observadas (importante)

- Faker: todos os geradores usam `Faker('pt_BR')` — use sempre esse provider para dados brasileiros.
- Nomes de tabelas SQL nem sempre seguem pluralização consistente: por exemplo `empresas.py` usa `INSERT INTO empresa (...)` enquanto `funcionarios.py` usa `INSERT INTO funcionarios (...)`. Confirme a tabela real no banco antes de alterar queries.
- Banco padrão vs README: `database.py` tem `DB_NAME` default `desenvolvimento` e porta `3305`, enquanto o `README.txt` menciona `base_teste`. Verificar qual schema/DB será usado antes de rodar scripts.

Como rodar (exemplos concretos)

- Instalar dependências (PowerShell):
  ```powershell
  python -m pip install -r requirements.txt
  ```
- Rodar com opções (ex.):
  ```powershell
  $env:DB_HOST='localhost'; $env:DB_PORT='3305'; python main.py --qtd_empresas 5 --qtd_funcionarios 10 --dias_marcacoes 7
  ```

Pontos importantes para agentes (quando mudar/estender código)

- Ao adicionar uma nova entidade `X`:
  - Crie `generators/x.py` com `gerar_x` e `insert_x` seguindo os exemplos em `generators/`.
  - Atualize `main.py` inserindo a etapa correta na ordem de dependências e use `insert_and_get_first_id` sempre que precisar do `AUTO_INCREMENT` real.
- Evite alterar `database.get_connection()` sem validar variáveis de ambiente — prefira parametrizar via env vars usadas atualmente (`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`).
- `insert_and_get_first_id` usa `cursor.lastrowid` após `executemany` — essa abordagem é dependente do conector MySQL; antes de grandes mudanças, confirme comportamento com a versão de `mysql-connector-python` listada em `requirements.txt`.

Referências rápidas no código

- Orquestração: `main.py` (parser de args e fluxo de inserção).
- Conexão / inserções: `database.py` (`get_connection`, `insert_many`, `insert_and_get_first_id`).
- Geradores: `generators/empresas.py`, `generators/funcionarios.py`, `generators/horarios.py`, `generators/marcacoes.py`.
- Esquema SQL: `banco_base.sql` (arquivo com DDL completo — use-o para confirmar nomes de tabelas e constraints).

Notas finais / riscos conhecidos

- Requisitos: `requirements.txt` contém `Faker` e `mysql-connector-python` — não sobrescreva versões sem testar.
- Banco de dados deve ter as tabelas com `AUTO_INCREMENT` e FKs já criados; use `banco_base.sql` para recriar esquema.
- Há pequenas discrepâncias entre README e `database.py` (nome do DB). Pergunte ao mantenedor qual é o ambiente alvo antes de rodar.

Se algo estiver ambíguo ou faltar (por exemplo, naming das tabelas alvo), diga especificamente qual arquivo/linha você quer que eu verifique e eu confirmo.
