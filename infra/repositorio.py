import json
import os
from datetime import date, datetime
from dominio.categoria import Categoria
from dominio.lancamento import Lancamento
from dominio.despesa import Despesa
from dominio.receita import Receita
from dominio.alerta import Alerta


class RepositorioFinancas:
    """
    Responsável unicamente por salvar e carregar dados do disco.
    Implementa o CRUD (Create, Read, Update, Delete) para Categoria e Lançamento.
    """
    
    CATEGORIAS_FILE = "categorias.json"
    LANCAMENTOS_FILE = "lancamentos.json"
    ALERTAS_FILE =  "alertas.json"

    # --- Métodos Auxiliares de JSON (Serialização e Persistência) ---

    @staticmethod
    def _to_dict(obj):
        """
        Converte um objeto Categoria, Lançamento ou Date em um dicionário/string.
        Método 'default' para o json.dump, lidando com objetos customizados.
        """
        if isinstance(obj, date):
            return obj.isoformat()
        
        if hasattr(obj, '__dict__'):
            data = {}

            for key, value in obj.__dict__.items():
                new_key = key.split('_')[-1]
                data[new_key] = RepositorioFinancas._to_dict(value)

            return data

        return obj

    def _load_data(self, file_path: str) -> list:
        """
        Carrega (lê) o conteúdo de um arquivo JSON.
        Retorna uma lista vazia se o arquivo não existir ou estiver vazio/corrompido.
        """
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Aviso: Arquivo {file_path} corrompido. Retornando lista vazia.")
            return []
        except Exception as e:
            print(f"Erro ao carregar dados do arquivo {file_path}: {e}")
            return []

    def _save_data(self, file_path: str, data: list):
        """
        Salva (escreve) uma lista de dicionários no arquivo JSON.
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False, default=self._to_dict)
        except Exception as e:
            print(f"Erro ao salvar dados no arquivo {file_path}: {e}")


    # --- Métodos de Desserialização (Dict -> Objeto) ---

    def _to_categoria(self, data):
        return Categoria(
            ID_categoria=data["categoria"],
            nome=data["nome"],
            tipo=data["tipo"],
            limite_mensal=data["limite_mensal"],
            descricao=data["descricao"]
        )


    def _to_lancamento(self, data: dict) -> Lancamento:
        """
        Converte um dicionário lido do JSON para um objeto Receita ou Despesa, 
        lidando com a Herança e a desserialização de objetos aninhados.
        """

        if 'categoria' in data and isinstance(data['categoria'], dict):
            data['categoria'] = self._to_categoria(data['categoria'])
        
        if 'data' in data and isinstance(data['data'], str):
            try:
                data['data'] = datetime.fromisoformat(data['data']).date()
            except ValueError:
                pass 
        
        if data['categoria'].tipo == "RECEITA":
            return Receita(**data)
        else:
            return Despesa(**data)
    
    def _to_alerta(self, data: dict):
        
        if 'categoria' in data and isinstance(data['categoria', dict]):
            data['categoria'] = self._to_categoria(data['categoria'])

        if 'data_cricao' in data and isinstance(data['data_criacao'], str):
            try:
                data['data_criacao'] = datetime.fromisoformat(data['data_criacao']).date()
            
            except ValueError:
                pass

    def carregar_categorias(self) -> list[Categoria]:
        """ READ: Carrega a lista de categorias do disco e retorna como objetos Categoria. """
        dados_brutos = self._load_data(self.CATEGORIAS_FILE)
        return [self._to_categoria(d) for d in dados_brutos]
    
    def salvar_categoria(self, categoria: Categoria):
        categorias = self.carregar_categorias()
        encontrada = False
        
        id_categoria_novo = categoria.ID

        for cat_existente in categorias:
            if (
                cat_existente.nome.lower() == categoria.nome.lower()
                and cat_existente.tipo == categoria.tipo
                and cat_existente.ID != categoria.ID
            ):
                raise ValueError("Já existe uma categoria com este nome e tipo.")

        for i, cat_existente in enumerate(categorias):
            if cat_existente.ID == id_categoria_novo:
                categorias[i] = categoria
                encontrada = True
                break

        if not encontrada:
            categorias.append(categoria)

        dados_a_salvar = [self._to_dict(c) for c in categorias]
        self._save_data(self.CATEGORIAS_FILE, dados_a_salvar)

        
    def remover_categoria(self, categoria_id: int):
            """ DELETE: Remove uma categoria pelo seu ID e persiste a lista completa. """
            categorias = self.carregar_categorias()
            
            categorias_apos_remocao = [
                c for c in categorias 
                if c.ID != categoria_id
            ]
            
            if len(categorias_apos_remocao) == len(categorias):
                print(f"Aviso: Categoria com ID {categoria_id} não encontrada para remoção.")
                return

            dados_a_salvar = [self._to_dict(c) for c in categorias_apos_remocao]
            self._save_data(self.CATEGORIAS_FILE, dados_a_salvar)

    def carregar_lancamentos(self) -> list[Lancamento]:
        """ READ: Carrega a lista de lançamentos (Receitas/Despesas) do disco e retorna como objetos. """
        dados_brutos = self._load_data(self.LANCAMENTOS_FILE)
        return [self._to_lancamento(d) for d in dados_brutos]

    def salvar_lancamento(self, lancamento: Lancamento):
            lancamentos = self.carregar_lancamentos()
            encontrado = False

            id_lancamento_novo = lancamento.ID

            for i, lanc_existente in enumerate(lancamentos):
                if lanc_existente.ID == id_lancamento_novo:
                    lancamentos[i] = lancamento
                    encontrado = True
                    break
        
            if not encontrado:
                lancamentos.append(lancamento)

            dados_a_salvar = [self._to_dict(l) for l in lancamentos]
            self._save_data(self.LANCAMENTOS_FILE, dados_a_salvar)

    def remover_lancamento(self, lancamento_id: int):
            """ DELETE: Remove um lançamento pelo seu ID e persiste a lista completa. """
            lancamentos = self.carregar_lancamentos()
            
            lancamentos_apos_remocao = [
                l for l in lancamentos 
                if l.ID != lancamento_id
            ]
            
            if len(lancamentos_apos_remocao) == len(lancamentos):
                print(f"Aviso: Lançamento com ID {lancamento_id} não encontrado para remoção.")
                return

            dados_a_salvar = [self._to_dict(l) for l in lancamentos_apos_remocao]
            self._save_data(self.LANCAMENTOS_FILE, dados_a_salvar)
    
    def carregar_alertas(self) -> list:
        
        dados_brutos = self._load_data(self.ALERTAS_FILE)
        return [self._to_alerta(d) for d in dados_brutos]

    def salvar_alertas():
        pass