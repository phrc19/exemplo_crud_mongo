import pandas as pd
from model.cliente import cliente
from model.telefone import telefone
from controller.controller_clientes import controllercliente
from conexion.mongo_queries import MongoQueries

class controller_telefone:

    def __init__(self):
        self.mongo = MongoQueries()
        self.controller_cliente = controllercliente()

    def inserir_telefone(self) -> telefone:
        self.mongo.connect()

        codigo_cliente = str(input("Digite o codigo do cliente referente ao telefone que deseja cadastrar: "))
        cliente = self.valida_cliente(codigo_cliente)
        if cliente is None:
            return None
        else:
            if self.verifica_existencia_telefone(codigo_cliente):
                numero = str(input("Insira o numero que deseja inserir: "))
                tipo_telefone = str(input("Insira o tipo no numero: "))
                self.mongo.db["telefones"].insert_one({"codigo_cliente": f"{codigo_cliente}", "numero": f"{numero}", "tipo_telefone": f"{tipo_telefone}"})
                df_telefone = self.recupera_telefone(codigo_cliente)
                novo_telefone = telefone(df_telefone.codigo_cliente.values[0], df_telefone.numero.values[0], df_telefone.tipo_telefone.values[0])
                print(novo_telefone.to_string())
                self.mongo.close()
                return novo_telefone
            else:
                self.mongo.close()
                print("O cliente ja possui um numero cadastrado")
                return None

    def atualizar_telefone(self) -> telefone:
        self.mongo.connect()

        codigo_cliente = str(input("Digite o codigo do cliente referente a telefone: "))
        cliente = self.valida_cliente(codigo_cliente)
        if cliente is None:
            return None
        else:
            if  not self.verifica_existencia_telefone(codigo_cliente):
                novo_numero = str(input("Insira o numero atualizado: "))
                novo_tipo_telefone = str(input("Insira o tipo do numero atualizado: "))
                self.mongo.db["telefones"].update_one({"codigo_cliente": f"{codigo_cliente}"}, {"$set": {"numero": f"{novo_numero}", "tipo_telefone": f"{novo_tipo_telefone}"}})
                df_telefone = self.recupera_telefone(codigo_cliente)
                telefone_atualizado = telefone(df_telefone.codigo_cliente.values[0], df_telefone.numero.values[0],
                                               df_telefone.tipo_telefone.values[0])

                print(telefone_atualizado.to_string())
                self.mongo.close()
                return telefone_atualizado
            else:
                self.mongo.close()
                print("Nao existe telefone cadastrado para esse cliente no momento")
                return None

    def excluir_telefone(self):
        self.mongo.connect()

        codigo_cliente = str(input("Digite o codigo do cliente referente a telefone: "))
        cliente = self.valida_cliente(codigo_cliente)
        if cliente is None:
            return None
        else:
            if not self.verifica_existencia_telefone(codigo_cliente):
                escolha = input(f"Tem certeza que deseja remover o registro de telefone referente ao cliente {codigo_cliente}? (Digite S para continuar ou N para cancelar a operacao)")
                while escolha.upper() != 'S' and escolha.upper() != 'N':
                    print(f"A escolha {escolha} e invalida")
                    escolha = input(f"Tem certeza que deseja remover o registro de telefone referente ao cliente {codigo_cliente}? (Digite S para continuar ou N para cancelar a operacao)")
                if escolha.upper() == 'S':
                    df_telefone = self.recupera_telefone(codigo_cliente)
                    self.mongo.db["telefones"].delete_one({"codigo_cliente": f"{codigo_cliente}"})
                    telefone_excluido = telefone(df_telefone.codigo_cliente.values[0], df_telefone.numero.values[0], df_telefone.tipo_telefone.values[0])
                    self.mongo.close()
                    print("O telefone foi excluido com sucesso")
                    print(telefone_excluido.to_string())
                    return None
                else:
                    self.mongo.close()
                    print("Nao e possivel fazer a exclusao com os dados fornecidos")
                    return None
    

    def verifica_existencia_telefone(self, codigo_cliente: str=None, external: bool=False) -> bool:
        if external:
            self.mongo.connect()

        df_telefone = pd.DataFrame(self.mongo.db["telefones"].find({"codigo_cliente": f"{codigo_cliente}"}, {"codigo_cliente": 1, "numero": 1, "tipo_telefone" :1, "_id": 0}))

        if external:
            self.mongo.close()

        return df_telefone.empty

    def recupera_telefone(self, codigo_cliente: str=None, external: bool=False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        df_telefone = pd.DataFrame(list(self.mongo.db["telefones"].find({"codigo_cliente": f"{codigo_cliente}"}, {"codigo_cliente": 1, "numero": 1, "tipo_telefone" :1,  "_id": 0})))

        if external:
            self.mongo.close()

        return df_telefone

    def valida_cliente(self, codigo_cliente: str=None) -> cliente:
        if self.controller_cliente.verifica_existencia_cliente(codigo_cliente, external=True):
            print(f"O codigo do cliente {codigo_cliente} nao esta cadastrado no sistema")
            return None
        else:
            df_cliente = self.controller_cliente.recupera_cliente(codigo_cliente, external=True)
            return cliente(df_cliente.codigo_cliente.values[0], df_cliente.nome.values[0])