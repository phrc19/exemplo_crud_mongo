class OrdemServico:

    def __init__(self, codigo_cliente: str, codigo_ordem: str, data_abertura: str, data_prevista: str, data_efetiva: str):
        self.codigo_cliente = codigo_cliente
        self.codigo_ordem = codigo_ordem
        self.data_abertura = data_abertura
        self.data_prevista = data_prevista
        self.data_efetiva = data_efetiva

    def set_data_abertura(self, data_abertura: str):
        self.data_abertura = data_abertura

    def set_data_prevista(self, data_prevista: str):
        self.data_prevista = data_prevista

    def set_data_efetiva(self, data_efetiva: str):
        self.data_efetiva = data_efetiva

    def get_codigo_cliente(self) -> str:
        return self.codigo_cliente

    def get_codigo_ordem(self) -> str:
        return self.codigo_ordem

    def get_data_abertura(self) -> str:
        return self.data_abertura

    def get_data_prevista(self) -> str:
        return self.data_prevista

    def get_data_efetiva(self) -> str:
        return self.data_efetiva

    def to_string(self) -> str:
        return "Codigo do cliente: " + self.get_codigo_cliente() + "\nCodigo da ordem: " + self.get_codigo_ordem() + \
            "\nData de abertura: " + self.get_data_abertura() + "\nData prevista: " + self.get_data_prevista() + \
            "\nData efetiva: " + self.get_data_efetiva()
