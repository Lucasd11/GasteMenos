import json
import os
from dominio.categoria import Categoria


class RepositorioFinancas:
    BASE_DIR = "data"
    CATEGORIAS_FILE = "categorias.json"
    LANCAMENTOS_FILE = "lancamentos.json"

    def __init__(self):
        os.makedirs(self.BASE_DIR, exist_ok=True)

    def _file_path(self, filename):
        return os.path.join(self.BASE_DIR, filename)

    def _load_data(self, filename):
        path = self._file_path(filename)

        if not os.path.exists(path):
            return []

        with open(path, "r", encoding="utf-8") as f:
            try:
                conteudo = f.read().strip()
                if not conteudo:
                    return []
                return json.loads(conteudo)
            except json.JSONDecodeError:
                return []


    def _save_data(self, filename, data):
        path = self._file_path(filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # ---------- CATEGORIAS ----------

    def salvar_categoria(self, categoria: Categoria):
        categorias = self._load_data(self.CATEGORIAS_FILE)

        # Evitar duplicidade por ID
        for c in categorias:
            if c["id"] == categoria.get_id():
                return  # já existe, não salva novamente

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

        for d in dados:
            categorias.append(
                Categoria(
                    nome=d.get("nome"),
                    tipo=d.get("tipo"),
                    limite_mensal=d.get("limite_mensal", 0.0),
                    descricao=d.get("descricao", ""),
                    id=d.get("id")
                )
            )

        return categorias
