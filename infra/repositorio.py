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
    
    def carregar_dados(self, file_path: str):
        """
        Carrega (lê) o conteúdo de um arquivo JSON.
        Retorna uma lista vazia se o arquivo não existir ou estiver vazio.
        """
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Caso o arquivo exista mas esteja corrompido ou mal formado
            print(f"Aviso: Arquivo {file_path} corrompido. Retornando lista vazia.")
            return []
        except Exception as e:
            print(f"Erro ao carregar dados do arquivo {file_path}: {e}")
            return []
        
    def salvar_dados(self, file_path: str, data: list):
        """
        Salva (escreve) uma lista de dicionários no arquivo JSON.
        Usa _to_dict como 'default' para garantir a serialização de objetos customizados.
        """

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                # O default é crucial para serializar objetos customizados (como datas dentro de objetos)
                json.dump(data, f, indent=4, ensure_ascii=False, default=self._to_dict)
        except Exception as e:
            print(f"Erro ao salvar dados no arquivo {file_path}: {e}")

    