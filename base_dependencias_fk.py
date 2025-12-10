"""
Mapa de Dependências de Foreign Keys
=====================================

Esta classe centraliza o mapeamento completo de dependências entre tabelas do banco de dados,
organizadas por níveis hierárquicos para garantir ordem correta em operações que dependem de FKs.

Uso básico:
    from base_dependencias_fk import DependenciasFK
    
    # Obter mapa completo
    mapa = DependenciasFK.MAPA_DEPENDENCIAS
    
    # Obter tabelas de um nível específico
    tabelas_base = DependenciasFK.MAPA_DEPENDENCIAS['nivel_0']
    
    # Usar o cache reverso (tabela → nível)
    nivel = DependenciasFK.CACHE_REVERSO.get('politicaHorario')  # retorna 'nivel_3'

Organização:
    - nivel_0: Tabelas base sem dependências (podem ser inseridas/deletadas livremente)
    - nivel_1: Dependem apenas de nível 0
    - nivel_2: Dependem de níveis 0 e 1
    - nivel_3: Dependem de níveis 0, 1 e 2
    - nivel_4: Dependem de todos os níveis anteriores
    - nivel_5: Links e relacionamentos finais (maior dependência)

Autor: Sistema de Migração
Versão: 1.0
Data: 2025-11-17
"""


