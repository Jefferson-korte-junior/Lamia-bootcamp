KG_maca = float(input('quantos Kg de macas voce vai querer levar : ')) #pede ao usuario quantos KG de maca vai querer
KG_morango = float(input ('Quantos kg de morango vai quererlevar : ')) #pede ao usuario quantos KG de morango vai querer

um_kg_maca =2.50 #estou definindo quanto vai ser o Kg da maca 
um_kg_morango = 1.80 ##estou definindo quanto vai ser o Kg do morango 

valor_pagar = KG_maca * um_kg_maca + KG_morango * um_kg_morango # calcula qual sera o valor a pagar


if KG_maca >= 8 and KG_morango >= 8: #se o usuario comprar mais de 8 Kg de maca e morango recebera um desconto de 10 porcento
        valor_desconto = (valor_pagar * 10/100) 
elif valor_pagar >= 25 : #se o valor a pagar dar mais de 25 reais, o usuario recebe um desconto
        valor_desconto =  valor_pagar * 10/100
else:
        valor_desconto = 0

valor_final = valor_pagar -  valor_desconto #calcula o valor final a pagar junto co o desconto

print (f'o valor a pagar sem desconto: RS {valor_pagar}')
print (f'O valor do deconto: RS {valor_desconto} \n')

print (f'O valor final a pagar deu {valor_final:2f}') #imprimi o valor final na tela




