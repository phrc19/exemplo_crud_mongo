import pandas as pd
from model.cliente import cliente
from model.endereco import endereco
from controller.controller_clientes import controllercliente
from conexion.mongo_queries import MongoQueries

class controller_endereco:

    def __init__(self):
        self.mongo = MongoQueries()
        self.controller_cliente = controllercliente()

    def inserir_endereco(self) -> endereco:
        self.mongo.connect()

        codigo_cliente = str(input("Digite o codigo do cliente referente ao endereco que deseja cadastrar: "))
        cliente = self.valida_cliente(codigo_cliente)
        if cliente is None:
            return None
        else:
            if  self.verifica_existencia_endereco(codigo_cliente):
                cep = str(input("Insira o cep que deseja inserir: "))
                logradouro = str(input("Insira o nome da rua: "))
                municipio = str(input("Insira o municipio: "))
                uf = str(input("Insira a sigla do estado: "))
                numero = str(input("Insira o numero: "))
                complemento = str(input("Caso queira, insira o complemento: "))
                self.mongo.db["enderecos"].insert_one({"codigo_cliente": f"{codigo_cliente}", "cep": f"{cep}", "logradouro": f"{logradouro}", "municipio": f"{municipio}", "uf": f"{uf}", "numero": f"{numero}", "complemento": f"{complemento}"})
                df_endereco = self.recupera_endereco(codigo_cliente)
                novo_endereco = endereco(df_endereco.codigo_cliente.values[0], df_endereco.cep.values[0], df_endereco.logradouro.values[0], df_endereco.municipio.values[0], df_endereco.uf.values[0], df_endereco.numero.values[0], df_endereco.complemento.values[0])
                print(novo_endereco.to_string())
                self.mongo.close()
                return novo_endereco
            else:
                self.mongo.close()
                print("Nao e possivel fazer a insercao com os dados fornecidos")
                return None

    def atualizar_endereco(self) -> endereco:
        self.mongo.connect()

        codigo_cliente = str(input("Digite o codigo do cliente referente ao endereco que deseja cadastrar: "))
        cliente = self.valida_cliente(codigo_cliente)
        if cliente is None:
            return None
        else:
            if not self.verifica_existencia_endereco(codigo_cliente):
                novo_cep = str(input("insira o cep atualizado: "))
                novo_logradouro = str(input("Insira nome da rua atualizado: "))
                novo_municipio = str(input("Insira o municipio atualizado: "))
                novo_uf = str(input("Insira a sigla do estado atualizada: "))
                novo_numero = str(input("Insira o numero atualizado: "))
                novo_complemento = str(input("Caso queira, insira o complemento atualizado: )"))
                self.mongo.db["enderecos"].update_one({"codigo_cliente": f"{codigo_cliente}"}, {"$set": {"cep": f"{novo_cep}", "logradouro": f"{novo_logradouro}", "municipio": f"{novo_municipio}", "uf": f"{novo_uf}", "numero": f"{novo_numero}", "complemento": f"{novo_complemento}"}})
                df_endereco = self.recupera_endereco(codigo_cliente)
                endereco_atualizado = endereco(df_endereco.codigo_cliente.values[0], df_endereco.cep.values[0], df_endereco.logradouro.values[0], df_endereco.municipio.values[0], df_endereco.uf.values[0], df_endereco.numero.values[0], df_endereco.complemento.values[0])
                print(endereco_atualizado.to_string())
                self.mongo.close()
                return endereco_atualizado
            else:
                self.mongo.close()
                print("Nao e possivel fazer a atualizacao com os dados fornecidos")
                return None

    def excluir_endereco(self):
        self.mongo.connect()
        codigo_cliente = str(input("Insira o codigo do cliente referente ao qual deseja excluir o endereco: "))

        if not self.verifica_existencia_endereco(codigo_cliente):
            escolha = input(f"Tem certeza que deseja remover o registro de endereco referente ao cliente {codigo_cliente}? (Digite S para continuar ou N para cancelar a operacao)")
            while escolha.upper() != 'S' and escolha.upper() != 'N':
                print(f"A escolha {escolha} e invalida")
                escolha = input(f"Tem certeza que deseja remover registro de endereco referente ao cliente {codigo_cliente}? (Digite S para continuar ou N para cancelar a operacao)")
            if escolha.upper() == 'S':
                df_endereco = self.recupera_endereco(codigo_cliente)
                self.mongo.db["enderecos"].delete_one({"codigo_cliente": f"{codigo_cliente}"})
                endereco_excluido = endereco(df_endereco.codigo_cliente.values[0], df_endereco.cep.values[0], df_endereco.logradouro.values[0], df_endereco.municipio.values[0], df_endereco.uf.values[0], df_endereco.numero.values[0], df_endereco.complemento.values[0])
                self.mongo.close()
                print("Endereco excluido com sucesso")
                print(endereco_excluido.to_string())
            else:
                self.mongo.close()
                print("Nao e possivel fazer a exclusao com os dados fornecidos")

    def verifica_existencia_endereco(self, codigo_cliente: str=None, external: bool=False) -> bool:
        if external:
            self.mongo.connect()

        df_endereco = pd.DataFrame(self.mongo.db["enderecos"].find({"codigo_cliente": f"{codigo_cliente}"}, {"codigo_cliente": 1, "cep": 1, "logradouro": 1, "municipio": 1, "uf": 1, "numero": 1, "complemento": 1, "_id": 0}))

        if external:
            self.mongo.close()

        return df_endereco.empty

    def recupera_endereco(self, codigo_cliente: str=None, external: bool=False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        df_endereco = pd.DataFrame(list(self.mongo.db["enderecos"].find({"codigo_cliente": f"{codigo_cliente}"}, {"codigo_cliente": 1, "cep": 1, "logradouro": 1, "municipio": 1, "uf": 1, "numero": 1, "complemento": 1, "_id": 0})))

        if external:
            self.mongo.close()

        return df_endereco

    def valida_cliente(self, codigo_cliente: str=None) -> cliente:
        if self.controller_cliente.verifica_existencia_cliente(codigo_cliente, external=True):
            print(f"O codigo do cliente {codigo_cliente} nao esta cadastrado no sistema")
            return None
        else:
            df_cliente = self.controller_cliente.recupera_cliente(codigo_cliente, external=True)
            return cliente(df_cliente.codigo_cliente.values[0], df_cliente.nome.values[0])