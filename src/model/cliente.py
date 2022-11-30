class cliente:

    def __init__(self, codigo_cliente: str, nome: str):
        self.codigo_cliente = codigo_cliente
        self.nome = nome

    def set_codigo_cliente(self, codigo_cliente: int):
        self.codigo_cliente = codigo_cliente

    def set_nome(self, nome: str):
        self.nome = nome

    def get_nome(self) -> str:
        return self.nome

    def get_codigo_cliente(self) -> str:
        return self.codigo_cliente

    
    def to_string(self) -> str:
        return "Codigo do cliente: " + self.get_codigo_cliente() + "\nNome do cliente: " + self.get_nome()
