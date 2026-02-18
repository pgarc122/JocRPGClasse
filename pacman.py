import math

import pygame
import random

# =============================================================================
# 1. CONFIGURACIÓ (La "carrosseria" del joc)
# =============================================================================
pygame.init()

MIDA_CELLA = 40
AMPLADA_GRID, ALCADA_GRID = 15, 11
AMPLADA_PANTALLA = AMPLADA_GRID * MIDA_CELLA
ALCADA_PANTALLA = ALCADA_GRID * MIDA_CELLA + 50  # Espai extra per punts/vides

# Colors en format RGB
NEGRE = (10, 10, 30)
BLAU = (30, 30, 200)
GROC = (255, 230, 0)
BLANC = (255, 255, 255)
VERMELL = (255, 50, 50)
TARONJA = (255, 160, 50)
ROSA = (255, 105, 180)

# Constants per no haver de recordar que el número 1 és un mur
BUIT, MUR, PUNT = 0, 1, 2

pantalla = pygame.display.set_mode((AMPLADA_PANTALLA, ALCADA_PANTALLA))
pygame.display.set_caption("PAC-MAN: Projecte 1r de batxillerat")
rellotge = pygame.time.Clock()

# =============================================================================
# 2. DADES DEL JOC (L'estat inicial)
# =============================================================================
mapa = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 0, 1, 0, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 1, 0, 0, 0, 1, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# El diccionari del jugador guarda tota la seva informació
jugador = {
    "x": 1, "y": 1,  # Posició actual a la graella
    "dx": 0, "dy": 0,  # Direcció en què s'està movent ARA
    "next_dx": 0, "next_dy": 0,  # La direcció que hem premut però encara no s'ha aplicat
    "punts": 0
}

fantasmes = [
    {"x": 7, "y": 5, "dx": 1, "dy": 0, "color": VERMELL},
    {"x": 8, "y": 5, "dx": 1, "dy": 0, "color": ROSA},
    {"x": 8, "y": 5, "dx": 1, "dy": 0, "color": TARONJA},
]


# =============================================================================
# 3. FUNCIONS (Lògica de suport)
# =============================================================================

def es_moviment_valid(x, y):
    """Comprova si la casella (x, y) de la graella és caminable (no és un mur)"""
    if 0 <= x < AMPLADA_GRID and 0 <= y < ALCADA_GRID:
        # if mapa[y][x] != MUR:
        #     return True
        # else:
        #    return False

        return mapa[y][x] != MUR
    return False


def obtenir_pixel_centre(grid_x, grid_y):
    px = grid_x * MIDA_CELLA + MIDA_CELLA // 2
    py = grid_y * MIDA_CELLA + MIDA_CELLA // 2 + 50
    return (px, py)


