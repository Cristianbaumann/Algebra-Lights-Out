# -*- coding: utf-8 -*-
"""
LIGHTS OUT - PYGAME + ÁLGEBRA APLICADA
Implementación visual del juego Lights Out con resolución algebraica automática

Requisitos del proyecto:
1. Juego visual n×n con interfaz Pygame
2. Modelo algebraico: sistema lineal mod 2
3. Resolución con eliminación de Gauss mod 2 (sin pivoteo)
4. Función de auto-resolución usando el vector solución

Autor: Cristian Baumann
Fecha: Noviembre 2024
Curso: Álgebra Aplicada
"""

import pygame
import sys
from typing import List, Tuple, Optional

# ===================================================================
# PARTE 1: MÓDULO ALGEBRAICO (Sistema lineal mod 2)
# ===================================================================

def construir_sistema(matriz: List[List[int]]) -> Tuple[List[List[int]], List[int]]:
    """
    Construye el sistema lineal Ax = b mod 2 para el juego Lights Out.
    
    Cada ecuación representa el comportamiento de una luz:
    - Variable xi = 1 si se presiona la luz i, 0 si no
    - Coeficiente A[i][j] = 1 si presionar la luz j afecta a la luz i
    - b[i] = estado inicial de la luz i (1=encendida, debe apagarse)
    
    Parámetros:
    -----------
    matriz : List[List[int]]
        Estado inicial del tablero (0=apagada, 1=encendida)
    
    Retorna:
    --------
    Tuple[List[List[int]], List[int]]
        Matriz de coeficientes A y vector independiente b
    """
    n = len(matriz)
    num_variables = n * n
    
    # Matriz de coeficientes A (n² × n²)
    A = [[0 for _ in range(num_variables)] for _ in range(num_variables)]
    
    # Vector independiente b (estado inicial linealizado)
    b = []
    
    # Para cada luz (i,j) del tablero
    for i in range(n):
        for j in range(n):
            luz_actual = i * n + j  # Índice lineal de la ecuación
            
            # La luz se afecta a sí misma al presionarla
            A[luz_actual][luz_actual] = 1
            
            # Verificar luces adyacentes (arriba, abajo, izquierda, derecha)
            direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            
            for di, dj in direcciones:
                ni, nj = i + di, j + dj
                # Solo si la posición adyacente está dentro del tablero
                if 0 <= ni < n and 0 <= nj < n:
                    luz_adyacente = ni * n + nj
                    A[luz_actual][luz_adyacente] = 1
            
            # Estado inicial de esta luz (debe cambiar si está encendida)
            b.append(matriz[i][j])
    
    return A, b


