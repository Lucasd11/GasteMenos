from infra.repositorio import RepositorioFinancas
from dominio.categoria import Categoria
from dominio.lancamento import Lancamento
from dominio.receita import Receita
from dominio.despesa import Despesa
from dominio.orcamento_mensal import OrcamentoMensal

class ServicoControleFinancas:
    """
    Coordena as ações, aplica lógica de negócio e gerencia o estado dos objetos
    (categorias, orçamentos). Não sabe como os dados são salvos ou como o usuário interage.
    """

    def __init__(self, orcamentos, categorias_map, repositorio: RepositorioFinancas):
        self.orcamentos = orcamentos
        self.categorias_map = categorias_map
        self.repositorio = repositorio

    def criar_categoria(self, nome, tipo, limite, descricao):
        nova_categoria = Categoria(nome, tipo, limite, descricao)
        self.repositorio.salvar_categoria(nova_categoria)
        return nova_categoria
    
    def registrar_lancamento(self, valor, categoria, data, descricao, pagamento):
        
        if categoria.tipo == "RECEITA":
            novo_lancamento = Receita(valor, categoria, data, descricao, pagamento)

        elif categoria.tipo == "DESPESA":
            novo_lancamento = Despesa(valor, categoria, data, descricao, pagamento)

        else:
            raise ValueError("Categoria inválida.")

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
