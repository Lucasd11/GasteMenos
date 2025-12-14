from dominio.lancamento import Lancamento
from dominio.categoria import Categoria

class Receita(Lancamento):
    """
    Representa um lançamento de receita.
    """

    def __init__(self, valor: float, categoria: Categoria, data, descricao: str, forma_pagmto: str):
        if categoria.get_tipo() != "RECEITA":
            raise ValueError("Receita deve usar categoria do tipo RECEITA.")
        super().__init__(valor, categoria, data, descricao, forma_pagmto)

    def __str__(self):
        return f"[RECEITA] {super().__str__()}"
