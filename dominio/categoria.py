class Categoria:
    """
    Gerencia categorias de receita e despesa, definindo atributos como **nome**, 
    **tipo** (`RECEITA` ou `DESPESA`) e o **limite mensal** (para despesas). 
    """

    def __init__(self, ID_categoria: int, nome: str, tipo: str, limite_mensal: float, descricao: str):
        self.__ID_categoria = ID_categoria
        self.__nome = nome
        self.__tipo = tipo.upper()
        self.__limite_mensal = limite_mensal
        self.__descricao = descricao

    @property    
    def ID_categoria(self):
        return self.__ID_categoria

    @property
    def nome(self):
        return self.__nome 
    
    @property
    def tipo(self):
        return self.__tipo 
    
    @property
    def limite_mensal(self):
        return self.__limite_mensal
    
    @property
    def descricao(self):
        return self.__descricao
    
    @nome.setter
    def nome(self, novo_nome):

        if not novo_nome or len(novo_nome.strip()) < 3:
            raise ValueError("O nome da categoria deve ter pelo menos 3 caracteres.")
        
        self.__nome = novo_nome

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

    @descricao.setter
    def descricao(self, nova_descricao: str):

        if len(nova_descricao.strip()) > 100:
            TypeError("A descrição deve ser de no máximo 100 caracteres.")
        
        self.__descricao = nova_descricao
    
