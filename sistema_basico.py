menu = """

[0] Depositar
[1] Sacar
[2] Extrato
[3] Sair

-> """

saldo = 0
limite = 500
extrato = 'Não há extratos.'
numero_saques = 0
limite_saques = 3
deposito = 0

while True:
    opcao = input(menu)
    
    if opcao == '0': #operação de depósito
        deposito = int(input('Qual o valor que você deseja depositar? '))
        if deposito > 0: #regra: apenas valores positivos
            print('Valor depositado com sucesso!')
            saldo = saldo + deposito
            extrato = f"\nDepósito: R$ {deposito:.2f}" 
        else:
            print('Valor inválido. Tente novamente.')
        continue
    
    elif opcao == '1': #operação de saque
        saque = int(input('Qual o valor que você deseja sacar? '))
        if saque > saldo or saque > limite or numero_saques >= limite_saques or saque < 0: #regras: limite de 500 reais por saque e impossibilidade de saque maior que saldo
            print('Não foi possível realizar a opção de saque.')
        else:
            numero_saques += 1
            saldo -= saque
            print('Saque realizado com sucesso!')
            extrato += f"\nSaque: R$ {saque:.2f}"
        continue

    elif opcao == '2': #operação de extrato
        print('Este é o extrato da sua conta: ' + extrato)
        print('Saldo final: R$' + str(saldo))
        continue
    
    elif opcao == '3':
        print('Saindo do sistema...')
        break
    else:
        print("Operação inválida! Por favor, selecione novamente a operação desejada.")