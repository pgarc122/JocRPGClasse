jugador = {
    'x' : 0,
    'y' : 0
}

jugador['x'] = 2
jugador['y'] = 4

jugador['x'] += 1
jugador['x'] = jugador['x'] + 1  ##print Identic al de dalt

print("La posició x del jugador és ", jugador['x'])
print("La posició y del jugador és ", jugador['y'])
# print("Això provoca un error (KEY_ERROR) perque la clau r no existeix", jugador['r'])


