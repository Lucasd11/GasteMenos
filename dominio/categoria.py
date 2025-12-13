import uuid

class Categoria:
    def __init__(self, nome, tipo, limite_mensal=0.0, descricao="", id=None):
        self._id = id or str(uuid.uuid4())
        self._nome = nome
        self._tipo = tipo
        self._limite_mensal = limite_mensal
        self._descricao = descricao

    # getters
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


    # setters
    def set_nome(self, nome):
        self._nome = nome


    def set_tipo(self, tipo):
        self._tipo = tipo


    def set_limite_mensal(self, limite):
        self._limite_mensal = limite


    def set_descricao(self, descricao):
        self._descricao = descricao