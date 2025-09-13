from datetime import datetime

#funções bancárias moduladas
def depositar(saldo, valor, extrato, /): 
    """Função de depósito (args posicionais apenas)."""
    if valor > 0:
        saldo += valor
        extrato += f"\nDepósito: R$ {valor:.2f}"
        print("\nDepósito realizado!")
    else:
        print("\nDepósito falhou! O valor é inválido.")
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """Função de saque (args apenas nomeados)."""
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\nOperação falhou! Saldo suficiente.")
    elif excedeu_limite:
        print("\nOperação falhou! Valor do saque excede o limite.")
    elif excedeu_saques:
        print("\nOperação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"\nSaque: R$ {valor:.2f}"
        numero_saques += 1
        print("\nSaque realizado!")
    else:
        print("\nOperação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    """Função de extrato (positional + keyword)."""
    print("\n=========== EXTRATO ===========")
    print("Sem movimentações." if not extrato else extrato)
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("================================")


def cadastrar_usuario(usuarios): #nova função de cadastro de usuário
    cpf = input("Informe o CPF (números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nJá existe usuário com esse CPF.")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nº - bairro - cidade/UF): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print("\nUsuário cadastrado!")


def filtrar_usuario(cpf, usuarios): #função de filtro 
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def cadastrar_conta(agencia, numero_conta, usuarios, contas): #nova função para criação de conta
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        conta = {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
        contas.append(conta)
        print("\nConta criada com sucesso!")
        return conta

    print("\nUsuário não encontrado.")


def listar_contas(contas):
    for conta in contas:
        linha = f"""
Agência: {conta['agencia']}
Número: {conta['numero_conta']}
Titular: {conta['usuario']['nome']}
"""
        print("=" * 30)
        print(linha)


def excluir_conta(contas): #nova função para exclusão de conta
    numero_conta = int(input("Informe o número da conta que deseja excluir: "))
    conta = next((c for c in contas if c["numero_conta"] == numero_conta), None)

    if conta:
        contas.remove(conta)
        print("\nConta excluída.")
    else:
        print("\nConta não encontrada.")

def main(): 
    AGENCIA = "0001"
    LIMITE_SAQUES = 3
    usuarios = []
    contas = []
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0

    menu = """
\n=========== MENU ===========
[0] Depositar
[1] Sacar
[2] Extrato
[3] Novo Usuário
[4] Nova Conta
[5] Listar Contas
[6] Excluir Conta
[7] Sair
-> """

    while True:
        opcao = input(menu)

        if opcao == "0":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "1":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == "2":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "3":
            cadastrar_usuario(usuarios)

        elif opcao == "4":
            numero_conta = len(contas) + 1
            conta = cadastrar_conta(AGENCIA, numero_conta, usuarios, contas)

        elif opcao == "5":
            listar_contas(contas)

        elif opcao == "6":
            excluir_conta(contas)

        elif opcao == "7":
            print("\n✅ Saindo do sistema...")
            break

        else:
            print("\n❌ Operação inválida! Tente novamente.")


if __name__ == "__main__":
    main()
