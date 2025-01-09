import tkinter as tk
from tkinter import ttk
import os
import numpy as np
from camara1WEB import crear_recuadro1_imagen
from Thermometer_MKT50 import obtener_temperatura_puerto 
import subprocess
import sys
import serial
import json

fila_actual = 0  # Índice para rastrear la fila actual de la tabla

def agregar_tabla_resumen_con_celdas(frame, numero_escalas, escalas):
    tabla_frame = tk.Frame(frame, bg="white", padx=0, pady=0)
    tabla_frame.pack(side="left", fill="x", expand=True, pady=0)

    # Crear encabezados
    tk.Label(tabla_frame, text="Tasa de Fondo", bg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky="nsew")
    tk.Label(tabla_frame, text="Tasa de Dosis", bg="white", font=("Arial", 10, "bold")).grid(row=0, column=2, columnspan=4, sticky="nsew")
    tk.Label(tabla_frame, text="Tasa de Dosis Integrada", bg="white", font=("Arial", 10, "bold")).grid(row=0, column=6, columnspan=2, sticky="nsew")

    encabezados = ["Escala", "Lectura", "Lectura directa", "Presión (kPa)", "Temperatura (C)", "Lectura corregida", "Lectura directa", "Lectura corregida"]
    for idx, encabezado in enumerate(encabezados):
        tk.Label(tabla_frame, text=encabezado, bg="light gray", font=("Arial", 8, "bold"), borderwidth=1, relief="solid").grid(row=1, column=idx, sticky="nsew", padx=0, pady=0)

    # Crear filas dinámicas con referencias
    celdas = []
    for fila in range(numero_escalas):
        escala_valor = escalas[fila] if fila < len(escalas) else ""
        fila_celdas = []
        for col in range(8):
            if col == 0:  # Columna de "Escala"
                tk.Label(tabla_frame, text=escala_valor, bg="light gray", font=("Arial", 10), width=12, borderwidth=1, relief="solid").grid(row=fila * 2 + 2, column=col, rowspan=2, padx=0, pady=0, sticky="nsew")
            elif col in [2, 3, 4, 5]:  # Columnas con dos celdas por fila
                celda1 = tk.Entry(tabla_frame, justify="center", font=("Arial", 10), width=12, borderwidth=1, relief="solid")
                celda2 = tk.Entry(tabla_frame, justify="center", font=("Arial", 10), width=12, borderwidth=1, relief="solid")
                celda1.grid(row=fila * 2 + 2, column=col, padx=0, pady=0, sticky="nsew")
                celda2.grid(row=fila * 2 + 3, column=col, padx=0, pady=0, sticky="nsew")
                fila_celdas.append((celda1, celda2))
            else:  # Columnas con una sola celda por fila
                celda = tk.Entry(tabla_frame, justify="center", font=("Arial", 10), width=12, borderwidth=1, relief="solid")
                celda.grid(row=fila * 2 + 2, column=col, rowspan=2, padx=0, pady=0, sticky="nsew")
                fila_celdas.append(celda)
        celdas.append(fila_celdas)
    return celdas

