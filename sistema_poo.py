from datetime import datetime, date
import textwrap
from abc import ABC, abstractmethod, abstractproperty

class Transacao:
    def registrar(self, conta):
        raise NotImplementedError("O método registrar deve ser implementado.")


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor > 0:
            conta._saldo += self.valor
            conta.historico.adicionar_transacao(self)
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! Valor inválido. @@@")


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor > conta._saldo:
            print("\n@@@ Saldo insuficiente! @@@")
        elif self.valor > conta.limite:
            print("\n@@@ Valor do saque excede o limite. @@@")
        elif conta.numero_saques >= conta.limite_saques:
            print("\n@@@ Número máximo de saques excedido. @@@")
        elif self.valor > 0:
            conta._saldo -= self.valor
            conta.numero_saques += 1
            conta.historico.adicionar_transacao(self)
            print("\n=== Saque realizado com sucesso! ===")
        else:
            print("\n@@@ Valor inválido. @@@")


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

    def exibir(self, saldo):
        print("\n================ EXTRATO ================")
        if not self.transacoes:
            print("Não foram realizadas movimentações.")
        else:
            for t in self.transacoes:
                tipo = t.__class__.__name__
                print(f"{tipo}:\tR$ {t.valor:.2f}")
        print(f"\nSaldo:\tR$ {saldo:.2f}")
        print("=========================================")


class Conta:
    def __init__(self, cliente, numero, agencia="0001"):
        self._saldo = 0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def saldo(self):
        return self._saldo

    def nova_conta(cliente, numero):
        return Conta(cliente, numero)

    def depositar(self, valor):
        transacao = Deposito(valor)
        transacao.registrar(self)

    def sacar(self, valor):
        transacao = Saque(valor)
        transacao.registrar(self)


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0


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


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            cpf = input("Informe o CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            valor = float(input("Informe o valor do depósito: "))
            cliente.contas[0].depositar(valor)

        elif opcao == "s":
            cpf = input("Informe o CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            valor = float(input("Informe o valor do saque: "))
            cliente.contas[0].sacar(valor)

        elif opcao == "e":
            cpf = input("Informe o CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            conta = cliente.contas[0]
            conta.historico.exibir(conta.saldo())

        elif opcao == "nu":
            nome = input("Nome: ")
            data_nascimento = input("Data nascimento (dd-mm-aaaa): ")
            cpf = input("CPF: ")
            endereco = input("Endereço: ")

            cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
            clientes.append(cliente)

            print("\n=== Usuário criado com sucesso! ===")

        elif opcao == "nc":
            cpf = input("Informe o CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            numero_conta = len(contas) + 1
            conta = ContaCorrente(cliente, numero_conta)
            cliente.adicionar_conta(conta)
            contas.append(conta)

            print("\n=== Conta criada com sucesso! ===")

        elif opcao == "lc":
            for conta in contas:
                print("=" * 100)
                print(f"Agência:\t{conta.agencia}")
                print(f"C/C:\t\t{conta.numero}")
                print(f"Titular:\t{conta.cliente.nome}")

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
