from lancamento import Lancamento
from categoria import Categoria

class Receita(Lancamento):
    """
    Representa um lançamento de receita.
    """

    def __init__(self, ID_lancamento: int, valor: float, categoria: Categoria, data, descricao: str, forma_pagmto: str):

        super().__init__(ID_lancamento, valor, categoria, data, descricao, forma_pagmto)

        if categoria.tipo != "RECEITA":
            raise TypeError("Receita deve estar associada a uma categoria de RECEITA.")

