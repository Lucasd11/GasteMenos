from dominio.lancamento import Lancamento
from dominio.receita import Receita
from dominio.despesa import Despesa
from collections import defaultdict
from typing import Dict, Union, List


class OrcamentoMensal:
    """
    Classe responsável por agrupar os lançamentos de um mês específico,
    calculando receitas, despesas, saldo e verificando limites por categoria.
    """

    def __init__(
        self,
        ano: int,
        mes: int,
        prev_receita: float = 0.0,
        lancamentos: List[Lancamento] | None = None,
        meta_economia: float = 0.0
    ):
        if mes < 1 or mes > 12:
            raise ValueError("Mês inválido.")
        if ano < 1900:
            raise ValueError("Ano inválido.")

        self.__ano = ano
        self.__mes = mes
        self.__prev_receita = prev_receita
        self.__lancamentos = lancamentos or []
        self.__meta_economia = meta_economia

    # ---------- CONTROLE ----------

    def inserir_lancamento(self, lancamento: Lancamento):
        if not isinstance(lancamento, Lancamento):
            raise TypeError("Objeto inválido.")
        self.__lancamentos.append(lancamento)

    # ---------- CÁLCULOS ----------

    def calcular_total_receitas(self) -> float:
        total = 0.0
        for lancamento in self.__lancamentos:
            if isinstance(lancamento, Receita):
                total += lancamento.valor
        return total

    def calcular_total_despesas(self) -> float:
        total = 0.0
        for lancamento in self.__lancamentos:
            if isinstance(lancamento, Despesa):
                total += lancamento.valor
        return total

    def calcular_saldo(self) -> float:
        return self.calcular_total_receitas() - self.calcular_total_despesas()

    # ---------- RELATÓRIOS ----------

    def _agrupar_despesas_por_categoria(self) -> Dict[str, float]:
        despesas_por_categoria = defaultdict(float)

        for lancamento in self.__lancamentos:
            if isinstance(lancamento, Despesa):
                categoria_id = lancamento.categoria.get_id()
                despesas_por_categoria[categoria_id] += lancamento.valor

        return dict(despesas_por_categoria)

    def relatorio_despesas_por_categoria(self) -> Dict[str, float]:
        mapa_por_id = self._agrupar_despesas_por_categoria()
        relatorio = {}

        for lancamento in self.__lancamentos:
            cat = lancamento.categoria
            cat_id = cat.get_id()

            if cat_id in mapa_por_id:
                relatorio[cat.get_nome()] = mapa_por_id[cat_id]

        return relatorio

    # ---------- REGRAS DE NEGÓCIO ----------

    def verificar_limite_categoria(self, categoria_id: str) -> Dict[str, Union[str, float]]:
        despesas_acumuladas = self._agrupar_despesas_por_categoria()
        gasto_total = despesas_acumuladas.get(categoria_id, 0.0)

        categoria_obj = None
        for lancamento in self.__lancamentos:
            if lancamento.categoria.get_id() == categoria_id:
                categoria_obj = lancamento.categoria
                break

        if categoria_obj is None:
            return {}

        if categoria_obj.get_tipo() != "DESPESA":
            return {}

        limite = categoria_obj.get_limite_mensal()

        if limite > 0 and gasto_total > limite:
            return {
                "categoria_nome": categoria_obj.get_nome(),
                "limite": limite,
                "gasto_total": gasto_total,
                "excedido_por": gasto_total - limite
            }

        return {}

    def relatorio_despesas_por_forma_pagamento(self):
        """
        Retorna o total de despesas agrupadas por forma de pagamento.
        """
        resultado = defaultdict(float)

        for lancamento in self.__lancamentos:
            if isinstance(lancamento, Despesa):
                resultado[lancamento.forma_pagmto] += lancamento.valor

        return dict(resultado)

    def relatorio_percentual_por_categoria(self):
        """
        Retorna o percentual de cada categoria em relação ao total de despesas.
        """
        total_despesas = self.calcular_total_despesas()
        if total_despesas == 0:
            return {}

        despesas_por_categoria = self.relatorio_despesas_por_categoria()
        percentual = {}

        for categoria, valor in despesas_por_categoria.items():
            percentual[categoria] = (valor / total_despesas) * 100

        return percentual
    
    def calcular_saldo_diario(self):
        saldo_por_dia = defaultdict(float)

        for lanc in self.__lancamentos:
            if isinstance(lanc, Receita):
                saldo_por_dia[lanc.data] += lanc.valor
            elif isinstance(lanc, Despesa):
                saldo_por_dia[lanc.data] -= lanc.valor

        return dict(saldo_por_dia)

