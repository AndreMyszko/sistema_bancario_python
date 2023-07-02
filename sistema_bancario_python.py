# SISTEMA BANCARIO PYTHON

#funcionalidades:
    # sacar
    # depositar
    # extrato

# deposito:
    # não pode depositar valores negativos para não ter problemas com o saldo

# saque:
    # permitir no maximo 3 saques 
    # cada saque tem valor limitado a R$500 reais

# extrato:
    # deve listar todos os depositos e saques afim de ao final demonstrar o saldo atual da conta.
    # os valores devem ser apresentados neste formato:
        # 1000.45 = R$ 1000.45


#utilizado para armazenar o memento de cada operação e armazenar no 'extrato'
import datetime

#dicionario/string, usada pra valor de input de incialização do programa dentro do laço while
menu = '''
Selecione uma das operacaoes:

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

=> '''

# variaveis e constantes globais instanciadas para programa
saldo = 0
limite = 500
extrato = ''
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)

    if opcao == 'd':
        valor = float(input('Informe valor do deposito: '))

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
            
            print(f'Deposito efetuado no valor de R$ {valor:.2f}')
        else:
            print('Operacao falhou, valor invalido para deposito')

    elif opcao == 's':
        valor = float(input('informe valor do sque: '))

        # verificando se usuario tem saldo para saque
        excedeu_saldo = valor > saldo
        #verifica se saque é menor que 500.00 reais
        excedeu_limite = valor > limite
        #verifica se limite de 3 saques foi excedido
        excedeu_saques = numero_saques >= LIMITE_SAQUES
        if excedeu_saldo:
            print('Operacao falhou, saldo insuficiente')
        elif excedeu_limite:
            print('Operacao falhou, nao e permitido saques acima de R$ 500 reais')
        elif excedeu_saques:
            print('Operacao falhou, nao e permitido mais de 3 saques')
        
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
            print(f'Saque efetuado no valor de R$ {valor:.2f}')
            numero_saques += 1
        
        #caso o input recebido não cai em nehuma das condições previstas
        else:
            print('Operacao falhou, valor invalido para deposito')

    elif opcao == 'e':
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

    #caso selecione a opcao 'q'(sair) o programa sera encerrado atraves do break
    elif opcao == 'q':
        break
    
    #quando input do menu não retorna nenhuma das opções esperadas (d,s,e,q)
    else:
        print('Opcao invalida')

#obs.: saques como '1.999' funcionam, ainda ficam 0.001 no saldo, mas na tela vai mostram como saldo = 'R$ 0.00' por conta do ':.2f'
