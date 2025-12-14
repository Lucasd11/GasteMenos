import json
import os
from typing import Dict

class Configuracoes:
    def __init__(self, arquivo="settings.json"):
        self._arquivo = arquivo
        self._cfg: Dict[str, float] = {}

        if not os.path.exists(arquivo):
            self._cfg = {
                "alerta_alto_valor": 500,
                "meses_comparativo": 3,
                "meta_economia_percentual": 10
            }
            self._salvar()
        else:
            with open(arquivo, "r", encoding="utf-8") as f:
                self._cfg = json.load(f)

    def _salvar(self):
        with open(self._arquivo, "w", encoding="utf-8") as f:
            json.dump(self._cfg, f, indent=4, ensure_ascii=False)

    def alerta_alto_valor(self):
        return self._cfg["alerta_alto_valor"]

    def meses_comparativo(self):
        return self._cfg["meses_comparativo"]

    def meta_economia(self):
        return self._cfg["meta_economia_percentual"]

    def set_alerta_alto_valor(self, valor: float):
        self._cfg["alerta_alto_valor"] = float(valor)
        self._salvar()

    def set_meses_comparativo(self, meses: int):
        self._cfg["meses_comparativo"] = int(meses)
        self._salvar()

    def set_meta_economia(self, percentual: float):
        self._cfg["meta_economia_percentual"] = float(percentual)
        self._salvar()
