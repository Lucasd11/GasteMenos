from dominio.categoria import Categoria
from datetime import date
import uuid

class Lancamento:
    """
    Classe base para Receitas e Despesas.
    """

    def __init__(self, valor: float, categoria: Categoria,
                 data: date = date.today(), descricao: str = "", forma_pagmto: str = ""):
        self.__id_lancamento = str(uuid.uuid4())
        self.categoria = categoria
        self.valor = valor
        self.data = data
        self.descricao = descricao
        self.forma_pagmto = forma_pagmto

    # ===== ID (somente leitura) =====
    @property
    def ID(self):
        return self.__id_lancamento

    # ===== VALOR =====
    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, novo_valor):
        if not isinstance(novo_valor, (int, float)):
            raise TypeError("O valor deve ser numérico.")
        if novo_valor <= 0:
            raise ValueError("O valor deve ser maior que zero.")
        self.__valor = float(novo_valor)

    # ===== CATEGORIA =====
    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, nova_categoria):
        if not isinstance(nova_categoria, Categoria):
            raise TypeError("Categoria inválida.")
        self.__categoria = nova_categoria

    # ===== DATA =====
    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, nova_data):
        if not isinstance(nova_data, date):
            raise TypeError("A data deve ser do tipo datetime.date.")
        self.__data = nova_data

    # ===== DESCRIÇÃO =====
    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, nova_descricao):
        if not isinstance(nova_descricao, str):
            raise TypeError("Descrição inválida.")
        self.__descricao = nova_descricao.strip()

    # ===== FORMA DE PAGAMENTO =====
    @property
    def forma_pagmto(self):
        return self.__forma_pagmto

    @forma_pagmto.setter
    def forma_pagmto(self, nova_forma):
        metodos = ["DINHEIRO", "DEBITO", "CREDITO", "PIX", "TRANSFERENCIA"]
        if not isinstance(nova_forma, str):
            raise TypeError("Forma de pagamento inválida.")
        forma = nova_forma.upper()
        if forma not in metodos:
            raise ValueError("Forma de pagamento desconhecida.")
        self.__forma_pagmto = forma

    # ===== TIPO =====
    @property
    def tipo(self):
        return self.categoria.get_tipo()

    # ===== MÉTODOS ESPECIAIS =====
    def __str__(self):
        data_fmt = self.data.strftime("%d/%m/%Y")
        return (
            f"ID: {self.ID} | Tipo: {self.tipo} | "
            f"Categoria: {self.categoria.get_nome()} | "
            f"Valor: R$ {self.valor:.2f} | Data: {data_fmt}"
        )

    def __repr__(self):
        return f"Lancamento(id={self.ID}, valor={self.valor})"

    def __eq__(self, other):
        if not isinstance(other, Lancamento):
            return False
        return self.ID == other.ID or (
            self.data == other.data and self.descricao == other.descricao
        )

    def __lt__(self, other):
        if not isinstance(other, Lancamento):
            return NotImplemented
        return (self.data, self.valor) < (other.data, other.valor)

    def __add__(self, other):
        if type(self) != type(other):
            raise TypeError("Só é possível somar lançamentos do mesmo tipo.")
        return self.valor + other.valor
