# Exercici 1
#
# tauler = [['-', '-', '-'],
#           ['-', '-', '-'],
#           ['-', '-', '-']]
#
# tauler[1][1] = 'X'
# tauler[0][0] = 'O'
#
# for fila in tauler:
#     print(fila)
#
# # Exercici 2
#
despeses = [[10, 5, 3],  # Despeses persona 1
            [15, 2, 8],  # DEspeses persona 2
            [7, 7, 7]]

persona1 = despeses[0][0] + despeses[0][1] + despeses[0][2]
print(persona1)

for persona in despeses:
    suma = 0
    for despesa in persona:
        suma += despesa
    print("La persona ", persona, " ha gastat ", suma)

for i in range(len(despeses)):
    suma = 0
    for j in range(len(despeses[i])):
        suma += despeses[i][j]
    print("La persona ", i, " ha gastat ", suma)

suma = 0
for i in range(len(despeses)):
    suma += despeses[i][0]
