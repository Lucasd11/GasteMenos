import json
import os
from datetime import date, datetime
from dominio.categoria import Categoria
from dominio.lancamento import Lancamento

class RepositorioFinancas:
    """
    Responsável unicamente por salvar e carregar dados do disco.
    """
    
    # Define os caminhos dos arquivos
    CATEGORIAS_FILE = "categorias.json"
    LANCAMENTOS_FILE = "lancamentos.json"

    @staticmethod
    def _to_dict(obj):
        """
        Converte um objeto Categoria ou Lançamento em um dicionário.
        """

        if isinstance(obj, date):
            return obj.isoformat() # Coverte datas para string ISO
        
        if hasattr(obj, '__dict__'):
            # Cria um dicionário a partir dos atributos internos (privados)
            data = {}

            for key, value in obj.__dict__.items():
                # Remove o prefixo privado '__NomeClasse' para facilitar a leitura
                new_key = key.split('-')[-1]
                data[new_key] = RepositorioFinancas._to_dict(value)

            return data

        return obj
    
    