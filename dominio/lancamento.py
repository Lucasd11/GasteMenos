from dominio.categoria import Categoria
from datetime import date
import uuid # Necessário para gerar IDs únicos

class Lancamento:
    """
    Classe base para Receitas e Despesas.
    Garante a inicialização de atributos comuns e implementa métodos especiais e validações.
    """

    def __init__(self, valor: float, categoria: Categoria, data: date = date.today(), descricao: str = "", forma_pagmto: str = ""):
        self.__ID_lancamento = str(uuid.uuid4())
        self.categoria = categoria
        self.valor = valor
        self.data = data
        self.descricao = descricao
        self.forma_pagmto = forma_pagmto
        
    @property
    def ID(self):
        # O ID deve ser somente leitura
        return self.__ID_lancamento
    
    @property
    def valor(self):
        return self.__valor
    
    @valor.setter
    def valor(self, novo_valor):
        
        if not isinstance(novo_valor, (int, float)):
            raise TypeError("O valor deve ser um número.")
        

        if novo_valor <= 0:

            raise ValueError("O valor deve ser positivo e maior que zero.")

        self.__valor = float(novo_valor)
    
    @property
    def categoria(self):
        return self.__categoria
    
    @categoria.setter
    def categoria(self, nova_categoria):

        if not isinstance(nova_categoria, Categoria):
            raise TypeError("A categoria de um Lançamento deve ser um objeto da classe Categoria.")
        
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
        
        if not isinstance(nova_descricao, str):
            raise TypeError("A descrição deve ser uma string.")


        descricao_limpa = nova_descricao.strip()
        
        if len(descricao_limpa) < 1:
            raise ValueError("A descrição não pode ser vazia.")
        
        elif len(descricao_limpa) > 100:
            raise ValueError("A descrição deve ter, no máximo, 100 dígitos.")

        self.__descricao = descricao_limpa
    
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
        
        self.__forma_pagmto = forma_upper


    @property
    def tipo(self):
        """Retorna o tipo de lançamento baseado na categoria."""
        return self.categoria.tipo # Retorna "RECEITA" ou "DESPESA"

    # --- Métodos Especiais ---
    
    def __str__(self):
        """Método __str__: resumo de lançamento."""
        data_formatada = self.data.strftime("%d/%m/%Y")

        return (
            f"ID: {self.ID} | Tipo: {self.tipo} | Categoria: {self.categoria.nome} | "
            f"Valor: R$ {self.valor:.2f} | Data: {data_formatada}"
        )
    
    def __repr__(self):
        """Método __repr__: detalhamento interno."""
        return (
            f"Lancamento(id='{self.ID}', valor={self.valor}, "
            f"categoria='{self.categoria.nome}', data={self.data})"
        )

    def __eq__(self, other):
        """Método __eq__: comparação por ID ou data + descrição."""
        if not isinstance(other, Lancamento):
            return NotImplemented
        

        if self.ID == other.ID:
             return True
             

        return self.data == other.data and self.descricao == other.descricao

    def __lt__(self, other):
        """Método __lt__: ordenação por data ou valor."""
        if not isinstance(other, Lancamento):
            return NotImplemented

        if self.data != other.data:
            return self.data < other.data
        return self.valor < other.valor

    def __add__(self, other):
        """Método __add__: somar receitas/despesas (mesmo tipo).""" 

        if type(self) != type(other):
            raise TypeError("Só é possível somar lançamentos do mesmo tipo (Receita ou Despesa).")
        return self.valor + other.valor