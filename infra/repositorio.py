import json
import os
from dominio.categoria import Categoria
from dominio.receita import Receita
from dominio.despesa import Despesa
from datetime import date
from collections import defaultdict


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
                return

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

    # ---------- LANÇAMENTOS ----------

    def salvar_lancamento(self, lancamento):
        lancamentos = self._load_data(self.LANCAMENTOS_FILE)

        lancamentos.append({
            "id": lancamento.ID,
            "tipo": lancamento.tipo,
            "valor": lancamento.valor,
            "categoria_id": lancamento.categoria.get_id(),
            "data": lancamento.data.isoformat(),
            "descricao": lancamento.descricao,
            "forma_pagmto": lancamento.forma_pagmto
        })

        self._save_data(self.LANCAMENTOS_FILE, lancamentos)

    def listar_lancamentos(self, categorias):
        dados = self._load_data(self.LANCAMENTOS_FILE)
        lancamentos = []

        categorias_por_id = {c.get_id(): c for c in categorias}

        for d in dados:
            categoria = categorias_por_id.get(d["categoria_id"])
            if not categoria:
                continue

            data_lanc = date.fromisoformat(d["data"])

            if d["tipo"] == "RECEITA":
                lancamentos.append(
                    Receita(
                        d["valor"],
                        categoria,
                        data_lanc,
                        d["descricao"],
                        d["forma_pagmto"]
                    )
                )
            elif d["tipo"] == "DESPESA":
                lancamentos.append(
                    Despesa(
                        d["valor"],
                        categoria,
                        data_lanc,
                        d["descricao"],
                        d["forma_pagmto"]
                    )
                )

        return lancamentos
    
    def atualizar_categoria(self, categoria: Categoria):
        categorias = self._load_data(self.CATEGORIAS_FILE)

        for c in categorias:
            if c["id"] == categoria.get_id():
                c["nome"] = categoria.get_nome()
                c["tipo"] = categoria.get_tipo()
                c["limite_mensal"] = categoria.get_limite_mensal()
                c["descricao"] = categoria.get_descricao()
                break

        self._save_data(self.CATEGORIAS_FILE, categorias)

    def excluir_categoria(self, categoria_id: str):
        categorias = self._load_data(self.CATEGORIAS_FILE)
        categorias = [c for c in categorias if c["id"] != categoria_id]
        self._save_data(self.CATEGORIAS_FILE, categorias)

    def total_despesas_por_mes(self):
        dados = self._load_data(self.LANCAMENTOS_FILE)
        totais = defaultdict(float)

        for d in dados:
            if d["tipo"] == "DESPESA":
                mes = d["data"][:7]
                totais[mes] += d["valor"]

        return dict(totais)