def gauss_mod2(A: List[List[int]], b: List[int]) -> List[int]:
    """
    Resuelve el sistema Ax = b usando eliminación de Gauss mod 2.
    
    Algoritmo según consigna:
    - Aritmética mod 2: suma binaria (1+1=0)
    - Sin pivoteo: usar el primer 1 disponible en cada columna
    - Solo operaciones Fi → Fi + Fj
    - Sustitución hacia atrás en mod 2
    
    Parámetros:
    -----------
    A : List[List[int]]
        Matriz de coeficientes n×n
    b : List[int]
        Vector independiente
    
    Retorna:
    --------
    List[int]
        Vector solución x (0s y 1s indicando qué luces presionar)
    """
    n = len(A)
    
    # Crear matriz aumentada [A|b]
    matriz_aumentada = []
    for i in range(n):
        fila = A[i][:] + [b[i]]  # Copiar fila de A y agregar b[i]
        matriz_aumentada.append(fila)
    
    # FASE 1: Eliminación hacia adelante
    for col in range(n):
        # Buscar fila con 1 en esta columna (desde la diagonal hacia abajo)
        fila_pivot = None
        for fila in range(col, n):
            if matriz_aumentada[fila][col] == 1:
                fila_pivot = fila
                break
        
        # Si no hay pivot, continuar (variable libre)
        if fila_pivot is None:
            continue
        
        # Intercambiar filas para llevar pivot a la diagonal
        if fila_pivot != col:
            matriz_aumentada[col], matriz_aumentada[fila_pivot] = matriz_aumentada[fila_pivot], matriz_aumentada[col]
        
        # Eliminar hacia abajo: Fi → Fi + F{col} para i > col
        for fila in range(col + 1, n):
            if matriz_aumentada[fila][col] == 1:
                # Sumar filas mod 2 (XOR elemento por elemento)
                for j in range(n + 1):  # Incluir columna aumentada
                    matriz_aumentada[fila][j] = (matriz_aumentada[fila][j] + matriz_aumentada[col][j]) % 2
    
    # FASE 2: Sustitución hacia atrás
    solucion = [0] * n
    
    for i in range(n - 1, -1, -1):
        # Calcular x[i] = (b[i] - suma de términos conocidos) mod 2
        suma = matriz_aumentada[i][n]  # Término independiente
        
        for j in range(i + 1, n):
            suma = (suma + matriz_aumentada[i][j] * solucion[j]) % 2
        
        # Si hay pivot en la diagonal, resolver normalmente
        if matriz_aumentada[i][i] == 1:
            solucion[i] = suma
        else:
            # Variable libre, asignar 0
            solucion[i] = 0
    
    return solucion


def resolver_lights_out(matriz: List[List[int]]) -> List[int]:
    """
    Función principal que resuelve el juego Lights Out.
    
    Combina la construcción del sistema lineal con la resolución
    por eliminación de Gauss mod 2.
    
    Parámetros:
    -----------
    matriz : List[List[int]]
        Estado inicial del tablero
    
    Retorna:
    --------
    List[int]
        Vector solución (qué luces presionar para ganar)
    """
    # Construir sistema lineal Ax = b mod 2
    A, b = construir_sistema(matriz)
    
    # Resolver usando Gauss mod 2
    solucion = gauss_mod2(A, b)
    
    return solucion


# ===================================================================
# PARTE 2: INTERFAZ VISUAL PYGAME
# ===================================================================

