# MODELANDO SISTEMA BANCARIO UTILIZANDO PRICIPIOS DE POO

from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime
import textwrap


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._numero = numero
        self._cliente = cliente

        self._saldo = 0
        self._agencia = '0001'
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_valor = valor > saldo

        if excedeu_valor:
            print('[ERROR]: saldo insuficiente')
        elif valor > 0:
            self._saldo -= valor
            print('[SUCCESS]: saque realizado')
            return True
        else:
            print('[ERROR]: valor invalido')

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('[SUCCESS]: deposito realizado')
        else:
            print('[ERROR]: valor invalido')
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500.00, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([
            transacao for transacao in self.historico.transacoes
            if transacao['tipo'] == Saque.__name__
        ])
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print('[ERROR]: excedeu limite de R$ 500.00 por saque')
        elif excedeu_saques:
            print('[ERROR]: excedeu limite de 3 saques')
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f'''\
            agencia:\t{self.agencia}
            conta_corrente:\t{self.numero}
            titular:\t{self.cliente.nome}
        '''


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'data': datetime.now().strftime('%d/%m/%Y - %H:%M:%S'),
        })


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
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


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes
                          if cliente.cpf == cpf]

    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('[ERROR] conta não encontrada')
        return

    return cliente.contas[0]


def depositar(clientes):
    cpf = input('informe CPF: ')

    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print('[ERROR] cliente nao encontrado')
        return

    valor = float(input('informe valor do deposito: '))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input('informe CPF: ')

    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print('[ERROR] cliente não encontrado')
        return

    valor = float(input('informe valor do deposito: '))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input('informe CPF: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('[ERROR] cliente não encontrado')
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print('===============EXTRATO===============')
    transacoes = conta.historico.transacoes

    extrato = ''
    if not transacoes:
        extrato = 'nao existem transacoes'
    else:
        for t in transacoes:
            extrato += f'\n{t["tipo"]}: {t["data"]}\n\tR$ {t["valor"]:.2f}'
    print(extrato)
    print(
        f'Saldo: {datetime.now().strftime(" %d/%m/%Y - %H:%M:%S")}\n\tR$ {conta.saldo:.2f}')
    print('=====================================')


def criar_cliente(clientes):
    cpf = input('informe CPF: ')
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print('[ERROR] CPF ja cadastrado')
        return

    nome = input('informe o nome do cliente: ')
    data_nascimento = input('informe a data de nascimento (dd-mm-yyyy): ')
    endereco = input(
        'informe endereco do cliente (logradoro, nro, bairro, cidade, sigla, estado): ')

    cliente = PessoaFisica(
        nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print('[SUCCESS] cliente registrado')


def criar_conta(numero_conta, clientes, contas):
    cpf = input('informe CPF: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('[ERROR] cliente nao encontrado')
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print('[SUCCESS] conta criada')


def listar_contas(contas):
    for conta in contas:
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 'd':
            depositar(clientes)

        elif opcao == 's':
            sacar(clientes)

        elif opcao == 'e':
            exibir_extrato(clientes)

        elif opcao == 'nu':
            criar_cliente(clientes)

        elif opcao == 'nc':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == 'lc':
            listar_contas(contas)

        elif opcao == 'q':
            break


main()
