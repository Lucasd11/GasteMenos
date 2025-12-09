from dominio.receita import Receita
from dominio.despesa import Despesa
from collections import defaultdict
from typing import List, Dict, Union

class OrcamentoMensal:
    """
    Classe auxiliar responsável por agrupar todos os Lancamentos de um mês específico, 
    calculando o total de receitas, total de despesas e o saldo disponível.
    Também verifica o excesso de limite das categorias.
    """

    def __init__(self, ano: int, mes: int, prev_receita: float = 0.0, lancamentos: List[Union[Receita, Despesa]] = None, meta_economia: float = 0.0):
        self.__ano = ano
        self.__mes = mes
        self.__prev_receita = prev_receita
        self.__lancamentos = lancamentos or []
        self.__meta_economia = meta_economia

    # --- Métodos de Controle ---
    
    def inserir_lancamento(self, lancamento: Union[Receita, Despesa]):
        """Adiciona um lançamento à lista do orçamento."""
        self.__lancamentos.append(lancamento)

    # --- Métodos de Cálculo ---

    def calcular_total_receitas(self) -> float:
        """Calcula a soma total das receitas do mês."""
        total = 0.0
        for lancamento in self.__lancamentos:
            if isinstance(lancamento, Receita):
                total += lancamento.valor
        return total

    def calcular_total_despesas(self) -> float:
        """Calcula a soma total das despesas do mês."""
        total = 0.0
        for lancamento in self.__lancamentos:
            if isinstance(lancamento, Despesa):
                total += lancamento.valor
        return total

    def calcular_saldo(self) -> float:
        """
        Calcula o saldo disponível: Total de Receitas - Total de Despesas.
        (Ajustado o nome do método para padronização)
        """
        receitas = self.calcular_total_receitas()
        despesas = self.calcular_total_despesas()
        return receitas - despesas

    # --- Métodos de Relatório e Regra de Negócio ---

    def _agrupar_despesas_por_categoria(self) -> Dict[str, float]:
        """
        Método auxiliar que agrupa as despesas totais por nome da categoria.
        Útil para relatórios e verificação de limites.
        """
        despesas_por_categoria = defaultdict(float)
        for lancamento in self.__lancamentos:
            if isinstance(lancamento, Despesa):
                chave_categoria = lancamento.categoria.ID
                despesas_por_categoria[chave_categoria] += lancamento.valor
        return dict(despesas_por_categoria)

    def relatorio_despesas_por_categoria(self) -> Dict[str, float]:
        """Gera um relatório das despesas totais por nome da categoria."""
        # Retorna um mapa mais legível para o relatório (nome da categoria e total)
        mapa_por_id = self._agrupar_despesas_por_categoria()
        
        relatorio = {}
        for lancamento in self.__lancamentos:
            if lancamento.categoria.ID in mapa_por_id:
                 relatorio[lancamento.categoria.nome] = mapa_por_id[lancamento.categoria.ID]
                 
        return relatorio
        
    def verificar_limite_categoria(self, categoria_id: str) -> Dict[str, float]:
        """
        🚨 IMPLEMENTAÇÃO FALTANTE DA SEMANA 4.
        Verifica se o total acumulado de despesas em uma categoria excedeu o limite.
        
        Retorna: Um dicionário com o total gasto e o limite, ou um dicionário vazio se não for excedido.
        """
        
        # 1. Obter o total gasto acumulado para a categoria
        despesas_acumuladas = self._agrupar_despesas_por_categoria()
        gasto_total = despesas_acumuladas.get(categoria_id, 0.0)
        
        # 2. Encontrar a Categoria (precisamos iterar sobre os lançamentos para achar o objeto Categoria)
        categoria_obj = None
        for lancamento in self.__lancamentos:
            if lancamento.categoria.ID == categoria_id:
                categoria_obj = lancamento.categoria
                break
        
        # Se a categoria não for encontrada ou não for de despesa, não há verificação de limite
        if categoria_obj is None or categoria_obj.tipo != "DESPESA":
             return {}
             
        limite = categoria_obj.limite_mensal
        
        # 3. Comparar
        if limite > 0 and gasto_total > limite:
            # Limite excedido! O ServicoControleFinancas usará esta informação para gerar um Alerta.
            return {
                "categoria_nome": categoria_obj.nome,
                "limite": limite,
                "gasto_total": gasto_total,
                "excedido_por": gasto_total - limite
            }
            
        return {} # Retorna vazio se o limite não for excedido ou se não houver limite