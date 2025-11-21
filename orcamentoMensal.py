class OrcamentoMensal:
    """
    Classe auxiliar responsável por agrupar todos os Lancamentos de um mês específico, 
    calculando o total de receitas, total de despesas e o saldo disponível.
    """

    def __init__(self, mes, prev_receita: float, lancamentos: list, meta_economia: float):
        self.mes = mes
        self.prev_receita = prev_receita
        self.lancamentos = lancamentos
        self.meta_economia = meta_economia