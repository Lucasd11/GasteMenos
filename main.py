from dominio.financas import Financas
from datetime import date


def menu():
    print("\n=== GasteMenos ===")
    print("1 - Criar categoria")
    print("2 - Listar categorias")
    print("3 - Adicionar receita")
    print("4 - Adicionar despesa")
    print("5 - Ver saldo do mês")
    print("6 - Listar alertas")
    print("0 - Sair")


def escolher_categoria(financas, tipo):
    categorias = [
        c for c in financas.listar_categorias()
        if c.get_tipo() == tipo
    ]

    if not categorias:
        print(f"Nenhuma categoria de {tipo} cadastrada.")
        return None

    print(f"\nCategorias de {tipo}:")
    for i, c in enumerate(categorias):
        print(f"{i + 1} - {c.get_nome()}")

    idx = int(input("Escolha a categoria: ")) - 1
    return categorias[idx]


def main():
    financas = Financas()

    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip()

        try:
            # ---------- CATEGORIAS ----------
            if opcao == "1":
                nome = input("Nome da categoria: ").strip()
                tipo = input("Tipo (RECEITA ou DESPESA): ").strip().upper()
                limite = float(input("Limite mensal (0 se não houver): "))
                descricao = input("Descrição (opcional): ").strip()

                financas.criar_categoria(nome, tipo, limite, descricao)
                print("Categoria criada com sucesso!")

            elif opcao == "2":
                categorias = financas.listar_categorias()
                if not categorias:
                    print("Nenhuma categoria cadastrada.")
                else:
                    for c in categorias:
                        print(
                            f"- {c.get_nome()} | "
                            f"Tipo: {c.get_tipo()} | "
                            f"Limite: R$ {c.get_limite_mensal():.2f}"
                        )

            # ---------- RECEITA ----------
            elif opcao == "3":
                categoria = escolher_categoria(financas, "RECEITA")
                if categoria:
                    valor = float(input("Valor da receita: "))
                    descricao = input("Descrição: ")
                    financas.adicionar_receita(valor, categoria, date.today(), descricao)
                    print("Receita adicionada!")

            # ---------- DESPESA ----------
            elif opcao == "4":
                categoria = escolher_categoria(financas, "DESPESA")
                if categoria:
                    valor = float(input("Valor da despesa: "))
                    descricao = input("Descrição: ")
                    financas.adicionar_despesa(valor, categoria, date.today(), descricao)
                    print("Despesa adicionada!")

            # ---------- SALDO ----------
            elif opcao == "5":
                saldo = financas.obter_saldo()
                print(f"Saldo do mês: R$ {saldo:.2f}")

            # ---------- ALERTAS ----------
            elif opcao == "6":
                alertas = financas.listar_alertas()
                if not alertas:
                    print("Nenhum alerta registrado.")
                else:
                    print("\nAlertas:")
                    for a in alertas:
                        print(f"- {a}")

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
