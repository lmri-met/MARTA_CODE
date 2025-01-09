import tkinter as tk
from tkinter import ttk
import importlib
from PIL import Image, ImageTk  
import webbrowser
from subframe_medidas_equipo import crear_subframes_medidas


def activar_menu():
    for boton in botones_menu:
        boton.config(state="normal")

# Crear la ventana principal
root = tk.Tk()
root.title("MARTA: Metrological Analysis and calibration of x-Ray´s monitors with Traceability and Accuracy")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

# Frame superior con título centrado y botón de cerrar alineado a la derecha
frame_superior = tk.Frame(root, bg="#001f3f", relief="raised", bd=2)
frame_superior.pack(side="top", fill="x")

# Usar grid para posicionar elementos en una sola línea
frame_superior.grid_columnconfigure(0, weight=1)
frame_superior.grid_columnconfigure(1, weight=0)

# Reducir padding para hacer el frame la mitad de alto
titulo = tk.Label(
    frame_superior,
    text="IR14D: CALIBRACIÓN DE EQUIPOS DE RAYOS X",
    font=("Arial", 14, "bold"),  # Reducir tamaño de la fuente
    bg="#001f3f",
    fg="white"
)
titulo.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")  # Reducir padding vertical

# Botón de cerrar con padding reducido
cerrar_boton = tk.Button(
    frame_superior,
    text="✖",
    font=("Arial", 12),  # Reducir tamaño de la fuente
    bg="red",
    fg="white",
    command=root.destroy
)
cerrar_boton.grid(row=0, column=1, padx=10, pady=5, sticky="e")  # Reducir padding vertical

# Frame contenedor inferior
frame_inferior_contenedor = tk.Frame(root)
frame_inferior_contenedor.pack(side="top", fill="both", expand=True)

# Frame izquierdo (menú)
frame_inferior_izquierdo = tk.Frame(frame_inferior_contenedor, width=200, bg="#001f3f", relief="sunken", bd=2)
frame_inferior_izquierdo.pack(side="left", fill="y")

# Opciones del menú
opciones = [
    "Acciones previas", 
    "Datos del servicio", 
    "Condiciones de calibración", 
    "Medidas Equipo + Monitora",
    "Medidas Patrón + Monitora",
    "Cálculo factor distancia",
    "Valor convencionalmente verdadero",
    "Cálculo factor de calibración",
    "Incertidumbres A y B",
    "Resultados: Aceptación/Rechazo"
]
botones_menu = []
estado_botones = {}

def mostrar_opcion(opcion):
    # Cambiar el color del botón seleccionado a naranja
    boton_actual = estado_botones[opcion]
    boton_actual.config(bg="#FFA500", fg="black", font=("Arial", 9, "bold"))

    # Limpiar cualquier contenido existente en el frame derecho
    for widget in frame_inferior_derecho.winfo_children():
        widget.destroy()

    # Restablecer los estilos de los demás botones
    for boton_opcion, boton in estado_botones.items():
        if boton_opcion != opcion:
            boton.config(bg="white", fg="black", font=("Arial", 9))

    frame = None

    # Importar y mostrar el frame correspondiente
    try:
        if opcion == "Acciones previas":
            module = importlib.import_module("actionsprevias")
            frame = module.create_actionsprevias_frame(frame_inferior_derecho, activar_menu)
        elif opcion == "Datos del servicio":
            module = importlib.import_module("subframe_datos_servicio")
            frame = module.create_datos_servicio_frame(frame_inferior_derecho)
        elif opcion == "Condiciones de calibración":
            module = importlib.import_module("subframe_condiciones")
            frame = module.create_condiciones_frame(frame_inferior_derecho)
        elif opcion == "Medidas Equipo + Monitora":
            module = importlib.import_module("subframe_medidas_equipo")
            crear_subframes_medidas(frame_inferior_derecho)
        elif opcion == "Medidas Patrón + Monitora":
            module = importlib.import_module("subframe_camara_patron")
            frame = module.create_camara_patron_frame(frame_inferior_derecho)
        elif opcion == "Cálculo factor distancia":
            module = importlib.import_module("subframe_factor_distancia")
            frame = module.create_factor_distancia_frame(frame_inferior_derecho)
        elif opcion == "Valor convencionalmente verdadero":
            module = importlib.import_module("subframe_valor_convencional")
            frame = module.create_valor_convencional_frame(frame_inferior_derecho)
        elif opcion == "Cálculo factor de calibración":
            module = importlib.import_module("subframe_factor_calibracion")
            frame = module.create_factor_calibracion_frame(frame_inferior_derecho)
        elif opcion == "Incertidumbres A y B":
            module = importlib.import_module("subframe_incertidumbres")
            frame = module.create_incertidumbres_frame(frame_inferior_derecho)
        elif opcion == "Resultados: Aceptación/Rechazo":
            module = importlib.import_module("subframe_resumen")
            frame = module.create_resumen_frame(frame_inferior_derecho)
    except Exception as e:
        print(f"Error al importar o crear el frame para la opción '{opcion}': {e}")

    if frame is not None:
        frame.grid(row=0, column=0, sticky="nsew")
        frame_inferior_derecho.grid_rowconfigure(0, weight=1)
        frame_inferior_derecho.grid_columnconfigure(0, weight=1)

    # Cambiar el fondo del botón a verde después de cargar el contenido
    boton_actual.config(bg="#90EE90", fg="black")

    # Activar todas las opciones del menú al finalizar "Acciones previas"
    if opcion == "Acciones previas":
        activar_menu()

# Crear botones del menú
for opcion in opciones:
    boton = tk.Button(
        frame_inferior_izquierdo, 
        text=opcion, 
        state="disabled", 
        font=("Arial", 9), 
        bg="white", 
        fg="black",
        command=lambda opt=opcion: mostrar_opcion(opt)
    )
    boton.pack(pady=10, padx=10, fill="x")
    botones_menu.append(boton)
    estado_botones[opcion] = boton

# Habilitar solo la primera opción al inicio
botones_menu[0].config(state="normal")

# Crear un frame interno en el frame izquierdo para colocar el logo y texto al fondo
frame_logo_texto = tk.Frame(frame_inferior_izquierdo, bg="#001f3f")
frame_logo_texto.pack(side="bottom", fill="x", pady=10)

# Cargar y redimensionar la imagen del logo
logo_path = "LMRI.png"  # Asegúrate de tener la imagen en el mismo directorio que el script
try:
    original_image = Image.open(logo_path)
    resized_image = original_image.resize((180, int(original_image.height / original_image.width * 180)))
    logo_image = ImageTk.PhotoImage(resized_image)
    logo_label = tk.Label(frame_logo_texto, image=logo_image, bg="#001f3f")
    logo_label.image = logo_image  # Evitar garbage collector
    logo_label.pack(pady=5)
except Exception as e:
    print(f"Error al cargar la imagen del logo: {e}")

# Función para abrir el correo
def abrir_correo():
    webbrowser.open("mailto:miguel.embid@ciemat.es")

# Texto clicable con enlace de correo
correo_label = tk.Label(
    frame_logo_texto,
    text="Miguel Embid Segura",
    fg="white",
    bg="#001f3f",
    font=("Arial", 10, "bold"),
    cursor="hand2"
)
correo_label.pack(pady=5)
correo_label.bind("<Button-1>", lambda e: abrir_correo())

# Frame derecho (contenido dinámico)
frame_inferior_derecho = tk.Frame(frame_inferior_contenedor, bg="white", relief="raised", bd=5)
frame_inferior_derecho.pack(side="right", fill="both", expand=True)

root.mainloop()
