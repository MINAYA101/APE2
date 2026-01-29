import os
import subprocess
from abc import ABC, abstractmethod

# --- PATRÓN STRATEGY PARA EJECUCIÓN ---
class EstrategiaEjecucion(ABC):
    @abstractmethod
    def ejecutar(self, ruta):
        pass

class EjecutorPython(EstrategiaEjecucion):
    def ejecutar(self, ruta):
        print(f"\n>>> Iniciando ejecución de: {os.path.basename(ruta)}")
        try:
            if os.name == 'nt':
                subprocess.Popen(['cmd', '/k', 'python', ruta])
            else:
                subprocess.run(['python3', ruta], check=True)
        except Exception as e:
            print(f"Error en la ejecución: {e}")

# --- CLASE DE DATOS PARA SCRIPTS ---
class ScriptPython:
    def __init__(self, ruta):
        self.ruta = ruta
        self.nombre = os.path.basename(ruta)

    def leer_contenido(self):
        try:
            with open(self.ruta, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"No se pudo leer el archivo: {e}"

# --- COMPONENTE DE INTERFAZ (SINGLETON) ---
class InterfazConsola:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(InterfazConsola, cls).__new__(cls)
        return cls._instancia

    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def imprimir_menu(self, titulo, opciones):
        print(f"\n{'*'*40}")
        print(f"{titulo.center(40)}")
        print(f"{'*'*40}")
        for i, opt in enumerate(opciones, 1):
            print(f"  [{i}] {opt}")
        print(f"  [0] Salir/Volver")
        print(f"{'*'*40}")

    def solicitar_opcion(self, max_val):
        while True:
            try:
                val = int(input(f"\nSeleccione una opción (0-{max_val}): "))
                if 0 <= val <= max_val: return val
                print("Fuera de rango.")
            except ValueError:
                print("Entrada inválida.")

# --- CONTROLADOR PRINCIPAL ---
class DashboardAvanzado:
    def __init__(self, ruta_raiz):
        self.ruta_raiz = ruta_raiz
        self.ui = InterfazConsola()
        self.ejecutor = EjecutorPython()

    def iniciar(self):
        while True:
            self.ui.limpiar_pantalla()
            if not os.path.exists(self.ruta_raiz):
                print(f"Error: No se encuentra la ruta raíz {self.ruta_raiz}")
                break
                
            unidades = sorted([d.name for d in os.scandir(self.ruta_raiz) if d.is_dir() and d.name.startswith('UNIDAD')])
            
            self.ui.imprimir_menu("SISTEMA DE GESTIÓN POO - V4", unidades)
            opc = self.ui.solicitar_opcion(len(unidades))
            
            if opc == 0: break
            self.gestionar_unidad(os.path.join(self.ruta_raiz, unidades[opc-1]))

    def gestionar_unidad(self, ruta_unidad):
        while True:
            self.ui.limpiar_pantalla()
            carpetas = sorted([d.name for d in os.scandir(ruta_unidad) if d.is_dir()])
            
            self.ui.imprimir_menu(os.path.basename(ruta_unidad), carpetas)
            opc = self.ui.solicitar_opcion(len(carpetas))
            
            if opc == 0: break
            self.gestionar_scripts(os.path.join(ruta_unidad, carpetas[opc-1]))

    def gestionar_scripts(self, ruta_carpeta):
        while True:
            self.ui.limpiar_pantalla()
            archivos = sorted([f.name for f in os.scandir(ruta_carpeta) if f.name.endswith('.py')])
            
            self.ui.imprimir_menu(f"SCRIPTS: {os.path.basename(ruta_carpeta)}", archivos)
            opc = self.ui.solicitar_opcion(len(archivos))
            
            if opc == 0: break
            
            script = ScriptPython(os.path.join(ruta_carpeta, archivos[opc-1]))
            self.ver_y_ejecutar(script)

    def ver_y_ejecutar(self, script):
        self.ui.limpiar_pantalla()
        print(f"--- VISUALIZANDO: {script.nombre} ---\n")
        print(script.leer_contenido())
        print("\n" + "-"*40)
        
        confirmar = input("\n¿Desea ejecutar este script? (s/n): ").lower()
        if confirmar == 's':
            self.ejecutor.ejecutar(script.ruta)
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    # CORRECCIÓN: Ruta dinámica para portabilidad
    PATH_PROYECTO = os.path.dirname(os.path.abspath(__file__))
    app = DashboardAvanzado(PATH_PROYECTO)
    app.iniciar()