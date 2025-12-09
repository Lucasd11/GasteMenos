import uuid
from datetime import date

class Alerta:
    """
    Representa uma notificação automática gerada pelo sistema (ex: limite excedido).
    """
    
    # Constantes para os tipos de alerta
    TIPO_ALTO_VALOR = "ALTO_VALOR"
    TIPO_LIMITE_EXCEDIDO = "LIMITE_EXCEDIDO"
    TIPO_SALDO_NEGATIVO = "SALDO_NEGATIVO"

    def __init__(self, tipo: str, mensagem: str, data: date = date.today()):
        # Geração de ID único
        self.__id = str(uuid.uuid4())
        
        self.tipo = tipo
        self.mensagem = mensagem
        self.data = data

    # --- Encapsulamento ---
    
    @property
    def id(self):
        return self.__id

    @property
    def tipo(self):
        return self.__tipo
        
    @tipo.setter
    def tipo(self, novo_tipo: str):
        tipos_validos = (self.TIPO_ALTO_VALOR, self.TIPO_LIMITE_EXCEDIDO, self.TIPO_SALDO_NEGATIVO)
        
        if novo_tipo not in tipos_validos:
            raise ValueError(f"Tipo de alerta inválido. Use um dos seguintes: {tipos_validos}")
        self.__tipo = novo_tipo

    @property
    def mensagem(self):
        return self.__mensagem

    @mensagem.setter
    def mensagem(self, nova_mensagem: str):
        if not nova_mensagem or len(nova_mensagem.strip()) < 5:
            raise ValueError("A mensagem do alerta deve ser informativa.")
        self.__mensagem = nova_mensagem
        
    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, nova_data: date):
        if not isinstance(nova_data, date):
            raise TypeError("A data do alerta deve ser um objeto date.")
        self.__data = nova_data

    # --- Métodos Especiais ---

    def __str__(self):
        data_formatada = self.data.strftime("%d/%m/%Y")
        return f"ALERTA ({self.tipo}) em {data_formatada}: {self.mensagem}"

    def __repr__(self):
        return f"Alerta(tipo='{self.tipo}', mensagem='{self.mensagem}', data={self.data})"