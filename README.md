# 🔷 Lights Out - Resolución con Álgebra Lineal mod 2

Este proyecto implementa un solucionador para el juego **Lights Out** utilizando sistemas de ecuaciones lineales sobre el campo finito `GF(2)` (aritmética mod 2).

## 📋 Descripción del Problema

**Lights Out** es un juego de rompecabezas en el que:
- Se tiene un tablero de luces `n×n` que pueden estar encendidas (1) o apagadas (0)
- Al presionar una luz, esta cambia de estado junto con sus vecinos adyacentes (arriba, abajo, izquierda, derecha)
- El objetivo es apagar todas las luces del tablero

## 🔧 Implementación

### Algoritmo

La solución utiliza **eliminación de Gauss mod 2** para resolver el sistema lineal:
- Cada luz del tablero es una variable `x_i` (1 = presionar, 0 = no presionar)
- Cada ecuación representa el comportamiento de una luz específica
- Todas las operaciones se realizan en aritmética mod 2 (1+1=0)

### Características

✅ **Eliminación de Gauss sin pivoteo**: Solo operaciones `F_i → F_i + F_j`  
✅ **Aritmética mod 2**: Suma binaria (XOR)  
✅ **Salida detallada**: Construcción del sistema paso a paso  
✅ **Verificación automática**: Comprueba que la solución sea correcta  
✅ **Cualquier tamaño**: Funciona para tableros `n×n` arbitrarios  

## 🚀 Uso

### Función Principal

```python
def resolver_lights_out(matriz, verbose=False):
    """
    Resuelve el juego Lights Out.
    
    Parámetros:
    -----------
    matriz : list of list
        Tablero n×n con valores 0 (apagada) o 1 (encendida)
    verbose : bool
        Si True, muestra el proceso paso a paso
    
    Retorna:
    --------
    list : Vector de 0s y 1s indicando qué luces presionar
    """
```

### Ejemplo de Uso

```python
# Tablero 3×3 del ejemplo
tablero = [
    [1, 0, 1],
    [0, 1, 0], 
    [1, 0, 1]
]

# Resolver con salida detallada
solucion = resolver_lights_out(tablero, verbose=True)
print(f"Solución: {solucion}")

# Verificar que funciona
verificar_solucion(tablero, solucion, verbose=True)
```

## 🏃‍♂️ Ejecutar

### Script Demostrador (Recomendado)

```powershell
python demo.py
```

Este script ofrece un menú para ejecutar cualquiera de las versiones disponibles.

### Versión Consola (Solo Álgebra)

```powershell
python resolver_lights_out.py
```

### Versión Visual (Pygame)

```powershell
python lights_out_pygame.py
```

**Nota**: La versión Pygame requiere instalar dependencias con `pip install -r requirements.txt`

## 📊 Ejemplo de Salida

El programa muestra:

1. **Construcción del sistema**: Ecuaciones para cada luz
2. **Matriz aumentada**: Sistema `[A|b]` inicial
3. **Eliminación de Gauss**: Pasos de la triangulación
4. **Sustitución hacia atrás**: Cálculo de variables
5. **Vector solución**: Qué luces presionar
6. **Verificación**: Aplicación de presiones y resultado final

### Resultado para el ejemplo 3×3:

```
Tablero inicial:      Vector solución:      Tablero final:
  1 0 1                [1, 1, 1]              0 0 0
  0 1 0         →      [1, 1, 1]      →       0 0 0  ✅
  1 0 1                [1, 1, 1]              0 0 0
```

**Interpretación**: Hay que presionar todas las luces del tablero.

## 🔬 Fundamento Matemático

### Modelo Lineal

Para un tablero `n×n`, el sistema tiene:
- **Variables**: `n²` variables `x₀, x₁, ..., x_{n²-1}` (por filas)
- **Ecuaciones**: `n²` ecuaciones (una por cada luz)
- **Coeficientes**: `A[i][j] = 1` si presionar la luz `j` afecta a la luz `i`

### Ecuación para la luz en posición `(i,j)`:

```
x_{i,j} + x_{i-1,j} + x_{i+1,j} + x_{i,j-1} + x_{i,j+1} ≡ estado_inicial[i][j] (mod 2)
```

Donde se consideran solo las posiciones válidas del tablero.

## 🎮 Versión Pygame (Interfaz Visual)

### Instalación

```powershell
pip install -r requirements.txt
```

### Ejecutar el Juego

```powershell
python lights_out_pygame.py
```

### Características de la Interfaz

🎯 **Visual completa**: Tablero n×n con luces clickeables  
🎯 **Colores intuitivos**: Amarillo (encendida), Gris (apagada), Verde (solución)  
🎯 **Auto-resolución**: Botón que aplica la solución algebraica automáticamente  
🎯 **Controles múltiples**: Mouse y teclado (R=reiniciar, S=solución, A=auto-resolver)  
🎯 **Verificación visual**: Indicador de victoria cuando todas las luces están apagadas  



## 📁 Archivos

- `resolver_lights_out.py`: Implementación algebraica pura con ejemplo
- `lights_out_pygame.py`: Juego visual completo con interfaz Pygame  
- `demo.py`: Script demostrador con menú de opciones
- `requirements.txt`: Dependencias del proyecto
- `README.md`: Documentación del proyecto

## 🎓 Contexto Académico

Este proyecto fue desarrollado como parte del curso de **Álgebra Aplicada**, demostrando:
- Aplicación de sistemas lineales a problemas reales
- Uso de campos finitos (`GF(2)`)
- Implementación de algoritmos algebraicos
- Verificación de soluciones matemáticas

---

**Fecha**: Noviembre 2025  
**Curso**: Álgebra Aplicada  