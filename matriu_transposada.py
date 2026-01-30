matriu = [
    [1, 2, 3],
    [4, 5, 6]
]

transposada = []

for i in range(len(matriu[0])): #columna
    nova_fila = []
    for j in range(len(matriu)): #fila
        nova_fila.append(matriu[j][i])
    transposada.append(nova_fila)

for fila in transposada:
    print(fila)