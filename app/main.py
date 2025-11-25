from infra.repositorio import RepositorioFinancas

class ServicoControleFinancas():
    """
        Coordena as ações, aplica lógica de negócio e gerencia o estado dos objetos
        (categorias, orçamentos). Não sabe como os dados são salvos ou como o usuário interage.
        """

    def __init__(self, repositorio: RepositorioFinancas):
        # O repositório é injetado, seguindo o princípio de Inversão de Dependência (DIP)
        pass

if __name__ == '__main__':
    # Bloco principal de execução
    pass