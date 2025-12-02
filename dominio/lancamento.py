from dominio.categoria import Categoria
from datetime import date, datetime

class Lancamento:
    """
    Classe base para Receitas e Despesas.
    Garante que o ID e a Categoria sejam inicializados.
    """

    def __init__(self, ID_lancamento: int, valor: float, categoria: Categoria, data: date = date.today(), descricao: str = "", forma_pagmto: str = ""):
        self.__ID_lancamento = ID_lancamento
        self.valor = valor
        self.categoria = categoria
        self.data = data
        self.descricao = descricao
        self.forma_pagmto = forma_pagmto
        
    @property
    def ID(self):
        return self.__ID_lancamento
    
    @property
    def valor(self):
        return self.__valor
    
    @valor.setter
    def valor(self, novo_valor):
        
        if not isinstance(novo_valor, (int, float)):
            raise TypeError("O valor deve ser um número.")
        
        elif novo_valor <= 0:
            raise ValueError("O valor deve ser positivo e maior que zero.")

        self.__valor = float(novo_valor)
    
    @property
    def categoria(self):
        return self.__categoria
    
    @categoria.setter
    def categoria(self, nova_categoria):

        if not isinstance(nova_categoria, Categoria):
            raise TypeError("A categoria de um Lançamento deve ser um objeto da classe Categoria")
        
        self.__categoria = nova_categoria

    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, nova_data):
        
        if not isinstance(nova_data, date):
            raise TypeError("A data de um lançamento deve ser um objeto datetime.date.")
        
        self.__data = nova_data

    @property
    def descricao(self):
        return self.__descricao
    
    @descricao.setter
    def descricao(self, nova_descricao: str):

        if len(nova_descricao) < 1:
            TypeError("Digite algum tipo de descrição!")
        
        elif len(nova_descricao) > 100:
            TypeError("A descrição deve ter, no máximo, 100 dígitos.")

        else:
            self.__descricao = nova_descricao
    
    @property
    def forma_pagmto(self):
        return self.__forma_pagmto

    @forma_pagmto.setter
    def forma_pagmto(self, nova_forma):

        metodos_pagamento = ["DINHEIRO", "DÉBITO", "CRÉDITO", "PIX", "TRANSFERÊNCIA"]

        if not isinstance(nova_forma, str):
            raise TypeError("A forma de pagamento deve ser um objeto string.")
        
        forma_upper = nova_forma.upper()

        if forma_upper not in metodos_pagamento:
            raise ValueError("Forma de pagamento desconhecida.")
        
        self.__forma_pagmto = nova_forma.upper()

    def __str__(self):

        data_formatada = self.data.strftime("%d/%m/%Y")

        return (
            f"ID: {self.__ID_lancamento} | "
            f"Categoria: {self.categoria.nome} | "
            f"Valor: R$ {self.valor:.2f} | "
            f"Data: {data_formatada} | "
            f"Forma de pagamento: {self.forma_pagmto}"
        )
    
    def __repr__(self):
        return f"Lancamento(id={self.ID}, valor={self.valor}, data={self.data}, descricao='{self.descricao}')"

    def __eq__(self, other):
        if not isinstance(other, Lancamento):
            return False
        return self.data == other.data and self.descricao == other.descricao

    def __lt__(self, other):
        if not isinstance(other, Lancamento):
            return NotImplemented
        return self.data < other.data

    def __add__(self, other):
        if type(self) != type(other):
            raise TypeError("Só é possível somar lançamentos do mesmo tipo.")
        return self.valor + other.valor

