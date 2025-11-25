from categoria import Categoria
from datetime import date, datetime

class Lancamento:
    """
    Classe base para Receitas e Despesas.
    Garante que o ID e a Categoria sejam inicializados.
    """

    def __init__(self, ID_lancamento: int, valor: float, categoria: Categoria, data: date = date.today(), descricao: str = "", forma_pagmto: str = ""):
        self.__ID_lancamento = ID_lancamento
        self.__valor = valor
        self.__categoria = categoria
        self.__data = data
        self.__descricao = descricao
        self.__forma_pagmto = forma_pagmto
        
    @property
    def valor(self):
        return self.__valor
    
    @property
    def categoria(self):
        return self.__categoria
    
    @property
    def data(self):
        return self.__data
    
    @property
    def descricao(self):
        return self.__descricao
    
    @property
    def forma_pagmto(self):
        return self.__forma_pagmto

    @valor.setter
    def valor(self, novo_valor):
        
        if not isinstance(novo_valor, (int, float)):
            raise TypeError("O valor deve ser um número.")
        
        elif novo_valor <= 0:
            raise ValueError("O valor deve ser positivo e maior que zero.")

        self.__valor = float(novo_valor)

    @categoria.setter
    def categoria(self, nova_categoria):

        if not isinstance(nova_categoria, Categoria):
            raise TypeError("A categoria de um Lançamento deve ser um objeto da classe Categoria")
        
        self.__categoria = nova_categoria

    @data.setter
    def data(self, nova_data):
        
        if not isinstance(nova_data, date):
            raise TypeError("A data de um lançamento deve ser um objeto datetime.date.")
        
        self.__data = nova_data

    @descricao.setter
    def descricao(self, nova_descricao: str):

        if len(nova_descricao) < 1:
            TypeError("Digite algum tipo de descrição!")
        
        elif len(nova_descricao) > 100:
            TypeError("A descrição deve ter, no máximo, 100 dígitos.")

        else:
            self.__descricao = nova_descricao

    @forma_pagmto.setter
    def forma_pagmto(self, nova_forma):

        metodos_pagamento = ["dinheiro", "débito", "crédito", "pix", "transferência"]

        if not isinstance(nova_forma, str):
            TypeError("A forma de pagamento deve ser um objeto string.")
        
        elif nova_forma.lower() not in metodos_pagamento:
            TypeError("Forma de pagamento desconhecida.")
        
        else:
            self.__forma_pagmto = nova_forma

    def __str__(self):
        return f"ID: {self.__ID_lancamento} | {self.__categoria.nome} | R$ {self.__valor:,2f}"
    
    def __eq__(self, outro):
        # Comparação por ID ou data + descrição
        if isinstance(outro, Lancamento):
            return self.__ID_lancamento == outro.__ID_lancamento or \
            (self.__data == outro.data and self.descricao == outro.descricao)
        
        return False

