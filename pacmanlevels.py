import math
import pygame
import random

# --- Constants i Configuració (Sense canvis) ---
MIDA_CELLA = 40
AMPLADA_GRID, ALCADA_GRID = 15, 11
AMPLADA_PANTALLA = AMPLADA_GRID * MIDA_CELLA
ALCADA_PANTALLA = ALCADA_GRID * MIDA_CELLA + 50
NEGRE, BLAU, GROC, BLANC, VERMELL, TARONJA, ROSA = (10, 10, 30), (30, 30, 200), (255, 230, 0), (255, 255, 255), (255,
                                                                                                                 50,
                                                                                                                 50), (
    255, 160, 50), (255, 105, 180)
BUIT, MUR, PUNT = 0, 1, 2


# --- Funcions de suport (Es mantenen igual) ---
def es_moviment_valid(mapa, x, y):
    if 0 <= x < AMPLADA_GRID and 0 <= y < ALCADA_GRID:
        return mapa[y][x] != MUR
    return False


def obtenir_pixel_centre(grid_x, grid_y):
    return (grid_x * MIDA_CELLA + MIDA_CELLA // 2, grid_y * MIDA_CELLA + MIDA_CELLA // 2 + 50)


def dibuixa_fantasma(pantalla, f):
    cx, cy = obtenir_pixel_centre(f['x'], f['y'])
    pygame.draw.circle(pantalla, f['color'], (cx, cy), MIDA_CELLA // 2 - 4)
    pygame.draw.rect(pantalla, f['color'], (cx - (MIDA_CELLA // 2 - 4), cy, MIDA_CELLA - 8, MIDA_CELLA // 2 - 4))
    pygame.draw.circle(pantalla, BLANC, (cx - 6, cy - 4), 5)
    pygame.draw.circle(pantalla, BLANC, (cx + 6, cy - 4), 5)
    pygame.draw.circle(pantalla, NEGRE, (cx - 6, cy - 4), 2)
    pygame.draw.circle(pantalla, NEGRE, (cx + 6, cy - 4), 2)


def moviment_inteligent(jugador, direccions_valides, fantasma):
    color = fantasma['color']
    if color == TARONJA: return random.choice(direccions_valides)
    jx, jy, fx, fy = jugador["x"], jugador["y"], fantasma["x"], fantasma["y"]

    millor_d = direccions_valides[0]
    distancia_ref = 10000 if color == VERMELL else 0

    for d in direccions_valides:
        h = math.sqrt((fx + d[0] - jx) ** 2 + (fy + d[1] - jy) ** 2)
        if (color == VERMELL and h < distancia_ref) or (color == ROSA and h > distancia_ref):
            distancia_ref, millor_d = h, d
    return millor_d


def mou_fantasma(jugador, mapa, f):
    direccions_valides = [(dx, dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)] if
                          es_moviment_valid(mapa, f["x"] + dx, f["y"] + dy)]
    if direccions_valides:
        f["dx"], f["dy"] = moviment_inteligent(jugador, direccions_valides, f)
        f["x"] += f["dx"];
        f["y"] += f["dy"]


# =============================================================================
# DEFINICIÓ DE NIVELLS
# =============================================================================
NIVELLS = [
    {
        "mapa": [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ],
        "fantasmes": [{"x": 7, "y": 3, "dx": 1, "dy": 0, "color": TARONJA}]
    },
    {
        "mapa": [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
            [1, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ],
        "fantasmes": [
            {"x": 6, "y": 2, "dx": 1, "dy": 0, "color": VERMELL},
            {"x": 8, "y": 2, "dx": -1, "dy": 0, "color": ROSA}
        ]
    }
]


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((AMPLADA_PANTALLA, ALCADA_PANTALLA))
    rellotge = pygame.time.Clock()

    nivell_actual = 0
    executant = True

    while executant and nivell_actual < len(NIVELLS):
        # Carregar dades del nivell actual
        mapa = [fila[:] for fila in NIVELLS[nivell_actual]["mapa"]]
        fantasmes = [f.copy() for f in NIVELLS[nivell_actual]["fantasmes"]]
        jugador = {"x": 1, "y": 1, "dx": 0, "dy": 0, "next_dx": 0, "next_dy": 0, "punts": 0}

        punts_totals = sum(fila.count(PUNT) for fila in mapa)
        guanyar_nivell = False
        perdre_joc = False
        frame_actual = 0
        jugant_nivell = True

        while jugant_nivell:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: executant = False; jugant_nivell = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:    jugador['next_dx'], jugador['next_dy'] = 0, -1
                    if event.key == pygame.K_DOWN:  jugador['next_dx'], jugador['next_dy'] = 0, 1
                    if event.key == pygame.K_LEFT:  jugador['next_dx'], jugador['next_dy'] = -1, 0
                    if event.key == pygame.K_RIGHT: jugador['next_dx'], jugador['next_dy'] = 1, 0

            # Lògica Moviment Pac-man
            if frame_actual % 10 == 0:
                if es_moviment_valid(mapa, jugador['x'] + jugador['next_dx'], jugador['y'] + jugador['next_dy']):
                    jugador['dx'], jugador['dy'] = jugador['next_dx'], jugador['next_dy']
                if es_moviment_valid(mapa, jugador['x'] + jugador['dx'], jugador['y'] + jugador['dy']):
                    jugador['x'] += jugador['dx'];
                    jugador['y'] += jugador['dy']
                    if mapa[jugador['y']][jugador['x']] == PUNT:
                        mapa[jugador['y']][jugador['x']] = BUIT;
                        jugador['punts'] += 1

            # Lògica Fantasmes
            if frame_actual % 20 == 0:
                for f in fantasmes:
                    mou_fantasma(jugador, mapa, f)
                    if jugador['x'] == f['x'] and jugador['y'] == f['y']: perdre_joc = True

            # Condicions de victòria/derrota
            if jugador['punts'] >= punts_totals: guanyar_nivell = True; jugant_nivell = False
            if perdre_joc: jugant_nivell = False; executant = False

            # Dibuixar
            pantalla.fill(NEGRE)
            for r, fila in enumerate(mapa):
                for c, valor in enumerate(fila):
                    px, py = c * MIDA_CELLA, r * MIDA_CELLA + 50
                    if valor == MUR: pygame.draw.rect(pantalla, BLAU, (px + 2, py + 2, MIDA_CELLA - 4, MIDA_CELLA - 4),
                                                      border_radius=5)
                    if valor == PUNT: pygame.draw.circle(pantalla, GROC, (px + 20, py + 20), 3)

            pygame.draw.circle(pantalla, GROC, (jugador['x'] * MIDA_CELLA + 20, jugador['y'] * MIDA_CELLA + 70), 16)
            for f in fantasmes: dibuixa_fantasma(pantalla, f)

            font = pygame.font.SysFont("Arial", 24, True)
            text = font.render(f"NIVELL: {nivell_actual + 1}  PUNTS: {jugador['punts']}/{punts_totals}", True, BLANC)
            pantalla.blit(text, (20, 10))

            pygame.display.flip()
            frame_actual += 1
            rellotge.tick(60)

        if guanyar_nivell: nivell_actual += 1

    # Pantalla Final
    pantalla.fill(NEGRE)
    msg = "VICTORIA TOTAL!" if nivell_actual >= len(NIVELLS) else "GAME OVER"
    text_final = pygame.font.SysFont("Arial", 60, True).render(msg, True, VERMELL)
    pantalla.blit(text_final, (AMPLADA_PANTALLA // 2 - text_final.get_width() // 2, ALCADA_PANTALLA // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()


if __name__ == "__main__":
    main()