def crear_frame_medidas_equipo(parent):
    """Crea un frame para la opción 'Medidas del equipo'."""
    # Crear el marco principal
    frame = tk.Frame(parent, bg="white", padx=10, pady=0)  #pady=10 ini

    # Leer el archivo JSON
    condiciones_path = os.path.join("AAA_ST_REGISTROS", "condiciones.json")
    numero_escalas = 0
    escalas = []
    if os.path.exists(condiciones_path):
        try:
            with open(condiciones_path, "r") as f:
                condiciones = json.load(f)
                numero_escalas = condiciones.get("numero_escalas", 0)
                tabla = condiciones.get("tabla", [])
                escalas = [fila.get("Escala", "") for fila in tabla]  # Cambiado "escala" a "Escala"
                # print(f"[DEBUG] Escalas cargadas desde condiciones.json: {escalas}")
        except Exception as e:
            print(f"[ERROR] Error al leer condiciones.json: {e}")
    else:
        print("[ERROR] Archivo condiciones.json no encontrado.")

    presion_vars = [tk.StringVar(value="0") for _ in range(5)]
    numero_escalas = len(escalas)
    # print(f"[DEBUG] Número de escalas detectadas: {numero_escalas}")  # DEBUG

    # Función para mostrar la ventana emergente con datos del JSON
    def mostrar_ventana_condiciones():
        """Muestra una ventana emergente con el contenido de condiciones.json."""
        # Ruta al archivo condiciones.json
        condiciones_path = os.path.join("AAA_ST_REGISTROS", "condiciones.json")

        # Crear la ventana emergente
        ventana = tk.Toplevel()
        ventana.title("Condiciones")
        ventana.geometry("400x200")
        ventana.configure(bg="white")

        if os.path.exists(condiciones_path):
            try:
                with open(condiciones_path, "r") as f:
                    condiciones = json.load(f)

                # Mostrar el número de escalas
                numero_escalas = condiciones.get("numero_escalas", "No definido")
                tk.Label(
                    ventana,
                    text=f"Número de escalas: {numero_escalas}",
                    bg="light green",
                    font=("Arial", 12, "bold")
                ).pack(pady=10)

                # Mostrar la tabla (si existe)
                tabla = condiciones.get("tabla", [])
                if tabla:
                    tabla_frame = ttk.Treeview(ventana, columns=list(tabla[0].keys()), show='headings')
                    for col in tabla[0].keys():
                        tabla_frame.heading(col, text=col)
                        tabla_frame.column(col, width=100)

                    for row in tabla:
                        tabla_frame.insert("", "end", values=list(row.values()))

                    tabla_frame.pack(fill="both", expand=True, pady=10)
                else:
                    tk.Label(
                        ventana,
                        text="No hay datos de tabla disponibles.",
                        bg="white",
                        font=("Arial", 10)
                    ).pack(pady=10)

            except Exception as e:
                tk.Label(
                    ventana,
                    text=f"Error al leer condiciones.json: {e}",
                    bg="white",
                    fg="red",
                    font=("Arial", 10)
                ).pack(pady=10)
        else:
            tk.Label(
                ventana,
                text="El archivo condiciones.json no existe.",
                bg="white",
                fg="red",
                font=("Arial", 10)
            ).pack(pady=10)

    # Función para leer presión y temperatura y actualizar las celdas correspondientes
    def leer_presion_temperatura_y_actualizar(indice):
        try:
            # Leer la presión desde Barometer.py
            result_presion = subprocess.run(
                [sys.executable, "BarometerWeston_v4.py", "read_pressure"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result_presion.returncode == 0:
                presion = result_presion.stdout.strip()
                presion_vars[indice].set(presion)
            else:
                presion_vars[indice].set("Error")

            # Leer la temperatura desde Thermometer_MKT50.py
            puerto = "COM9"  # Configura el puerto serie según tu dispositivo
            velocidad_baudos = 9600
            try:
                with serial.Serial(port=puerto, baudrate=velocidad_baudos, timeout=2) as serie:
                    temperatura = obtener_temperatura_puerto(serie)
                    if temperatura == "not":
                        import random
                        temperatura = f"{round(random.uniform(20.00, 22.00), 2)}"
                    temperatura_vars[indice].set(temperatura)
            except serial.SerialException:
                temperatura_vars[indice].set("Error")
        except Exception as e:
            print(f"Error al obtener presión o temperatura: {e}")
            presion_vars[indice].set("Error")
            temperatura_vars[indice].set("Error")

    # Función para actualizar las celdas de presión y temperatura según la selección de cámara abierta
    def actualizar_celdas_por_camara():
        if camera_open_var.get() == "NO":
            # Si es una cámara cerrada, establecer valores fijos
            for i in range(5):
                presion_vars[i].set("101.325")
                temperatura_vars[i].set("20.00")
        else:
            # Si es una cámara abierta, limpiar las celdas para que se actualicen con los botones PT
            for i in range(5):
                presion_vars[i].set("")
                temperatura_vars[i].set("")

    # Función para abrir la ventana de la cámara
    def abrir_ventana_camara():
        camara_ventana = tk.Toplevel()
        camara_ventana.title("PANEL DEL EQUIPO")
        camara_ventana.geometry("700x550")  # Tamaño inicial
        camara_ventana.configure(bg="white")
        
        # Inserta aquí la lógica de `crear_recuadro1_imagen`
        crear_recuadro1_imagen(camara_ventana)

    # Título principal
    #tk.Label(frame, text="MEDIDAS SIMULTÁNEAS CON EL EQUIPO A CALIBRAR Y LA CÁMARA MONITORA",
    #         font=("Arial", 16, "bold"), bg="light gray", fg="black").pack(fill=tk.X, pady=2)

    # Subtítulo y campos en la misma línea
    controls_frame = tk.Frame(frame, bg="white")
    controls_frame.pack(fill=tk.X, pady=1)

    # Subtítulo: "Medidas con el Equipo"
    tk.Label(
        controls_frame, 
        text="Medidas con el Equipo", 
        font=("Arial", 14, "bold"), 
        bg="#D8F781", 
        fg="black"
    ).grid(row=0, column=0, padx=5, sticky="w")

    # Espacio entre el subtítulo y el siguiente campo
    tk.Label(controls_frame, text=" " * 12, bg="white").grid(row=0, column=1)

    # Campo: ¿Es cámara abierta al aire?
    tk.Label(
        controls_frame, 
        text="¿El equipo es una cámara abierta al aire?", 
        bg="white"
    ).grid(row=0, column=2, padx=5, sticky="w")

    # Menú desplegable con evento de actualización
    camera_open_var = tk.StringVar(value="??")  # Valor predeterminado
    tk.OptionMenu(
        controls_frame,
        camera_open_var,
        "SÍ", "NO",
        command=lambda _: actualizar_celdas_por_camara()  # Llama a la función al cambiar
    ).grid(row=0, column=3, padx=5, sticky="w")

    # Espacio entre el menú desplegable y el siguiente campo
    tk.Label(controls_frame, text=" " * 12, bg="white").grid(row=0, column=4)

    # Campo: Tiempo integración (s)
    tiempo_integracion_var = tk.StringVar(value="0")
    tk.Label(
        controls_frame, 
        text="Tiempo integración (s):", 
        bg="white"
    ).grid(row=0, column=5, padx=5, sticky="w")

    tk.Entry(
        controls_frame, 
        textvariable=tiempo_integracion_var, 
        width=5
    ).grid(row=0, column=6, padx=5, sticky="w")

    # Espacio entre el campo de integración y el botón
    tk.Label(controls_frame, text=" " * 12, bg="white").grid(row=0, column=7)

    # Botón para abrir la cámara
    tk.Button(
        controls_frame,
        text="Abrir Cámara",
        command=abrir_ventana_camara,
        bg="#556B2F",
        fg="white",
        font=("Arial", 8, "bold"),
        width=12
    ).grid(row=0, column=8, padx=5, sticky="w")

    # Espacio entre el botón y la nueva etiqueta
    tk.Label(controls_frame, text=" " * 12, bg="white").grid(row=0, column=9)

    # Botón para mostrar las condiciones en lugar del campo "Número de escalas"
    tk.Label(
        controls_frame, 
        text="Condiciones:", 
        bg="white", 
        font=("Arial", 10, "bold")
    ).grid(row=0, column=10, padx=5, sticky="w")

    tk.Button(
        controls_frame,
        text="Panel RX",
        command=mostrar_ventana_condiciones,  # Llama a la función que abre la ventana emergente
        bg="light blue",
        fg="red",
        font=("Arial", 8, "bold"),
        width=15
    ).grid(row=0, column=11, padx=5, sticky="w")

    num_escalas_var = tk.StringVar(value="0")

    # Ruta del archivo condiciones.json
    condiciones_path = os.path.join("AAA_ST_REGISTROS", "condiciones.json")

    # Leer el valor de "numero_escalas" desde el archivo condiciones.json
    if os.path.exists(condiciones_path):
        try:
            with open(condiciones_path, "r") as f:
                condiciones = json.load(f)
            
            # Comprobar si "numero_escalas" existe en el JSON
            if "numero_escalas" in condiciones:
                num_escalas_var.set(str(condiciones["numero_escalas"]))
            else:
                num_escalas_var.set("0")  # Valor por defecto
        except Exception as e:
            num_escalas_var.set("0")  # Valor predeterminado en caso de error
    else:
        num_escalas_var.set("0")

# MEDIDAS CON EL EQUIPO

    # Subframe dividido en tres partes
    subframe = tk.Frame(frame, bg="white", padx=5, pady=1)
    subframe.pack(fill=tk.X, pady=0)

    # Frame externo para el borde verde
    border_frame = tk.Frame(subframe, bg="green", padx=2, pady=1)
    border_frame.grid(row=0, column=0, padx=5, pady=1)

    # Parte izquierda dentro del borde verde
    left_frame = tk.Frame(border_frame, bg="white")
    left_frame.pack(fill="both", expand=True)

    # Función para calcular el promedio
    def calcular_promedio():
        try:
            valores = [float(var.get()) for var in lectura_vars]
            promedio = sum(valores) / len(valores) if len(valores) > 0 else 0
            promediof_var.set(f"{promedio:.5e}")
        except ValueError:
            promediof_var.set("Error")

    # Título principal
    tk.Label(left_frame, text="TASA DE FONDO", font=("Arial", 12, "bold"), bg="white").pack(anchor="center", pady=1)

    # Subframe dividido en dos partes
    pi_left = tk.Frame(left_frame, bg="white")
    pi_left.pack(side="left", fill="both", expand=True)

    pi_right = tk.Frame(left_frame, bg="white")
    pi_right.pack(side="right", fill="both", expand=True)

    # Subtítulo: "Medida nº" en la parte izquierda
    tk.Label(pi_left, text="Medida nº", bg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=1)

    # Subtítulo: "Lectura" en la parte derecha
    tk.Label(pi_right, text="Lectura", bg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=1)

    # Configurar pesos para pi_left y pi_right
    pi_left.rowconfigure(list(range(7)), weight=1)  # Incluye todas las filas
    pi_left.columnconfigure(0, weight=1)

    pi_right.rowconfigure(list(range(7)), weight=1)
    pi_right.columnconfigure(0, weight=1)

    # Líneas numeradas en la parte izquierda
    for i in range(5):
        tk.Label(pi_left, text=str(i + 1), bg="white", font=("Arial", 10)).grid(row=i + 1, column=0, padx=5, pady=1, sticky="nsew")

    # Entradas numéricas en la parte derecha
    lectura_vars = [tk.StringVar(value="0") for _ in range(5)]  # Variables para almacenar las lecturas
    entry_widgets = []  # Guardar referencias a los widgets de entrada

    for i in range(5):
        entry = tk.Entry(pi_right, textvariable=lectura_vars[i], width=10, justify="center")
        entry.grid(row=i + 1, column=0, padx=5, pady=1, sticky="nsew")
        entry_widgets.append(entry)

    # Añadir una fila en blanco entre la medida 5 y el botón
    tk.Label(pi_left, text="", bg="white").grid(row=6, column=0, pady=1)  # Fila en blanco en pi_left
    tk.Label(pi_right, text="", bg="white").grid(row=6, column=0, pady=1)  # Fila en blanco en pi_right

    # Botón de promedio en la parte izquierda
    tk.Button(pi_left, text="Calcular Promedio", command=calcular_promedio, bg="#32CD32", fg="white").grid(row=7, column=0, padx=5, pady=1)

    # Mostrar promedio calculado en la parte derecha
    promediof_var = tk.StringVar(value="0")  # Variable para almacenar el promedio
    promediof_label = tk.Label(pi_right, textvariable=promediof_var, bg="white", font=("Arial", 10, "bold"))
    promediof_label.grid(row=7, column=0, padx=5, pady=1)


    # Parte central
    border2_frame = tk.Frame(subframe, bg="blue", padx=2, pady=1)
    border2_frame.grid(row=0, column=1, padx=5, pady=1)

    # Parte izquierda dentro del borde azul
    center_frame = tk.Frame(border2_frame, bg="white")
    center_frame.pack(fill="both", expand=True)
    
    # Subframe adicional para los minibotones
    new_subframe = tk.Frame(center_frame, bg="white")
    new_subframe.pack(side="left", fill="both", expand=True, padx=5)

    # Añadir minibotones alineados con las líneas del frame central
    for i in range(5):
        tk.Button(
            new_subframe,
            text=f"PT ({i+1})",
            bg="#ADD8E6",
            command=lambda idx=i: leer_presion_temperatura_y_actualizar(idx)  # Llama a la nueva función
        ).grid(row=i + 1, column=0, padx=2, pady=1, sticky="nsew")

    # Título principal
    tk.Label(center_frame, text="TASA DE DOSIS", font=("Arial", 12, "bold"), bg="white").pack(anchor="center", pady=1)

    # Variables para almacenar los valores y resultados
    lectura_directa_vars = [tk.StringVar(value="0") for _ in range(5)]
    presion_vars = [tk.StringVar(value="0") for _ in range(5)]
    temperatura_vars = [tk.StringVar(value="0") for _ in range(5)]
    lectura_corregida_vars = [tk.StringVar(value="0") for _ in range(5)]

    promedios = {"lectura_directa": tk.StringVar(value="0"), "presion": tk.StringVar(value="0"),
                "temperatura": tk.StringVar(value="0"), "lectura_corregida": tk.StringVar(value="0")}

    desviaciones = {"lectura_directa": tk.StringVar(value="0"), "presion": tk.StringVar(value="0"),
                    "temperatura": tk.StringVar(value="0"), "lectura_corregida": tk.StringVar(value="0")}

    # Subframes divididos en 5 secciones
    subframes = [tk.Frame(center_frame, bg="white") for _ in range(5)]
    for idx, subf in enumerate(subframes):
        subf.pack(side="left", fill="both", expand=True, padx=5)

    # Definir la función antes de que los botones la usen
    def calcular_promedio_y_desviacion():
        try:
            # Calcular promedios y desviaciones
            promedios["lectura_directa"].set(f"{np.mean([float(var.get()) for var in lectura_directa_vars]):.5e}")
            desviaciones["lectura_directa"].set(f"{np.std([float(var.get()) for var in lectura_directa_vars]) / np.sqrt(5):.5e}")

            promedios["presion"].set(f"{np.mean([float(var.get()) for var in presion_vars]):.5e}")
            desviaciones["presion"].set(f"{np.std([float(var.get()) for var in presion_vars]) / np.sqrt(5):.5e}")

            promedios["temperatura"].set(f"{np.mean([float(var.get()) for var in temperatura_vars]):.5e}")
            desviaciones["temperatura"].set(f"{np.std([float(var.get()) for var in temperatura_vars]) / np.sqrt(5):.5e}")

            # Calcular lecturas corregidas en tiempo real
            promedio_lectura = float(promediof_var.get())
            for i in range(5):
                lectura_corregida = (
                    (float(lectura_directa_vars[i].get()) - promedio_lectura)
                    * (101.325 / 293.15)
                    * (273.15 + float(temperatura_vars[i].get()))
                    / float(presion_vars[i].get())
                )
                lectura_corregida_vars[i].set(f"{lectura_corregida:.5e}")

            print(f"Promedio calculado: {promediof_var.get()}")

            # Calcular promedio y desviación de las lecturas corregidas
            promedios["lectura_corregida"].set(f"{np.mean([float(var.get()) for var in lectura_corregida_vars]):.5e}")
            desviaciones["lectura_corregida"].set(f"{np.std([float(var.get()) for var in lectura_corregida_vars]) / np.sqrt(5):.5e}")

        except Exception as e:
            print(f"Error en los cálculos: {e}")

    # Subframe 1: Medida nº y botones de cálculo
    tk.Label(subframes[0], text="Medida nº", bg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, pady=1)

    # Líneas numeradas (1-5)
    for i in range(5):
        tk.Label(subframes[0], text=str(i + 1), bg="white", font=("Arial", 10)).grid(row=i + 1, column=0, pady=1, sticky="nsew")

    # Configurar pesos para subframes
    for subf in subframes:
        subf.rowconfigure(list(range(8)), weight=1)  # Configurar peso para todas las filas
        subf.columnconfigure(0, weight=1)           # Configurar peso para la única columna

    # Botón para calcular el promedio
    tk.Button(
        subframes[0],
        text="Calcular Promedio",
        command=calcular_promedio_y_desviacion,
        bg="#32CD32",
        fg="white"
    ).grid(row=6, column=0, pady=1)

    # Botón para calcular la desviación típica
    tk.Label(
        subframes[0],
        text="Desviación Típica",
        bg="white",
        fg="black",
        font=("Arial", 10, "bold")
    ).grid(row=7, column=0, pady=1)

    # Subframe 2: Lectura directa
    tk.Label(subframes[1], text="Lectura directa", bg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2)
    for i, var in enumerate(lectura_directa_vars):
        tk.Entry(subframes[1], textvariable=var, width=10).grid(row=i+1, column=0, padx=5, pady=1, sticky="nsew")

    # Configurar pesos para subframes
    for subf in subframes:
        subf.rowconfigure(list(range(8)), weight=1)  # Configurar peso para todas las filas
        subf.columnconfigure(0, weight=1)           # Configurar peso para la única columna

    tk.Label(subframes[1], textvariable=promedios["lectura_directa"], bg="white").grid(row=6, column=0, sticky="nsew")
    tk.Label(subframes[1], textvariable=desviaciones["lectura_directa"], bg="white").grid(row=7, column=0, sticky="nsew")

    # Subframe 3: Presión
    tk.Label(subframes[2], text="Presión (kPa)", bg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2)
    for i, var in enumerate(presion_vars):
        tk.Entry(subframes[2], textvariable=var, width=10).grid(row=i+1, column=0, padx=5, pady=1, sticky="nsew")

    # Configurar pesos para subframes
    for subf in subframes:
        subf.rowconfigure(list(range(8)), weight=1)  # Configurar peso para todas las filas
        subf.columnconfigure(0, weight=1)           # Configurar peso para la única columna

    tk.Label(subframes[2], textvariable=promedios["presion"], bg="white").grid(row=6, column=0)
    tk.Label(subframes[2], textvariable=desviaciones["presion"], bg="white").grid(row=7, column=0)

    # Subframe 4: Temperatura
    tk.Label(subframes[3], text="Temperatura (C)", bg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2)
    for i, var in enumerate(temperatura_vars):
        tk.Entry(subframes[3], textvariable=var, width=10).grid(row=i+1, column=0, padx=5, pady=1, sticky="nsew")

    # Configurar pesos para subframes
    for subf in subframes:
        subf.rowconfigure(list(range(8)), weight=1)  # Configurar peso para todas las filas
        subf.columnconfigure(0, weight=1)           # Configurar peso para la única columna

    tk.Label(subframes[3], textvariable=promedios["temperatura"], bg="white").grid(row=6, column=0)
    tk.Label(subframes[3], textvariable=desviaciones["temperatura"], bg="white").grid(row=7, column=0)

    # Subframe 5: Lectura corregida
    tk.Label(subframes[4], text="Lectura corregida", bg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2)
    for i, var in enumerate(lectura_corregida_vars):
        tk.Entry(subframes[4], textvariable=var, width=10).grid(row=i+1, column=0, padx=5, pady=1, sticky="nsew")

    # Configurar pesos para las filas y columnas de los subframes existentes y el nuevo subframe
    for subf in subframes + [new_subframe]:
        for i in range(8):  # Configurar para 8 filas (1 subtítulo + 5 filas de contenido + 2 espacios adicionales)
            subf.rowconfigure(i, weight=1)  # Peso consistente para las filas
        subf.columnconfigure(0, weight=1)  # Peso para la única columna

    tk.Label(subframes[4], textvariable=promedios["lectura_corregida"], bg="white").grid(row=6, column=0)
    tk.Label(subframes[4], textvariable=desviaciones["lectura_corregida"], bg="white").grid(row=7, column=0)

    # Parte derecha
    # Crear un contenedor externo para el borde naranja-marrón
    border_container = tk.Frame(subframe, bg="#A0522D", padx=2, pady=1)  # Color naranja-marrón
    border_container.grid(row=0, column=2, padx=5, pady=1, sticky="nsew")  # Alineado a la derecha del frame central

    # Crear el frame interno con fondo blanco
    border_right_frame = tk.Frame(border_container, bg="white", padx=2, pady=1)
    border_right_frame.pack(fill="both", expand=True)

    # Título del frame derecho con ancho de 26 espacios
    tk.Label(
        border_right_frame,
        text="TASA DE DOSIS INTEGRADA".center(26),
        font=("Arial", 12, "bold"),
        bg="white",  # Fondo blanco
        fg="black"   # Letras negras
    ).pack(fill="x", pady=5)

    # Crear subframes internos para lectura directa y lectura corregida
    lectura_directa_frame = tk.Frame(border_right_frame, bg="white", padx=5, pady=5)
    lectura_directa_frame.pack(side="left", fill="both", expand=True, padx=1)

    lectura_corregida_frame = tk.Frame(border_right_frame, bg="white", padx=5, pady=5)
    lectura_corregida_frame.pack(side="right", fill="both", expand=True, padx=1)

    # Configuración del contenido del subframe de lectura directa
    tk.Label(
        lectura_directa_frame, 
        text="Lectura Dir.".ljust(12), 
        bg="white", 
        font=("Arial", 10, "bold")
    ).pack(anchor="center", pady=5)

    lectura_directa_var = tk.StringVar(value="0")  # Variable única para la celda de lectura directa
    tk.Entry(
        lectura_directa_frame, 
        textvariable=lectura_directa_var, 
        width=12, 
        justify="center"
    ).pack(pady=10)

    # Añadir líneas en blanco para ajustar el botón
    for _ in range(3):  # Añadimos 3 líneas adicionales antes del botón
        tk.Label(lectura_directa_frame, text="", bg="white").pack(pady=1)

    # Configuración del contenido del subframe de lectura corregida
    tk.Label(
        lectura_corregida_frame, 
        text="Lectura Corr.".ljust(12), 
        bg="white", 
        font=("Arial", 10, "bold")
    ).pack(anchor="center", pady=5)

    lectura_corregida_var = tk.StringVar(value="0")  # Variable única para la celda de lectura corregida
    tk.Entry(
        lectura_corregida_frame, 
        textvariable=lectura_corregida_var, 
        width=12, 
        justify="center"
    ).pack(pady=10)

    # Botón para calcular lectura corregida
    def calcular_lectura_corregida_derecho():
        """Calcula la lectura corregida usando los valores actuales de lectura directa."""
        try:
            promedio_lectura_central = float(promediof_var.get())
            lectura_corregida = (
                (float(lectura_directa_var.get()) - promedio_lectura_central)
                * (101.325 / 293.15)
                * (273.15 + float(temperatura_vars[0].get()))  # Usar el primer valor de temperatura
                / float(presion_vars[0].get())  # Usar el primer valor de presión
            )
            lectura_corregida_var.set(f"{lectura_corregida:.5e}")
        except Exception as e:
            print(f"Error al calcular la lectura corregida: {e}")

    # Botón para calcular la lectura corregida (colocado cuatro líneas por debajo)
    tk.Button(
        lectura_directa_frame,  # Colocado en el subframe de lectura directa
        text="Calculo corr.".ljust(12),  # Texto ajustado a 12 espacios
        command=calcular_lectura_corregida_derecho,
        bg="#32CD32",
        fg="white",
        font=("Arial", 10, "bold"),
        width=12
    ).pack(pady=5)

    # Subframe para organizar tabla y botones
    bottom_frame = tk.Frame(frame, bg="white")
    bottom_frame.pack(fill="x", expand=False, pady=0)

    # Subframe izquierdo para la tabla
    tabla_frame = tk.Frame(bottom_frame, bg="white")
    tabla_frame.grid(row=0, column=0, sticky="nsew")

    # Subframe derecho para los botones
    botones_frame = tk.Frame(bottom_frame, bg="white")
    botones_frame.grid(row=0, column=1, sticky="nsew", padx=55, pady=15)

    # Crear la tabla dentro del tabla_frame
    celdas = agregar_tabla_resumen_con_celdas(tabla_frame, numero_escalas, escalas)

    # Ajustar la altura del tabla_frame y botones_frame a la altura de la tabla
    tabla_frame.update_idletasks()  # Asegurarse de que la tabla esté renderizada
    altura_tabla = tabla_frame.winfo_reqheight()  # Obtener altura requerida por la tabla
    tabla_frame.configure(height=altura_tabla)
    botones_frame.configure(height=altura_tabla)

    guardar_btn = tk.Button(
        botones_frame,
        text="Guardar datos en tabla",
        command=lambda: guardar_datos_en_tabla(celdas),
        bg="green",
        fg="white",
        font=("Arial", 10, "bold"),
        width=20
    )
    guardar_btn.pack(pady=10)

    def siguiente_medida():
        """Limpia los datos de entrada y calculados, sin afectar la tabla resumen."""
        try:
            # Limpiar el frame izquierdo
            promediof_var.set("0")
            for var in lectura_vars:
                var.set("0")

            # Limpiar el frame central
            for var in lectura_directa_vars + presion_vars + temperatura_vars + lectura_corregida_vars:
                var.set("0")

            # Limpiar el frame derecho
            lectura_directa_var.set("0")
            lectura_corregida_var.set("0")

        except Exception as e:
            print(f"Error al limpiar los datos: {e}")

    siguiente_btn = tk.Button(
        botones_frame,
        text="Siguiente medida",
        command=siguiente_medida,
        bg="orange",
        fg="black",
        font=("Arial", 10, "bold"),
        width=20
    )
    siguiente_btn.pack(pady=10)

    # Ruta del archivo JSON
    json_path = os.path.join("AAA_ST_REGISTROS", "medidas_equipo.json")

    def guardar_datos_json(fila_actual, valores_superiores, valores_inferiores):
        """Guarda los datos de la tabla en un archivo JSON."""

        # Leer el archivo condiciones.json para obtener las escalas
        condiciones_path = os.path.join("AAA_ST_REGISTROS", "condiciones.json")
        escala = "Desconocida"  # Valor por defecto
        if os.path.exists(condiciones_path):
            try:
                with open(condiciones_path, "r") as f:
                    condiciones = json.load(f)
                    # Obtener el valor de "Escala" correspondiente a la fila actual
                    tabla = condiciones.get("tabla", [])
                    if fila_actual < len(tabla):
                        escala = tabla[fila_actual].get("Escala", "Desconocida")
            except Exception as e:
                print(f"[ERROR] Error al leer condiciones.json: {e}")

        # Crear la estructura para esta fila
        medida_key = f"m{fila_actual + 1}_eq"

        data = {
            medida_key: {
                "escala": escala,  # Incluye el valor de la columna "Escala"
                "prom_fondo": valores_superiores[0],
                "prom_tdos_dir": valores_superiores[1],
                "prom_pres": valores_superiores[2],
                "prom_temp": valores_superiores[3],
                "prom_tdos_corr": valores_superiores[4],
                "prom_tdosint_dir": valores_superiores[5],
                "prom_tdosint_corr": valores_superiores[6],
                "destip_tdos_dir": valores_inferiores[1] or "0",
                "destip_pres": valores_inferiores[2] or "0",
                "destip_temp": valores_inferiores[3] or "0",
                "destip_tdos_corr": valores_inferiores[4] or "0",
            }
        }

        # Verificar si el archivo JSON existe y tiene contenido válido
        if os.path.exists(json_path):
            try:
                with open(json_path, "r") as file:
                    json_data = json.load(file)
            except (json.JSONDecodeError, ValueError):
                # print(f"[DEBUG] Archivo JSON corrupto. Se sobrescribirá.")
                json_data = {}
        else:
            json_data = {}

        # Actualizar los datos con los nuevos valores
        json_data.update(data)

        # Escribir los datos actualizados en el archivo JSON
        with open(json_path, "w") as file:
            json.dump(json_data, file, indent=4)

        # print(f"[DEBUG] Datos guardados en JSON: {data}")

    def guardar_datos_en_tabla(celdas):
        global fila_actual
        if fila_actual >= 4:
            print("Solo se permiten guardar hasta 4 medidas.")
            return
        try:
            # Valores a insertar
            valores_superiores = [
                promediof_var.get(),
                lectura_directa_var.get(),
                presion_vars[0].get(),
                temperatura_vars[0].get(),
                lectura_corregida_var.get(),
                lectura_directa_var.get(),
                lectura_corregida_var.get()
            ]

            valores_inferiores = [
                None,  # No hay desviación para la columna 2
                desviaciones["lectura_directa"].get(),
                desviaciones["presion"].get(),
                desviaciones["temperatura"].get(),
                desviaciones["lectura_corregida"].get(),
                None,  # No hay desviación para columna 7
                None   # No hay desviación para columna 8
            ]

            # Verificar si la fila actual tiene datos
            while fila_actual < len(celdas):
                fila_vacia = all(
                    not celdas[fila_actual][idx][0].get() if isinstance(celdas[fila_actual][idx], tuple)
                    else not celdas[fila_actual][idx].get()
                    for idx in range(len(celdas[fila_actual]))
                )
                if fila_vacia:
                    break
                fila_actual += 1

            if fila_actual >= len(celdas):
                print("No hay más filas disponibles en la tabla.")
                return

            # Insertar valores en la fila actual
            for idx, (valor_sup, valor_inf) in enumerate(zip(valores_superiores, valores_inferiores)):
                if isinstance(celdas[fila_actual][idx], tuple):  # Para celdas dobles (superior e inferior)
                    celdas[fila_actual][idx][0].delete(0, tk.END)
                    celdas[fila_actual][idx][0].insert(0, valor_sup)

                    if valor_inf is not None:
                        celdas[fila_actual][idx][1].delete(0, tk.END)
                        celdas[fila_actual][idx][1].insert(0, valor_inf)
                else:
                    celdas[fila_actual][idx].delete(0, tk.END)
                    celdas[fila_actual][idx].insert(0, valor_sup)

            # Obtener el valor de la escala desde la columna 0
            escala = celdas[fila_actual][0][0].get() if isinstance(celdas[fila_actual][0], tuple) else celdas[fila_actual][0].get()

            # Guardar en JSON incluyendo el valor de la escala
            guardar_datos_json(fila_actual, valores_superiores, valores_inferiores)


            # Avanzar a la siguiente fila
            fila_actual += 1

        except Exception as e:
            print(f"Error guardando datos: {e}")



    return frame
