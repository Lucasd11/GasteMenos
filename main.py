from infra.repositorio import RepositorioFinancas
from dominio.orcamento_mensal import OrcamentoMensal
from dominio.financas import ServicoControleFinancas
from datetime import date


def listar_categorias_e_obter_escolha(categorias_disponiveis, tipo_lancamento):
    """Filtra e lista categorias e retorna a categoria escolhida."""
    print(f"\n--- Categorias de {tipo_lancamento} ---")
    
    # Filtra categorias pelo tipo
    categorias_validas = [
        c for c in categorias_disponiveis.values() 
        if c.tipo == tipo_lancamento
    ]

    if not categorias_validas:
        print(f"Nenhuma categoria de {tipo_lancamento} cadastrada.")
        return None

    # Exibe as categorias com um índice
    for i, cat in enumerate(categorias_validas):
        limite_info = f" (Limite R$ {cat.limite_mensal:.2f})" if cat.tipo == "DESPESA" else ""
        print(f"{i + 1} - {cat.nome}{limite_info}")
    
    while True:
        try:
            escolha = int(input(f"Selecione a categoria (1 a {len(categorias_validas)}): "))
            if 1 <= escolha <= len(categorias_validas):
                return categorias_validas[escolha - 1]
            else:
                print("Escolha inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

if __name__ == '__main__':
    
    repo = RepositorioFinancas()
    # Carregar categorias deve ser feito uma vez para manter a lista
    categorias_map = repo.carregar_categorias()
    lancamentos = repo.carregar_lancamentos()

    orcamentos = {}
    for i in lancamentos:
        chave = i.data.strftime("%Y-%m")
        if chave not in orcamentos:
            orcamentos[chave] = OrcamentoMensal(i.data.year, i.data.month)
        orcamentos[chave].inserir_lancamento(i)

    servico = ServicoControleFinancas(orcamentos, categorias_map, repo)

    while True:
        print("\n==========GasteMenos==========\n"
              "Criar categoria - 1\n"
              "Inserir lançamento - 2\n"
              "Ver Relatório Mensal - 3\n"
              "Sair - 0"
              )
        
        try:
            opcao = int(input("Opção: "))
        except ValueError:
            print("Opção inválida. Digite um número.")
            continue

        if opcao == 0:
            print("Saindo do sistema.")
            break
            
        elif opcao == 1:
            print("==========Nova Categoria==========\n")
            nome = str(input("Nome: "))
            
            # Garante que o tipo seja "RECEITA" ou "DESPESA"
            while True:
                tipo_input = input(" | Receita - 1 |\n | Despesa - 2 |\nTipo: ")
                if tipo_input == '1':
                    tipo = "RECEITA"
                    limite = 0.0 
                    break
                elif tipo_input == '2':
                    tipo = "DESPESA"
                    while True:
                        try:
                            limite = float(input("Limite mensal (0 para sem limite): "))
                            break
                        except ValueError:
                            print("Valor de limite inválido.")
                    break
                else:
                    print("Opção de tipo inválida.")

            descricao = str(input("Descrição (opcional): "))
            
            try:

                servico.criar_categoria(nome, tipo, limite, descricao)
                print(f"Categoria '{nome}' ({tipo}) criada com sucesso!")
            except Exception as e:
                print(f"Erro ao criar categoria: {e}")

        
        elif opcao == 2:
            print("==========Novo Lançamento==========\n")
            
            # 1. Escolher tipo de lançamento
            while True:
                tipo_lancamento_input = input("Tipo de Lançamento (Receita - 1 / Despesa - 2): ")
                if tipo_lancamento_input == '1':
                    tipo_lancamento = "RECEITA"
                    break
                elif tipo_lancamento_input == '2':
                    tipo_lancamento = "DESPESA"
                    break
                else:
                    print("Opção inválida.")
            
            while True:
                try:
                    valor = float(input("Valor do Lançamento: "))
                    if tipo_lancamento == "DESPESA" and valor <= 0:
                        print("Despesas não podem ter valor menor ou igual a zero. ")
                        continue
                    break
                except ValueError:
                    print("Valor inválido. Use números.")

            data_hoje = date.today()
            data = data_hoje # Simplificado: usa data de hoje. Poderia pedir input formatado.
            
            # 4. Selecionar Categoria
            categoria_escolhida = listar_categorias_e_obter_escolha(categorias_map, tipo_lancamento)
            if not categoria_escolhida:
                continue

            # 5. Coletar detalhes
            descricao = str(input("Descrição: "))
            
            # Opções de forma de pagamento
            formas_pagamento = ["dinheiro", "débito", "crédito", "PIX"]
            print("\n--- Forma de Pagamento ---")
            for i, fp in enumerate(formas_pagamento):
                print(f"{i + 1} - {fp}")
            
            while True:
                try:
                    fp_input = int(input(f"Selecione a forma de pagamento (1 a {len(formas_pagamento)}): "))
                    if 1 <= fp_input <= len(formas_pagamento):
                        forma_pagamento = formas_pagamento[fp_input - 1]
                        break
                    else:
                        print("Escolha inválida.")
                except ValueError:
                    print("Entrada inválida. Digite um número.")
            
            try:

                servico.registrar_lancamento(
                    tipo_lancamento, valor, data, categoria_escolhida, descricao, forma_pagamento
                )
                print(f"\n--- Lançamento de {tipo_lancamento} registrado com sucesso! ---")
                
                # Exibe alertas se houver
                alerta_msg = servico.obter_alertas_atuais(data.year, data.month)
                if alerta_msg:
                    print("\nALERTA(S) REGISTRADO(S):")
                    for msg in alerta_msg:
                        print(f"- {msg}")
                    print("-----------------------------")

            except Exception as e:
                print(f"Erro ao registrar lançamento: {e}")


        elif opcao == 3:

            hoje = date.today()
            chave_mes_atual = hoje.strftime("%Y-%m")
            
            if chave_mes_atual in orcamentos:
                orcamento_atual = orcamentos[chave_mes_atual]
                total_receita = orcamento_atual.calcular_total_receitas()
                total_despesa = orcamento_atual.calcular_total_despesas()
                saldo = orcamento_atual.calcular_saldo()

                print(f"\n========== Relatório Mensal ({chave_mes_atual}) ==========")
                print(f"Total de Receitas: R$ {total_receita:.2f}")
                print(f"Total de Despesas: R$ {total_despesa:.2f}")
                print(f"SALDO DISPONÍVEL: R$ {saldo:.2f}")
                
                if saldo < 0:
                    print("Alerta: Saldo negativo! (Déficit Orçamentário)")
                print("=====================================================")
            else:
                print(f"Nenhum lançamento registrado para o mês {chave_mes_atual}.")


        else:
            print("Opção não implementada. Tente novamente.")