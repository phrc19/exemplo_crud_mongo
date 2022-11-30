class Servico:

    def __init__(self, codigo_cliente: str, codigo_ordem: str, codigo_servico: str, nome: str, cat: str,
                 valor_unitario: str, tempo_execucao: str, garantia: str):
        self.codigo_cliente = codigo_cliente
        self.codigo_ordem = codigo_ordem
        self.codigo_servico = codigo_servico
        self.nome = nome
        self.cat = cat
        self.valor_unitario = valor_unitario
        self.tempo_execucao = tempo_execucao
        self.garantia = garantia

    def set_nome(self, nome: str):
        self.nome = nome

    def set_cat(self, cat: str):
        self.cat = cat

    def set_valor_unitario(self, valor_unitario: str):
        self.valor_unitario = valor_unitario

    def set_tempo_execucao(self, tempo_execucao: str):
        self.tempo_execucao = tempo_execucao

    def set_garantia(self, garantia: str):
        self.garantia = garantia

    def get_codigo_cliente(self) -> str:
        return self.codigo_cliente

    def get_codigo_ordem(self) -> str:
        return self.codigo_ordem

    def get_codigo_servico(self) -> str:
        return self.codigo_servico

    def get_nome(self) -> str:
        return self.garantia

    def get_cat(self) -> str:
        return self.cat

    def get_valor_unitario(self) -> str:
        return self.valor_unitario

    def get_tempo_execucao(self) -> str:
        return self.tempo_execucao

    def get_garantia(self) -> str:
        return self.garantia

    def to_string(self) -> str:
        return "Codigo do cliente: " + self.get_codigo_cliente() + "\nCodigo da ordem de servico: " + \
               self.get_codigo_ordem() + "\nCodigo do servico: " + self.get_codigo_servico() + "\nNome: " + \
               self.get_nome() + "\nCat: " + self.get_cat() + "\nValor unitario: " + self.get_valor_unitario() + \
               "\nTempo de execucao: " + self.get_tempo_execucao() + "\nGarantia: " + self.get_garantia()
