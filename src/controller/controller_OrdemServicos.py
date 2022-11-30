import pandas as pd
from model.cliente import cliente
from model.ordem_servico import OrdemServico
from controller.controller_clientes import controllercliente
from conexion.mongo_queries import MongoQueries

class Controller_Ordem_Servicos:
    def __init__(self):
        self.mongo = MongoQueries()
        self.controller_cliente = controllercliente()

    def inserir_ordem_servico(self) -> OrdemServico:
        self.mongo.connect()

        codigo_cliente = str(input("Digite o codigo do cliente referente a ordem de servico: "))
        cliente = self.valida_cliente(codigo_cliente)
        if cliente is None:
            return None
        else:
            codigo_ordem = str(input("Digite o codigo da ordem de servico: "))
            if self.verifica_existencia_ordem_servico(codigo_ordem, codigo_cliente):
                dt_abertura = str(input("Digite a data de abertura da ordem de servico: "))
                dt_prevista = str(input("Digite a data prevista da ordem de servico: "))
                dt_efetiva = str(input("Digite a data efetiva da ordem de servico: "))
                self.mongo.db["ordens_servico"].insert_one({"codigo_ordem": f"{codigo_ordem}", "codigo_cliente": f"{codigo_cliente}", "dt_abertura": f"{dt_abertura}", "dt_prevista": f"{dt_prevista}", "dt_efetiva": f"{dt_efetiva}"})
                df_ordem_servico = self.recupera_ordem_servico(codigo_ordem, codigo_cliente)
                novo_ordem_servico = OrdemServico(df_ordem_servico.codigo_ordem.values[0], df_ordem_servico.codigo_cliente.values[0], df_ordem_servico.dt_abertura.values[0], df_ordem_servico.dt_prevista.values[0], df_ordem_servico.dt_efetiva.values[0])
                print(novo_ordem_servico.to_string())
                self.mongo.close()
                return novo_ordem_servico
            else:
                self.mongo.close()
                print(f"O codigo da ordem de servico {codigo_ordem} ja foi cadastrado")
                return None

    def atualizar_ordem_servico(self) -> OrdemServico:
        self.mongo.connect()

        codigo_cliente = str(input("Digite o codigo do cliente referente a ordem de servico: "))
        cliente = self.valida_cliente(codigo_cliente)
        if cliente is None:
            return None
        else:
            codigo_ordem = str(input("Digite o codigo da ordem de servico: "))
            if not self.verifica_existencia_ordem_servico(codigo_ordem, codigo_cliente):
                dt_abertura = str(input("Digite a data de abertura da ordem de servico atualizada: "))
                dt_prevista = str(input("Digite a data prevista da ordem de servico atualizada: "))
                dt_efetiva = str(input("Digite a data efetiva da ordem de servico atualizada: "))
                self.mongo.db["ordens_servico"].update_one({"codigo_ordem": f"{codigo_ordem}"}, {"$set": {"dt_abertura": f"{dt_abertura}", "dt_prevista": f"{dt_prevista}", "dt_efetiva": f"{dt_efetiva}"}})
                df_ordem_servico = self.recupera_ordem_servico(codigo_ordem, codigo_cliente)
                ordem_atualizada = OrdemServico(df_ordem_servico.codigo_ordem.values[0], df_ordem_servico.codigo_cliente.values[0], df_ordem_servico.dt_abertura.values[0], df_ordem_servico.dt_prevista.values[0], df_ordem_servico.dt_efetiva.values[0])
                print(ordem_atualizada.to_string())
                self.mongo.close()
                return ordem_atualizada
            else:
                self.mongo.close()
                print(f"O codigo de ordem de servico {codigo_ordem} nao existe")
                return None

    def excluir_ordem_servico(self):
        self.mongo.connect()

        codigo_cliente = str(input("Digite o codigo do cliente referente a ordem de servico: "))
        cliente = self.valida_cliente(codigo_cliente)
        if cliente is None:
            return None
        else:
            codigo_ordem = str(input("Digite o codigo da ordem de servico: "))
            
            if not self.verifica_existencia_ordem_servico(codigo_ordem, codigo_cliente):
                escolha = input(f"Tem certeza que deseja remover a ordem de servico {codigo_ordem}? (Digite S para continuar ou N para cancelar a operacao)")
                while escolha.upper() != 'S' and escolha.upper() != 'N':
                    print(f"A escolha {escolha} e invalida")
                    escolha = input(f"Tem certeza que deseja remover a ordem de servico {codigo_ordem}? (Digite S para continuar ou N para cancelar a operacao)")
                if escolha.upper() == 'S':
                    df_servico = pd.DataFrame(self.mongo.db["servicos"].find({"codigo_ordem": f"{codigo_ordem}"}, {"codigo_servico": 1, "codigo_ordem": 1, "codigo_cliente": 1, "nome": 1, "cat": 1, "vlr_unitario": 1, "tempo_execucao": 1, "garantia": 1, "_id": 0}))
                    if not df_servico.empty:
                        escolha = input(f"Existem registros em outras colecoes relacionados a ordem de servico {codigo_ordem}.\nSe voce quiser continuar, os dados nas outras colecoes serao apagados.\nTem certeza que deseja continuar com a operacao? (Digite S para continuar ou N para cancelar a operacao)")
                        while escolha.upper() != 'S' and escolha.upper() != 'N':
                            print(f"A escolha {escolha} e invalida")
                            escolha = input(f"Tem certeza que deseja continuar com a operacao? (Digite S para continuar ou N para cancelar a operacao)")
                        if escolha.upper() == 'S':
                            self.mongo.db["servicos"].delete_many({"codigo_ordem": f"{codigo_ordem}"})
                            print("Servicos excluidos com sucesso")
                    df_ordem_servico = self.recupera_ordem_servico(codigo_ordem, codigo_cliente)
                    self.mongo.db["ordens_servico"].delete_one({"codigo_ordem": f"{codigo_ordem}"})
                    ordem_excluida = OrdemServico(df_ordem_servico.codigo_ordem.values[0], df_ordem_servico.codigo_cliente.values[0], df_ordem_servico.dt_abertura.values[0], df_ordem_servico.dt_prevista.values[0], df_ordem_servico.dt_efetiva.values[0])
                    self.mongo.close()
                    print("Ordem de servico excluida")
                    print(ordem_excluida.to_string())
            else:
                self.mongo.close()
                print(f"O codigo de ordem de servico {codigo_ordem} nao existe!")

    def verifica_existencia_ordem_servico(self, codigo_ordem: str=None, codigo_cliente: str=None, external: bool=False) -> bool:
        if external:
            self.mongo.connect()

        df_ordem_servico = pd.DataFrame(self.mongo.db["ordens_servico"].find({"codigo_ordem": f"{codigo_ordem}", "codigo_cliente": f"{codigo_cliente}"}, {"codigo_ordem": 1, "codigo_cliente": 1, "dt_abertura": 1, "dt_prevista": 1, "dt_efetiva": 1, "_id": 0}))

        if external:
            self.mongo.close()

        return df_ordem_servico.empty

    def recupera_ordem_servico(self, codigo_ordem: str=None, codigo_cliente: str=None, external: bool=False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        df_ordem_servico = pd.DataFrame(list(self.mongo.db["ordens_servico"].find({"codigo_ordem": f"{codigo_ordem}", "codigo_cliente": f"{codigo_cliente}"}, {"codigo_ordem": 1, "codigo_cliente": 1, "dt_abertura": 1, "dt_prevista": 1, "dt_efetiva": 1, "_id": 0})))

        if external:
            self.mongo.close()

        return df_ordem_servico

    def valida_cliente(self, codigo_cliente: str=None) -> cliente:
        if self.controller_cliente.verifica_existencia_cliente(codigo_cliente, external=True):
            print(f"O codigo do cliente {codigo_cliente} nao esta cadastrado no sistema")
            return None
        else:
            df_cliente = self.controller_cliente.recupera_cliente(codigo_cliente, external=True)
            return cliente(df_cliente.codigo_cliente.values[0], df_cliente.nome.values[0])
