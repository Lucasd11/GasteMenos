class SistemaControle():
    """
    O gerenciador central da aplicação. É responsável por orquestrar a persistência (JSON/SQLite), 
    manter as coleções de Categoria e OrcamentoMensal, e servir como ponto de entrada para comandos CLI.
    """

    def __init__(self, categorias: list, orcamentos: list, configuracoes: dict):
        self.categorias = categorias
        self.orcamentos =orcamentos
        self.configuracoes = configuracoes

