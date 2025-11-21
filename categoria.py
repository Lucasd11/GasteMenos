class Categoria:
    """
    Gerencia categorias de receita e despesa, definindo atributos como **nome**, 
    **tipo** (`RECEITA` ou `DESPESA`) e o **limite mensal** (para despesas). 
    """

    def __init__(self, ID_categoria: int, nome: str, limite_mensal: float, descricao: str):
        self.ID_categoria = ID_categoria
        self.nome = nome
        self.limite_mensal = limite_mensal
        self.descricao = descricao
