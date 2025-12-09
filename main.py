from infra.repositorio import RepositorioFinancas
from dominio.orcamento_mensal import OrcamentoMensal
from dominio.financas import ServicoControleFinancas
from datetime import date

if __name__ == '__main__':
    
    repo = RepositorioFinancas()
    categorias = repo.carregar_categorias()
    lancamentos = repo.carregar_lancamentos()

    orcamentos = {}
    for i in lancamentos:
        chave = i.data.strftime("%Y-%m")
        if chave not in orcamentos:
            orcamentos[chave] = OrcamentoMensal(i.data.year, i.data.month)
        orcamentos[chave].inserir_lancamento(i)

    servico = ServicoControleFinancas(orcamentos, repo)

    while True:
        print("==========GasteMenos==========\n"
              "Criar categoria - 1\n"
              "Inserir lançamento - 2"
              )
        
        opcao = int(input("Opção: "))

        if opcao == 1:

            print("==========Nova Categoria==========\n")
            nome = str(input("Nome: "))
            tipo = int(input("Receita - 1\n"
                             "Despesa - 2\n"
                             "Tipo: "
                             ))
            if tipo == 2:
                limite = float(input("Limite mensal: "))
            
            descricao = str(input("Descrição: "))

            if tipo == 1:
                tipo = str(tipo)
                tipo = "RECEITA"
            
            elif tipo == 2:
                tipo = str(tipo)
                tipo = "DESPESA"
            

            servico.criar_categoria(1, nome, tipo, limite, descricao)

