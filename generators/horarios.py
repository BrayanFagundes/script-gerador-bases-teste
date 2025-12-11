"""Compatibilidade: wrapper para o gerador/insert de `horario`.

Algumas versões antigas do projeto usavam módulos/pluralizações `horarios`.
Este arquivo traduz chamadas antigas para os geradores atuais em `horario.py`.
"""
from .horario import gerar_horarios as gerar_horarios_new, insert_horarios as insert_horarios_new


def gerar_horarios(funcionarios_or_empresas):
    """Aceita tanto `empresas` quanto `funcionarios`.

    - Se receber empresas (cada item com chave `id`), usa gerador novo diretamente.
    - Se receber funcionários (cada item com `id` e possivelmente `empresa_id`), cria um horário "por funcionário"
      transformando em entradas de `horario` (descrição) para compatibilidade.
    """
    # Detecta se são empresas (possui chave 'razaoSocial' ou 'idTipoDocumentoCadastro')
    if funcionarios_or_empresas and isinstance(funcionarios_or_empresas, list):
        first = funcionarios_or_empresas[0]
        if isinstance(first, dict) and ("razaoSocial" in first or "idTipoDocumentoCadastro" in first):
            return gerar_horarios_new(funcionarios_or_empresas)

    # Caso sejam funcionários, converte para uma lista de 'horario' por empresa fictícia
    horarios = []
    for f in funcionarios_or_empresas:
        descricao = f"Horário padrão do funcionário {f.get('id', f.get('registro_id', 'unknown'))}"
        horarios.append({"descricao": descricao, "idSituacaoCadastro": 1})

    return horarios


def insert_horarios(horarios):
    """Apenas delega ao insert_horarios do módulo novo (mesma assinatura)."""
    return insert_horarios_new(horarios)
