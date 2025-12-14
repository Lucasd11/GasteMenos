import uuid
from datetime import date


class Alerta:
    """
    Representa uma notificação automática gerada pelo sistema.
    """

    TIPO_ALTO_VALOR = "ALTO_VALOR"
    TIPO_LIMITE_EXCEDIDO = "LIMITE_EXCEDIDO"
    TIPO_SALDO_NEGATIVO = "SALDO_NEGATIVO"

    def __init__(self, tipo: str, mensagem: str, data: date = date.today()):
        self.__id = str(uuid.uuid4())
        self.tipo = tipo
        self.mensagem = mensagem
        self.data = data

    # ---------- ENCAPSULAMENTO ----------

    @property
    def id(self):
        return self.__id

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, novo_tipo: str):
        tipos_validos = (
            self.TIPO_ALTO_VALOR,
            self.TIPO_LIMITE_EXCEDIDO,
            self.TIPO_SALDO_NEGATIVO
        )
        if novo_tipo not in tipos_validos:
            raise ValueError("Tipo de alerta inválido.")
        self.__tipo = novo_tipo

    @property
    def mensagem(self):
        return self.__mensagem

    @mensagem.setter
    def mensagem(self, nova_mensagem: str):
        if not isinstance(nova_mensagem, str) or not nova_mensagem.strip():
            raise ValueError("Mensagem do alerta inválida.")
        self.__mensagem = nova_mensagem.strip()

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, nova_data: date):
        if not isinstance(nova_data, date):
            raise TypeError("Data inválida.")
        self.__data = nova_data

    # ---------- MÉTODOS ÚTEIS ----------

    def to_dict(self):
        """Facilita persistência em JSON (Semana 5)."""
        return {
            "id": self.id,
            "tipo": self.tipo,
            "mensagem": self.mensagem,
            "data": self.data.isoformat()
        }

    # ---------- MÉTODOS ESPECIAIS ----------

    def __str__(self):
        data_formatada = self.data.strftime("%d/%m/%Y")
        return f"ALERTA ({self.tipo}) - {data_formatada}: {self.mensagem}"

    def __repr__(self):
        return f"Alerta(tipo='{self.tipo}', mensagem='{self.mensagem}')"
