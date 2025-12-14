from dominio.lancamento import Lancamento
from dominio.categoria import Categoria

class Despesa(Lancamento):
    """
    Representa um lançamento de despesa.
    """

    def __init__(self, valor: float, categoria: Categoria, data, descricao: str, forma_pagmto: str):
        if categoria.get_tipo() != "DESPESA":
            raise ValueError("Despesa deve usar categoria do tipo DESPESA.")
        super().__init__(valor, categoria, data, descricao, forma_pagmto)

    def __str__(self):
        return f"[DESPESA] {super().__str__()}"
