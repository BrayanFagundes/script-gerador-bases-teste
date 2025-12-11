import argparse
from config import CONFIG
from database import insert_many, insert_and_get_first_id # <-- IMPORT NOVO- função pega id inicial agora 

from generators.empresa import gerar_empresas, insert_empresas
from generators.funcionario import gerar_funcionarios, insert_funcionarios, gerar_registros, insert_registros
from generators.horario import gerar_horarios, insert_horarios
from generators.marcacao import gerar_marcacoes, insert_marcacoes


def main():
    parser = argparse.ArgumentParser() # Cria o parser que lê argumentos passados pelo terminal, perguuntar se tem outra maneira
    parser.add_argument("--qtd_empresa", type=int, default=CONFIG["qtd_empresa"]) # type=int garante que retorne um número, default usa a config
    parser.add_argument("--qtd_funcionario", type=int, default=CONFIG["qtd_funcionario"])
    parser.add_argument("--dias_marcacao", type=int, default=CONFIG["dias_marcacao"])
    # Aliases plurais compatíveis com versões anteriores / uso comum
    parser.add_argument("--qtd_empresas", type=int, dest="qtd_empresa", help="alias for --qtd_empresa")
    parser.add_argument("--qtd_funcionarios", type=int, dest="qtd_funcionario", help="alias for --qtd_funcionario")
    parser.add_argument("--dias_marcacoes", type=int, dest="dias_marcacao", help="alias for --dias_marcacao")
    parser.add_argument("--dry_run", action="store_true", help="Imprime queries/valores sem executar no banco")
    args = parser.parse_args()

    # Se o usuário solicitou dry_run, ainda assim tentamos abrir uma conexão
    # apenas para exibir qual `database` seria usado (diagnóstico), sem executar inserts.
    if args.dry_run:
        try:
            from database import get_connection
            conn = get_connection()
            # get_connection() já imprime o database conectado; fechamos imediatamente
            conn.close()
        except Exception as e:
            print(f"❌ Aviso: não foi possível abrir conexão para diagnóstico: {e}")

    # --- INSERÇÃO DE empresas ---
    empresas = gerar_empresas(args.qtd_empresa)  # gera empresas fake
    q, v = insert_empresas(empresas)
    if args.dry_run:
        print("-- DRY RUN: insert_empresas")
        print(q)
        print("Exemplo valores:", v[:3])
        primeiro_id_empresa = 1
    else:
        primeiro_id_empresa = insert_and_get_first_id(q, v)

    for i, e in enumerate(empresas):
        e["id"] = primeiro_id_empresa + i

    # --- INSERÇÃO DE FUNCIONÁRIOS ---
    funcionarios = gerar_funcionarios(empresas, args.qtd_funcionario)
    q, v = insert_funcionarios(funcionarios)
    if args.dry_run:
        print("-- DRY RUN: insert_funcionarios")
        print(q)
        print("Exemplo valores:", v[:3])
        primeiro_id_funcionario = primeiro_id_empresa + 1
    else:
        primeiro_id_funcionario = insert_and_get_first_id(q, v)

    for i, f in enumerate(funcionarios):
        f["id"] = primeiro_id_funcionario + i

    # --- INSERÇÃO DE REGISTROS (registroFuncionario) ---
    registros = gerar_registros(funcionarios)
    q, v = insert_registros(registros)
    if args.dry_run:
        print("-- DRY RUN: insert_registros (registroFuncionario)")
        print(q)
        print("Exemplo valores:", v[:3])
        primeiro_id_registro = primeiro_id_funcionario + 1
    else:
        primeiro_id_registro = insert_and_get_first_id(q, v)

    for i, r in enumerate(registros):
        r["id"] = primeiro_id_registro + i
        # vincula o registro ao funcionário correspondente
        funcionarios[i]["registro_id"] = r["id"]

    # --- INSERÇÃO DE HORÁRIOS (opcional) ---
    horarios = gerar_horarios(empresas)
    # Construir query canônica para `horario` (schema do dump)
    q_horario = "INSERT INTO horario (descricao, idSituacaoCadastro) VALUES (%s, %s)"
    v_horario = []
    for h in horarios:
        # Aceita várias formas de saída de geradores (compatibilidade):
        # - dict com 'descricao' and 'idSituacaoCadastro'
        # - dict com 'funcionario_id' (antigo) -> cria descricao a partir do id
        # - tuple/list -> ignora e transforma em descricao simples
        if isinstance(h, dict):
            descricao = h.get("descricao")
            situ = h.get("idSituacaoCadastro")
            if descricao is None:
                # tenta formar a descricao a partir de campos conhecidos
                if "funcionario_id" in h:
                    descricao = f"Horário padrão do funcionário {h.get('funcionario_id') }"
                elif "id" in h:
                    descricao = f"Horário padrão da empresa {h.get('id')}"
                else:
                    descricao = str(h)
            if situ is None:
                situ = 1
            v_horario.append((descricao, situ))
        elif isinstance(h, (list, tuple)):
            # pega primeiro campo como descricao
            descricao = str(h[0]) if len(h) > 0 else "Horario"
            v_horario.append((descricao, 1))
        else:
            v_horario.append((str(h), 1))
    if args.dry_run:
        print("-- DRY RUN: insert_horarios (canônico)")
        print(q_horario)
        print("Exemplo valores:", v_horario[:3])
    else:
        insert_many(q_horario, v_horario)

    # --- INSERÇÃO DE MARCAÇÕES ---
    marcacoes = gerar_marcacoes(registros, args.dias_marcacao, CONFIG["variacao_minutos"])
    # Construir query canônica para `marcacao` (schema do dump)
    q_marc = "INSERT INTO marcacao (idRegistroFuncionario, dataMarcacao, data, hora, idTpOrigemMarcacao, considerar, numeroMarcacao, descricao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    # build map funcionario_id -> registro_id (quando disponível)
    func_to_reg = {f["id"]: f.get("registro_id") for f in funcionarios}

    from datetime import datetime, date, time as timecls

    def to_epoch_datetime(dt):
        if isinstance(dt, int):
            return dt
        if isinstance(dt, datetime):
            return int(dt.timestamp())
        if isinstance(dt, date):
            return int(datetime(dt.year, dt.month, dt.day).timestamp())
        return None

    def to_epoch_time(t):
        if isinstance(t, int):
            return t
        if isinstance(t, timecls):
            # segundos desde meia-noite
            return t.hour * 3600 + t.minute * 60 + getattr(t, "second", 0)
        if isinstance(t, datetime):
            return t.hour * 3600 + t.minute * 60 + t.second
        if isinstance(t, str):
            # tenta parse simples HH:MM[:SS]
            try:
                parts = t.split(":")
                h = int(parts[0])
                m = int(parts[1]) if len(parts) > 1 else 0
                s = int(parts[2]) if len(parts) > 2 else 0
                return h * 3600 + m * 60 + s
            except Exception:
                return 0
        return 0

    v_marc = []
    for m in marcacoes:
        # resolve registro id
        id_reg = m.get("idRegistroFuncionario") or m.get("idRegistro") or m.get("registro_id") or m.get("id") or m.get("funcionario_id")
        # if id_reg refers to funcionario id, map to registro_id
        if id_reg in func_to_reg and func_to_reg[id_reg] is not None:
            # when id_reg is a funcionario id, use mapped registro_id
            mapped = func_to_reg[id_reg]
            id_reg = mapped

        # dataMarcacao: prefer explicit, else compose from data+hora
        data_marc = m.get("dataMarcacao")
        if data_marc is None:
            d = m.get("data")
            h = m.get("hora")
            if isinstance(d, (date, datetime)) and isinstance(h, timecls):
                dtc = datetime(d.year, d.month, d.day, h.hour, h.minute, getattr(h, 'second', 0))
                data_marc = int(dtc.timestamp())
            else:
                data_marc = to_epoch_datetime(d) or 0

        data_field = m.get("data")
        if isinstance(data_field, (date, datetime)):
            data_field = to_epoch_datetime(data_field)

        hora_field = m.get("hora")
        if isinstance(hora_field, timecls):
            hora_field = to_epoch_time(hora_field)

        v_marc.append((
            id_reg,
            data_marc,
            data_field,
            hora_field,
            m.get("idTpOrigemMarcacao", 1),
            m.get("considerar", 1),
            m.get("numeroMarcacao", 1),
            m.get("descricao", "")
        ))
    if args.dry_run:
        print("-- DRY RUN: insert_marcacoes (canônico)")
        print(q_marc)
        print("Exemplo valores:", v_marc[:3])
    else:
        insert_many(q_marc, v_marc)

    print("Processo concluído!")

if __name__ == "__main__":
    main()