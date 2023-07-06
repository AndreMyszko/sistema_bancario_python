# OTIMIZANDO SISTEMA BANCARIO COM FUNCOES

import datetime
import textwrap

def menu():
    #dicionario/string, usada pra valor de input de incialização do programa dentro do laço while
    menu = '''
    Selecione uma das operacaoes:

        [d] \tDepositar
        [s] \tSacar
        [e] \tExtrato
        [nc]\tNova Conta
        [lc]\tListar Contas
        [nu]\tNovo Usuario
        [q] \tSair

    => '''
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
#atencao na '/' ao final da sobrecarga..
    # evita depositos de valores negativo:
    if valor > 0:
        saldo += valor
        #pegar data atual formatada
        data_atual = datetime.datetime.now()
        data_formatada = data_atual.strftime('%d/%m/%Y - %H:%M:%S')
        #dia da semana em texto('monday', 'sunday'...etc)
        dia_semana = data_atual.strftime('  %A')
        #concatena extrato
        extrato += f'{dia_semana} - {data_formatada}\ndeposito: .............................. R$+{valor:.2f}\n'
        print(f'[SUCCESS] Deposito efetuado no valor de R$ {valor:.2f}')
    else:
        print('[ERROR] Operacao falhou, valor invalido para deposito')

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
        # verificando se usuario tem saldo para saque
        excedeu_saldo = valor > saldo
        #verifica se saque é menor que 500.00 reais
        excedeu_limite = valor > limite
        #verifica se limite de 3 saques foi excedido
        excedeu_saques = numero_saques >= limite_saques
        if excedeu_saldo:
            print('[ERROR] Saldo insuficiente')
        elif excedeu_limite:
            print('[ERROR] Nao é permitido saques acima de R$ 500 reais')
        elif excedeu_saques:
            print('[ERROR] Limite de 3 saques atingido')
        #caso o valor do saque seja um float maior que 0 e nao caia nas condições anteriores
        elif valor > 0:
            saldo -= valor
            #pegar data atual formatada
            data_atual = datetime.datetime.now()
            data_formatada = data_atual.strftime('%d/%m/%Y - %H:%M:%S')
            #dia da semana em texto('monday', 'sunday'...etc)
            dia_semana = data_atual.strftime('  %A')
            #concatena extrato
            extrato += f'{dia_semana} - {data_formatada}\nsaque: ................................. R$-{valor:.2f}\n'
            print(f'[SUCCESS] Saque efetuado no valor de R$ {valor:.2f}')
            numero_saques += 1  
        #caso o input recebido não cai em nehuma das condições previstas
        else:
            print('[ERROR] valor invalido')

        return saldo, extrato, numero_saques

def exibir_extrato(saldo, /,*, extrato):
    #imprime o extrato recebendo o valor de:
    #'extrato'(strings concatenadas a cada operacao de saque ou deposito)
        #'saldo'(valor float alterado a cada saque(saldo-=valor) ou deposito(saldo+=valor))
        #extrato é uma string que é concatenada sempre que um saque ou deposito é feito: (extrato += f'saque ou deposito' \n')
    print('==============================EXTRATO===============================\ndia-semana  |  dia   |   hrs/min/seg')
    #nesta linha muita elegancia
        #caso não haja 'inf not' extrato(str('')/FALSE) imprime a msg
        #caso haja 'else' imprime o extrato
    print('Nao houve movimentacao.' if not extrato else extrato)
    #imprime o valor do saldo

    #pegar data atual formatada
    data_atual = datetime.datetime.now()
    data_formatada = data_atual.strftime('%d/%m/%Y - %H:%M:%S')
    #dia da semana em texto('monday', 'sunday'...etc)
    dia_semana = data_atual.strftime('  %A')
    
    print(
        f'\n{dia_semana} - {data_formatada}\nsaldo: ................................. R$ {saldo:.2f}')
    print('====================================================================')

def criar_usuario(usuarios):
    cpf = input('informe CPF (apenas numeros): ')
    # chama a funcao 'filtrar_usuario'(entra em outra funcao) responsavel por verificar na lista 'usuarios' se o 'cpf' ja existe
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print('\n[ERROR] ja existe usuario com este CPF')
        return
    nome = input('informe nome completo do usuario: ')
    data_nascimento = input('informe data de nascimento do usuario (dd-mm-aaaa): ')
    endereco = input('Informe endereco (logradouro, nro - bairro - cidade/sigle estado): ')
    usuarios.append({'nome':nome, 'data_nascimento':data_nascimento, 'cpf':cpf, 'endereco':endereco})
    print(f'\n[SUCCESS] Usuario criado com sucesso:\n{nome, data_nascimento,cpf,endereco}\n')

def filtrar_usuario(cpf, usuarios):
    # este filtro é muito poderoso e com muita logica imbutida, o filtro de usuario pela lista.usuarios['cpf'] 
    # anilisar com toda calma do mundo os params passados e o retorno condifional
    usuarios_fitrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuarios_fitrados[0] if usuarios_fitrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('informe seu CPF de usuario cadastrado (apenas numeros): ')
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print(f'[SUCCESS] Conta criada com sucesso:\n{usuario, agencia, numero_conta}')
        return {'agencia':agencia, 'numero_conta':numero_conta, 'usuario': usuario}
    else:
        print('[ERROR] usuario não encontrado, operacao encerrada')
    #quando o return é 'return None', não precisa declarar, o compilador ja set 'None' como default, colocado apenas para ilustrar..
    return None

def listar_contas(contas):
    print('\nLista de contas:\n')

    if contas:
        for conta in contas:
            if conta:
                linha = f'''\
                agencia:\t{conta['agencia']}
                C/C:\t\t{conta['numero_conta']}
                Titular:\t{conta['usuario']['nome']} 
                '''
                print(textwrap.dedent(linha))
                print('------------------------')
    else: 
        print('Nenhuma conta encontrada')

def main():
    #metodo main é o metodo chamado assim que o código é executado, é o metodo principal do programa
    #variaveis 'globais' digamos, que são iniciadas junto com o metodo main (no inicio do progrma)
    LIMITE_SAQUES = 3
    AGENCIA = '0001'
    saldo = 0.00
    limite = 500.00
    extrato = ''
    numero_saques = 0.00
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 'd':
            valor = float(input('valor do deposito: '))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == 's':
            valor = float(input('valor do saque: '))

            saldo, extrato, numero_saques = sacar(
                saldo = saldo,
                valor = valor,
                extrato = extrato,
                limite = limite,
                numero_saques = numero_saques,
                limite_saques = LIMITE_SAQUES,
            )

        elif opcao == 'e':
            exibir_extrato(saldo, extrato = extrato)

        elif opcao == 'nu':
            criar_usuario(usuarios)

        elif opcao == 'nc':
            # somar mais um não éboa pratica, só funciona neste exemplo porque não existe a opção de excluir
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
        
        elif opcao == 'lc':
            listar_contas(contas)

        elif opcao == 'q':
        #caso selecione a opcao 'q'(sair) o programa sera encerrado atraves do break
            print('\n[SUCCESS] Sistema encerrado\n')
            break
            
        else:
        #quando input do menu não retorna nenhuma das opções esperadas (d,s,e,q,nu,nc... etc)
            print('[ERROR] Opcao invalida')   

    #obs.: saques como '1.999' funcionam, ainda ficam 0.001 no saldo, mas na tela vai mostram como saldo = 'R$ 0.00' por conta do ':.2f'

main()