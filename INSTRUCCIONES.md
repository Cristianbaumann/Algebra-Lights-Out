# 🚀 INSTRUCCIONES DE USO - LIGHTS OUT

## 📦 Instalación Rápida

```powershell
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar el menú principal
python demo.py
```

## 🎮 Opciones Disponibles

### 1️⃣ Versión Consola
```powershell
python resolver_lights_out.py
```
- Muestra paso a paso el algoritmo algebraico
- Construcción del sistema lineal mod 2
- Eliminación de Gauss sin pivoteo
- Verificación de la solución

### 2️⃣ Versión Visual (Pygame)
```powershell
python lights_out_pygame.py
```
- Juego interactivo con interfaz gráfica
- Click para presionar luces
- Botones de auto-resolución
- Indicadores visuales de la solución

### 3️⃣ Menú Principal (Recomendado)
```powershell
python demo.py
```
- Menú para elegir entre las versiones
- Ejecuta ambas versiones en secuencia
- Manejo de errores mejorado

## 🎯 Controles del Juego Pygame

- **Mouse**: Click para presionar luces
- **Botones**:
  - `Mostrar Solución`: Ver luces a presionar (verde)
  - `Auto-Resolver`: Aplicar solución automáticamente
  - `Reiniciar`: Volver al estado inicial
- **Teclado**:
  - `R`: Reiniciar juego
  - `S`: Mostrar/ocultar solución
  - `A`: Auto-resolver
  - `ESC`: Salir

## 🔧 Solución de Problemas

### Error "No module named 'pygame'"
```powershell
pip install pygame
```

### Error al ejecutar demo.py
- Asegúrese de estar en la carpeta correcta
- Verifique que todos los archivos .py estén presentes

### La ventana de pygame no se abre
- Verifique que tenga permisos para crear ventanas
- Pruebe ejecutar como administrador si es necesario

## 📚 Ejemplo de Uso Completo

1. **Abrir terminal en la carpeta del proyecto**
2. **Instalar dependencias**: `pip install -r requirements.txt`
3. **Ejecutar menú**: `python demo.py`
4. **Seleccionar opción 3** para ver ambas versiones
5. **En la versión pygame**: Probar los controles y botones

¡Listo para usar! 🎉