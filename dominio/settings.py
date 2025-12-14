import json

class Configuracoes:
    def __init__(self, arquivo="settings.json"):
        with open(arquivo, "r", encoding="utf-8") as f:
            self._cfg = json.load(f)

    def alerta_alto_valor(self):
        return self._cfg.get("alerta_alto_valor", 500)

    def meses_comparativo(self):
        return self._cfg.get("meses_comparativo", 3)

    def meta_economia(self):
        return self._cfg.get("meta_economia_percentual", 0)
