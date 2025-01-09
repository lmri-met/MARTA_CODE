import tkinter as tk
from tkinter import ttk
from threading import Thread
import time
import serial
import random
import json
import os
import subprocess
from Thermometer_MKT50 import obtener_temperatura_puerto
import sys
# Índice global para rastrear la fila actual
fila_actual2 = 0

# Variables globales
tiempos = [0, 0, 0, 0, 0]
cargas = [0.0, 0.0, 0.0, 0.0, 0.0]
presiones = [0.0, 0.0, 0.0, 0.0, 0.0]
temperaturas = [0.0, 0.0, 0.0, 0.0, 0.0]
stop_thread = False
active_thread = None
promedio_corriente_fuga_fcd1_mon = 0.0
promedio_corriente_fcd1_mon = 0.0

def crear_frame_FCD_1_monitora(parent):
    def enviar_comando(ser, comando):
        print(f"Enviando comando: {comando}")
        ser.write((comando + '\r\n').encode('utf-8'))
        time.sleep(0.5)
        respuesta = ''
        while ser.in_waiting > 0:
            respuesta += ser.read(ser.in_waiting).decode('utf-8', errors='replace')
        print(f"Respuesta del dispositivo: {respuesta.strip()}")
        return respuesta.strip()

    def calcular_promedios():
        global promedio_corriente_fuga_fcd1_mon
        promedio_carga = sum(cargas) / len(cargas)
        promedio_corriente_fuga_fcd1_mon = sum(carga / tiempo if tiempo > 0 else 0 for carga, tiempo in zip(cargas, tiempos)) / len(cargas)
        tabla.item("promedio", values=("Promedio", f"{promedio_carga:.5e}", f"{promedio_corriente_fuga_fcd1_mon:.5e}"))

    def realizar_medidas():
        global stop_thread
        try:
            with serial.Serial('COM8', 9600, timeout=2) as ser:
                print("Conexión establecida con el electrómetro.")

                for i in range(5):
                    if stop_thread:
                        break

                    # Configurar rango
                    rango = rango_var.get()
                    rango_valor = {"LOW": "0", "MEDIUM": "1", "HIGH": "2"}[rango]
                    enviar_comando(ser, f"RGE;{rango_valor}")

                    # Configurar tiempo de integración
                    enviar_comando(ser, f"IT;{tiempos[i]}")

                    # Iniciar medición
                    enviar_comando(ser, "INT")

                    # Simular cuenta atrás
                    for t in range(tiempos[i], 0, -1):
                        if stop_thread:
                            break
                        tabla.item(f"item_{i}", values=(t, "", ""))
                        parent.update()
                        time.sleep(1)

                    # Obtener resultado
                    resultado = enviar_comando(ser, "MV")
                    partes = resultado.split(';')

                    if len(partes) > 4:
                        try:
                            carga = float(partes[4])
                        except ValueError:
                            carga = 0.0
                    else:
                        carga = 0.0

                    cargas[i] = carga
                    corriente = carga / tiempos[i] if tiempos[i] > 0 else 0.0
                    tabla.item(f"item_{i}", values=("0", f"{carga:.5e}", f"{corriente:.5e}"))
                    parent.update()

                calcular_promedios()

        except serial.SerialException as e:
            print(f"Error de conexión: {e}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def iniciar_medicion():
        global stop_thread, active_thread
        stop_thread = True
        if active_thread and active_thread.is_alive():
            active_thread.join()

        for i in range(5):
            try:
                tiempos[i] = int(tiempo_var.get())
            except ValueError:
                tiempos[i] = 0

        stop_thread = False
        active_thread = Thread(target=realizar_medidas)
        active_thread.start()

    def detener_medicion():
        global stop_thread
        stop_thread = True

    def reiniciar_tabla():
        """Vacía todas las celdas de la tabla."""
        for i in range(5):
            tabla.item(f"item_{i}", values=("", "", ""))
        tabla.item("promedio", values=("Promedio", "", ""))

    def iniciar_medicion2():
        global stop_thread, active_thread

        # Asegurar que no haya un hilo activo
        stop_thread = True
        if active_thread and active_thread.is_alive():
            active_thread.join()

        # Configurar tiempos
        for i in range(5):
            try:
                tiempos[i] = int(tiempo_var.get())
            except ValueError:
                tiempos[i] = 0

        # Crear e iniciar el nuevo hilo
        stop_thread = False
        active_thread = Thread(target=realizar_medidas2)
        active_thread.start()

    def realizar_medidas2():
        global stop_thread
        try:
            with serial.Serial('COM8', 9600, timeout=2) as ser:
                print("Conexión establecida con el electrómetro.")

                for i in range(5):
                    if stop_thread:
                        break

                    # Configurar rango
                    rango = rango_var.get()
                    rango_valor = {"LOW": "0", "MEDIUM": "1", "HIGH": "2"}[rango]
                    enviar_comando(ser, f"RGE;{rango_valor}")

                    # Configurar tiempo de integración
                    enviar_comando(ser, f"IT;{tiempos[i]}")

                    # Iniciar medición
                    enviar_comando(ser, "INT")

                    # Simular cuenta atrás
                    for t in range(tiempos[i], 0, -1):
                        if stop_thread:
                            break
                        tabla2.item(f"item2_{i}", values=(t, "", "", "", ""))
                        parent.update()
                        time.sleep(1)

                    # Obtener carga
                    resultado = enviar_comando(ser, "MV")
                    partes = resultado.split(';')
                    carga = float(partes[4]) if len(partes) > 4 else 0.0
                    cargas[i] = carga

                    # Leer presión desde BarometerWeston_v4.py
                    try:
                        result_presion = subprocess.run(
                            [sys.executable, "BarometerWeston_v4.py", "read_pressure"],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True
                        )
                        if result_presion.returncode == 0:
                            presion = float(result_presion.stdout.strip())
                        else:
                            raise RuntimeError(f"Error al ejecutar el script: {result_presion.stderr.strip()}")
                    except Exception as e:
                        print(f"Error al leer la presión: {e}")
                        presion = 101.325  # Valor por defecto

                    # Leer temperatura desde Thermometer_MKT50.py
                    try:
                        puerto = "COM9"  # Ajusta este puerto según tu configuración
                        velocidad_baudos = 9600
                        with serial.Serial(port=puerto, baudrate=velocidad_baudos, timeout=2) as serie:
                            temperatura = obtener_temperatura_puerto(serie)
                            if temperatura == "not":
                                temperatura = random.uniform(20.0, 22.0)  # Valor simulado si falla
                            temperatura = float(temperatura)
                    except Exception as e:
                        print(f"Error al leer la temperatura: {e}")
                        temperatura = 20.0  # Valor por defecto si ocurre un error

                    presiones[i] = presion
                    temperaturas[i] = temperatura

                    # Calcular corriente usando la ecuación proporcionada
                    tiempo_integracion = tiempos[i]
                    if tiempo_integracion > 0:
                        corriente = (
                            (carga / tiempo_integracion)
                            - (promedio_corriente_fuga_fcd1_mon * (101.325 / 293.15) * ((273.15 + temperatura) / presion))
                        )
                    else:
                        corriente = 0.0

                    # Actualizar tabla con datos adicionales
                    tabla2.item(
                        f"item2_{i}",
                        values=(0, f"{presion:.3f}", f"{temperatura:.3f}", f"{carga:.5e}", f"{corriente:.5e}")
                    )
                    parent.update()

                # Calcular promedios
                promedio_presion = sum(presiones) / len(presiones)
                promedio_temperatura = sum(temperaturas) / len(temperaturas)
                promedio_carga = sum(cargas) / len(cargas)
                promedio_corriente_fcd1_mon = sum(carga / tiempo if tiempo > 0 else 0 for carga, tiempo in zip(cargas, tiempos)) / len(cargas)

                # Actualizar fila de promedios en la tabla adicional
                tabla2.item(
                    "promedio2",
                    values=(
                        "Promedio",
                        f"{promedio_presion:.3f}",
                        f"{promedio_temperatura:.3f}",
                        f"{promedio_carga:.5e}",
                        f"{promedio_corriente_fcd1_mon:.5e}"
                    )
                )

        except serial.SerialException as e:
            print(f"Error de conexión: {e}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def reiniciar_tabla2():
        for i in range(5):
            tabla2.item(f"item2_{i}", values=("", "", "", "", ""))
        tabla2.item("promedio2", values=("Promedio", "", "", "", ""))

    def guardar_datos():
        # Crear el diccionario con los valores
        datos = {
            "promedio_corriente_fuga_fcd1_mon": promedio_corriente_fuga_fcd1_mon,
            "promedio_corriente_fcd1_mon": promedio_corriente_fcd1_mon,
        }

        # Definir la ruta del archivo
        carpeta = "AAA_ST_REGISTROS"
        archivo = os.path.join(carpeta, "fcd.json")

        # Asegurarse de que la carpeta existe
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        # Leer, actualizar y escribir los datos en el archivo JSON
        try:
            datos_existentes = []
            if os.path.exists(archivo):
                with open(archivo, "r") as f:
                    datos_existentes = json.load(f)

            if isinstance(datos_existentes, list):
                datos_existentes.append(datos)
            else:
                datos_existentes = [datos_existentes, datos]

            with open(archivo, "w") as f:
                json.dump(datos_existentes, f, indent=4)
            print(f"Datos guardados en {archivo}")
        except Exception as e:
            print(f"Error al guardar los datos: {e}")

    # Frame principal con borde inferior negro
    frame = tk.Frame(parent, bg="light gray")
    frame.pack(fill=tk.BOTH, expand=False, pady=0)

    # Simulación del borde inferior
    borde_inferior = tk.Frame(frame, bg="#001f3f", height=9)  # Altura 9
    borde_inferior.pack(fill=tk.X, side=tk.BOTTOM)

    # Contenedor para la línea de título y campos
    linea_superior = tk.Frame(frame, bg="light gray")
    linea_superior.pack(fill=tk.X, pady=0)

    # Título
    titulo = tk.Label(
        linea_superior,
        text="Medidas con la cámara monitora",
        font=("Arial", 16, "bold"),
        bg="#CCFF99"  # Fondo verde limón
    )
    titulo.grid(row=0, column=0, padx=10, pady=15, sticky="w")

    # Campo: Vacío
    vacio_label = tk.Label(linea_superior, text="                          ", bg="light gray")
    vacio_label.grid(row=0, column=2, padx=5, sticky="w")

    # Campo: Rango del electrómetro
    rango_label = tk.Label(linea_superior, text="Rango del electrómetro:", bg="white")
    rango_label.grid(row=0, column=3, padx=5, sticky="w")

    rango_var = tk.StringVar(value="LOW")
    rango_combo = ttk.Combobox(linea_superior, textvariable=rango_var, state="readonly")
    rango_combo["values"] = ("LOW", "MEDIUM", "HIGH")
    rango_combo.grid(row=0, column=4, padx=5, sticky="w")

    # Campo: Vacío
    vacio_label = tk.Label(linea_superior, text="                      ", bg="light gray")
    vacio_label.grid(row=0, column=5, padx=5, sticky="w")

    # Campo: Tiempo de integración
    tiempo_label = tk.Label(linea_superior, text="Tiempo de integración (s):", bg="white")
    tiempo_label.grid(row=0, column=6, padx=5, sticky="w")

    tiempo_var = tk.StringVar()
    tiempo_entry = tk.Entry(linea_superior, textvariable=tiempo_var, width=6)
    tiempo_entry.grid(row=0, column=7, padx=5, sticky="w")

#########################

    # Frame para la tabla y los botones
    tabla_y_botones_frame = tk.Frame(frame, bg="light gray")
    tabla_y_botones_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=0)

    # Botones a la izquierda de la tabla
    botones_frame = tk.Frame(tabla_y_botones_frame, bg="light gray")
    botones_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5) ##

    iniciar_btn = tk.Button(botones_frame, text="Iniciar", command=iniciar_medicion, bg="light green", fg="black", font=("Arial", 10), width=10)
    iniciar_btn.grid(row=0, column=0, pady=5)

    detener_btn = tk.Button(botones_frame, text="Detener", command=detener_medicion, bg="#FF6666", fg="black", font=("Arial", 10), width=10)
    detener_btn.grid(row=1, column=0, pady=5)

    rehacer_btn = tk.Button(botones_frame, text="Rehacer", command=reiniciar_tabla, bg="light blue", fg="black", font=("Arial", 10), width=10)
    rehacer_btn.grid(row=2, column=0, pady=5)

    # Tabla
    tabla_frame = tk.Frame(tabla_y_botones_frame, bg="light gray")
    tabla_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=0)

    # Configurar estilo de la tabla
    estilo = ttk.Style()
    estilo.configure("Treeview.Heading", font=("Arial", 8), padding=0)

    columnas = ("Tº restante (s)", "Carga (C)", "Corriente (A)")
    tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=6)

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=100, anchor="center")

    # Crear items iniciales en la tabla
    for i in range(5):
        tabla.insert("", "end", iid=f"item_{i}", values=("", "", ""), tags=("col1",))

    # Agregar fila para el promedio
    tabla.insert("", "end", iid="promedio", values=("Promedio", "", ""))

    # Configurar fondo gris claro para la primera columna
    tabla.tag_configure("col1", background="white")

    tabla.pack(fill=tk.BOTH, expand=False)

    # Tabla duplicada con columnas adicionales
    tabla_frame2 = tk.Frame(tabla_y_botones_frame, bg="light gray")
    tabla_frame2.grid(row=0, column=3, sticky="nsew", padx=5, pady=0)

    tabla2 = ttk.Treeview(tabla_frame2, columns=("Tº restante (s)", "Presión (kPa)", "Temp. (ºC)", "Carga (C)", "Corriente (A)"), show="headings", height=6)

    for col in ("Tº restante (s)", "Presión (kPa)", "Temp. (ºC)", "Carga (C)", "Corriente (A)"):
        tabla2.heading(col, text=col)
        tabla2.column(col, width=100, anchor="center")

    for i in range(5):
        tabla2.insert("", "end", iid=f"item2_{i}", values=("", "", "", "", ""), tags=("col1",))

    tabla2.insert("", "end", iid="promedio2", values=("Promedio", "", "", "", ""))

    tabla2.tag_configure("col1", background="white")

    tabla2.pack(fill=tk.BOTH, expand=False)

    # Botones adicionales a la derecha de la tabla
    botones_frame_derecha = tk.Frame(tabla_y_botones_frame, bg="light gray")
    botones_frame_derecha.grid(row=0, column=2, sticky="nsew", padx=15, pady=5)

    extra_btn1 = tk.Button(botones_frame_derecha, text="Iniciar", command=iniciar_medicion2, bg="light green", fg="black", font=("Arial", 10), width=10)
    extra_btn1.grid(row=0, column=0, pady=5)

    extra_btn2 = tk.Button(botones_frame_derecha, text="Detener", command=detener_medicion, bg="#FF6666", fg="black", font=("Arial", 10), width=10)
    extra_btn2.grid(row=1, column=0, pady=5)

    extra_btn3 = tk.Button(botones_frame_derecha, text="Rehacer", command=reiniciar_tabla2, bg="light blue", fg="black", font=("Arial", 10), width=10)
    extra_btn3.grid(row=2, column=0, pady=5)

    # Botón para guardar datos
    guardar_btn2 = tk.Button(
        tabla_y_botones_frame,  # Cambiamos el padre a tabla_y_botones_frame
        text="Guardar datos",
        command=guardar_datos,
        bg="light green",
        fg="black",
        font=("Arial", 10),
        width=12
    )
    guardar_btn2.grid(row=0, column=4, padx=5, pady=5)  # Colocamos el botón en la columna 4

    return frame
