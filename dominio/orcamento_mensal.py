from dominio.receita import Receita
from dominio.despesa import Despesa
from collections import defaultdict

class OrcamentoMensal:
    """
    Classe auxiliar responsável por agrupar todos os Lancamentos de um mês específico, 
    calculando o total de receitas, total de despesas e o saldo disponível.
    """

    def __init__(self, ano, mes, prev_receita=0.0, lancamentos=None, meta_economia=0.0):
        self.ano = ano
        self.mes = mes
        self.prev_receita = prev_receita
        self.lancamentos = lancamentos or []
        self.meta_economia = meta_economia

    def inserir_lancamento(self, lancamento):
        self.lancamentos.append(lancamento)

    def calcular_total_receitas(self):
        total = 0.0
        for lancamento in self.lancamentos:
            if isinstance(lancamento, Receita):
                total += lancamento.valor
        return total

    def calcular_total_despesas(self):
        total = 0.0
        for lancamento in self.lancamentos:
            if isinstance(lancamento, Despesa):
                total += lancamento.valor
        return total

    def calcular_saldo_mensal(self):
        receitas = self.calcular_total_receitas()
        despesas = self.calcular_total_despesas()
        return receitas - despesas

    def relatorio_despesas_por_categoria(self):
        despesas_por_categoria = defaultdict(float)
        for lancamento in self.lancamentos:
            if isinstance(lancamento, Despesa):
                nome_categoria = lancamento.categoria.nome
                despesas_por_categoria[nome_categoria] += lancamento.valor
        return dict(despesas_por_categoria)
