from conexion.mongo_queries import MongoQueries
import pandas as pd
from pymongo import ASCENDING

class Relatorio:
    def __init__(self):
        pass

    def get_relatorio_cliente(self):
        mongo = MongoQueries()
        mongo.connect()
        query_result = mongo.db["clientes"].find({}, {"codigo_cliente": 1, "nome": 1, "_id": 0}).sort("nome", ASCENDING)
        df_relatorio_clientes = pd.DataFrame(list(query_result))
        mongo.close()
        print(df_relatorio_clientes)
        input("Pressione Enter para sair do relatorio de clientes")

    def get_relatorio_endereco(self):
        mongo = MongoQueries()
        mongo.connect()
        query_result = mongo.db["enderecos"].find({}, {"codigo_cliente": 1, "cep": 1, "logradouro": 1, "numero": 1, "UF": 1, "complemento": 1, "municipio": 1, "_id": 0}).sort("codigo_cliente", ASCENDING)
        df_relatorio_enderecos = pd.DataFrame(list(query_result))
        mongo.close()
        print(df_relatorio_enderecos)
        input("Pressione Enter para sair do relatorio de endereco")

    def get_relatorio_telefone(self):
        mongo = MongoQueries()
        mongo.connect()
        query_result = mongo.db["telefones"].find({}, {"codigo_cliente": 1, "numero": 1, "tipo_telefone": 1,"_id": 0}).sort("codigo_cliente", ASCENDING)
        df_relatorio_telefones = pd.DataFrame(list(query_result))
        mongo.close()
        print(df_relatorio_telefones)
        input("Pressione Enter para sair do relatorio de telefones")

    def get_relatorio_ordem_servico(self):
        mongo = MongoQueries()
        mongo.connect()
        query_result = mongo.db["ordens_servico"].find({}, {"codigo_ordem": 1, "codigo_cliente": 1, "dt_abertura": 1, "dt_prevista": 1, "dt_efetiva": 1, "_id": 0}).sort("dt_abertura", ASCENDING)
        df_relatorio_ordens_servico = pd.DataFrame(list(query_result))
        mongo.close()
        print(df_relatorio_ordens_servico)
        input("Pressione Enter para sair do relatorio de ordem de servico")

    def get_relatorio_servico(self):
        mongo = MongoQueries()
        mongo.connect()
        query_result = mongo.db["servicos"].find({}, {"codigo_ordem": 1, "codigo_cliente": 1, "codigo_servico": 1, "nome": 1, "cat": 1, "vlr_unitario": 1, "tempo": 1, "garantia": 1, "_id": 0 })
        df_relatorio_servicos = pd.DataFrame(list(query_result))
        mongo.close()
        print(df_relatorio_servicos)
        input("Pressione Enter para sair do relatorio de Servico")

    def get_relatorio_cliente_endereco(self):
        mongo = MongoQueries()
        mongo.connect()
        query_result = mongo.db["clientes"].aggregate([{
                              '$lookup': {
                                             'from': 'enderecos',
                                             'localField': 'codigo_cliente',
                                             'foreignField': 'codigo_cliente',
                                             'as': 'ende'
                                         }
                             },
                             {
                              '$unwind':  { 'path': '$ende'}
                             },
                             {
                              '$lookup':{
                                             'from': 'telefones',
                                             'localField': 'codigo_cliente',
                                             'foreignField': 'codigo_cliente',
                                             'as': 'tele'
                                         }
                             },
                             {
                              '$unwind':  { 'path': '$tele'}
                             },
                             {
                              '$project': {'codigo_cliente': 1,
                                           'nome': 1,
                                           'enderecos_codigo_cliente':'$ende.cep',
                                           'tele_codigo_cliente':'$tele.clientes',
                                           'tele_numero':'$tele.numero',
                                           'ende_cep':'$ende.cep',
                                           'ende_logradouro':'$ende.logradouro',  
                                           'ende_municipio':'$ende.municipio',           
                                           'ende_uf':'$ende.uf',    
                                           'ende_numero':'$ende.numero',       
                                           'ende_complemento':'$ende.complemento',
                                           '_id': 0
                                          }
                            }])
        df_relatorio_cliente_endereco = pd.DataFrame(list(query_result))
        mongo.close()
        print(df_relatorio_cliente_endereco)
        input("Pressione Enter para sair do relatorio")