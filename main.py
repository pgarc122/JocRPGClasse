import pygame

# --- 1. CONFIGURACIÓ I COLORS ---
pygame.init()
MIDA_RAJOLA = 60
AMPLADA_MAPA, ALCADA_MAPA = 12, 6
pantalla = pygame.display.set_mode((AMPLADA_MAPA * MIDA_RAJOLA, ALCADA_MAPA * MIDA_RAJOLA))
pygame.display.set_caption("Projecte: El Laberint")
rellotge = pygame.time.Clock()

COLORS = {
    'terra': (60, 50, 40),
    'mur': (100, 100, 110),
    'aigua': (60, 160, 220),
    'jugador': (230, 50, 50),
    'clau': (255, 215, 0),
    'porta': (139, 69, 19),
    'final': (138, 43, 226)
}

# Constants del joc
TERRA = 0
MUR = 1
AIGUA = 2
CLAU = 3
PORTA = 4
FINAL = 9

# --- 2. DADES DEL JOC (Aquí els alumnes han de dissenyar) ---

# TODO: Dissenyeu el vostre mapa (0=terra, 1=mur, 2=aigua, 3=clau, 4=porta, 9=final)
mapa_nivell = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 9, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# TODO: Completeu el diccionari del jugador
jugador = {
    "x": 1,
    "y": 1,
    "claus": 0,
    "ha_guanyat": False
}


# --- 3. FUNCIONS DE LÒGICA ---

def intentar_moure(dx, dy):
    """
    Aquesta funció ha de calcular la nova posició i decidir si el jugador hi pot anar.
    """
    # TODO: Calcula la nova posició (nova_x, nova_y) sumant dx i dy a la posició actual

    # TODO: Comprova què hi ha al 'mapa_nivell' en aquesta nova posició (desti)

    # TODO: Lògica de col·lisions:
    # 1. Si el destí és terra (0) o el final (9), el jugador es mou.
    # 2. Si el destí és una clau (3), puja l'inventari i el terra es torna 0.
    # 3. Si el destí és una porta (4), comprova si tens claus.
    # 4. Si el destí és un mur (1) o aigua (2), no facis res.

    pass  # Esborra aquest 'pass' quan escriguis el codi


# --- 4. FUNCIONS DE DIBUIX  ---

def dibuixa_escenari():
    for fila in range(len(mapa_nivell)):
        for col in range(len(mapa_nivell[fila])):
            x, y = col * MIDA_RAJOLA, fila * MIDA_RAJOLA
            tipus = mapa_nivell[fila][col]

            # Dibuix bàsic segons el tipus (simplificat per a la plantilla)
            pygame.draw.rect(pantalla, COLORS['terra'], (x, y, MIDA_RAJOLA, MIDA_RAJOLA))
            if tipus == MUR:
                pygame.draw.rect(pantalla, COLORS['mur'], (x, y, MIDA_RAJOLA, MIDA_RAJOLA))
            elif tipus == AIGUA:
                pygame.draw.rect(pantalla, COLORS['aigua'], (x, y, MIDA_RAJOLA, MIDA_RAJOLA))
            elif tipus == CLAU:
                pygame.draw.circle(pantalla, COLORS['clau'], (x + 30, y + 30), 10)
            elif tipus == PORTA:
                pygame.draw.rect(pantalla, COLORS['porta'], (x + 10, y + 5, 40, 50))
            elif tipus == FINAL:
                pygame.draw.circle(pantalla, COLORS['final'], (x + 30, y + 30), 15)


def dibuixa_jugador():
    px = jugador['x'] * MIDA_RAJOLA
    py = jugador['y'] * MIDA_RAJOLA

    pygame.draw.circle(pantalla, COLORS['jugador'], (px + 30, py + 30), 20)


# --- 5. BUCLE PRINCIPAL ---
executant = True
while executant:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            executant = False

        # TODO: Captura les tecles de fletxes i crida a la funció intentar_moure(dx, dy)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:    intentar_moure(0, -1)
            if event.key == pygame.K_DOWN:  intentar_moure(0, 1)
            if event.key == pygame.K_LEFT:  intentar_moure(-1, 0)
            if event.key == pygame.K_RIGHT: intentar_moure(1,0)

    # Pintar la pantalla
    pantalla.fill((0, 0, 0))
    dibuixa_escenari()
    dibuixa_jugador()
    pygame.display.flip()
    rellotge.tick(30)

pygame.quit()
