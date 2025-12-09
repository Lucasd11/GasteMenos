from infra.repositorio import RepositorioFinancas
from dominio.categoria import Categoria
from dominio.lancamento import Lancamento
from dominio.orcamento_mensal import OrcamentoMensal

class ServicoControleFinancas:
    """
    Coordena as ações, aplica lógica de negócio e gerencia o estado dos objetos
    (categorias, orçamentos). Não sabe como os dados são salvos ou como o usuário interage.
    """

    def __init__(self, orcamentos, repositorio: RepositorioFinancas):
        self.orcamentos = orcamentos
        self.repositorio = repositorio

    def criar_categoria(self, ID, nome, tipo, limite, descricao):
        nova_categoria = Categoria(ID, nome, tipo, limite, descricao)
        self.repositorio.salvar_categoria(nova_categoria)
        return nova_categoria
    
    def criar_lancamento(self, ID, valor, categoria, data, descricao, pagamento):
        novo_lancamento = Lancamento(ID, valor, categoria, data, descricao, pagamento)
        self.adicionar_lancamento(novo_lancamento)
        return novo_lancamento

    def adicionar_lancamento(self, lancamento: Lancamento):

        chave_mes = lancamento.data.strftime("%Y-%m")
        if chave_mes not in self.orcamentos:
            self.orcamentos[chave_mes] = OrcamentoMensal(
                ano = lancamento.data.year,
                mes = lancamento.data.month
            )

        self.orcamentos[chave_mes].inserir_lancamento(lancamento)

        self.repositorio.salvar_lancamento(lancamento)
    
    def relatorio_mensal(self, ano: int, mes: int):
        chave = f"{ano}-{mes:02d}"
        if chave not in self.orcamentos:
            raise ValueError("Nenhum orçamento encontrado para este mês.")
        o = self.orcamentos[chave]
        return {
            "total_receitas": o.calcular_total_receitas(),
            "total_despesas": o.calcular_total_despesas(),
            "saldo": o.calcular_saldo(),
            "por_categoria": o.relatorio_despesas_por_categoria(),
        }
