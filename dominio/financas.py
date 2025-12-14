from dominio.categoria import Categoria
from dominio.receita import Receita
from dominio.despesa import Despesa
from dominio.alerta import Alerta
from dominio.orcamento_mensal import OrcamentoMensal
from infra.repositorio import RepositorioFinancas
from dominio.settings import Configuracoes
from datetime import date
from collections import defaultdict



class Financas:
    """
    Classe de fachada para operações financeiras.
    """

    def __init__(self, ano=None, mes=None):
        self._repo = RepositorioFinancas()
        hoje = date.today()
        self._orcamento = OrcamentoMensal(
            ano or hoje.year,
            mes or hoje.month
        )
        self._alertas = []

    # ---------- CATEGORIAS ----------

    def criar_categoria(self, nome, tipo, limite_mensal=0.0, descricao=""):
        if tipo not in ("RECEITA", "DESPESA"):
            raise ValueError("Tipo de categoria deve ser RECEITA ou DESPESA.")

        for cat in self._repo.listar_categorias():
            if cat.get_nome() == nome and cat.get_tipo() == tipo:
                raise ValueError("Já existe uma categoria com esse nome e tipo.")

        if tipo == "RECEITA":
            limite_mensal = 0.0

        categoria = Categoria(nome, tipo, limite_mensal, descricao)
        self._repo.salvar_categoria(categoria)
        return categoria

    def listar_categorias(self):
        return self._repo.listar_categorias()

    # ---------- LANÇAMENTOS ----------

    def adicionar_receita(self, valor, categoria, data_lanc=None, descricao = "", forma_pagmto = ""):
        receita = Receita(
            valor,
            categoria,
            data_lanc or date.today(),
            descricao,
            forma_pagmto
        )

        self._orcamento.inserir_lancamento(receita)
        self._repo.salvar_lancamento(receita)

        return receita

    def adicionar_despesa(self, valor, categoria, data_lanc = None, descricao = "", forma_pagmto = ""):
        despesa = Despesa(
            valor,
            categoria,
            data_lanc or date.today(),
            descricao,
            forma_pagmto
        )

        self._orcamento.inserir_lancamento(despesa)
        self._repo.salvar_lancamento(despesa)

        if valor > self._config.alerta_alto_valor():

            self._alertas.append(
                Alerta(
                    Alerta.TIPO_ALTO_VALOR,
                    f"Despesa de alto valor registrada: R$ {valor:.2f}"
                )
            )

        resultado = self._orcamento.verificar_limite_categoria(categoria.get_id())
        if resultado:
            self._alertas.append(
                Alerta(
                    Alerta.TIPO_LIMITE_EXCEDIDO,
                    f"Categoria '{resultado['categoria_nome']}' excedeu o limite "
                    f"em R$ {resultado['excedido_por']:.2f}"
                )
            )

        if self._orcamento.calcular_saldo() < 0:
            self._alertas.append(
                Alerta(
                    Alerta.TIPO_SALDO_NEGATIVO,
                    "Saldo mensal negativo detectado."
                )
            )

        return despesa
    
    def relatorio_comparativo(self):
        """
        Retorna um comparativo simples entre receitas e despesas do mês atual.
        """
        return {
            "total_receitas": self._orcamento.calcular_total_receitas(),
            "total_despesas": self._orcamento.calcular_total_despesas(),
            "saldo": self._orcamento.calcular_saldo()
        }
    

    # ---------- CONSULTAS ----------

    def obter_saldo(self):
        return self._orcamento.calcular_saldo()

    def listar_alertas(self):
        return self._alertas
    
    def editar_categoria(self, categoria: Categoria):
        self._repo.atualizar_categoria(categoria)

    def excluir_categoria(self, categoria_id: str):
        self._repo.excluir_categoria(categoria_id)

    def mes_mais_economico(self):
        totais = self._repo.total_despesas_por_mes()
        if not totais:
            return None
        return min(totais, key=totais.get)

    def comparativo_ultimos_meses(self, meses=3):
        dados = self._repo._load_data(self._repo.LANCAMENTOS_FILE)
        resultado = defaultdict(lambda: {"receitas": 0, "despesas": 0})

        for d in dados:
            mes = d["data"][:7]
            if d["tipo"] == "RECEITA":
                resultado[mes]["receitas"] += d["valor"]
            else:
                resultado[mes]["despesas"] += d["valor"]

        meses_ordenados = sorted(resultado.keys(), reverse=True)[:meses]
        return {m: resultado[m] for m in meses_ordenados}

