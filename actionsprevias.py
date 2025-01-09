import tkinter as tk
from tkinter import messagebox
import os
import json

# Nombre de la carpeta y archivo
CARPETA_REGISTROS = "AAA_ST_REGISTROS"
ARCHIVO_ACCIONES = "acciones.json"

# Estados iniciales de las acciones
ESTADOS_INICIALES = {
    "LaserTEST": False,
    "ColimadoresTEST": False,
    "ColimadoresPOS": False,
    "EquipoPOS": False,
    "ObturadorONOFF": False,
    "FiltrosONOFF": False,
    "ElectrometroTEST": False,
    "BarometroTEST": False,
    "TermometroTEST": False,
    "PRONOFF": False,
    "WebareaONOFF": False,
    "RodajeTEST": False,    
}

ACCIONES_COMPLETAS = {
    "LaserTEST": "Comprobación del láser",
    "ColimadoresTEST": "Encender fuente de alimentación de colimadores",
    "ColimadoresPOS": "Posicionar colimadores", 
    "EquipoPOS": "Posicionar equipo del cliente",
    "ObturadorONOFF": "Encender obturador",
    "FiltrosONOFF": "Encender rueda de filtros",
    "ElectrometroTEST": "Chequear electrómetro cámara monitora",
    "BarometroTEST": "Chequear barómetro",
    "TermometroTEST": "Chequear termómetro",
    "PRONOFF": "Chequear equipos de PR y dosímetro",
    "WebareaONOFF": "Chequear cámara de área",
    "RodajeTEST": "Rodaje de tubo de rayos X",   
}


def inicializar_registros():
    """Inicializa la carpeta de registros y el archivo JSON según las opciones del usuario."""
    estados = [ESTADOS_INICIALES]  # Usamos lista mutable para asegurar la persistencia entre closures

    # Verificar si la carpeta existe
    if os.path.exists(CARPETA_REGISTROS):
        ventana = tk.Toplevel()
        ventana.title("Carpeta existente")
        ventana.geometry("300x150")
        tk.Label(ventana, text="La carpeta ya existe. ¿Qué desea hacer?", font=("Arial", 12)).pack(pady=10)

        def conservar():
            # Cargar los estados si el archivo existe, de lo contrario, usar iniciales
            archivo_acciones = os.path.join(CARPETA_REGISTROS, ARCHIVO_ACCIONES)
            if os.path.exists(archivo_acciones):
                with open(archivo_acciones, "r") as f:
                    estados[0] = json.load(f)
            else:
                messagebox.showerror(
                    "Error", 
                    f"No se encontró '{ARCHIVO_ACCIONES}' en '{CARPETA_REGISTROS}'. Se inicializarán valores predeterminados."
                )
                estados[0] = ESTADOS_INICIALES
            ventana.destroy()

        def borrar():
            # Intentar borrar la carpeta solo si existe
            if os.path.exists(CARPETA_REGISTROS):
                for root, dirs, files in os.walk(CARPETA_REGISTROS, topdown=False):
                    for file in files:
                        os.remove(os.path.join(root, file))
                    for dir in dirs:
                        os.rmdir(os.path.join(root, dir))
                os.rmdir(CARPETA_REGISTROS)
            os.makedirs(CARPETA_REGISTROS, exist_ok=True)
            with open(os.path.join(CARPETA_REGISTROS, ARCHIVO_ACCIONES), "w") as f:
                json.dump(ESTADOS_INICIALES, f)
            estados[0] = ESTADOS_INICIALES
            ventana.destroy()

        def renombrar():
            i = 1
            nueva_carpeta = f"{CARPETA_REGISTROS}_01"
            while os.path.exists(nueva_carpeta):
                i += 1
                nueva_carpeta = f"{CARPETA_REGISTROS}_{i:02d}"
            os.rename(CARPETA_REGISTROS, nueva_carpeta)
            os.makedirs(CARPETA_REGISTROS, exist_ok=True)
            with open(os.path.join(CARPETA_REGISTROS, ARCHIVO_ACCIONES), "w") as f:
                json.dump(ESTADOS_INICIALES, f)
            estados[0] = ESTADOS_INICIALES
            ventana.destroy()

        tk.Button(ventana, text="Conservar", command=conservar).pack(side="left", padx=10, pady=10)
        tk.Button(ventana, text="Borrar", command=borrar).pack(side="left", padx=10, pady=10)
        tk.Button(ventana, text="Renombrar", command=renombrar).pack(side="left", padx=10, pady=10)
        ventana.wait_window()
    else:
        # Crear la carpeta y el archivo inicial si no existen
        os.makedirs(CARPETA_REGISTROS, exist_ok=True)
        with open(os.path.join(CARPETA_REGISTROS, ARCHIVO_ACCIONES), "w") as f:
            json.dump(ESTADOS_INICIALES, f)
        estados[0] = ESTADOS_INICIALES

    return estados[0]

