mapa = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0]]

fila = int(input("Fila: "))
columna = int(input("Columna: "))


# if mapa[fila-1][columna] == 1:
#         minas +=1
#
# mapa[fila+1][columna]
# mapa[fila][columna+1]
# mapa[fila][columna-1]
# mapa[fila+1][columna+1]
# mapa[fila-1][columna+1]
# mapa[fila+1][columna-1]
# mapa[fila-1][columna-1]

minas = 0
for i in range(fila-1, fila+2):
        for j in range(columna-1, columna+2):
                if mapa[i][j] == 1:
                        minas += 1


print(minas)