class LightsOutGame:
    """
    Clase principal del juego Lights Out con interfaz Pygame.
    
    Funcionalidades:
    - Tablero visual n×n con luces clickeables
    - Mecánica del juego: click afecta luz y adyacentes
    - Botón de auto-resolución usando álgebra
    - Indicador de victoria
    """
    
    def __init__(self, tamano_tablero: int = 3):
        """
        Inicializa el juego.
        
        Parámetros:
        -----------
        tamano_tablero : int
            Tamaño del tablero (n×n)
        """
        # Configuración del juego
        self.n = tamano_tablero
        self.tamano_celda = 80
        self.margen = 10
        self.tamano_boton = 40
        
        # Dimensiones de la ventana - calculadas dinámicamente
        self.ancho_tablero = self.n * self.tamano_celda + (self.n + 1) * self.margen
        self.alto_tablero = self.n * self.tamano_celda + (self.n + 1) * self.margen
        
        # Asegurar ancho mínimo para botones y UI
        ancho_minimo_botones = 420  # Espacio para 3 botones
        self.ancho_ventana = max(self.ancho_tablero, ancho_minimo_botones)
        
        # Espacio para botones e información
        espacio_interfaz = 120  # Más espacio para botones e información
        self.alto_ventana = self.alto_tablero + espacio_interfaz
        
        # Estado del juego
        self.tablero = [[0 for _ in range(self.n)] for _ in range(self.n)]
        self.tablero_inicial = None  # Guardará el estado inicial para auto-resolver
        self.solucion_calculada = None
        self.solucion_inicial = None  # Solución para el estado inicial
        self.mostrando_solucion = False
        self.juego_ganado = False
        
        # Configurar Pygame
        try:
            pygame.init()
            self.pantalla = pygame.display.set_mode((self.ancho_ventana, self.alto_ventana))
            pygame.display.set_caption("Lights Out - Álgebra Aplicada")
            
            # Verificar que la pantalla se haya creado correctamente
            if self.pantalla is None:
                raise pygame.error("No se pudo crear la ventana de pygame")
                
        except pygame.error as e:
            print(f"Error al inicializar Pygame: {e}")
            raise
        
        # Fuentes
        self.fuente_grande = pygame.font.Font(None, 36)
        self.fuente_mediana = pygame.font.Font(None, 20)  # Más pequeña para que quepa mejor
        self.fuente_pequena = pygame.font.Font(None, 16)
        
        # Colores
        self.COLOR_FONDO = (50, 50, 50)
        self.COLOR_LUZ_APAGADA = (100, 100, 100)
        self.COLOR_LUZ_ENCENDIDA = (255, 255, 0)
        self.COLOR_SOLUCION = (0, 255, 0)
        self.COLOR_TEXTO = (255, 255, 255)
        self.COLOR_BOTON = (70, 130, 180)
        self.COLOR_BOTON_HOVER = (100, 160, 210)
        
        # Configurar tablero inicial (ejemplo del enunciado)
        self.configurar_tablero_inicial()
    
    def configurar_tablero_inicial(self):
        """
        Configura el tablero inicial con luces aleatorias.
        Genera un patrón aleatorio de luces encendidas/apagadas.
        """
        import random
        
        # Generar configuración aleatoria
        for i in range(self.n):
            for j in range(self.n):
                self.tablero[i][j] = random.choice([0, 1])
        
        # Asegurar que no todas las luces estén apagadas (sería un juego trivial)
        luces_encendidas = sum(sum(fila) for fila in self.tablero)
        if luces_encendidas == 0:
            # Encender algunas luces aleatorias
            for _ in range(random.randint(2, min(5, self.n * self.n // 2))):
                i, j = random.randint(0, self.n-1), random.randint(0, self.n-1)
                self.tablero[i][j] = 1
        
        # Guardar copia del estado inicial para auto-resolver
        self.tablero_inicial = [fila[:] for fila in self.tablero]
        
        # Calcular la solución para el estado inicial
        self.solucion_inicial = resolver_lights_out(self.tablero_inicial)
        print(f"🔍 Nuevo tablero aleatorio generado")
        print(f"🎯 Luces encendidas: {sum(sum(fila) for fila in self.tablero)}")
    
    def obtener_posicion_celda(self, mouse_pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Convierte coordenadas del mouse a posición de celda en el tablero.
        
        Parámetros:
        -----------
        mouse_pos : Tuple[int, int]
            Posición (x, y) del mouse
        
        Retorna:
        --------
        Optional[Tuple[int, int]]
            Posición (fila, columna) de la celda, o None si está fuera
        """
        x, y = mouse_pos
        
        # Obtener offset si existe (para tablero centrado)
        offset_x = getattr(self, 'offset_tablero_x', 0)
        
        for i in range(self.n):
            for j in range(self.n):
                # Calcular posición de la celda (con offset)
                celda_x = offset_x + self.margen + j * (self.tamano_celda + self.margen)
                celda_y = self.margen + i * (self.tamano_celda + self.margen)
                
                # Verificar si el click está dentro de esta celda
                if (celda_x <= x <= celda_x + self.tamano_celda and
                    celda_y <= y <= celda_y + self.tamano_celda):
                    return (i, j)
        
        return None
    
    def presionar_luz(self, fila: int, columna: int):
        """
        Simula presionar una luz, cambiando su estado y el de sus adyacentes.
        
        Esta función implementa la mecánica central del juego según la consigna:
        - Cambia el estado de la luz presionada
        - Cambia el estado de las luces adyacentes (arriba, abajo, izq, der)
        
        Parámetros:
        -----------
        fila : int
            Fila de la luz presionada
        columna : int
            Columna de la luz presionada
        """
        # Cambiar luz actual
        self.tablero[fila][columna] = 1 - self.tablero[fila][columna]
        
        # Cambiar luces adyacentes (según consigna: arriba, abajo, izq, der)
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for df, dc in direcciones:
            nueva_fila = fila + df
            nueva_columna = columna + dc
            
            # Solo cambiar si la posición está dentro del tablero
            if 0 <= nueva_fila < self.n and 0 <= nueva_columna < self.n:
                self.tablero[nueva_fila][nueva_columna] = 1 - self.tablero[nueva_fila][nueva_columna]
        
        # Resetear indicadores
        self.mostrando_solucion = False
        self.verificar_victoria()
    
    def verificar_victoria(self):
        """
        Verifica si el jugador ha ganado (todas las luces apagadas).
        """
        self.juego_ganado = all(self.tablero[i][j] == 0 
                              for i in range(self.n) 
                              for j in range(self.n))
    
    def calcular_solucion(self):
        """
        Calcula la solución usando el módulo algebraico para el estado ACTUAL del tablero.
        
        Utiliza la función resolver_lights_out() que implementa:
        1. Construcción del sistema lineal mod 2
        2. Resolución por eliminación de Gauss mod 2
        3. Retorna vector de presiones necesarias
        """
        self.solucion_calculada = resolver_lights_out(self.tablero)
        print(f"🔍 Solución para estado actual: {self.solucion_calculada}")
        
        # Convertir vector lineal a matriz para visualización
        solucion_matriz = []
        for i in range(self.n):
            fila = []
            for j in range(self.n):
                idx = i * self.n + j
                fila.append(self.solucion_calculada[idx])
            solucion_matriz.append(fila)
        
        print("🎯 Solución por filas (estado actual):")
        for i, fila in enumerate(solucion_matriz):
            print(f"   Fila {i+1}: {fila}")
    
    def aplicar_solucion_automatica(self):
        """
        Aplica automáticamente la solución calculada por el módulo algebraico.
        
        IMPORTANTE: Esta función calcula la solución para el estado ACTUAL del tablero,
        no para el estado inicial. Es útil para resolver el estado actual.
        """
        if self.solucion_calculada is None:
            self.calcular_solucion()
        
        print("🤖 Aplicando solución para estado actual...")
        
        # Aplicar cada presión indicada en la solución
        for i in range(self.n):
            for j in range(self.n):
                idx = i * self.n + j
                if self.solucion_calculada[idx] == 1:
                    print(f"   Presionando luz ({i},{j})")
                    self.presionar_luz(i, j)
        
        print("✅ Solución aplicada")
    
    def aplicar_solucion_inicial(self):
        """
        Aplica la solución para resolver el juego desde el estado inicial.
        
        Esta función reinicia el tablero al estado inicial y aplica la solución
        que llevará directamente a todas las luces apagadas.
        """
        if self.solucion_inicial is None:
            print("❌ No hay solución inicial calculada")
            return
        
        print("🔄 Reiniciando al estado inicial y aplicando solución...")
        
        # Reiniciar al estado inicial
        self.tablero = [fila[:] for fila in self.tablero_inicial]
        
        # Aplicar cada presión indicada en la solución inicial
        for i in range(self.n):
            for j in range(self.n):
                idx = i * self.n + j
                if self.solucion_inicial[idx] == 1:
                    print(f"   Presionando luz ({i},{j})")
                    self.presionar_luz(i, j)
        
        print("✅ Solución inicial aplicada - ¡Juego resuelto!")
        
        # Resetear estados
        self.solucion_calculada = None
        self.mostrando_solucion = False
    
    def reiniciar_juego(self):
        """
        Reinicia el juego generando un tablero aleatorio completamente nuevo.
        """
        print("🔄 Generando nuevo tablero aleatorio...")
        self.configurar_tablero_inicial()  # Esto genera un nuevo tablero aleatorio
        self.solucion_calculada = None
        self.mostrando_solucion = False
        self.juego_ganado = False
    
    def dibujar_tablero(self):
        """
        Dibuja el tablero del juego con las luces.
        
        Representación visual:
        - Gris: luz apagada (0)
        - Amarillo: luz encendida (1)
        - Verde: luz que debe presionarse según solución (si se muestra)
        """
        # Obtener offset si existe (para centrar el tablero)
        offset_x = getattr(self, 'offset_tablero_x', 0)
        
        for i in range(self.n):
            for j in range(self.n):
                # Calcular posición de la celda (con offset para centrar)
                x = offset_x + self.margen + j * (self.tamano_celda + self.margen)
                y = self.margen + i * (self.tamano_celda + self.margen)
                
                # Determinar color según estado
                if self.mostrando_solucion and self.solucion_calculada:
                    idx = i * self.n + j
                    if self.solucion_calculada[idx] == 1:
                        color = self.COLOR_SOLUCION  # Verde para presiones necesarias
                    else:
                        color = self.COLOR_LUZ_APAGADA if self.tablero[i][j] == 0 else self.COLOR_LUZ_ENCENDIDA
                else:
                    color = self.COLOR_LUZ_ENCENDIDA if self.tablero[i][j] == 1 else self.COLOR_LUZ_APAGADA
                
                # Dibujar celda
                pygame.draw.rect(self.pantalla, color, (x, y, self.tamano_celda, self.tamano_celda))
                pygame.draw.rect(self.pantalla, (255, 255, 255), (x, y, self.tamano_celda, self.tamano_celda), 2)
                
                # Dibujar número de la luz (para referencia) - más pequeño
                texto = self.fuente_pequena.render(f"{i},{j}", True, (0, 0, 0))
                texto_rect = texto.get_rect(center=(x + self.tamano_celda//2, y + self.tamano_celda//2))
                self.pantalla.blit(texto, texto_rect)
    
    def dibujar_interfaz(self):
        """
        Dibuja la interfaz completa del juego.
        """
        # Limpiar pantalla
        self.pantalla.fill(self.COLOR_FONDO)
        
        # Dibujar tablero (centrado horizontalmente si la ventana es más ancha)
        offset_x = (self.ancho_ventana - self.ancho_tablero) // 2
        self.offset_tablero_x = offset_x
        self.dibujar_tablero()
        
        # Área de botones - calculada dinámicamente
        y_botones = self.alto_tablero + 20
        margen_boton = 15
        
        # Dimensiones de botones (más anchos para que quepa el texto)
        ancho_boton1 = 110  # Ver Solución
        ancho_boton2 = 120  # Resolver Juego  
        ancho_boton3 = 90   # Reiniciar
        alto_boton = 35     # Más alto para el texto
        
        # Calcular posiciones centradas
        ancho_total_botones = ancho_boton1 + ancho_boton2 + ancho_boton3 + (margen_boton * 2)
        x_inicio = (self.ancho_ventana - ancho_total_botones) // 2
        
        # Botón "Ver Solución"
        x_boton1 = x_inicio
        boton_solucion = pygame.Rect(x_boton1, y_botones, ancho_boton1, alto_boton)
        color_boton = self.COLOR_BOTON_HOVER if boton_solucion.collidepoint(pygame.mouse.get_pos()) else self.COLOR_BOTON
        pygame.draw.rect(self.pantalla, color_boton, boton_solucion)
        texto_solucion = self.fuente_mediana.render("Ver Solución", True, self.COLOR_TEXTO)
        texto_rect = texto_solucion.get_rect(center=boton_solucion.center)
        self.pantalla.blit(texto_solucion, texto_rect)
        
        # Botón "Resolver Juego"
        x_boton2 = x_boton1 + ancho_boton1 + margen_boton
        boton_resolver = pygame.Rect(x_boton2, y_botones, ancho_boton2, alto_boton)
        color_boton = self.COLOR_BOTON_HOVER if boton_resolver.collidepoint(pygame.mouse.get_pos()) else self.COLOR_BOTON
        pygame.draw.rect(self.pantalla, color_boton, boton_resolver)
        texto_resolver = self.fuente_mediana.render("Resolver Juego", True, self.COLOR_TEXTO)
        texto_rect = texto_resolver.get_rect(center=boton_resolver.center)
        self.pantalla.blit(texto_resolver, texto_rect)
        
        # Botón "Reiniciar"
        x_boton3 = x_boton2 + ancho_boton2 + margen_boton
        boton_reiniciar = pygame.Rect(x_boton3, y_botones, ancho_boton3, alto_boton)
        color_boton = self.COLOR_BOTON_HOVER if boton_reiniciar.collidepoint(pygame.mouse.get_pos()) else self.COLOR_BOTON
        pygame.draw.rect(self.pantalla, color_boton, boton_reiniciar)
        texto_reiniciar = self.fuente_mediana.render("Reiniciar", True, self.COLOR_TEXTO)
        texto_rect = texto_reiniciar.get_rect(center=boton_reiniciar.center)
        self.pantalla.blit(texto_reiniciar, texto_rect)
        
        # Información del estado - centrada
        y_info = y_botones + alto_boton + 15
        
        if self.juego_ganado:
            texto_estado = "🎉 ¡GANASTE! Todas las luces apagadas"
            color_estado = (0, 255, 0)
        else:
            luces_encendidas = sum(sum(fila) for fila in self.tablero)
            texto_estado = f"Luces encendidas: {luces_encendidas}"
            color_estado = self.COLOR_TEXTO
        
        superficie_estado = self.fuente_mediana.render(texto_estado, True, color_estado)
        estado_rect = superficie_estado.get_rect(center=(self.ancho_ventana // 2, y_info))
        self.pantalla.blit(superficie_estado, estado_rect)
        
        # Información adicional si se muestra la solución - centrada
        if self.mostrando_solucion:
            info_solucion = "Verde = presionar según álgebra mod 2"
            superficie_info = self.fuente_mediana.render(info_solucion, True, (0, 255, 0))
            info_rect = superficie_info.get_rect(center=(self.ancho_ventana // 2, y_info + 25))
            self.pantalla.blit(superficie_info, info_rect)
        
        # Guardar rectángulos de botones para detección de clicks
        self.rect_boton_solucion = boton_solucion
        self.rect_boton_resolver = boton_resolver
        self.rect_boton_reiniciar = boton_reiniciar
    
    def manejar_evento(self, evento):
        """
        Maneja los eventos de entrada del usuario.
        
        Parámetros:
        -----------
        evento : pygame.event.Event
            Evento de Pygame a procesar
        """
        if evento.type == pygame.QUIT:
            return False
        
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:  # Click izquierdo
                pos_mouse = evento.pos
                
                # Verificar clicks en botones
                if hasattr(self, 'rect_boton_solucion') and self.rect_boton_solucion.collidepoint(pos_mouse):
                    # Mostrar/ocultar solución
                    if not self.mostrando_solucion:
                        self.calcular_solucion()
                    self.mostrando_solucion = not self.mostrando_solucion
                    
                elif hasattr(self, 'rect_boton_resolver') and self.rect_boton_resolver.collidepoint(pos_mouse):
                    # Resolver juego completo
                    self.aplicar_solucion_inicial()
                    
                elif hasattr(self, 'rect_boton_reiniciar') and self.rect_boton_reiniciar.collidepoint(pos_mouse):
                    # Reiniciar juego con tablero aleatorio nuevo
                    self.reiniciar_juego()
                    
                else:
                    # Click en el tablero
                    posicion_celda = self.obtener_posicion_celda(pos_mouse)
                    if posicion_celda and not self.juego_ganado:
                        fila, columna = posicion_celda
                        self.presionar_luz(fila, columna)
                        print(f"🔸 Luz presionada: ({fila},{columna})")
        
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                # Tecla R para reiniciar
                self.reiniciar_juego()
                print("🔄 Juego reiniciado")
            elif evento.key == pygame.K_s:
                # Tecla S para mostrar solución
                if not self.mostrando_solucion:
                    self.calcular_solucion()
                self.mostrando_solucion = not self.mostrando_solucion
                print(f"👁️ Solución {'mostrada' if self.mostrando_solucion else 'ocultada'}")
            elif evento.key == pygame.K_g:
                # Tecla G para resolver juego completo
                self.aplicar_solucion_inicial()
            elif evento.key == pygame.K_ESCAPE:
                # ESC para salir
                print("🔚 Saliendo del juego...")
                return False
        
        return True
    
    def ejecutar(self):
        """
        Bucle principal del juego.
        """
        try:
            reloj = pygame.time.Clock()
            ejecutando = True
            
            print("🎮 LIGHTS OUT - ÁLGEBRA APLICADA")
            print("=" * 50)
            print("Controles:")
            print("  • Click: presionar luz")
            print("  • 'Ver Solución': ver qué luces presionar (verde)")
            print("  • 'Resolver Juego': resolver completamente el juego")
            print("  • 'Reiniciar': generar nuevo tablero aleatorio")
            print("  • Teclas: R (reiniciar), S (ver solución), G (resolver juego)")
            print("  • ESC o cerrar ventana: salir")
            print("=" * 50)
            
            while ejecutando:
                # Procesar eventos
                for evento in pygame.event.get():
                    if not self.manejar_evento(evento):
                        ejecutando = False
                        break
                
                if not ejecutando:
                    break
                
                # Dibujar interfaz
                try:
                    self.dibujar_interfaz()
                    pygame.display.flip()
                except pygame.error as e:
                    print(f"Error al dibujar: {e}")
                    ejecutando = False
                    break
                
                # Controlar FPS
                reloj.tick(60)
            
            print("🔚 Cerrando juego...")
            
        except KeyboardInterrupt:
            print("\n🔚 Juego interrumpido por el usuario")
        except Exception as e:
            print(f"❌ Error en el bucle principal: {e}")
            import traceback
            traceback.print_exc()
        finally:
            try:
                pygame.quit()
            except:
                pass


# ===================================================================
# FUNCIÓN PRINCIPAL
# ===================================================================

def main():
    """
    Función principal que inicia el juego.
    """
    print("🔷 LIGHTS OUT - PROYECTO ÁLGEBRA APLICADA")
    print("Implementación con Pygame + Resolución Algebraica mod 2")
    print()
    
    # Permitir seleccionar tamaño del tablero
    tamano = 3  # Valor por defecto
    
    try:
        entrada = input("Ingrese tamaño del tablero (3, 4, 5, etc.) [Enter para 3x3]: ").strip()
        if entrada == "":
            tamano = 3
        else:
            tamano = int(entrada)
        
        if tamano < 2:
            print("El tamaño debe ser al menos 2x2, usando 3x3 por defecto")
            tamano = 3
        elif tamano > 8:
            print("El tamaño máximo recomendado es 8x8, usando 8x8")
            tamano = 8
            
    except ValueError:
        print("Entrada inválida, usando 3x3 por defecto")
        tamano = 3
    except KeyboardInterrupt:
        print("\nOperación cancelada")
        return
    
    print(f"🎯 Iniciando juego {tamano}×{tamano}")
    print()
    
    try:
        # Crear e iniciar el juego
        juego = LightsOutGame(tamano)
        juego.ejecutar()
    except pygame.error as e:
        print(f"❌ Error de Pygame: {e}")
        print("Asegúrese de que Pygame esté instalado correctamente:")
        print("   pip install pygame")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()