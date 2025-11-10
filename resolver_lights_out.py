# -*- coding: utf-8 -*-
"""
PROYECTO LIGHTS OUT - ÁLGEBRA APLICADA
Implementación del algoritmo de resolución usando eliminación de Gauss mod 2

Autor: Cristian Baumann
Fecha: Noviembre 2024
"""

def resolver_lights_out(matriz, verbose=False):
    """
    Resuelve el juego Lights Out usando eliminación de Gauss mod 2.
    
    Parámetros:
    -----------
    matriz : list of list
        Matriz n×n con valores 0 (luz apagada) o 1 (luz encendida)
    verbose : bool
        Si True, muestra paso a paso la construcción del sistema
    
    Retorna:
    --------
    list : Vector de 0s y 1s indicando qué luces presionar
    """
    n = len(matriz)
    
    if verbose:
        print("🔷 RESOLUCIÓN LIGHTS OUT - ÁLGEBRA APLICADA")
        print(f"Tablero inicial {n}×{n}:")
        imprimir_matriz(matriz)
        print()
    
    # Construir el sistema lineal Ax = b (mod 2)
    A, b = construir_sistema(matriz, verbose)
    
    if verbose:
        print("📐 SISTEMA LINEAL CONSTRUIDO:")
        print("Matriz aumentada [A|b]:")
        imprimir_matriz_aumentada(A, b)
        print()
    
    # Resolver usando eliminación de Gauss mod 2
    solucion = gauss_mod2(A, b, verbose)
    
    if verbose:
        print("✅ VECTOR SOLUCIÓN:")
        print(f"x = {solucion}")
        print("\nInterpretación (por filas del tablero):")
        for i in range(n):
            fila_indices = [i*n + j for j in range(n)]
            fila_valores = [solucion[idx] for idx in fila_indices]
            print(f"Fila {i+1}: {fila_valores}")
        print()
    
    return solucion


def construir_sistema(matriz, verbose=False):
    """
    Construye el sistema lineal Ax = b donde:
    - A[i][j] = 1 si presionar la luz j afecta a la luz i
    - b[i] = estado inicial de la luz i (1=encendida, 0=apagada)
    """
    n = len(matriz)
    num_variables = n * n
    
    # Matriz de coeficientes A (n² × n²)
    A = [[0 for _ in range(num_variables)] for _ in range(num_variables)]
    
    # Vector independiente b (estado inicial)
    b = []
    
    if verbose:
        print("🔧 CONSTRUCCIÓN DEL SISTEMA:")
        print("Cada ecuación representa el comportamiento de una luz")
        print("Variables: x₀, x₁, ..., x_{n²-1} (por filas)")
        print()
    
    # Para cada luz (i,j) del tablero
    for i in range(n):
        for j in range(n):
            luz_actual = i * n + j  # Índice de la ecuación
            
            if verbose:
                print(f"Ecuación {luz_actual} (luz en posición ({i},{j})):")
            
            # La luz se afecta a sí misma al presionarla
            A[luz_actual][luz_actual] = 1
            if verbose:
                print(f"  + x_{luz_actual} (presionar esta luz)")
            
            # Verificar luces adyacentes
            direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # arriba, abajo, izq, der
            
            for di, dj in direcciones:
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < n:
                    luz_adyacente = ni * n + nj
                    A[luz_actual][luz_adyacente] = 1
                    if verbose:
                        print(f"  + x_{luz_adyacente} (presionar luz en ({ni},{nj}))")
            
            # Estado inicial de esta luz
            b.append(matriz[i][j])
            
            if verbose:
                ecuacion = " + ".join([f"x_{k}" for k in range(num_variables) if A[luz_actual][k] == 1])
                print(f"  = {matriz[i][j]} (estado inicial)")
                print(f"  Ecuación: {ecuacion} ≡ {matriz[i][j]} (mod 2)")
                print()
    
    return A, b


