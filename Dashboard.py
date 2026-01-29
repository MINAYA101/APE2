import os
import subprocess

class MenuBase:
    """Clase base para todos los menús (Abstracción)."""
    def __init__(self, titulo):
        self.titulo = titulo

    def mostrar_encabezado(self):
        print(f"\n{'='*30}")
        print(f" {self.titulo.upper()} ")
        print(f"{'='*30}")

    def obtener_opcion(self, max_opc):
        try:
            opc = int(input(f"\nSeleccione una opción (0-{max_opc}): "))
            return opc if 0 <= opc <= max_opc else -1
        except ValueError:
            return -1

class MenuPrincipal(MenuBase):
    """Menú principal que hereda de MenuBase."""
    def __init__(self, unidades, ruta_base):
        super().__init__("Dashboard POO v3 (Herencia)")
        self.unidades = unidades
        self.ruta_base = ruta_base

    def ejecutar(self):
        while True:
            self.mostrar_encabezado()
            opciones = list(self.unidades.values())
            for i, unidad in enumerate(opciones, 1):
                print(f"{i}. {unidad}")
            print("0. Salir")
            
            opc = self.obtener_opcion(len(opciones))
            if opc == 0: break
            if opc > 0:
                ruta = os.path.join(self.ruta_base, opciones[opc-1])
                if os.path.exists(ruta):
                    MenuSubcarpeta(opciones[opc-1], ruta).ejecutar()
                else:
                    print(f"Error: No se encontró la ruta {ruta}")

class MenuSubcarpeta(MenuBase):
    """Menú de subcarpetas."""
    def __init__(self, nombre, ruta):
        super().__init__(nombre)
        self.ruta = ruta

    def ejecutar(self):
        while True:
            self.mostrar_encabezado()
            # CORRECCIÓN: Verificación de existencia de ruta antes de scandir
            if not os.path.exists(self.ruta):
                print(f"Error: La ruta {self.ruta} no existe.")
                break
                
            carpetas = sorted([f.name for f in os.scandir(self.ruta) if f.is_dir()])
            for i, c in enumerate(carpetas, 1):
                print(f"{i}. {c}")
            print("0. Volver")
            
            opc = self.obtener_opcion(len(carpetas))
            if opc == 0: break
            if opc > 0:
                ruta_c = os.path.join(self.ruta, carpetas[opc-1])
                MenuScripts(carpetas[opc-1], ruta_c).ejecutar()

class MenuScripts(MenuBase):
    """Menú final para gestión de scripts."""
    def __init__(self, nombre, ruta):
        super().__init__(nombre)
        self.ruta = ruta

    def ejecutar(self):
        while True:
            self.mostrar_encabezado()
            scripts = sorted([f.name for f in os.scandir(self.ruta) if f.name.endswith('.py')])
            for i, s in enumerate(scripts, 1):
                print(f"{i}. {s}")
            print("0. Volver")
            
            opc = self.obtener_opcion(len(scripts))
            if opc == 0: break
            if opc > 0:
                self.procesar_script(os.path.join(self.ruta, scripts[opc-1]))

    def procesar_script(self, ruta):
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                print(f"\n--- CÓDIGO: {os.path.basename(ruta)} ---\n")
                print(f.read())
            
            if input("\n¿Ejecutar script? (s/n): ").lower() == 's':
                if os.name == 'nt':
                    subprocess.Popen(['cmd', '/k', 'python', ruta])
                else:
                    subprocess.run(['python3', ruta])
                input("\nPresione Enter para continuar...")
        except Exception as e:
            print(f"Error al procesar script: {e}")

if __name__ == "__main__":
    # CORRECCIÓN: Obtener ruta base dinámica
    RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
    unidades = {'1': 'UNIDAD 1', '2': 'UNIDAD 2'}
    MenuPrincipal(unidades, RUTA_BASE).ejecutar()