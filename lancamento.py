class Lancamento:
    """
    Classe base para Receitas e Despesas.
    Garante que o ID e a Categoria sejam inicializados.
    """

    def __init__(self, ID_lancamento: int, valor: float, categoria, data, descricao: str, forma_pagmto: str):
        self.ID_lancamento = ID_lancamento
        self.valor = valor
        self.categoria = categoria
        self.data = data
        self.descricao = descricao
        self.forma_pagmto = forma_pagmto