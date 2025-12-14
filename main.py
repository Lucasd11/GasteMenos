from dominio.financas import Financas
from datetime import date
from dominio.settings import Configuracoes


FORMAS_PAGAMENTO = ["DINHEIRO", "DEBITO", "CREDITO", "PIX", "TRANSFERENCIA"]


def menu():
    print("\n=== GasteMenos ===")
    print("1 - Criar categoria")
    print("2 - Listar categorias")
    print("3 - Adicionar receita")
    print("4 - Adicionar despesa")
    print("5 - Ver saldo do mês")
    print("6 - Listar alertas")
    print("7 - Relatórios")
    print("8 - Configurações")
    print("0 - Sair")



def escolher_categoria(financas, tipo):
    categorias = [c for c in financas.listar_categorias() if c.get_tipo() == tipo]

    if not categorias:
        print(f"Nenhuma categoria de {tipo} cadastrada.")
        return None

    print(f"\nCategorias de {tipo}:")
    for i, c in enumerate(categorias, start=1):
        print(f"{i} - {c.get_nome()}")

    try:
        idx = int(input("Escolha a categoria: ")) - 1
        return categorias[idx]
    except (ValueError, IndexError):
        print("Categoria inválida.")
        return None


def main():
    financas = Financas()

    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip()

        try:
            # ---------- CATEGORIAS ----------
            if opcao == "1":
                nome = input("Nome da categoria: ").strip()
                escolher_tipo = int(input("1 - RECEITA\n2 - DESPESA\nTipo: : "))
                limite = float(input("Limite mensal (0 se não houver): "))
                descricao = input("Descrição (opcional): ").strip()

                if escolher_tipo == 1:
                    tipo = "RECEITA"

                elif escolher_tipo == 2:
                    tipo = "DESPESA"

                financas.criar_categoria(nome, tipo, limite, descricao)
                print("Categoria criada com sucesso!")

            elif opcao == "2":
                categorias = financas.listar_categorias()
                if not categorias:
                    print("Nenhuma categoria cadastrada.")
                else:
                    print("\nCategorias:")
                    for c in categorias:
                        print(
                            f"- {c.get_nome()} | "
                            f"{c.get_tipo()} | "
                            f"Limite: R$ {c.get_limite_mensal():.2f}"
                        )

            # ---------- RECEITA ----------
            elif opcao == "3":
                categoria = escolher_categoria(financas, "RECEITA")
                if categoria:
                    valor = float(input("Valor da receita: "))
                    descricao = input("Descrição: ").strip()
                    forma = input("Forma (DINHEIRO | DEBITO | CREDITO | PIX | TRANSFERENCIA): ").upper()

                    if forma not in FORMAS_PAGAMENTO:
                        raise ValueError("Forma de pagamento inválida.")

                    financas.adicionar_receita(valor, categoria, date.today(), descricao, forma)
                    print("Receita adicionada com sucesso!")

            # ---------- DESPESA ----------
            elif opcao == "4":
                categoria = escolher_categoria(financas, "DESPESA")
                if categoria:
                    valor = float(input("Valor da despesa: "))
                    descricao = input("Descrição: ").strip()
                    forma = input("Forma (DINHEIRO | DEBITO | CREDITO | PIX | TRANSFERENCIA): ").upper()

                    if forma not in FORMAS_PAGAMENTO:
                        raise ValueError("Forma de pagamento inválida.")

                    financas.adicionar_despesa(valor, categoria, date.today(), descricao, forma)
                    print("Despesa adicionada com sucesso!")

            # ---------- SALDO ----------
            elif opcao == "5":
                saldo = financas.calcular_saldo_mensal()
                print(f"Saldo do mês: R$ {saldo:.2f}")

            # ---------- ALERTAS ----------
            elif opcao == "6":
                alertas = financas.listar_alertas()
                if not alertas:
                    print("Nenhum alerta registrado.")
                else:
                    print("\nAlertas:")
                    for alerta in alertas:
                        print(f"- {alerta}")

            # ---------- RELATÓRIOS ----------
            elif opcao == "7":
                print("\nRELATÓRIOS")

                print("\nDespesas por categoria:")
                for cat, valor in financas.relatorio_despesas_por_categoria().items():
                    print(f"- {cat}: R$ {valor:.2f}")

                print("\nDespesas por forma de pagamento:")
                for forma, valor in financas.relatorio_despesas_por_forma_pagamento().items():
                    print(f"- {forma}: R$ {valor:.2f}")

                print("\nPercentual por categoria:")
                for cat, perc in financas.relatorio_percentual_por_categoria().items():
                    print(f"- {cat}: {perc:.2f}%")

                comp = financas.relatorio_comparativo()
                print("\nComparativo mensal:")
                print(f"Receitas: R$ {comp['total_receitas']:.2f}")
                print(f"Despesas: R$ {comp['total_despesas']:.2f}")
                print(f"Saldo: R$ {comp['saldo']:.2f}")

            elif opcao == "8":
                config = Configuracoes()

                print("\nCONFIGURAÇÕES ATUAIS")
                print(f"1 - Alerta alto valor (R$): {config.alerta_alto_valor()}")
                print(f"2 - Meses do comparativo: {config.meses_comparativo()}")
                print(f"3 - Meta de economia (%): {config.meta_economia()}")
                print("0 - Voltar")

                escolha = input("Escolha o que deseja alterar: ").strip()

                if escolha == "1":
                    novo_valor = float(input("Novo valor para alerta de alto gasto: "))
                    config.set_alerta_alto_valor(novo_valor)
                    print("Configuração atualizada com sucesso!")

                elif escolha == "2":
                    meses = int(input("Novo número de meses para comparativo: "))
                    config.set_meses_comparativo(meses)
                    print("Configuração atualizada com sucesso!")

                elif escolha == "3":
                    percentual = float(input("Nova meta de economia (%): "))
                    config.set_meta_economia(percentual)
                    print("Configuração atualizada com sucesso!")

                elif escolha == "0":
                    pass
                else:
                    print("Opção inválida.")

            elif opcao == "0":
                print("Saindo...")
                break

            else:
                print("Opção inválida!")

        except ValueError as e:
            print(f"Erro: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")


if __name__ == "__main__":
    main()
