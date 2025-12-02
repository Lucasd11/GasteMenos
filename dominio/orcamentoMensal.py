from dominio.receita import Receita
from dominio.despesa import Despesa
from collections import defaultdict

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

    def calcular_total_receitas(self):
        """
        Calcula o total de todas as Receitas no mês.
        """
        total = 0.0

        for lancamento in self.lancamentos:

            if isinstance(lancamento, Receita):
                total += lancamento.valor
        
        return total

    def calcular_total_despesas(self):
        """
        Calcula o total de todas as Despesas no mês.
        """
        total = 0.0

        for lancamento in self.lancamentos:
            # Verifica se o lançamento é uma instância da classe Despesa
            if isinstance(lancamento, Despesa):
                total += lancamento.valor

        return total    

    def calcular_saldo_mensal(self):
        """
        Calcula o saldo mensal.
        """
        receitas = self.calcular_total_receitas()
        despesas = self.calcular_total_despesas()
        saldo = receitas - despesas

        return saldo

    def relatorio_despesas_por_categoria(self):
        """
        Retorna um dicionário com o total de despesas agrupado por nome da Categoria.
        Exemplo: {'Alimentação': 500.0, 'Transporte': 200.0}
        """
        despesas_por_categoria = defaultdict(float)
        
        for lancamento in self.lancamentos:
            # Apenas Despesas devem entrar neste relatório
            if isinstance(lancamento, Despesa):
                nome_categoria = lancamento.categoria.nome
                despesas_por_categoria[nome_categoria] += lancamento.valor
                
        # Converte defaultdict de volta para dict para o retorno
        return dict(despesas_por_categoria)