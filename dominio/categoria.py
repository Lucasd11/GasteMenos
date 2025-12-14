import uuid

class Categoria:
    """
    Representa uma categoria de receita ou despesa.
    """

    def __init__(self, nome, tipo, limite_mensal=0.0, descricao="", id=None):
        self._id = id or str(uuid.uuid4())
        self.set_nome(nome)
        self.set_tipo(tipo)
        self.set_limite_mensal(limite_mensal)
        self.set_descricao(descricao)

    # ========= GETTERS =========
    def get_id(self):
        return self._id

    def get_nome(self):
        return self._nome

    def get_tipo(self):
        return self._tipo

    def get_limite_mensal(self):
        return self._limite_mensal

    def get_descricao(self):
        return self._descricao

    # ========= SETTERS =========
    def set_nome(self, nome):
        if not nome or not isinstance(nome, str):
            raise ValueError("Nome da categoria inválido.")
        self._nome = nome

    def set_tipo(self, tipo):
        if tipo not in ("RECEITA", "DESPESA"):
            raise ValueError("Tipo deve ser 'RECEITA' ou 'DESPESA'.")
        self._tipo = tipo

        # Se for receita, não pode ter limite
        if tipo == "RECEITA":
            self._limite_mensal = 0.0

    def set_limite_mensal(self, limite):
        if self._tipo == "RECEITA":
            self._limite_mensal = 0.0
            return

        if limite < 0:
            raise ValueError("Limite mensal não pode ser negativo.")
        self._limite_mensal = limite

    def set_descricao(self, descricao):
        self._descricao = descricao or ""

    # ========= MÉTODOS ESPECIAIS =========
    def __str__(self):
        return f"{self._nome} ({self._tipo}) - Limite: R$ {self._limite_mensal:.2f}"

    def __eq__(self, other):
        if not isinstance(other, Categoria):
            return False
        return self._id == other._id
