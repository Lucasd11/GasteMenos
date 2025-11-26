class RepositorioFinancas:
    """Responsável unicamente por salvar e carregar dados do disco."""
    
    def __init__(self, tipo_persistencia: str):
        self.tipo_persistencia = tipo_persistencia
    
    def carregar_tudo(self):
        pass
        
    def salvar_tudo(self):
        pass