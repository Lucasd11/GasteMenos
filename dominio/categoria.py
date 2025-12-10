import uuid
import numbers 

class Categoria:
    """
    Gerencia categorias de receita e despesa, definindo atributos como **nome**, 
    **tipo** (RECEITA ou DESPESA) e o **limite mensal** (para despesas). 
    """

    def __init__(self, ID_categoria, nome: str, tipo: str, limite_mensal: float = 0.0, descricao: str = ""):
        self.__ID_categoria = str(uuid.uuid4())
        self.tipo = tipo 
        self.nome = nome
        self.descricao = descricao
        self.limite_mensal = limite_mensal


    # Getter de ID (não deve ter setter)
    @property
    def ID(self):
        return self.__ID_categoria

    # Getter e Setter de nome
    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, novo_nome):
        if not novo_nome or not isinstance(novo_nome, str) or len(novo_nome.strip()) < 3:
            raise ValueError("O nome da categoria deve ser uma string e ter pelo menos 3 caracteres.")
        
        self.__nome = novo_nome.strip()
    
    # Getter e Setter de tipo (RECEITA ou DESPESA)
    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, novo_tipo):
        if not isinstance(novo_tipo, str):
            raise TypeError("O tipo de categoria deve ser uma string.")
        
        tipo_upper = novo_tipo.upper()

        if tipo_upper not in ("RECEITA", "DESPESA"):
            raise ValueError("Uma categoria deve ser de 'RECEITA' ou 'DESPESA'.")
    
        self.__tipo = tipo_upper

    # Getter e Setter de limite_mensal
    @property
    def limite_mensal(self):
        return self.__limite_mensal
    
    @limite_mensal.setter
    def limite_mensal(self, novo_limite: float):
        
        # Validação de tipo numérico (int/float)
        if not isinstance(novo_limite, numbers.Number):
            raise TypeError("O limite deve ser um valor numérico.")
        
        if novo_limite < 0:
            raise ValueError("O limite mensal não pode ser negativo.")

        if self.__tipo == "RECEITA":
            self.__limite_mensal = 0.0

        elif self.__tipo == "DESPESA":
            self.__limite_mensal = novo_limite
        

    # Getter e Setter de descricao
    @property
    def descricao(self):
        return self.__descricao
    
    @descricao.setter
    def descricao(self, nova_descricao: str):
        if not isinstance(nova_descricao, str):
             raise TypeError("A descrição deve ser uma string.")
             
        if len(nova_descricao.strip()) > 100:
            raise ValueError("A descrição deve ser de no máximo 100 caracteres.")
        
        self.__descricao = nova_descricao.strip()


    def __str__(self):
        limite_info = ""
        if self.tipo == "DESPESA" and self.limite_mensal > 0:
            limite_info = f" | Limite: R$ {self.limite_mensal:.2f}"
            
        return (
            f"Categoria ({self.tipo}) - {self.nome}"
            f"{limite_info}"
            f" (ID: {self.ID})"
        )


    def __repr__(self):
        return (
            f"Categoria(ID='{self.ID}', nome='{self.nome}', tipo='{self.tipo}', "
            f"limite={self.limite_mensal}, descricao='{self.descricao}')"
        )