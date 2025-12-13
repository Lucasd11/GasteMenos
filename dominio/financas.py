from dominio.categoria import Categoria
from infra.repositorio import RepositorioFinancas


class Financas:
    def __init__(self):
        self._repo = RepositorioFinancas()


    def criar_categoria(self, nome, tipo, limite_mensal=0.0, descricao=""):
        categoria = Categoria(nome, tipo, limite_mensal, descricao)
        self._repo.salvar_categoria(categoria)
        return categoria


    def listar_categorias(self):
        return self._repo.listar_categorias()