class DependenciasFK:
    """
    Mapa completo de dependências de Foreign Keys entre tabelas.
    
    Use este mapa para:
    - Ordenar operações de INSERT (nivel_0 → nivel_5)
    - Ordenar operações de DELETE (nivel_5 → nivel_0)
    - Validar ordem de criação/drop de tabelas
    - Planejar migrações de dados
    """
    
    # Mapa principal: nível → lista de tabelas
    MAPA_DEPENDENCIAS = {
        # NIVEL 0: Tabelas base sem dependências de FK
        'nivel_0': [
            'situacaoCadastro', 'estadoCivil', 'tipoDocumentoCadastro', 'sitEmpresa',
            'temaSistema', 'perfilUsuario', 'linguagemSistema', 'permissao',
            'tipoFuncionario', 'sinalGmt', 'modeloEquipDixi', 'tipoBiometria',
            'menu', 'tipoDocumentoEmpresa', 'feriado', 'datasys', 'tpOrigemMarcacao',
            'tipoCampo', 'tipoCampoExpo', 'tipoDiaExtra', 'tipoCampoMascara',
            'tipoPesquisaCampo', 'tipoValidacao', 'tipoValorPadrao', 'tipoMascara',
            'departamento', 'cargo', 'motivoAfastamento', 'planoContas', 'centroCusto',
            'tipoProcesso', 'tipoControleExtra', 'tipoDiaCompensacao', 'statusTarefa',
            'sentidoComando', 'itemAgendamento', 'delimitadorExpo', 'tipoAgrupExpo',
            'tipoCargaHoraria', 'periodoGrafico', 'origemHorarioDia', 'tipoPercentualExtra',
            'tipoImagemTabela', 'tpDiaEscala', 'tipoDiponibilidade',
            'eventoDebitoCompensacao', 'eventoCreditoCompensacao', 'sitProcessoExpo',
            'tipoListaProc', 'modoConexaoEquip', 'sitConexao', 'tipoTolerancia',
            'tipoRegistroAfd', 'tipoAlertaEmailEquipDixi', 'regone', 'usuarioAdminsChat',
            'dashboard', 'tipoValorEspelho', 'comandoDixi'
        ],
        
        # NIVEL 1: Dependem apenas de nível 0
        'nivel_1': [
            'gmt',                      # FK: sinalGmt
            'funcionario',              # FK: estadoCivil, situacaoCadastro
            'empresa',                  # FK: tipoDocumentoCadastro, sitEmpresa
            'usuario',                  # FK: perfilUsuario, linguagemSistema, situacaoCadastro, temaSistema
            'detalhePermissao',         # FK: permissao
            'biometriaModeloEquipDixi', # FK: modeloEquipDixi, tipoBiometria
            'cargaHoraria',             # FK: tipoCargaHoraria
            'justificativa',            # FK: situacaoCadastro
            'afastamento',              # FK: motivoAfastamento
            'layoutExpo',               # FK: delimitadorExpo, tipoAgrupExpo
            'grupoMenu',                # FK: menu
            'grupoPermissao',           # Base
            'tabela',                   # FK: perfilUsuario, tipoProcesso, tipoImagemTabela
            'afd',                      # Base
            'valoresDashboard',         # FK: dashboard
            'horario',                  # Base
            'periodos',                 # Base
            'politicaExtra'             # Base
        ],
        
        # NIVEL 2: Dependem de níveis 0 e 1
        'nivel_2': [
            'registroFuncionario',      # FK: empresa, tipoFuncionario, gmt, funcionario, situacaoCadastro
            'afdMobile',                # FK: empresa
            'equipDixi',                # FK: empresa, gmt, modeloEquipDixi, modoConexaoEquip, situacaoCadastro, tipoBiometria
            'permissaoUsuario',         # FK: detalhePermissao, usuario
            'grupoDetalhePermissao',    # FK: grupoPermissao, detalhePermissao
            'itemMenu',                 # FK: menu, grupoMenu
            'campoExpo',                # FK: tipoCampoExpo
            'formatoOcorrenciaExpo',    # FK: campoExpo, layoutExpo
            'formatoGeralExpo',         # FK: campoExpo, layoutExpo
            'politica',                 # FK: cargaHoraria
            'abas',                     # FK: tabela
            'campo',                    # FK: perfilUsuario, tabela, tipoCampo, tipoValidacao, tipoMascara, tipoValorPadrao, tipoPesquisaCampo
            'tabelasCascata',           # FK: perfilUsuario, tabela
            'tarefaDixi',               # FK: comandoDixi, usuario, statusTarefa
            'afastamentoFuncionario',   # FK: afastamento, registroFuncionario
            'documentoEmpresa'          # FK: empresa, tipoDocumentoEmpresa
        ],
        
        # NIVEL 3: Dependem de níveis anteriores (0, 1, 2)
        'nivel_3': [
            'politicaHorario',          # FK: horario (nivel_1), politica (nivel_2)
            'marcacao',                 # FK: registroFuncionario, tpOrigemMarcacao
            'lancamentoContas',         # FK: registroFuncionario, planoContas
            'horarioDia',               # FK: tpDiaEscala, registroFuncionario, origemHorarioDia, horario
            'tipoDiaFuncionario',       # FK: registroFuncionario, tpDiaEscala
            'horFuncDia',               # FK: horario, registroFuncionario
            'feriadoFunc',              # FK: registroFuncionario, feriado
            'cargoFunc',                # FK: cargo, registroFuncionario
            'dptoFunc',                 # FK: departamento, registroFuncionario
            'linhasAFD',                # FK: afd
            'linhaAfd',                 # FK: afdMobile, tipoRegistroAfd
            'statusEquipDixi',          # FK: equipDixi, sitConexao
            'tarefaEquipDixi',          # FK: tarefaDixi, equipDixi, statusTarefa
            'campoComFK',               # FK: tabela, campo
            'permissaoMobileMenu',      # FK: permissaoMobile, itemMenu
            'registroPermissaoMobile',  # FK: funcionario, permissaoMobile
            'linhaRepDixi',             # FK: equipDixi
            'lancOcorrJustificativa',   # FK: lancamentoContas
            'lancamentoDsr',            # FK: lancamentoContasDsr, lancamentoContasComposicao
            'politicaExtraHorario',     # FK: horario, politicaExtra
            'cargaHorario'              # FK: horario
        ],
        
        # NIVEL 4: Dependem de todos os níveis anteriores
        'nivel_4': [
            'marcacaoAFD',              # FK: afd, linhasAFD
            'marcacaoRepDixi',          # FK: linhaRepDixi
            'tarefaEquipDixiRegistros', # FK: tarefaEquipDixi
            'lancamentoContasJust'      # FK: justificativa, lancOcorrJustificativa, lancamentoContas
        ],
        
        # NIVEL 5: Links e relacionamentos finais (maior dependência)
        'nivel_5': [
            'linkMarcacaoAFD',          # FK: marcacaoAFD, marcacao
            'linkRepDixiMarcacao'       # FK: marcacaoRepDixi, marcacao
        ]
    }
    
    # Cache reverso: tabela → nível (para acesso O(1))
    CACHE_REVERSO = None
    
    @classmethod
    def _construir_cache_reverso(cls):
        """Constrói o cache reverso: tabela → nível"""
        if cls.CACHE_REVERSO is None:
            cache = {}
            for nivel, tabelas in cls.MAPA_DEPENDENCIAS.items():
                for tabela in tabelas:
                    cache[tabela] = nivel
            cls.CACHE_REVERSO = cache
        return cls.CACHE_REVERSO
    
    @classmethod
    def obter_nivel(cls, tabela):
        """
        Retorna o nível de dependência de uma tabela.
        
        Args:
            tabela (str): Nome da tabela
            
        Returns:
            str: Nível da tabela ('nivel_0' a 'nivel_5') ou None se não encontrada
        """
        if cls.CACHE_REVERSO is None:
            cls._construir_cache_reverso()
        return cls.CACHE_REVERSO.get(tabela)
    
    @classmethod
    def obter_estatisticas(cls):
        """
        Retorna estatísticas do mapeamento.
        
        Returns:
            dict: Quantidade de tabelas por nível
        """
        stats = {}
        for nivel, tabelas in cls.MAPA_DEPENDENCIAS.items():
            stats[nivel] = len(tabelas)
        
        if cls.CACHE_REVERSO is None:
            cls._construir_cache_reverso()
        stats['total'] = len(cls.CACHE_REVERSO)
        
        return stats


# Inicializar cache automaticamente ao importar
DependenciasFK._construir_cache_reverso()


# Exemplo de uso
if __name__ == '__main__':
    print("📊 Mapa de Dependências FK")
    print("=" * 70)
    
    # Estatísticas
    stats = DependenciasFK.obter_estatisticas()
    for nivel, qtd in stats.items():
        print(f"{nivel}: {qtd} tabelas")
    
    print("\n🔍 Exemplos:")
    print("=" * 70)
    
    # Consultar nível de uma tabela
    tabela = 'politicaHorario'
    nivel = DependenciasFK.obter_nivel(tabela)
    print(f"Nível de '{tabela}': {nivel}")
    
    # Obter todas as tabelas de um nível
    tabelas_nivel_0 = DependenciasFK.MAPA_DEPENDENCIAS['nivel_0']
    print(f"\nPrimeiras 5 tabelas do nivel_0: {tabelas_nivel_0[:5]}")
    
    # Verificar se tabela existe no mapa
    tabela_teste = 'empresa'
    existe = tabela_teste in DependenciasFK.CACHE_REVERSO
    print(f"\n'{tabela_teste}' está mapeada? {existe}")
    if existe:
        print(f"  → Nível: {DependenciasFK.obter_nivel(tabela_teste)}")
