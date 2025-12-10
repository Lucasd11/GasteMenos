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
    (categorias, orçamentos). 
    """

    LIMITE_ALTO_VALOR = 500.00 

    def __init__(self, orcamentos, categorias_map, repositorio: RepositorioFinancas):
        self.orcamentos = orcamentos
        self.categorias_map = categorias_map
        self.repositorio = repositorio
        self.alertas = repositorio.carregar_alertas() 

    # --- Métodos de CRUD Básico ---
    
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
        [cite_start]Implementa a atualização automática de saldo e alertas[cite: 82].
        """
        chave_mes = lancamento.data.strftime("%Y-%m")
        orcamento_mensal = self.orcamentos.get(chave_mes)
        
        if orcamento_mensal is None:
            orcamento_mensal = OrcamentoMensal(
                ano = lancamento.data.year,
                mes = lancamento.data.month
            )
            self.orcamentos[chave_mes] = orcamento_mensal

        orcamento_mensal.inserir_lancamento(lancamento)
        self.repositorio.salvar_lancamento(lancamento)
        self.verificar_e_gerar_alertas(lancamento, orcamento_mensal)
        

    def verificar_e_gerar_alertas(self, lancamento: Lancamento, orcamento_mensal: OrcamentoMensal):
        """
        Verifica as três regras de alerta: Alto Valor, Limite Excedido e Saldo Negativo.
        """
        alertas_gerados = []
        
        if isinstance(lancamento, Despesa) and lancamento.valor >= self.LIMITE_ALTO_VALOR:
            mensagem = (f"ALERTA: Despesa de alto valor (R$ {lancamento.valor:.2f}) na categoria "
                        f"'{lancamento.categoria.nome}'. Limite: R$ {self.LIMITE_ALTO_VALOR:.2f}.")
            alerta = Alerta(Alerta.TIPO_ALTO_VALOR, mensagem, lancamento.data)
            alertas_gerados.append(alerta)
            

        if isinstance(lancamento, Despesa) and lancamento.categoria.limite_mensal > 0:
            
            verificacao = orcamento_mensal.verificar_limite_categoria(lancamento.categoria.ID)
            
            if verificacao:
                mensagem = (f"ALERTA: A categoria '{verificacao['categoria_nome']}' excedeu o limite mensal "
                            f"de R$ {verificacao['limite']:.2f}. Gasto total: R$ {verificacao['gasto_total']:.2f}.")
                alerta = Alerta(Alerta.TIPO_LIMITE_EXCEDIDO, mensagem, lancamento.data)
                alertas_gerados.append(alerta)


        saldo_atual = orcamento_mensal.calcular_saldo()
        if saldo_atual < 0:
            mensagem = f"ALERTA: Déficit orçamentário detectado! Saldo atual do mês: R$ {saldo_atual:.2f}."
            alerta = Alerta(Alerta.TIPO_SALDO_NEGATIVO, mensagem, lancamento.data)
            alertas_gerados.append(alerta)
            

        for alerta in alertas_gerados:
            self.repositorio.salvar_alerta(alerta)
            self.alertas.append(alerta)
            
    def obter_alertas_mensais(self, ano: int, mes: int) -> list:
        """Busca e retorna todos os alertas ativos (como strings) para um determinado mês."""
        alertas_mes = [
            str(a) for a in self.alertas 
            if a.data.year == ano and a.data.month == mes
        ]
        return alertas_mes

    def obter_alertas_atuais(self, ano: int, mes: int) -> list:
        """Alias para obter_alertas_mensais, conforme esperado pelo trecho da CLI."""
        return self.obter_alertas_mensais(ano, mes)