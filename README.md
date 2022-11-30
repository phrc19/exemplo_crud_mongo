# exemplo_crud_mongo


Exemplo de Sistema em Python fazendo CRUD no MongoDB Esse sistema de exemplo é composto por um conjunto de coleções (collections) que representam Ordens de serviço e serviço de telefonia e internet, contendo coleções como: clientes, endereço, ordens serviço, serviço e telefone.

O sistema exige que as coleções existam, então basta executar o script Python a seguir para criação das coleções e preenchimento de dados de exemplos:

~$ python createCollectionsAndData.py Atenção: tendo em vista que esse projeto é continuidade do example_crud_oracle , é importante que as tabelas do Oracle existam e estejam instaladas, pois o script createCollectionsAndData.py irá realizar uma consulta em cada uma das tabelas e preencher as collections com os novos documentos .

Para executar o sistema basta executar o script Python a seguir:

~$ python principal.py Organização diagramas : Nesse diretório está o diagrama relacional (lógico) do sistema. O sistema possui cinco entidades: CLIENTES, ENDEREÇO, TELEFONE, ORDEM DE SERVIÇO E SERVIÇO src : Nesse diretório estão os scripts do sistema conexão : Nesse repositório encontra-se o módulo de conexão com o banco de dados Oracle e o módulo de conexão com o banco de dados Mongo . Esses módulos possuem algumas funcionalidades úteis para execução de instruções. O módulo do Oracle permite obter como resultado das consultas JSON, Matriz e Pandas DataFrame. Já o módulo do Mongo apenas realiza a conexão, os métodos CRUD e de recuperação de dados são aplicados diretamente nos objetos controladores ( Controladores ) e no objeto de Relatório ( relatório ). Exemplo de uso para consultas simples no MONGO:

def init (self): self.mongo = MongoQueries()

def inserir_cliente(self) -> cliente:
    self.mongo.connect()

    codigo_cliente = input("Insira o codigo do cliente: ")

    if self.verifica_existencia_cliente(codigo_cliente):
        nome = input("Digite o nome do cliente: ")
        self.mongo.db["clientes"].insert_one({"codigo_cliente": codigo_cliente, "nome": nome})
        df_cliente = self.recupera_cliente(codigo_cliente)
        novo_cliente = cliente(df_cliente.codigo_cliente.values[0], df_cliente.nome.values[0])
        print(novo_cliente.to_string())
        self.mongo.close()
        return novo_cliente
    else:
        self.mongo.close()
        print(f"O codigo do cliente {codigo_cliente} ja foi cadastrado")
        return None
Exemplo de uso para alteração de registros no MONGO

def atualizar_cliente(self) -> cliente: self.mongo.connect()

    codigo_cliente = int(input("Insira o codigo do cliente: "))

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
Exemplo de utilização para conexão no Mongo; ``` # Importa o módulo MongoQueries from conexion.mongo_queries import MongoQueries

  # Cria o objeto MongoQueries
  mongo = MongoQueries()

  # Realiza a conexão com o Mongo
  mongo.connect()



  # Fecha a conexão com o Mong
  mongo.close()
  ```
    - Exemplo de criação de um documento no Mongo:
  ```
  from conexion.mongo_queries import MongoQueries
  import pandas as pd
  
  # Cria o objeto MongoQueries
  mongo = MongoQueries()

  # Realiza a conexão com o Mongo
  mongo.connect()

  nome = input("Digite o nome do cliente: ")
        self.mongo.db["clientes"].insert_one({"codigo_cliente": codigo_cliente, "nome": nome})
        df_cliente = self.recupera_cliente(codigo_cliente)
        novo_cliente = cliente(df_cliente.codigo_cliente.values[0], df_cliente.nome.values[0])
        print(novo_cliente.to_string())
        self.mongo.close()
        return novo_cliente

  # Fecha a conexão com o Mong
  mongo.close()
  ```
*controller : Nesse diretório encontram-sem as classes controladoras, responsáveis ​​por realizar inserção, alteração e exclusão dos registros das tabelas. *model : Nesse diretório encontre-ser as classes das entidades descritas no diagrama relacional *reports Nesse diretório encontre-se a classe responsável por gerar todos os relatório do sistema *utils : Nesse diretório encontre-se scripts de configuração e automatização da tela de informações iniciais *createCollectionsAndData.py : Script responsável por criar as tabelas e registros fictícios. Esse script deve ser executado antes do script principal.py para gerar as tabelas, caso não execute os scripts diretamente no SQL Developer ou em algum outro IDE de acesso ao Banco de Dados. *principal.py : Script responsável por ser a interface entre o usuário e os módulos de acesso ao Banco de Dados. Deve ser executado após a criação das tábuas. ###Bibliotecas Utilizadas

requisitos.txt :pip install -r requisitos.txt
