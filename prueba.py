# contador = 1
# while contador <= 5:
#     print("Iteración: ",contador)
#     contador += 1
    
# suma = 0
# while suma < 100:
#     numero = int(input("Introduce un número: "))
#     suma += numero
#     print("Suma actual: ",suma)
    
    
    
# continuar = True
# while continuar:
#     numero = int(input("Introduce un número (0 para terminar): "))
#     if numero == 0:
#         continuar = False
#     else:
#         print("Número introducido:", numero)


a = 943
continuar = True
n = 0
b = 0
c = 0
while continuar:
    d = a % 10
    a = a // 10
    n = n * 10 + d	
    if d % 2 == 0:
        b+=1
    else:
        c+=1
    if a == 0:
        continuar = False
print(n)
print(b)
print(c)