def dibuixa_fantasma(f):
    """Aquí els alumnes han de programar el dibuix de l'enemic."""
    # TODO: EXERCICI 1
    cx, cy = obtenir_pixel_centre(f['x'], f['y'])
    pygame.draw.circle(pantalla, f['color'], (cx, cy), MIDA_CELLA // 2 - 4)
    rect_cos = (cx - (MIDA_CELLA // 2 - 4), cy, MIDA_CELLA - 8, MIDA_CELLA // 2 - 4)
    pygame.draw.rect(pantalla, f['color'], rect_cos)
    pygame.draw.circle(pantalla, BLANC, (cx - 6, cy - 4), 5)
    pygame.draw.circle(pantalla, BLANC, (cx + 6, cy - 4), 5)
    pygame.draw.circle(pantalla, NEGRE, (cx - 6, cy - 4), 2)
    pygame.draw.circle(pantalla, NEGRE, (cx + 6, cy - 4), 2)


# =============================================================================
# 4. BUCLE PRINCIPAL (El cor del joc)
# =============================================================================
frame_actual = 0
executant = True


def moviment_inteligent(direccions_valides, fantasma):
    color = fantasma['color']

    # Fantasma dummy
    if color == TARONJA:
        return random.choice(direccions_valides)

    # Fantasma intel·ligent
    elif color == VERMELL:
        minimia = 10000
        direccio_minima = None

        for d in direccions_valides:
            jx, jy = jugador["x"], jugador["y"]
            fx, fy = fantasma["x"], fantasma["y"]
            fx += d[0]
            fy += d[1]

            a = fx - jx
            b = fy - jy
            h = math.sqrt(a * a + b * b)

            if h < minimia:
                minimia = h
                direccio_minima = d

        return direccio_minima

    # Fantasma que fuig
    elif color == ROSA:
        maxima = 0
        direccio_maxima = None

        for d in direccions_valides:
            jx, jy = jugador["x"], jugador["y"]
            fx, fy = fantasma["x"], fantasma["y"]
            fx += d[0]
            fy += d[1]

            a = fx - jx
            b = fy - jy
            h = math.sqrt(a * a + b * b)

            if h > maxima:
                maxima = h
                direccio_maxima = d

        return direccio_maxima


    else:
        return random.choice(direccions_valides)


def mou_fantasma(f):
    x, y = f["x"], f["y"]
    dx, dy = f["dx"], f["dy"]

    # 1. Intentar seguir en la direcció actual
    if dx != 0 and mapa[y + 1][x] == MUR and mapa[y - 1][x] == MUR:
        f["x"] = x + dx
        return

    if dy != 0 and mapa[y][x + 1] == MUR and mapa[y][x - 1] == MUR:
        f["y"] = y + dy
        return

        # 2. Si no puede seguir, buscamos nuevas direcciones válidas
    direccions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    direccions_valides = []

    for dx, dy in direccions:
        if es_moviment_valid(f["x"] + dx, f["y"] + dy):
            direccions_valides.append((dx, dy))

    # 3. Elegimos una dirección aleatoria
    if direccions_valides:
        f["dx"], f["dy"] = moviment_inteligent(direccions_valides, f)
        f["x"] += f["dx"]
        f["y"] += f["dy"]


while executant:
    # --- A. CAPTURAR INPUTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT: executant = False

        if event.type == pygame.KEYDOWN:
            # Quan premem una tecla, NO movem el personatge directament.
            # Només guardem el "desig" de girar a next_dx i next_dy.
            if event.key == pygame.K_UP:    jugador['next_dx'], jugador['next_dy'] = 0, -1
            if event.key == pygame.K_DOWN:  jugador['next_dx'], jugador['next_dy'] = 0, 1
            if event.key == pygame.K_LEFT:  jugador['next_dx'], jugador['next_dy'] = -1, 0
            if event.key == pygame.K_RIGHT: jugador['next_dx'], jugador['next_dy'] = 1, 0

    # --- B. LÒGICA DE MOVIMENT (Només s'executa 1 de cada 8 vegades per no anar massa ràpid) ---
    if frame_actual % 8 == 0:

        # 1. Intentem aplicar el "desig" de girar
        # Mirem si la direcció que l'usuari vol (next) està lliure
        if es_moviment_valid(jugador['x'] + jugador['next_dx'], jugador['y'] + jugador['next_dy']):
            # Si està lliure, la direcció actual (dx) passa a ser la desitjada (next)
            jugador['dx'] = jugador['next_dx']
            jugador['dy'] = jugador['next_dy']

        # 2. Intentem moure el personatge
        # Mirem si pot seguir avançant en la seva direcció actual
        if es_moviment_valid(jugador['x'] + jugador['dx'], jugador['y'] + jugador['dy']):
            jugador['x'] += jugador['dx']
            jugador['y'] += jugador['dy']

            # TODO: EXERCICI 2 (Menjar punts)
            # Escriviu aquí la lògica per detectar si hi ha un PUNT a la posició actual.
            if mapa[jugador['y']][jugador['x']] == PUNT:
                mapa[jugador['y']][jugador['x']] = BUIT
                jugador['punts'] += 1

    # --- C. LÒGICA DELS FANTASMES ---
    if frame_actual % 24 == 0:  # El fantasma es mou cada 12 frames (més lent!)
        for f in fantasmes:
            # TODO: EXERCICI 3 (Moviment automàtic del fantasma)
            mou_fantasma(f)

    # --- D. DIBUIXAR ---
    pantalla.fill(NEGRE)

    # Dibuixem el mapa
    for fila in range(ALCADA_GRID):
        for col in range(AMPLADA_GRID):
            # Calculem on cau cada casella en píxels (x, y)
            # Afegim +50 de marge superior per no tapar el marcador
            px, py = col * MIDA_CELLA, fila * MIDA_CELLA + 50
            if mapa[fila][col] == MUR:
                pygame.draw.rect(pantalla, BLAU, (px + 2, py + 2, MIDA_CELLA - 4, MIDA_CELLA - 4), border_radius=5)
            if mapa[fila][col] == PUNT:
                pygame.draw.circle(pantalla, GROC, (col * MIDA_CELLA + 20, fila * MIDA_CELLA + 70), 3)

    # Dibuixem el jugador (Convertint la seva X/Y de graella a Píxels)
    # El +20 és per posar el centre del cercle al mig de la casella de 40.
    pygame.draw.circle(pantalla, GROC, (jugador['x'] * MIDA_CELLA + 20, jugador['y'] * MIDA_CELLA + 70), 16)

    for f in fantasmes: dibuixa_fantasma(f)

    font_marcador = pygame.font.SysFont("Arial", 24, bold=True)
    text = font_marcador.render(f"PUNTS: {jugador['punts']} / 72", True, BLANC)
    pantalla.blit(text, (20, 10))

    # Actualitzem la finestra
    pygame.display.flip()
    frame_actual += 1
    rellotge.tick(60)

pygame.quit()
