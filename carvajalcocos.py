import pygame
import random
import sys
import tkinter as tk
from tkinter import messagebox

# Inicializar pygame
pygame.init()

# Definir constantes
MAPA_ANCHO = 20
MAPA_ALTO = 9
ANCHO, ALTO = 1200, 800
TAMANO_CELDA = min(ANCHO // MAPA_ANCHO, ALTO // MAPA_ALTO)

# Configurar la ventana del juego
pantalla = pygame.display.set_mode((MAPA_ANCHO * TAMANO_CELDA, MAPA_ALTO * TAMANO_CELDA))
pygame.display.set_caption("Comecocos")

# Definir colores
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# Mapa del juego (1 = pared, 0 = espacio libre, 2 = punto)
mapa = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 2, 2, 0, 1, 0, 2, 2, 2, 2, 2, 2, 2, 0, 1, 0, 2, 2, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    [1, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 2, 2, 0, 1, 0, 2, 2, 2, 2, 2, 2, 2, 0, 1, 0, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Posiciones iniciales de Comecocos y el fantasma
come_x, come_y = 1, 1
fan_x, fan_y = 10, 5
puntos = 0
velocidad = 100

# Función para verificar si todas las bolitas han sido comidas
def verificar_victoria():
    for fila in mapa:
        if 2 in fila:
            return False
    messagebox.showinfo("¡Ganaste!", "¡Felicidades, has ganado!")
    reiniciar_juego()

# Función para verificar si el fantasma atrapó a Comecocos
def verificar_derrota():
    if come_x == fan_x and come_y == fan_y:
        messagebox.showinfo("¡Perdiste!", "no te dejes tocar")
        reiniciar_juego()

# Función para reiniciar el juego
def reiniciar_juego():
    global come_x, come_y, fan_x, fan_y, puntos
    come_x, come_y = 1, 1
    fan_x, fan_y = 10, 5
    puntos = 0
    for fila in range(len(mapa)):
        for columna in range(len(mapa[fila])):
            if mapa[fila][columna] == 0:
                mapa[fila][columna] = 2

# Función para mover a Comecocos
def mover_comecocos(dx, dy):
    global come_x, come_y, puntos
    nuevo_x = come_x + dx
    nuevo_y = come_y + dy
    if mapa[nuevo_y][nuevo_x] != 1:  # Verificar que no sea una pared
        come_x, come_y = nuevo_x, nuevo_y
        if mapa[come_y][come_x] == 2:  # Comer punto
            puntos += 10
            mapa[come_y][come_x] = 0
            verificar_victoria()

# Función para mover al fantasma de manera aleatoria
def mover_fantasma():
    global fan_x, fan_y
    direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    random.shuffle(direcciones)
    for dx, dy in direcciones:
        nuevo_x = fan_x + dx
        nuevo_y = fan_y + dy
        if mapa[nuevo_y][nuevo_x] != 1:
            fan_x, fan_y = nuevo_x, nuevo_y
            break

# Bucle principal del juego
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        mover_comecocos(-1, 0)
    if teclas[pygame.K_RIGHT]:
        mover_comecocos(1, 0)
    if teclas[pygame.K_UP]:
        mover_comecocos(0, -1)
    if teclas[pygame.K_DOWN]:
        mover_comecocos(0, 1)

    mover_fantasma()
    verificar_derrota()  # Verificar si el fantasma atrapó a Comecocos

    # Dibujar el mapa y los personajes
    pantalla.fill(NEGRO)
    for fila in range(len(mapa)):
        for columna in range(len(mapa[fila])):
            x = columna * TAMANO_CELDA
            y = fila * TAMANO_CELDA
            if mapa[fila][columna] == 1:
                pygame.draw.rect(pantalla, AZUL, (x, y, TAMANO_CELDA, TAMANO_CELDA))
            elif mapa[fila][columna] == 2:
                pygame.draw.circle(pantalla, BLANCO, (x + TAMANO_CELDA // 2, y + TAMANO_CELDA // 2), 5)

    pygame.draw.rect(pantalla, AMARILLO, (come_x * TAMANO_CELDA, come_y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
    pygame.draw.rect(pantalla, ROJO, (fan_x * TAMANO_CELDA, fan_y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))

    # Mostrar puntuación
    fuente = pygame.font.Font(None, 36)
    texto = fuente.render(f"Puntos: {puntos}", True, BLANCO)
    pantalla.blit(texto, (10, 10))

    pygame.display.flip()
    pygame.time.delay(velocidad)

pygame.quit()
