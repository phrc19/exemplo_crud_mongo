import utils.config as config
from utils.splash_screen import SplashScreen
from reports.Relatorio import Relatorio
from controller.controller_servicos import ControllerServico
from controller.controller_clientes import controllercliente
from controller.controller_OrdemServicos import Controller_Ordem_Servicos
from controller.controller_endereco import controller_endereco
from controller.controller_telefone import controller_telefone

tela_inicial = SplashScreen()
relatorio = Relatorio()
ctrl_servico = ControllerServico()
ctrl_cliente = controllercliente()
ctrl_ordem_servico = Controller_Ordem_Servicos()
ctrl_telefone = controller_telefone()
ctrl_endereco = controller_endereco()

def reports(opcao_relatorio: int = 0):
    if opcao_relatorio == 1:
        relatorio.get_relatorio_servico()
    elif opcao_relatorio == 2:
        relatorio.get_relatorio_cliente()
    elif opcao_relatorio == 3:
        relatorio.get_relatorio_ordem_servico()
    elif opcao_relatorio == 4:
        relatorio.get_relatorio_telefone()
    elif opcao_relatorio == 5:
        relatorio.get_relatorio_endereco()
    elif opcao_relatorio == 6:
        relatorio.get_relatorio_cliente_endereco()
    else:
        return

def inserir(opcao_inserir: int = 0):
    if opcao_inserir == 1:
        relatorio.get_relatorio_ordem_servico()
        relatorio.get_relatorio_cliente()
        novo_servico = ctrl_servico.inserir_servico()
    elif opcao_inserir == 2:
        relatorio.get_relatorio_cliente()
        novo_cliente = ctrl_cliente.inserir_cliente()
    elif opcao_inserir == 3:
        relatorio.get_relatorio_cliente()
        relatorio.get_relatorio_ordem_servico()
        relatorio.get_relatorio_servico()
        novo_ordem_servico = ctrl_ordem_servico.inserir_ordem_servico()
    elif opcao_inserir == 4:
        relatorio.get_relatorio_cliente()
        novo_telefone = ctrl_telefone.inserir_telefone()
    elif opcao_inserir == 5:
        relatorio.get_relatorio_cliente()
        novo_endereco = ctrl_endereco.inserir_endereco()


def atualizar(opcao_atualizar: int = 0):
    if opcao_atualizar == 1:
        relatorio.get_relatorio_servico()
        servico_atualizado = ctrl_servico.atualizar_servico()
    elif opcao_atualizar == 2:
        relatorio.get_relatorio_cliente()
        cliente_atualizado = ctrl_cliente.atualizar_cliente()
    elif opcao_atualizar == 3:
        relatorio.get_relatorio_ordem_servico()
        ordem_servico_atualizado = ctrl_ordem_servico.atualizar_ordem_servico()
    elif opcao_atualizar == 4:
        relatorio.get_relatorio_telefone()
        telefone_atualizado = ctrl_telefone.atualizar_telefone()
    elif opcao_atualizar == 5:
        relatorio.get_relatorio_endereco()
        endereco_atualizado = ctrl_endereco.atualizar_endereco()


def excluir(opcao_excluir: int = 0):
    if opcao_excluir == 1:
        relatorio.get_relatorio_servico()
        ctrl_servico.excluir_servico()
    elif opcao_excluir == 2:
        relatorio.get_relatorio_cliente()
        ctrl_cliente.excluir_cliente()
    elif opcao_excluir == 3:
        relatorio.get_relatorio_ordem_servico()
        ctrl_ordem_servico.excluir_ordem_servico()
    elif opcao_excluir == 4:
        relatorio.get_relatorio_telefone()
        ctrl_telefone.excluir_telefone()
    elif opcao_excluir == 5:
        relatorio.get_relatorio_endereco()
        ctrl_endereco.excluir_endereco()

