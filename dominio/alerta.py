class Alerta:
    """
    Objeto de suporte utilizado para registrar e representar notificações automáticas do sistema,
    como "limite excedido", "alto valor" ou "déficit orçamentário".
    """

    def __init__(self, tipo: str, mensagem: str, data, referencia):
        self.tipo = tipo
        self.mensagem = mensagem
        self.data = data
        self.referencia = referencia
