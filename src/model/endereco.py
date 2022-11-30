class endereco:

    def __init__(self, codigo_cliente: str, cep: str, logradouro: str, municipio: str, uf: str, numero: str, complemento: str):
        self.codigo_cliente = codigo_cliente
        self.cep = cep
        self.logradouro = logradouro
        self.municipio = municipio
        self.uf = uf
        self.numero = numero
        self.complemento = complemento

    def set_codigo_cliente(self, codigo_cliente: int):
        self.codigo_cliente = codigo_cliente
        
    def set_cep(self, cep: str):
        self.cep = cep

    def set_logradouro(self, logradouro: str):
        self.logradouro = logradouro

    def set_municipio(self, municipio: str):
        self.municipio = municipio

    def set_uf(self, uf: str):
        self.uf = uf

    def set_numero(self, numero: str):
        self.numero = numero

    def set_complemento(self, complemento: str):
        self.complemento = complemento

    def get_codigo_cliente(self) -> str:
        return self.codigo_cliente

    def get_cep(self) -> str:
        return self.cep

    def get_logradouro(self) -> str:
        return self.logradouro

    def get_municipio(self) -> str:
        return self.municipio

    def get_uf(self) -> str:
        return self.uf

    def get_numero(self) -> str:
        return self.numero

    def get_complemento(self) -> str:
        return self.complemento

    def to_string(self) -> str:
        return "Codigo do cliente: " + self.get_codigo_cliente() + "\nCEP: " + self.get_cep() + "\nLogradouro: " + \
               self.get_logradouro() + "\nMunicipio: " + self.get_municipio() + "\nUF: " + self.get_uf() + "\nNumero: " + \
               self.get_numero() + "\nComplemento: " + self.get_complemento()
