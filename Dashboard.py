import os
import subprocess

class GestorArchivos:
    """Clase especializada en manejar operaciones de archivos."""
    @staticmethod
    def leer_archivo(ruta):
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error al leer: {e}"

    @staticmethod
    def listar_directorios(ruta):
        if not os.path.exists(ruta): return []
        return [f.name for f in os.scandir(ruta) if f.is_dir()]

    @staticmethod
    def listar_scripts(ruta):
        if not os.path.exists(ruta): return []
        return [f.name for f in os.scandir(ruta) if f.is_file() and f.name.endswith('.py')]

class Dashboard:
    """
    Versión 2: Modularización.
    Se separa la lógica de archivos de la lógica de la interfaz.
    """
    def __init__(self):
        # Ajuste para encontrar la carpeta del proyecto si se ejecuta desde fuera
        self.ruta_base = "/home/ubuntu/proyecto_poo"
        self.gestor = GestorArchivos()
        self.unidades = {'1': 'UNIDAD 1', '2': 'UNIDAD 2'}

    def ejecutar_script(self, ruta):
        print(f"\n--- Ejecutando: {os.path.basename(ruta)} ---")
        try:
            subprocess.run(['python3', ruta])
        except Exception as e:
            print(f"Error de ejecución: {e}")

    def menu_principal(self):
        while True:
            print("\n=== DASHBOARD POO v2 (Modular) ===")
            for k, v in self.unidades.items():
                print(f"{k}. {v}")
            print("0. Salir")
            
            opcion = input("Seleccione unidad: ")
            if opcion == '0': break
            if opcion in self.unidades:
                self.menu_subcarpetas(os.path.join(self.ruta_base, self.unidades[opcion]))

    def menu_subcarpetas(self, ruta_unidad):
        carpetas = self.gestor.listar_directorios(ruta_unidad)
        while True:
            print(f"\n--- {os.path.basename(ruta_unidad)} ---")
            for i, c in enumerate(carpetas, 1):
                print(f"{i}. {c}")
            print("0. Volver")
            
            opcion = input("Seleccione carpeta: ")
            if opcion == '0': break
            try:
                idx = int(opcion) - 1
                if 0 <= idx < len(carpetas):
                    self.menu_scripts(os.path.join(ruta_unidad, carpetas[idx]))
            except ValueError: pass

    def menu_scripts(self, ruta_carpeta):
        scripts = self.gestor.listar_scripts(ruta_carpeta)
        while True:
            print(f"\n--- Scripts en {os.path.basename(ruta_carpeta)} ---")
            for i, s in enumerate(scripts, 1):
                print(f"{i}. {s}")
            print("0. Volver")
            
            opcion = input("Seleccione script: ")
            if opcion == '0': break
            try:
                idx = int(opcion) - 1
                if 0 <= idx < len(scripts):
                    ruta_s = os.path.join(ruta_carpeta, scripts[idx])
                    print("\nCONTENIDO:")
                    print(self.gestor.leer_archivo(ruta_s))
                    if input("\n¿Ejecutar? (s/n): ").lower() == 's':
                        self.ejecutar_script(ruta_s)
            except ValueError: pass

if __name__ == "__main__":
    Dashboard().menu_principal()