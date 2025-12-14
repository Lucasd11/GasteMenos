from dominio.categoria import Categoria
from dominio.receita import Receita
from dominio.despesa import Despesa
from dominio.alerta import Alerta
from dominio.orcamento_mensal import OrcamentoMensal
from infra.repositorio import RepositorioFinancas
from datetime import date


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

    def adicionar_receita(self, valor, categoria, data_lanc=None, descricao="", forma_pagmto="PIX"):
        receita = Receita(
            valor,
            categoria,
            data_lanc or date.today(),
            descricao,
            forma_pagmto
        )
        self._orcamento.inserir_lancamento(receita)
        return receita

    def adicionar_despesa(self, valor, categoria, data_lanc=None, descricao="", forma_pagmto="PIX"):
        despesa = Despesa(
            valor,
            categoria,
            data_lanc or date.today(),
            descricao,
            forma_pagmto
        )
        self._orcamento.inserir_lancamento(despesa)

        # --- ALERTA: ALTO VALOR ---
        if valor > 500:
            self._alertas.append(
                Alerta(
                    Alerta.TIPO_ALTO_VALOR,
                    f"Despesa de alto valor registrada: R$ {valor:.2f}"
                )
            )

        # --- ALERTA: LIMITE EXCEDIDO ---
        resultado = self._orcamento.verificar_limite_categoria(categoria.get_id())
        if resultado:
            self._alertas.append(
                Alerta(
                    Alerta.TIPO_LIMITE_EXCEDIDO,
                    f"Categoria '{resultado['categoria_nome']}' excedeu o limite "
                    f"em R$ {resultado['excedido_por']:.2f}"
                )
            )

        # --- ALERTA: SALDO NEGATIVO ---
        if self._orcamento.calcular_saldo() < 0:
            self._alertas.append(
                Alerta(
                    Alerta.TIPO_SALDO_NEGATIVO,
                    "Saldo mensal negativo detectado."
                )
            )

        return despesa

    # ---------- CONSULTAS ----------

    def obter_saldo(self):
        return self._orcamento.calcular_saldo()

    def listar_alertas(self):
        return self._alertas
