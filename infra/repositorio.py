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
    
    @classmethod
    def salvar_categorias(cls, lista_categorias):
        """
        Salva a lista de objetos Categoria no arquivo JSON.
        """

        data_to_save = [cls._to_dict(c) for c in lista_categorias]

        with open(cls.CATEGORIAS_FILE, 'w', encoding = 'utf-8') as f: # Escreve no arquivo
            json.dump(data_to_save, f, indent = 4, default = cls._to_dict)
    
    @classmethod
    def carregar_categorias(cls):
        """
        Carrega a lista de categorias do arquivo JSON e retorna como objetos.
        """

        if not os.path.exists(cls.CATEGORIAS_FILE):
            return [] # Retorna lista vazia se o arquivo não existir
        
        with open(cls.CATEGORIAS_FILE, 'r', encoding = 'utf-8') as f:
            data = json.load(f)

        categorias = []
        for item in data:
            try:
                categoria = Categoria(
                    item.get('ID_categoria', 0),
                    item.get('nome', ''),
                    item.get('tipo', ''),
                    item.get('limite', None),
                    item.get('descricao', '')
                )
                categorias.append(categoria)
            except NameError:
                # Trata o caso de Categoria não estar importada/definida
                print("ERRO: Classe Categoria não definida para reconstrução do objeto.")
                return []
        
        return categorias