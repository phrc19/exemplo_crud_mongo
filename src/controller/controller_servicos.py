import pandas as pd
from model.cliente import cliente
from model.ordem_servico import OrdemServico
from model.servico import Servico
from controller.controller_clientes import controllercliente
from controller.controller_OrdemServicos import Controller_Ordem_Servicos
from conexion.mongo_queries import MongoQueries

class ControllerServico:

    #Cria uma nova conexão com o banco que permite alteração
    def __init__(self):
        self.mongo = MongoQueries()
        self.controller_cliente = controllercliente()
        self.controller_ordem_servico = Controller_Ordem_Servicos()

    def inserir_servico(self) -> Servico:
        self.mongo.connect()
        # Solicita ao usuario o novo codigo do cliente para o servico, a ordem de servico que sera incluido, o codigo do servico que sera incluido
        codigo_cliente = str(input("Insira o codigo do cliente referente ao servico que sera incluido: "))
        cliente = self.valida_cliente(codigo_cliente)
        if cliente is None:
            return None
        else:
            codigo_ordem = str(input("Insira a ordem de servico referente ao servico que sera incluido: "))
            servico = self.valida_ordem_servico(codigo_ordem, codigo_cliente)
            if servico is None:
                return None
            else:
                codigo_servico = str(input("Insira o codigo do servico que sera incluido: "))
                if self.verifica_existencia_servico(codigo_servico, codigo_ordem, codigo_cliente):
                    # solicita ao usuario o nome do servico
                    nome = str(input("Insira o nome do servico: "))
                    # Solicita a categoria do servico
                    cat = str(input("Insira o categoria do servico: "))
                    # solicita ao usuario o valor do servico
                    valor_unitario = str(input("Insira o valor unitario: "))
                    # solicita ao usuario o tempo de execucao
                    tempo_execucao = str(input("insira o tempo de execucao: "))
                    # solicita ao usuario a garantia do servico
                    garantia = str(input("Insira a garantia do servico: "))
                    self.mongo.db["servicos"].insert_one({"codigo_servico": f"{codigo_servico}", "codigo_ordem": f"{codigo_ordem}", "codigo_cliente": f"{codigo_cliente}", "nome": f"{nome}", "cat": f"{cat}", "vlr_unitario": f"{valor_unitario}", "tempo_execucao": f"{tempo_execucao}", "garantia": f"{garantia}"})
                    df_servico = self.recupera_servico(codigo_servico, codigo_ordem, codigo_cliente)
                    novo_servico = Servico(df_servico.codigo_servico.values[0], df_servico.codigo_ordem.values[0], df_servico.codigo_cliente.values[0], df_servico.nome.values[0], df_servico.cat.values[0], df_servico.vlr_unitario.values[0], df_servico.tempo_execucao.values[0], df_servico.garantia.values[0])
                    print(novo_servico.to_string())
                    self.mongo.close()
                    return novo_servico
                else:
                    self.mongo.close()
                    print(f"O codigo do servico {codigo_servico} ja esta cadastrado no sistema")
                    return None

    def atualizar_servico(self) -> Servico:
        self.mongo.connect()
        # Solicita ao usuario o novo codigo do cliente para o servico, a ordem de servico que sera incluido, o codigo do servico que sera incluido
        codigo_cliente = str(input("Insira o codigo do cliente referente ao servico: "))
        cliente = self.valida_cliente(codigo_cliente)
        if cliente is None:
            return None
        else:
            codigo_ordem = str(input("Insira a ordem de servico referente ao servico: "))
            servico = self.valida_ordem_servico(codigo_ordem, codigo_cliente)
            if servico is None:
                return None
            else:
                codigo_servico = str(input("Insira o codigo do servico que sera atualizado: "))
                if not self.verifica_existencia_servico(codigo_servico, codigo_ordem, codigo_cliente):
                    # solicita ao usuario o nome do servico
                    novo_nome = str(input("Insira o nome do servico atualizado: "))
                    # Solicita a categoria do servico
                    novo_cat = str(input("Insira o categoria do servico atualizado: "))
                    # solicita ao usuario o valor do servico
                    novo_valor_unitario = str(input("Insira o valor unitario do servico atualizado: "))
                    # solicita ao usuario o tempo de execucao
                    novo_tempo_execucao = str(input("insira o tempo de execucao do servico atualizado: "))
                    # solicita ao usuario a garantia do servico
                    novo_garantia = str(input("Insira a garantia do servico atualizado: "))
                    self.mongo.db["servicos"].update_one({"codigo_servico": f"{codigo_servico}"}, {"$set": {"nome": f"{novo_nome}", "cat": f"{novo_cat}", "vlr_unitario": f"{novo_valor_unitario}", "tempo_execucao": f"{novo_tempo_execucao}", "garantia": f"{novo_garantia}"}})
                    df_servico = self.recupera_servico(codigo_servico, codigo_ordem, codigo_cliente)
                    servico_atualizado = Servico(df_servico.codigo_servico.values[0], df_servico.codigo_ordem.values[0], df_servico.codigo_cliente.values[0], df_servico.nome.values[0], df_servico.cat.values[0], df_servico.vlr_unitario.values[0], df_servico.tempo_execucao.values[0], df_servico.garantia.values[0])
                    print(servico_atualizado.to_string())
                    self.mongo.close()
                    return servico_atualizado
                else:
                    self.mongo.close()
                    print(f"O codigo do servico {codigo_servico} ja esta cadastrado no sistema")
                    return None

    def excluir_servico(self):
        self.mongo.connect()
        # Solicita ao usuario o novo codigo do cliente para o servico, a ordem de servico que sera incluido, o codigo do servico que sera incluido
        codigo_cliente = str(input("Insira o codigo do cliente referente ao servico: "))
        cliente = self.valida_cliente(codigo_cliente)
        if cliente is None:
            return None
        else:
            codigo_ordem = str(input("Insira a ordem de servico referente ao servico: "))
            servico = self.valida_ordem_servico(codigo_ordem, codigo_cliente)
            if servico is None:
                return None
            else:
                codigo_servico = str(input("Insira o codigo do servico que sera excluido: "))
                if not self.verifica_existencia_servico(codigo_servico, codigo_ordem, codigo_cliente):
                    escolha = input(f"Tem certeza que deseja remover o registro do servico {codigo_servico}? (Digite S para continuar ou N para cancelar a operacao)")
                    while escolha.upper() != 'S' and escolha.upper() != 'N':
                        print(f"A escolha {escolha} e invalida")
                        escolha = input(f"Tem certeza que deseja remover o registro do servico {codigo_servico}? (Digite S para continuar ou N para cancelar a operacao)")
                    if escolha.upper() == 'S':
                        df_servico = self.recupera_servico(codigo_servico, codigo_ordem, codigo_cliente)
                        self.mongo.db["servicos"].delete_one({"codigo_servico": f"{codigo_servico}"})
                        servico_excluido = Servico(df_servico.codigo_servico.values[0], df_servico.codigo_ordem.values[0], df_servico.codigo_cliente.values[0], df_servico.nome.values[0], df_servico.cat.values[0], df_servico.vlr_unitario.values[0], df_servico.tempo_execucao.values[0], df_servico.garantia.values[0])
                        self.mongo.close()
                        print("Servico excluido com sucesso")
                        print(servico_excluido.to_string())
                    else:
                        self.mongo.close()
                        print(f"O codigo de servico {codigo_servico} nao existe")

    def verifica_existencia_servico(self, codigo_servico: str=None, codigo_ordem: str=None, codigo_cliente: str=None, external: bool=False) -> bool:
        if external:
            self.mongo.connect()

        df_servico = pd.DataFrame(self.mongo.db["servicos"].find({"codigo_servico": f"{codigo_servico}", "codigo_ordem": f"{codigo_ordem}", "codigo_cliente": f"{codigo_cliente}"}, {"codigo_servico": 1, "codigo_ordem": 1, "codigo_cliente": 1, "nome": 1, "cat": 1, "vlr_unitario": 1, "tempo_execucao": 1, "garantia": 1, "_id": 0}))

        if external:
            self.mongo.close()

        return df_servico.empty

    def recupera_servico(self, codigo_servico: str=None, codigo_ordem: str=None, codigo_cliente: str=None, external: bool=False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        df_servico = pd.DataFrame(list(self.mongo.db["servicos"].find({"codigo_servico": f"{codigo_servico}", "codigo_ordem": f"{codigo_ordem}", "codigo_cliente": f"{codigo_cliente}"}, {"codigo_servico": 1, "codigo_ordem": 1, "codigo_cliente": 1, "nome": 1, "cat": 1, "vlr_unitario": 1, "tempo_execucao": 1, "garantia": 1, "_id": 0})))

        if external:
            self.mongo.close()

        return df_servico

    def valida_cliente(self, codigo_cliente: str=None) -> cliente:
        if self.controller_cliente.verifica_existencia_cliente(codigo_cliente, external=True):
            print(f"O codigo do cliente {codigo_cliente} nao esta cadastrado no sistema")
            return None
        else:
            df_cliente = self.controller_cliente.recupera_cliente(codigo_cliente, external=True)
            return cliente(df_cliente.codigo_cliente.values[0], df_cliente.nome.values[0])

    def valida_ordem_servico(self, codigo_ordem: str=None, codigo_cliente: str=None) -> OrdemServico:
        if self.controller_ordem_servico.verifica_existencia_ordem_servico(codigo_ordem, codigo_cliente, external=True):
            print(f"O codigo da ordem de servico {codigo_ordem} nao esta cadastrado no sistema")
            return None
        else:
            df_ordem_servico = self.controller_ordem_servico.recupera_ordem_servico(codigo_ordem, codigo_cliente, external=True)
            return OrdemServico(df_ordem_servico.codigo_ordem.values[0], df_ordem_servico.codigo_cliente.values[0], df_ordem_servico.dt_abertura.values[0], df_ordem_servico.dt_prevista.values[0], df_ordem_servico.dt_efetiva.values[0])
