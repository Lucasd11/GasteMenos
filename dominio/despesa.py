from .lancamento import Lancamento
from .categoria import Categoria
from datetime import date

class Despesa(Lancamento):
    """
    Representa um lançamento de despesa.
    """

    def __init__(self, ID_lancamento: int, valor: float, categoria: Categoria, data, descricao: str, forma_pagmto: str):
        
        super().__init__(ID_lancamento, valor, categoria, data, descricao, forma_pagmto)

        if categoria.tipo != "DESPESA":
            raise TypeError("Despesa deve estar associada a uma categoria de DESPESA.")


