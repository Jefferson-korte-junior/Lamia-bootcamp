quantidade = int(input('Vai querer ler quantos numeros : '))

soma = 0

for con in range(1, quantidade + 1):
    numero = int(input(f'Digite o {con} numero :'))
    if numero % 2 == 0 and numero > 5:
        soma += numero


print (f'\n A soma dos numeros pares maiores que 5 sao : {soma} \n')
