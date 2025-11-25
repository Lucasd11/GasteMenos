class RepositorioFinancas:
    """Responsável unicamente por salvar e carregar dados do disco."""
    
    def __init__(self, tipo_persistencia: str):
        self.tipo_persistencia = tipo_persistencia # 'JSON' ou 'SQLite'
    
    def carregar_tudo(self):
        # Lógica para ler 'categorias', 'orcamentos', etc., do arquivo/banco
        pass
        
    def salvar_tudo(self):
        # Lógica para escrever tudo no arquivo/banco
        pass