def actualizar_registro(clave, estado):
    """Actualiza el archivo JSON con el nuevo estado."""
    ruta_json = os.path.join(CARPETA_REGISTROS, ARCHIVO_ACCIONES)
    if os.path.exists(ruta_json):
        with open(ruta_json, "r") as f:
            data = json.load(f)
    else:
        data = ESTADOS_INICIALES
    data[clave] = estado
    with open(ruta_json, "w") as f:
        json.dump(data, f, indent=4)

from PIL import Image, ImageTk

def create_actionsprevias_frame(parent, activar_menu_callback):
    """Crea un frame con contenido específico para 'Acciones previas'."""
    estados = inicializar_registros()
    frame = tk.Frame(parent, bg="white", padx=10, pady=10)
    tk.Label(frame, text="Acciones Previas", bg="lightblue", font=("Arial", 16, "bold")).pack(pady=10)

    # Diccionario de archivos de ayuda
    archivos_ayuda = {
        "LaserTEST": "laser.jpeg",
        "ColimadoresTEST": "colimadores.jpeg",
        "ColimadoresPOS": "colimadores_pos.jpeg",
        "EquipoPOS": "equipo_pos.jpeg",
        "ObturadorONOFF": "obturador_jpeg",
        "FiltrosONOFF": "filtros.jpeg",
        "ElectrometroTEST": "electrometro.jpeg",
        "BarometroTEST": "barometro.jpeg",
        "TermometroTEST": "termometro.jpeg",
        "PRONOFF": "pr_dosimetro.jpeg",
        "WebareaONOFF": "webcam.jpeg",
        "RodajeTEST": "rodaje.jpeg",
    }

    def verificar_completado():
        """Verifica si todas las acciones están completas y llama al callback para activar el menú."""
        if all(estados.values()):
            activar_menu_callback()

    def crear_toggle(clave, frame, label, boton):
        """Crea una función de toggle para manejar el botón correctamente."""
        def toggle_estado():
            estados[clave] = not estados[clave]
            frame.config(bg="lightgreen" if estados[clave] else "lightgray")
            label.config(bg="lightgreen" if estados[clave] else "lightgray")
            boton.config(text="✔" if estados[clave] else "")  # Actualizar el texto del botón
            actualizar_registro(clave, estados[clave])
            verificar_completado()
        return toggle_estado

    def mostrar_imagen_ayuda(event, imagen_path, dimensiones=(400, 300)):
        """Muestra una ventana emergente con la imagen centrada en pantalla."""
        ventana_imagen = tk.Toplevel()
        ventana_imagen.title("Ayuda")
        ventana_imagen.overrideredirect(True)

        # Resolver la ruta absoluta de la imagen
        ruta_absoluta = os.path.abspath(imagen_path)

        try:
            img = Image.open(ruta_absoluta)
            img = img.resize(dimensiones)  # Redimensionar la imagen
            img_tk = ImageTk.PhotoImage(img)

            label_imagen = tk.Label(ventana_imagen, image=img_tk)
            label_imagen.image = img_tk  # Guardar referencia para evitar recolección de basura
            label_imagen.pack()
        except Exception as e:
            tk.Label(ventana_imagen, text=f"No se pudo cargar la imagen: {e}", fg="red").pack()

        # Calcular el centro de la pantalla
        screen_width = ventana_imagen.winfo_screenwidth()
        screen_height = ventana_imagen.winfo_screenheight()
        x_centrado = (screen_width - dimensiones[0]) // 2
        y_centrado = (screen_height - dimensiones[1]) // 2

        # Configurar la posición de la ventana
        ventana_imagen.geometry(f"{dimensiones[0]}x{dimensiones[1]}+{x_centrado}+{y_centrado}")

        # Cierra la ventana cuando el mouse sale
        event.widget.bind("<Leave>", lambda e: ventana_imagen.destroy())

    # Tamaños específicos para cada acción
    tamaños_imagenes = {
        "LaserTEST": (400, 300),
        "ColimadoresTEST": (450, 300),
        "ColimadoresPOS": (400, 400),
        "EquipoPOS": (350, 300),
        "ObturadorONOFF": (350, 300),
        "FiltrosONOFF": (350, 300),
        "ElectrometroTEST": (400, 300),
        "BarometroTEST": (400, 400),
        "TermometroTEST": (800, 500),
        "PRONOFF": (400, 300),
        "WebareaONOFF": (400, 300),
        "RodajeTEST": (500, 350),               
    }

    for clave, descripcion in ACCIONES_COMPLETAS.items():
        # Crear un frame para cada acción
        action_frame = tk.Frame(frame, bg="lightgreen" if estados[clave] else "lightgray", pady=5)
        action_frame.pack(fill="x", pady=2)

        # Etiqueta para la descripción de la acción
        descripcion_label = tk.Label(
            action_frame,
            text=descripcion,
            bg="lightgreen" if estados[clave] else "lightgray",
            font=("Arial", 12),
        )
        descripcion_label.pack(side="left", padx=5)

        # Botón de chequeo
        boton_chequeo = tk.Button(
            action_frame,
            text="✔" if estados[clave] else "",
            width=2,
            font=("Arial", 12),
        )
        boton_chequeo.pack(side="left", padx=5)
        boton_chequeo.config(command=crear_toggle(clave, action_frame, descripcion_label, boton_chequeo))

        # Agregar botón "TEST" para barómetro, termómetro y electrómetro
        if clave == "ElectrometroTEST":
            def realizar_test_electrometro():
                """Ejecuta el test del electrómetro utilizando UNIDOS10022_Web.py."""
                import subprocess
                try:
                    # Ejecutar el script UNIDOS10022_Web.py como subproceso
                    resultado = subprocess.run(
                        [r"T:\SIGOR\SGC\MARXAN\Pruebas de desarrollo\14DCALIB\venv\Scripts\python", 
                         r"T:\SIGOR\SGC\MARXAN\Pruebas de desarrollo\14DCALIB\UNIDOS10022_Web.py"],  
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )

                    # Procesar la salida
                    if resultado.returncode == 0:
                        salida = resultado.stdout.strip()
                        # Crear ventana emergente personalizada
                        ventana_test = tk.Toplevel()
                        ventana_test.title("Test del Electrómetro")
                        ventana_test.configure(bg="#ADFF2F")  # Fondo azul claro

                        # Mensajes en la ventana emergente
                        tk.Label(
                            ventana_test,
                            text="Electrómetro funcionando correctamente.",
                            font=("Arial", 12),
                            bg="#ADFF2F"
                        ).pack(pady=5)

                        tk.Label(
                            ventana_test,
                            text=f"Salida del test:\n{salida}",
                            font=("Arial", 10),
                            bg="#ADFF2F",
                            wraplength=400,  # Ajuste de texto largo
                            justify="left",
                        ).pack(pady=10)

                        # Botón para cerrar la ventana emergente
                        tk.Button(
                            ventana_test,
                            text="Cerrar",
                            font=("Arial", 10),
                            command=ventana_test.destroy
                        ).pack(pady=10)
                    else:
                        # Mostrar error en caso de fallo
                        messagebox.showerror(
                            "Error",
                            f"Error al ejecutar el test del electrómetro:\n{resultado.stderr.strip()}",
                        )
                except FileNotFoundError:
                    messagebox.showerror(
                        "Error",
                        "No se encontró el archivo UNIDOS10022_Web.py. Asegúrate de que está en el directorio correcto.",
                    )
                except Exception as e:
                    messagebox.showerror(
                        "Error",
                        f"Error inesperado al ejecutar el test del electrómetro: {e}",
                    )
            if clave == "ElectrometroTEST":
                # Crear botón "TEST" para el electrómetro
                boton_test = tk.Button(
                    action_frame,
                    text="TEST",
                    width=6,
                    font=("Arial", 10),
                    bg="light blue",
                    fg="black",
                    command=realizar_test_electrometro,
                )
                boton_test.pack(side="left", padx=5)

        elif clave == "BarometroTEST":
            def realizar_test_barometro():
                import subprocess
                try:
                    # Ejecutar el script BarometerWeston_v4.py como subproceso
                    resultado = subprocess.run(
                        [r"T:\SIGOR\SGC\MARXAN\Pruebas de desarrollo\14DCALIB\venv\Scripts\python", 
                         r"T:\SIGOR\SGC\MARXAN\Pruebas de desarrollo\14DCALIB\BarometerWeston_v4.py", "read_pressure"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )

                    # Procesar la salida
                    if resultado.returncode == 0:
                        valor = resultado.stdout.strip()
                        # Crear ventana emergente personalizada
                        ventana_test = tk.Toplevel()
                        ventana_test.title("Test del Barómetro")
                        ventana_test.configure(bg="#ADFF2F")  # Fondo verde limón chillón

                        # Mensajes en la ventana emergente
                        tk.Label(
                            ventana_test,
                            text=f"Presión actual (kPa) = {valor}",
                            font=("Arial", 14),
                            bg="#ADFF2F"
                        ).pack(pady=10)

                        tk.Label(
                            ventana_test,
                            text="Barómetro funcionando correctamente.",
                            font=("Arial", 12),
                            bg="#ADFF2F"
                        ).pack(pady=5)

                        # Botón para cerrar la ventana emergente
                        tk.Button(
                            ventana_test,
                            text="Cerrar",
                            font=("Arial", 10),
                            command=ventana_test.destroy
                        ).pack(pady=10)
                    else:
                        messagebox.showerror(
                            "Error",
                            f"Error al ejecutar el test del barómetro:\n{resultado.stderr.strip()}",
                        )
                except FileNotFoundError:
                    messagebox.showerror(
                        "Error",
                        "No se encontró el archivo BarometerWeston_v4.py. Asegúrate de que está en el directorio correcto.",
                    )
                except Exception as e:
                    messagebox.showerror(
                        "Error",
                        f"Error inesperado al ejecutar el test del barómetro: {e}",
                    )

            # Crear botón "TEST" para el barómetro
            boton_test = tk.Button(
                action_frame,
                text="TEST",
                width=6,
                font=("Arial", 10),
                bg="light blue",
                fg="black",
                command=realizar_test_barometro,
            )
            boton_test.pack(side="left", padx=5)

        elif clave == "TermometroTEST":
            def realizar_test_termometro():
                import subprocess
                import tkinter as tk
                from tkinter import messagebox
                try:
                    # Ejecutar el script Thermometer_MKT50.py como subproceso
                    resultado = subprocess.run(
                        [r"T:\SIGOR\SGC\MARXAN\Pruebas de desarrollo\14DCALIB\venv\Scripts\python", 
                        r"T:\SIGOR\SGC\MARXAN\Pruebas de desarrollo\14DCALIB\Thermometer_MKT50.py"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )

                    # Procesar la salida
                    if resultado.returncode == 0:
                        # Leer y separar las temperaturas de la salida
                        valores = resultado.stdout.strip().splitlines()
                        if len(valores) >= 2:
                            temperatura_t1 = valores[0]
                            temperatura_t2 = valores[1]
                        else:
                            raise ValueError("No se recibieron ambas temperaturas desde el script.")

                        # Crear ventana emergente personalizada
                        ventana_test = tk.Toplevel()
                        ventana_test.title("Test del Termómetro")
                        ventana_test.configure(bg="#ADFF2F")  # Fondo verde limón chillón

                        # Mostrar las temperaturas en la ventana
                        tk.Label(
                            ventana_test,
                            text=f"Temperatura T1 (Cámara monitora): {temperatura_t1}°C",
                            font=("Arial", 14),
                            bg="#ADFF2F"
                        ).pack(pady=10)

                        tk.Label(
                            ventana_test,
                            text=f"Temperatura T2 (Plataforma de medida): {temperatura_t2}°C",
                            font=("Arial", 14),
                            bg="#ADFF2F"
                        ).pack(pady=10)

                        # Mensaje adicional
                        tk.Label(
                            ventana_test,
                            text="Termómetro funcionando correctamente.",
                            font=("Arial", 12),
                            bg="#ADFF2F"
                        ).pack(pady=5)

                        # Botón para cerrar la ventana emergente
                        tk.Button(
                            ventana_test,
                            text="Cerrar",
                            font=("Arial", 10),
                            command=ventana_test.destroy
                        ).pack(pady=10)
                    else:
                        messagebox.showerror(
                            "Error",
                            f"Error al ejecutar el test del termómetro:\n{resultado.stderr.strip()}",
                        )
                except FileNotFoundError:
                    messagebox.showerror(
                        "Error",
                        "No se encontró el archivo Thermometer_MKT50.py. Asegúrate de que está en el directorio correcto.",
                    )
                except Exception as e:
                    messagebox.showerror(
                        "Error",
                        f"Error inesperado al ejecutar el test del termómetro: {e}",
                    )


            # Crear botón "TEST" para el termómetro
            boton_test = tk.Button(
                action_frame,
                text="TEST",
                width=6,
                font=("Arial", 10),
                bg="light blue",
                fg="black",
                command=realizar_test_termometro,
            )
            boton_test.pack(side="left", padx=5)

        # Asignar ruta de ayuda y tamaño
        archivo_ayuda = archivos_ayuda.get(clave, "default.jpeg")
        tamaño_imagen = tamaños_imagenes.get(clave, (400, 300))  # Tamaño por defecto

        # Crear enlace de ayuda
        ayuda_label = tk.Label(
            action_frame,
            text="Ayuda",
            fg="blue",
            cursor="hand2",
            font=("Arial", 10, "underline"),
            bg="lightgray",
        )
        ayuda_label.pack(side="right", padx=5)
        ayuda_label.bind("<Enter>", lambda e, path=archivo_ayuda, size=tamaño_imagen: mostrar_imagen_ayuda(e, path, dimensiones=size))

    return frame
