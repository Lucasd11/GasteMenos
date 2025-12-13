from dominio.financas import Financas


def menu():
    print("\n=== GasteMenos ===")
    print("1 - Criar categoria")
    print("2 - Listar categorias")
    print("0 - Sair")


def main():
    financas = Financas()

    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome da categoria: ")
            tipo = input("Tipo (RECEITA ou DESPESA): ").upper()
            limite = float(input("Limite mensal (0 se não houver): "))
            descricao = input("Descrição (opcional): ")

            financas.criar_categoria(nome, tipo, limite, descricao)
            print("Categoria criada com sucesso!")

        elif opcao == "2":
            categorias = financas.listar_categorias()

            if not categorias:
                print("Nenhuma categoria cadastrada.")
            else:
                print("\nCategorias cadastradas:")
                for c in categorias:
                    print(
                        f"- {c.get_nome()} | "
                        f"Tipo: {c.get_tipo()} | "
                        f"Limite: {c.get_limite_mensal()}"
                    )

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()