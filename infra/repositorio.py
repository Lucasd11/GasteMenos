import json
import os
from dominio.categoria import Categoria


class RepositorioFinancas:
    BASE_DIR = "data"
    CATEGORIAS_FILE = "categorias.json"


    def __init__(self):
        os.makedirs(self.BASE_DIR, exist_ok=True)


    def _file_path(self, filename):
        return os.path.join(self.BASE_DIR, filename)


    def _load_data(self, filename):
        path = self._file_path(filename)

        if not os.path.exists(path):
            return [] # SEMPRE lista
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)


    def _save_data(self, filename, data):
        path = self._file_path(filename)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


    # ---------- CATEGORIAS ----------


    def salvar_categoria(self, categoria: Categoria):
        categorias = self._load_data(self.CATEGORIAS_FILE)


        categorias.append({
        "id": categoria.get_id(),
        "nome": categoria.get_nome(),
        "tipo": categoria.get_tipo(),
        "limite_mensal": categoria.get_limite_mensal(),
        "descricao": categoria.get_descricao()
        })


        self._save_data(self.CATEGORIAS_FILE, categorias)


    def listar_categorias(self):
        dados = self._load_data(self.CATEGORIAS_FILE)
        categorias = []


        for d in dados: # d é dict, dados é list
            categorias.append(Categoria(
            id=d.get("id"),
            nome=d.get("nome"),
            tipo=d.get("tipo"),
            limite_mensal=d.get("limite_mensal", 0.0),
            descricao=d.get("descricao", "")
            ))


        return categorias