def gauss_mod2(A, b, verbose=False):
    """
    Resuelve el sistema Ax = b usando eliminación de Gauss mod 2.
    
    Características del algoritmo:
    - Todas las operaciones en {0, 1} con suma binaria (1+1=0)
    - Sin pivoteo (usar el primer 1 disponible en cada columna)
    - Solo operaciones Fi → Fi + Fj
    """
    n = len(A)
    
    # Crear matriz aumentada [A|b]
    matriz_aumentada = []
    for i in range(n):
        fila = A[i][:] + [b[i]]  # Copiar fila de A y agregar b[i]
        matriz_aumentada.append(fila)
    
    if verbose:
        print("⚙️ ELIMINACIÓN DE GAUSS MOD 2:")
        print("Matriz aumentada inicial:")
        imprimir_matriz_aumentada_numerada(matriz_aumentada)
        print()
    
    # Fase de eliminación hacia adelante
    for col in range(n):
        if verbose:
            print(f"🔹 Procesando columna {col}:")
        
        # Buscar fila con 1 en esta columna (desde la diagonal hacia abajo)
        fila_pivot = None
        for fila in range(col, n):
            if matriz_aumentada[fila][col] == 1:
                fila_pivot = fila
                break
        
        if fila_pivot is None:
            if verbose:
                print(f"  No hay pivot en columna {col}, continuando...")
            continue
        
        # Intercambiar filas si es necesario (llevar pivot a la diagonal)
        if fila_pivot != col:
            matriz_aumentada[col], matriz_aumentada[fila_pivot] = matriz_aumentada[fila_pivot], matriz_aumentada[col]
            if verbose:
                print(f"  Intercambio F{col} ↔ F{fila_pivot}")
        
        if verbose:
            print(f"  Pivot: matriz_aumentada[{col}][{col}] = 1")
        
        # Eliminar hacia abajo: Fi → Fi + F{col} para i > col
        for fila in range(col + 1, n):
            if matriz_aumentada[fila][col] == 1:
                if verbose:
                    print(f"  F{fila} → F{fila} + F{col}")
                
                # Sumar filas mod 2
                for j in range(n + 1):  # Incluir columna aumentada
                    matriz_aumentada[fila][j] = (matriz_aumentada[fila][j] + matriz_aumentada[col][j]) % 2
        
        if verbose:
            print("  Matriz después de eliminación:")
            imprimir_matriz_aumentada_numerada(matriz_aumentada)
            print()
    
    # Fase de sustitución hacia atrás
    if verbose:
        print("🔸 SUSTITUCIÓN HACIA ATRÁS:")
    
    solucion = [0] * n
    
    for i in range(n - 1, -1, -1):
        if verbose:
            print(f"  Resolviendo variable x_{i}:")
        
        # Calcular x[i] = (b[i] - suma de términos conocidos) mod 2
        suma = matriz_aumentada[i][n]  # Término independiente
        
        for j in range(i + 1, n):
            suma = (suma + matriz_aumentada[i][j] * solucion[j]) % 2
        
        if matriz_aumentada[i][i] == 1:
            solucion[i] = suma
        else:
            # Variable libre, asignar 0
            solucion[i] = 0
        
        if verbose:
            print(f"    x_{i} = {solucion[i]}")
    
    if verbose:
        print()
    
    return solucion


def verificar_solucion(matriz_inicial, solucion, verbose=False):
    """
    Verifica que la solución sea correcta aplicando las presiones
    y comprobando que todas las luces queden apagadas.
    """
    n = len(matriz_inicial)
    
    # Copiar matriz inicial
    matriz_final = [fila[:] for fila in matriz_inicial]
    
    if verbose:
        print("🔍 VERIFICACIÓN DE LA SOLUCIÓN:")
        print("Estado inicial:")
        imprimir_matriz(matriz_inicial)
        print("\nPresiones a realizar:")
        for i in range(n):
            fila_presiones = [solucion[i*n + j] for j in range(n)]
            print(f"Fila {i+1}: {fila_presiones}")
        print()
    
    # Aplicar cada presión
    for i in range(n):
        for j in range(n):
            idx = i * n + j
            if solucion[idx] == 1:
                # Presionar luz en (i,j)
                aplicar_presion(matriz_final, i, j)
                if verbose:
                    print(f"Presionando luz ({i},{j}):")
                    imprimir_matriz(matriz_final)
                    print()
    
    # Verificar que todas las luces estén apagadas
    todas_apagadas = all(matriz_final[i][j] == 0 for i in range(n) for j in range(n))
    
    if verbose:
        print("🎯 RESULTADO FINAL:")
        print("Estado final del tablero:")
        imprimir_matriz(matriz_final)
        print(f"\n✅ Todas las luces apagadas: {'SÍ' if todas_apagadas else 'NO'}")
    
    return todas_apagadas


def aplicar_presion(matriz, i, j):
    """
    Aplica una presión en la posición (i,j), cambiando el estado
    de esa luz y sus adyacentes.
    """
    n = len(matriz)
    
    # Cambiar luz actual
    matriz[i][j] = 1 - matriz[i][j]
    
    # Cambiar luces adyacentes
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for di, dj in direcciones:
        ni, nj = i + di, j + dj
        if 0 <= ni < n and 0 <= nj < n:
            matriz[ni][nj] = 1 - matriz[ni][nj]


def imprimir_matriz(matriz):
    """Imprime una matriz de forma legible."""
    for fila in matriz:
        print("  " + " ".join(map(str, fila)))


def imprimir_matriz_aumentada(A, b):
    """Imprime la matriz aumentada [A|b]."""
    n = len(A)
    for i in range(n):
        fila_str = " ".join(map(str, A[i])) + " | " + str(b[i])
        print("  " + fila_str)


def imprimir_matriz_aumentada_numerada(matriz_aumentada):
    """Imprime la matriz aumentada con números de fila."""
    for i, fila in enumerate(matriz_aumentada):
        parte_A = fila[:-1]
        parte_b = fila[-1]
        fila_str = " ".join(map(str, parte_A)) + " | " + str(parte_b)
        print(f"  F{i}: {fila_str}")


# =====================================================================
# EJEMPLO DE EJECUCIÓN
# =====================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🔷 LIGHTS OUT - RESOLUCIÓN CON ÁLGEBRA LINEAL MOD 2")
    print("=" * 60)
    print()
    
    # Ejemplo del enunciado: tablero 3×3
    tablero_3x3 = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1]
    ]
    
    print("🎮 EJEMPLO: TABLERO 3×3")
    print("Tablero inicial (1=encendida, 0=apagada):")
    imprimir_matriz(tablero_3x3)
    print()
    
    # Resolver con salida detallada
    solucion = resolver_lights_out(tablero_3x3, verbose=True)
    
    print("=" * 60)
    
    # Verificar la solución
    es_correcta = verificar_solucion(tablero_3x3, solucion, verbose=True)
    
    print("\n" + "=" * 60)
    print(f"🏆 RESULTADO: {'ÉXITO' if es_correcta else 'ERROR'}")
    print("=" * 60)