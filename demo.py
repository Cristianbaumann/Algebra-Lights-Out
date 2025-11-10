#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DEMOSTRACIÓN COMPLETA - LIGHTS OUT
Proyecto de Álgebra Aplicada

Este script permite ejecutar tanto la versión console como la versión Pygame
del solucionador de Lights Out.
"""

import sys
import os

def mostrar_menu():
    """Muestra el menú principal de opciones."""
    print("=" * 60)
    print("🔷 LIGHTS OUT - ÁLGEBRA APLICADA")
    print("   Proyecto: Cristian Baumann")
    print("=" * 60)
    print()
    print("Seleccione la versión a ejecutar:")
    print()
    print("1️⃣  Versión CONSOLA (Solo álgebra)")
    print("    • Muestra paso a paso la resolución algebraica")
    print("    • Construcción del sistema lineal mod 2")
    print("    • Eliminación de Gauss sin pivoteo")
    print("    • Verificación de la solución")
    print("    • Ejemplo fijo: tablero 3×3")
    print()
    print("2️⃣  Versión PYGAME (Interfaz visual)")
    print("    • Juego interactivo con mouse y teclado")
    print("    • Visualización del tablero y luces")
    print("    • Auto-resolución con algoritmo algebraico")
    print("    • Indicadores visuales de la solución")
    print("    • Tamaños personalizables (3×3, 4×4, 5×5, etc.)")
    print()
    print("3️⃣  AMBAS versiones (primero consola, luego visual)")
    print()
    print("4️⃣  PYGAME Rápido (tablero 3×3)")
    print()
    print("5️⃣  PYGAME Rápido (tablero 5×5)")
    print()
    print("0️⃣  Salir")
    print()

def ejecutar_version_consola():
    """Ejecuta la versión de consola."""
    print("🔧 Ejecutando versión CONSOLA...")
    print("=" * 40)
    try:
        import subprocess
        result = subprocess.run([sys.executable, "resolver_lights_out.py"], 
                              capture_output=False, text=True)
        if result.returncode == 0:
            print("✅ Versión consola ejecutada correctamente")
        else:
            print(f"❌ Error en la ejecución (código: {result.returncode})")
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo resolver_lights_out.py")
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")

def ejecutar_version_pygame():
    """Ejecuta la versión Pygame."""
    print("🎮 Ejecutando versión PYGAME...")
    print("=" * 40)
    try:
        import pygame
        print("✅ Pygame disponible")
        
        # Ejecutar el juego en un proceso separado
        import subprocess
        print("🎯 Iniciando juego visual...")
        result = subprocess.run([sys.executable, "lights_out_pygame.py"], 
                              capture_output=False, text=True)
        if result.returncode == 0:
            print("✅ Juego cerrado correctamente")
        else:
            print(f"⚠️ Juego cerrado (código: {result.returncode})")
        
    except ImportError as e:
        print(f"❌ Error: {e}")
        print()
        print("Para usar la versión Pygame, instale las dependencias:")
        print("   pip install -r requirements.txt")
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo lights_out_pygame.py")
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")


def ejecutar_pygame_rapido(tamano):
    """Ejecuta pygame con un tamaño específico."""
    print(f"🎮 Ejecutando versión PYGAME {tamano}×{tamano}...")
    print("=" * 40)
    try:
        import pygame
        print("✅ Pygame disponible")
        
        # Ejecutar el juego en un proceso separado con tamaño específico
        import subprocess
        print(f"🎯 Iniciando juego visual {tamano}×{tamano}...")
        result = subprocess.run([sys.executable, "-c", f"""
import sys
sys.path.append('.')
from lights_out_pygame import LightsOutGame
try:
    juego = LightsOutGame({tamano})
    juego.ejecutar()
except Exception as e:
    print(f'Error: {{e}}')
"""], capture_output=False, text=True)
        
        if result.returncode == 0:
            print("✅ Juego cerrado correctamente")
        else:
            print(f"⚠️ Juego cerrado (código: {result.returncode})")
        
    except ImportError as e:
        print(f"❌ Error: {e}")
        print()
        print("Para usar la versión Pygame, instale las dependencias:")
        print("   pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")

def main():
    """Función principal del demostrador."""
    while True:
        mostrar_menu()
        
        try:
            opcion = input("Ingrese su opción (0-5): ").strip()
            print()
            
            if opcion == "0":
                print("👋 ¡Hasta luego!")
                break
                
            elif opcion == "1":
                ejecutar_version_consola()
                input("\nPresione Enter para continuar...")
                print()
                
            elif opcion == "2":
                ejecutar_version_pygame()
                input("\nPresione Enter para continuar...")
                print()
                
            elif opcion == "3":
                print("🔄 Ejecutando AMBAS versiones...")
                print()
                ejecutar_version_consola()
                print()
                input("Presione Enter para continuar con la versión Pygame...")
                print()
                ejecutar_version_pygame()
                input("\nPresione Enter para continuar...")
                print()
                
            elif opcion == "4":
                ejecutar_pygame_rapido(3)
                input("\nPresione Enter para continuar...")
                print()
                
            elif opcion == "5":
                ejecutar_pygame_rapido(5)
                input("\nPresione Enter para continuar...")
                print()
                
            else:
                print("❌ Opción no válida. Por favor seleccione 0, 1, 2, 3, 4 o 5.")
                input("Presione Enter para continuar...")
                print()
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            input("Presione Enter para continuar...")
            print()

if __name__ == "__main__":
    main()