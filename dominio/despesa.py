from dominio.lancamento import Lancamento
from dominio.categoria import Categoria
from datetime import date

class Despesa(Lancamento):
    """
    Representa um lançamento de despesa.
    """

    def __init__(self, valor: float, categoria: Categoria, data, descricao: str, forma_pagmto: str):
        
        super().__init__(valor, categoria, data, descricao, forma_pagmto)

        if categoria.tipo != "DESPESA":
            raise TypeError("Despesa deve estar associada a uma categoria de DESPESA.")


