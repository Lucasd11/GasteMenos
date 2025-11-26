class Categoria:
    """
    Gerencia categorias de receita e despesa, definindo atributos como **nome**, 
    **tipo** (`RECEITA` ou `DESPESA`) e o **limite mensal** (para despesas). 
    """

    def __init__(self, ID_categoria: int, nome: str, tipo: str, limite_mensal: float, descricao: str):
        self.__ID_categoria = ID_categoria
        self.nome = nome
        self.tipo = tipo
        self.limite_mensal = limite_mensal
        self.descricao = descricao

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, novo_nome):

        if not novo_nome or len(novo_nome.strip()) < 3:
            raise ValueError("O nome da categoria deve ter pelo menos 3 caracteres.")
        
        self.__nome = novo_nome 
    
    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, novo_tipo):

        if not isinstance(novo_tipo, str):
            raise TypeError("O tipo de categoria deve ser uma string.")
        
        tipo_upper = novo_tipo.upper()

        if tipo_upper not in ("RECEITA", "DESPESA"):
            raise ValueError("Um categoria deve ser de \"RECEITA\" ou \"DESPESA\".")
    
        self.__tipo = tipo_upper

    @property
    def limite_mensal(self):
        return self.__limite_mensal
    
    @limite_mensal.setter
    def limite_mensal(self, novo_limite):

        if self.__tipo == "RECEITA":
            self.__limite_mensal = 0.0
            return
        
        elif self.__tipo == "DESPESA":
            if not isinstance(novo_limite, (int, float)):
                raise TypeError("O limite deve ser um valor numérico.")
            
            if novo_limite < 0:
                raise ValueError("O limite mensal não pode ser negativo.")

        self.__limite_mensal = novo_limite
    
    @property
    def descricao(self):
        return self.__descricao
    
    @descricao.setter
    def descricao(self, nova_descricao: str):

        if len(nova_descricao.strip()) > 100:
            raise TypeError("A descrição deve ser de no máximo 100 caracteres.")
        
        self.__descricao = nova_descricao

    def __str__(self):

        string_base = (
            f"ID: {self.__ID_categoria} | "
            f"Nome: {self.nome} | "
            f"Tipo: {self.tipo} | "
        )    
        
        string_limite = ""

        if self.tipo == "DESPESA":

            if self.limite_mensal is not None and self.limite_mensal > 0:
                string_limite = f" | Limite mensal: R$ {self.limite_mensal:.2f}"

        string_final = f" | Descrição: {self.descricao}"

        return string_base + string_limite + string_final
        
