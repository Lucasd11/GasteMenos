class Categoria:
    """
    Gerencia categorias de receita e despesa, definindo atributos como **nome**, 
    **tipo** (`RECEITA` ou `DESPESA`) e o **limite mensal** (para despesas). 
    """

    def __init__(self, ID_categoria: int, nome: str, tipo: str, limite_mensal: float, descricao: str):
        self.ID_categoria = ID_categoria
        self.nome = nome
        self.tipo = tipo
        self.limite_mensal = limite_mensal
        self.descricao = descricao

class Lancamento:
    """
    Classe base para Receitas e Despesas.
    Garante que o ID e a Categoria sejam inicializados.
    """

    def __init__(self, ID_lancamento: int, valor: float, categoria: Categoria, data, descricao: str, forma_pagmto: str):
        self.ID_lancamento = ID_lancamento
        self.valor = valor
        self.categoria = categoria
        self.data = data
        self.descricao = descricao
        self.forma_pagmto = forma_pagmto

class Receita(Lancamento):
    """
    Representa um lançamento de receita.
    """

    def __init__(self):
        pass

class Despesa(Lancamento):
    """
    Representa um lançamento de despesa.
    """

    def __init__(self):
        pass

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

class Relatorio:
    """
    Classe de serviço dedicada a processar os dados financeiros e gerar todas as saídas analíticas e estatísticas, 
    como comparativos mensais e grupos por categoria/pagamento.
    """
    
class Alerta:
    """
    Objeto de suporte utilizado para registrar e representar notificações automáticas do sistema,
    como "limite excedido", "alto valor" ou "déficit orçamentário".
    """

    def __init__(self, tipo: str, mensagem: str, data, referencia: Lancamento):
        self.tipo = tipo
        self.mensagem = mensagem
        self.data = data
        self.referencia = referencia

class SistemaControle:
    """
    O gerenciador central da aplicação. É responsável por orquestrar a persistência (JSON/SQLite), 
    manter as coleções de Categoria e OrcamentoMensal, e servir como ponto de entrada para comandos CLI.
    """

    def __init__(self, categorias: list, orcamentos: list, configuracoes: dict):
        self.categorias = categorias
        self.orcamentos =orcamentos
        self.configuracoes = configuracoes