def verifica_existencia_documentos() -> bool:
    contador = 0
    verificador = False
    while contador < 5 and verificador == False:
        if contador == 0 and tela_inicial.get_documents_count(collection_name="enderecos") > 0:
            verificador = True
        elif contador == 1 and tela_inicial.get_documents_count(collection_name="telefones") > 0:
            verificador = True
        elif contador == 2 and tela_inicial.get_documents_count(collection_name="servicos") > 0:
            verificador = True
        elif contador == 3 and tela_inicial.get_documents_count(collection_name="ordens_servico") > 0:
            verificador = True
        elif contador == 4 and tela_inicial.get_documents_count(collection_name="clientes") > 0:
            verificador = True
        contador += 1
    return verificador

def run():
    print(tela_inicial.get_updated_screen())
    config.clear_console()

    while True:
        print(config.MENU_PRINCIPAL)
        opcao = int(input("Escolha uma opção [1-5]: "))
        config.clear_console(1)

        if opcao == 1:  # Relatórios

            print(config.MENU_RELATORIOS)
            opcao_relatorio = int(input("Escolha uma opção [1-9]: "))
            config.clear_console(1)

            reports(opcao_relatorio)

            config.clear_console(1)

        elif opcao == 2:  # Inserir Novos Registros
            escolha = 'S'

            while escolha.upper() == 'S':
                print(config.MENU_ENTIDADES)
                opcao_inserir = int(input("Escolha uma opção [1-5]: "))
                config.clear_console(1)

                inserir(opcao_inserir=opcao_inserir)

                config.clear_console()
                print(tela_inicial.get_updated_screen())
                config.clear_console()
                escolha = input("Deseja continuar inserindo registros? (Digite S para sim e N caso nao queira)")
                while escolha.upper() != 'N' and escolha.upper() != 'S':
                    print(f"A escolha {escolha} e invalida")
                    escolha = input("Deseja continuar inserindo registros? (Digite S para sim e N caso nao queira)")
                    config.clear_console()



        elif opcao == 3:  # Atualizar Registros
            escolha = 'S'

            while escolha.upper() == 'S' and verifica_existencia_documentos() == True:
                print(config.MENU_ENTIDADES)
                opcao_atualizar = int(input("Escolha uma opção [1-5]: "))
                config.clear_console(1)

                atualizar(opcao_atualizar=opcao_atualizar)

                config.clear_console()
                escolha = input("Deseja continuar atualizando registros? (Digite S para sim e N caso nao queira)")
                while escolha.upper() != 'N' and escolha.upper() != 'S':
                    print(f"A escolha {escolha} e invalida")
                    escolha = input("Deseja continuar atualizando registros? (Digite S para sim e N caso nao queira)")
                    config.clear_console()
            if not verifica_existencia_documentos():
                print("As colecoes estao vazias. E impossivel continuar com essa operacao.")
                config.clear_console()

        elif opcao == 4:
            escolha = 'S'

            while escolha.upper() == 'S' and verifica_existencia_documentos() == True:
                print(config.MENU_ENTIDADES)
                opcao_excluir = int(input("Escolha uma opção [1-5]: "))
                config.clear_console(1)

                excluir(opcao_excluir=opcao_excluir)

                config.clear_console()
                print(tela_inicial.get_updated_screen())
                config.clear_console()
                escolha = input("Deseja continuar excluindo registros? (Digite S para sim e N caso nao queira)")
                while escolha.upper() != 'N' and escolha.upper() != 'S':
                    print(f"A escolha {escolha} e invalida")
                    escolha = input("Deseja continuar excluindo registros? (Digite S para sim e N caso nao queira)")
                    config.clear_console()
            if not verifica_existencia_documentos():
                print("As colecoes estao vazias. E impossivel continuar com essa operacao.")
                config.clear_console()

        elif opcao == 5:

            print(tela_inicial.get_updated_screen())
            config.clear_console()
            print("Obrigado por utilizar o nosso sistema.")
            exit(0)

        else:
            print("Opção incorreta.")
            exit(1)


if __name__ == "__main__":
    run()