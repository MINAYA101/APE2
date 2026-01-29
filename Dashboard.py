import os
import subprocess

class Dashboard:
    """
    Versión 1: Encapsulamiento Básico.
    Se agrupan las funciones dentro de una clase para organizar el código.
    """
    def __init__(self):
        self.ruta_base = os.path.dirname(__file__)
        self.unidades = {
            '1': 'UNIDAD 1',
            '2': 'UNIDAD 2'
        }

    def mostrar_codigo(self, ruta_script):
        ruta_script_absoluta = os.path.abspath(ruta_script)
        try:
            with open(ruta_script_absoluta, 'r') as archivo:
                codigo = archivo.read()
                print(f"\n--- Código de {ruta_script} ---\n")
                print(codigo)
                return codigo
        except FileNotFoundError:
            print("El archivo no se encontró.")
            return None
        except Exception as e:
            print(f"Ocurrió un error al leer el archivo: {e}")
            return None

    def ejecutar_codigo(self, ruta_script):
        try:
            if os.name == 'nt':  # Windows
                subprocess.Popen(['cmd', '/k', 'python', ruta_script])
            else:  # Unix-based systems
                # En entornos sin xterm, intentamos ejecutar directamente
                subprocess.run(['python3', ruta_script])
        except Exception as e:
            print(f"Ocurrió un error al ejecutar el código: {e}")

    def mostrar_menu(self):
        while True:
            print("\nMenu Principal - Dashboard (v1: Clase Básica)")
            for key in self.unidades:
                print(f"{key} - {self.unidades[key]}")
            print("0 - Salir")

            eleccion_unidad = input("Elige una unidad o '0' para salir: ")
            if eleccion_unidad == '0':
                print("Saliendo del programa.")
                break
            elif eleccion_unidad in self.unidades:
                self.mostrar_sub_menu(os.path.join(self.ruta_base, self.unidades[eleccion_unidad]))
            else:
                print("Opción no válida.")

    def mostrar_sub_menu(self, ruta_unidad):
        if not os.path.exists(ruta_unidad):
            print(f"Error: La ruta {ruta_unidad} no existe.")
            return
            
        sub_carpetas = [f.name for f in os.scandir(ruta_unidad) if f.is_dir()]

        while True:
            print("\nSubmenú - Selecciona una subcarpeta")
            for i, carpeta in enumerate(sub_carpetas, start=1):
                print(f"{i} - {carpeta}")
            print("0 - Regresar al menú principal")

            eleccion_carpeta = input("Elige una subcarpeta o '0' para regresar: ")
            if eleccion_carpeta == '0':
                break
            else:
                try:
                    indice = int(eleccion_carpeta) - 1
                    if 0 <= indice < len(sub_carpetas):
                        self.mostrar_scripts(os.path.join(ruta_unidad, sub_carpetas[indice]))
                    else:
                        print("Opción no válida.")
                except ValueError:
                    print("Opción no válida.")

    def mostrar_scripts(self, ruta_sub_carpeta):
        scripts = [f.name for f in os.scandir(ruta_sub_carpeta) if f.is_file() and f.name.endswith('.py')]

        while True:
            print("\nScripts - Selecciona un script")
            for i, script in enumerate(scripts, start=1):
                print(f"{i} - {script}")
            print("0 - Regresar")
            print("9 - Menú Principal")

            eleccion_script = input("Elige un script: ")
            if eleccion_script == '0':
                break
            elif eleccion_script == '9':
                return
            else:
                try:
                    indice = int(eleccion_script) - 1
                    if 0 <= indice < len(scripts):
                        ruta_script = os.path.join(ruta_sub_carpeta, scripts[indice])
                        if self.mostrar_codigo(ruta_script):
                            ejecutar = input("¿Ejecutar? (1: Sí, 0: No): ")
                            if ejecutar == '1':
                                self.ejecutar_codigo(ruta_script)
                    else:
                        print("Opción no válida.")
                except ValueError:
                    print("Opción no válida.")

if __name__ == "__main__":
    app = Dashboard()
    app.mostrar_menu()