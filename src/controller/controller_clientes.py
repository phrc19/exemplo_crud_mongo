import pandas as pd
from model.cliente import cliente
from conexion.mongo_queries import MongoQueries

class controllercliente:
    def __init__(self):
        self.mongo = MongoQueries()

    def inserir_cliente(self) -> cliente:
        self.mongo.connect()

        codigo_cliente = str(input("Insira o codigo do cliente: "))

        if self.verifica_existencia_cliente(codigo_cliente):
            nome = str(input("Digite o nome do cliente: "))
            self.mongo.db["clientes"].insert_one({"codigo_cliente": f"{codigo_cliente}", "nome": f"{nome}"})
            df_cliente = self.recupera_cliente(codigo_cliente)
            novo_cliente = cliente(df_cliente.codigo_cliente.values[0], df_cliente.nome.values[0])
            print(novo_cliente.to_string())
            self.mongo.close()
            return novo_cliente
        else:
            self.mongo.close()
            print(f"O codigo do cliente {codigo_cliente} ja foi cadastrado")
            return None

    def atualizar_cliente(self) -> cliente:
        self.mongo.connect()

        codigo_cliente = str(input("Insira o codigo do cliente: "))

        if not self.verifica_existencia_cliente(codigo_cliente):
            novo_nome = str(input("Insira o novo nome do cliente: "))
            self.mongo.db["clientes"].update_one({"codigo_cliente": f"{codigo_cliente}"}, {"$set": {"nome": f"{novo_nome}"}})
            df_cliente = self.recupera_cliente(codigo_cliente)
            cliente_atualizado = cliente(df_cliente.codigo_cliente.values[0], df_cliente.nome.values[0])
            print(cliente_atualizado.to_string())
            self.mongo.close()
            return cliente_atualizado
        else:
            self.mongo.close()
            print(f"O codigo do cliente {codigo_cliente} nao existe")
            return None

    def excluir_cliente(self):
        self.mongo.connect()

        codigo_cliente = str(input("Insira o codigo do cliente: "))

        if not self.verifica_existencia_cliente(codigo_cliente):
            escolha = input(f"Tem certeza que deseja remover o registro do cliente {codigo_cliente}? (Digite S para continuar ou N para cancelar a operacao)")
            while escolha.upper() != 'S' and escolha.upper() != 'N':
                print(f"A escolha {escolha} e invalida")
                escolha = input(f"Tem certeza que deseja remover o registro do cliente {codigo_cliente}? (Digite S para continuar ou N para cancelar a operacao)")
            if escolha.upper() == 'S':
                verificador = False
                contador = 0
                while contador < 3 and verificador == False:
                    if contador == 0:
                        df_endereco = pd.DataFrame(self.mongo.db["enderecos"].find({"codigo_cliente": f"{codigo_cliente}"}, {"codigo_cliente": 1, "cep": 1, "logradouro": 1, "municipio": 1, "uf": 1, "numero": 1, "complemento": 1, "_id": 0}))
                        if not df_endereco.empty:
                            verificador = True
                    elif contador == 1:
                        df_telefone = pd.DataFrame(self.mongo.db["telefones"].find({"codigo_cliente": f"{codigo_cliente}"}, {"codigo_cliente": 1, "numero": 1, "tipo_telefone" :1, "_id": 0}))
                        if not df_telefone.empty:
                            verificador = True
                    elif contador == 2:
                        df_ordem_servico = pd.DataFrame(self.mongo.db["ordens_servico"].find({"codigo_cliente": f"{codigo_cliente}"}, {"codigo_ordem": 1, "codigo_cliente": 1, "dt_abertura": 1, "dt_prevista": 1, "dt_efetiva": 1, "_id": 0}))
                        if not df_ordem_servico.empty:
                            verificador = True
                    contador += 1
                if verificador == True:
                    escolha = input(f"Existem registros em outras colecoes relacionados ao codigo do cliente {codigo_cliente}.\nSe voce quiser continuar, os dados nas outras colecoes serao apagados.\nTem certeza que deseja continuar com a operacao? (Digite S para continuar ou N para cancelar a operacao)")
                    while escolha.upper() != 'S' and escolha.upper() != 'N':
                        print(f"A escolha {escolha} e invalida")
                        escolha = input(f"Tem certeza que deseja continuar com a operacao? (Digite S para continuar ou N para cancelar a operacao)")
                    if escolha.upper() == 'S':
                        self.mongo.db["enderecos"].delete_one({"codigo_cliente": f"{codigo_cliente}"})
                        print("Endereco do cliente excluido")
                        self.mongo.db["telefones"].delete_one({"codigo_cliente": f"{codigo_cliente}"})
                        print("Telefone do cliente excluido")
                        self.mongo.db["servicos"].delete_many({"codigo_cliente": f"{codigo_cliente}"})
                        print("Servicos excluidos com sucesso")
                        self.mongo.db["ordens_servico"].delete_many({"codigo_cliente": f"{codigo_cliente}"})
                        print("Ordens de servico excluidas com sucesso")
                df_cliente = self.recupera_cliente(codigo_cliente)
                self.mongo.db["clientes"].delete_one({"codigo_cliente": f"{codigo_cliente}"})
                cliente_excluido = cliente(df_cliente.codigo_cliente.values[0], df_cliente.nome.values[0])
                self.mongo.close()
                print("cliente removido com sucesso")
                print(cliente_excluido.to_string())
            else:
                self.mongo.close()
                print("Operacao de insercao cancelada")
        else:
            self.mongo.close()
            print(f"O codigo do cliente {codigo_cliente} nao existe")

    def verifica_existencia_cliente(self, codigo_cliente: str=None, external: bool=False) -> bool:
        if external:
            self.mongo.connect()

        df_cliente = pd.DataFrame(self.mongo.db["clientes"].find({"codigo_cliente": f"{codigo_cliente}"}, {"codigo_cliente": 1, "nome": 1, "_id": 0}))

        if external:
            self.mongo.close()

        return df_cliente.empty

    def recupera_cliente(self, codigo_cliente: str=None, external: bool=False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        df_cliente = pd.DataFrame(list(self.mongo.db["clientes"].find({"codigo_cliente": f"{codigo_cliente}"}, {"codigo_cliente": 1, "nome": 1, "_id": 0})))

        if external:
            self.mongo.close()

        return df_cliente
