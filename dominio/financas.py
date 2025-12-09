from infra.repositorio import RepositorioFinancas
from dominio.categoria import Categoria
from dominio.lancamento import Lancamento
from dominio.receita import Receita
from dominio.despesa import Despesa
from dominio.orcamento_mensal import OrcamentoMensal
from dominio.alerta import Alerta

class ServicoControleFinancas:
    """
    Coordena as ações, aplica lógica de negócio e gerencia o estado dos objetos
    (categorias, orçamentos). Não sabe como os dados são salvos ou como o usuário interage.
    """

    # Valor limite para alerta de alto valor (Regra de Negócio 5)
    LIMITE_ALTO_VALOR = 500.00 

    def __init__(self, orcamentos, categorias_map, repositorio: RepositorioFinancas):
        self.orcamentos = orcamentos
        self.categorias_map = categorias_map
        self.repositorio = repositorio
        self.alertas = repositorio.carregar_alertas() 

    def criar_categoria(self, nome, tipo, limite, descricao):
        nova_categoria = Categoria(nome, tipo, limite, descricao)
        

        self.categorias_map[nova_categoria.ID] = nova_categoria
        
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
        """
        Adiciona o lançamento ao orçamento mensal e salva no repositório.
        Implementa a atualização automática de saldo e alertas (Regra de Negócio 4.4).
        """
        chave_mes = lancamento.data.strftime("%Y-%m")
        orcamento_mensal = self.orcamentos.get(chave_mes)
        

        if orcamento_mensal is None:
            orcamento_mensal = OrcamentoMensal(
                ano=lancamento.data.year,
                mes=lancamento.data.month
            )
            self.orcamentos[chave_mes] = orcamento_mensal

        orcamento_mensal.inserir_lancamento(lancamento)
        self.repositorio.salvar_lancamento(lancamento)
        self.verificar_e_gerar_alertas(lancamento, orcamento_mensal)
        


    def verificar_e_gerar_alertas(self, lancamento: Lancamento, orcamento_mensal: OrcamentoMensal):
        """
        Verifica as três regras de alerta e registra novos objetos Alerta.
        """
        alertas_gerados = []
        

        if isinstance(lancamento, Despesa) and lancamento.valor >= self.LIMITE_ALTO_VALOR:
            mensagem = (f"Despesa de alto valor (R$ {lancamento.valor:.2f}) na categoria "
                        f"'{lancamento.categoria.nome}'. Limite: R$ {self.LIMITE_ALTO_VALOR:.2f}.")
            alerta = Alerta(Alerta.TIPO_ALTO_VALOR, mensagem, lancamento.data)
            alertas_gerados.append(alerta)
            
