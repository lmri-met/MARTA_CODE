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
promedio_corriente_fuga = 0.0

def crear_frame_medidas_monitorap(parent):
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
        global promedio_corriente_fuga
        promedio_carga = sum(cargas) / len(cargas)
        promedio_corriente_fuga = sum(carga / tiempo if tiempo > 0 else 0 for carga, tiempo in zip(cargas, tiempos)) / len(cargas)
        tabla.item("promedio", values=("Promedio", f"{promedio_carga:.5e}", f"{promedio_corriente_fuga:.5e}"))

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
                            - (promedio_corriente_fuga * (101.325 / 293.15) * ((273.15 + temperatura) / presion))
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
                promedio_corriente = sum(carga / tiempo if tiempo > 0 else 0 for carga, tiempo in zip(cargas, tiempos)) / len(cargas)

                # Actualizar fila de promedios en la tabla adicional
                tabla2.item(
                    "promedio2",
                    values=(
                        "Promedio",
                        f"{promedio_presion:.3f}",
                        f"{promedio_temperatura:.3f}",
                        f"{promedio_carga:.5e}",
                        f"{promedio_corriente:.5e}"
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

    # Frame principal
    frame = tk.Frame(parent, bg="#FDF6F2")
    frame.pack(fill=tk.BOTH, expand=True)

    # Contenedor para la línea de título y campos
    linea_superior = tk.Frame(frame, bg="#FDF6F2")
    linea_superior.pack(fill=tk.X, pady=20)

    # Título
    titulo = tk.Label(
        linea_superior,
        text="Medidas con la cámara monitora",
        font=("Arial", 16, "bold"),
        bg="#CCFF99"  # Fondo verde limón
    )
    titulo.grid(row=0, column=0, padx=10, sticky="w")

    # Campo: Tiempo de integración
    vacio_label = tk.Label(linea_superior, text="                          ", bg="#FDF6F2")
    vacio_label.grid(row=0, column=2, padx=5, sticky="w")

    # Campo: Rango del electrómetro
    rango_label = tk.Label(linea_superior, text="Rango del electrómetro:", bg="white")
    rango_label.grid(row=0, column=3, padx=5, sticky="w")

    rango_var = tk.StringVar(value="LOW")
    rango_combo = ttk.Combobox(linea_superior, textvariable=rango_var, state="readonly")
    rango_combo["values"] = ("LOW", "MEDIUM", "HIGH")
    rango_combo.grid(row=0, column=4, padx=5, sticky="w")

    # Campo: Tiempo de integración
    vacio_label = tk.Label(linea_superior, text="                      ", bg="#FDF6F2")
    vacio_label.grid(row=0, column=5, padx=5, sticky="w")

    # Campo: Tiempo de integración
    tiempo_label = tk.Label(linea_superior, text="Tiempo de integración (s):", bg="white")
    tiempo_label.grid(row=0, column=6, padx=5, sticky="w")

    tiempo_var = tk.StringVar()
    tiempo_entry = tk.Entry(linea_superior, textvariable=tiempo_var)
    tiempo_entry.grid(row=0, column=7, padx=5, sticky="w")

    # Frame para la tabla y los botones
    tabla_y_botones_frame = tk.Frame(frame, bg="#FDF6F2")
    tabla_y_botones_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=0)

    # Botones a la izquierda de la tabla
    botones_frame = tk.Frame(tabla_y_botones_frame, bg="#FDF6F2")
    botones_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=50) ##

    iniciar_btn = tk.Button(botones_frame, text="Iniciar", command=iniciar_medicion, bg="light green", fg="black", font=("Arial", 10), width=10)
    iniciar_btn.grid(row=0, column=0, pady=5)

    detener_btn = tk.Button(botones_frame, text="Detener", command=detener_medicion, bg="#FF6666", fg="black", font=("Arial", 10), width=10)
    detener_btn.grid(row=1, column=0, pady=5)

    rehacer_btn = tk.Button(botones_frame, text="Rehacer", command=reiniciar_tabla, bg="light blue", fg="black", font=("Arial", 10), width=10)
    rehacer_btn.grid(row=2, column=0, pady=5)

    # Tabla
    tabla_frame = tk.Frame(tabla_y_botones_frame, bg="#FDF6F2")
    tabla_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    # Título de la tabla
    tabla_titulo = tk.Label(
        tabla_frame,
        text="Corriente de fuga",
        font=("Arial", 12, "bold"),
        bg="#FDF6F2"
    )
    tabla_titulo.pack(pady=(0, 2))

    # Configurar estilo de la tabla
    estilo = ttk.Style()
    estilo.configure("Treeview.Heading", font=("Arial", 8))

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
    tabla_frame2 = tk.Frame(tabla_y_botones_frame, bg="#FDF6F2")
    tabla_frame2.grid(row=0, column=3, sticky="nsew", padx=5, pady=0)

    tabla_titulo2 = tk.Label(
        tabla_frame2,
        text="Medida de la tasa de kerma en aire ",
        font=("Arial", 12, "bold"),
        bg="#FDF6F2"
    )
    tabla_titulo2.pack(pady=(0, 2))

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
    botones_frame_derecha = tk.Frame(tabla_y_botones_frame, bg="#FDF6F2")
    botones_frame_derecha.grid(row=0, column=2, sticky="nsew", padx=15, pady=50)

    extra_btn1 = tk.Button(botones_frame_derecha, text="Iniciar", command=iniciar_medicion2, bg="light green", fg="black", font=("Arial", 10), width=10)
    extra_btn1.grid(row=0, column=0, pady=5)

    extra_btn2 = tk.Button(botones_frame_derecha, text="Detener", command=detener_medicion, bg="#FF6666", fg="black", font=("Arial", 10), width=10)
    extra_btn2.grid(row=1, column=0, pady=5)

    extra_btn3 = tk.Button(botones_frame_derecha, text="Rehacer", command=reiniciar_tabla2, bg="light blue", fg="black", font=("Arial", 10), width=10)
    extra_btn3.grid(row=2, column=0, pady=5)

    # Botones adicionales a la derecha de tabla2
    botones_frame_derecha_tabla2 = tk.Frame(tabla_y_botones_frame, bg="#FDF6F2")
    botones_frame_derecha_tabla2.grid(row=0, column=4, sticky="nsew", padx=10, pady=50)

    # Ruta del archivo medidas_monitorap.json
    json_path_monitorap = os.path.join("AAA_ST_REGISTROS", "medidas_monitorap.json")

    # Función para guardar datos en la tabla resumen y archivo JSON
    def guardar_datos_en_tabla_monitorap():
        global fila_actual2
        if fila_actual2 >= numero_escalas:
            print("Solo se permiten guardar hasta el número máximo de escalas.")
            return

        try:
            # Verificar si existen valores calculados en la tabla principal
            promedio_corriente_fuga = tabla.item("promedio", "values")[1]  # Columna 2
            promedio_corriente = tabla.item("promedio", "values")[2]  # Columna 3

            if not promedio_corriente_fuga or not promedio_corriente:
                print("Los valores promedio no están disponibles.")
                return

            # Insertar los datos en la fila correspondiente de la tabla resumen
            escala = escalas[fila_actual2] if fila_actual2 < len(escalas) else f"Escala {fila_actual2 + 1}"
            tabla_resumen.item(f"item_{fila_actual2}", values=(escala, promedio_corriente_fuga, promedio_corriente))

            # Guardar los datos en el archivo JSON
            medida_key = f"m{fila_actual2 + 1}_monitorap"
            data = {
                medida_key: {
                    "escala": escala,
                    "prom_corriente_fuga": promedio_corriente_fuga,
                    "prom_corriente": promedio_corriente,
                }
            }

            # Verificar si el archivo JSON ya existe
            if os.path.exists(json_path_monitorap):
                try:
                    with open(json_path_monitorap, "r") as file:
                        json_data = json.load(file)
                except (json.JSONDecodeError, ValueError):
                    print("Archivo JSON corrupto. Se sobrescribirá.")
                    json_data = {}
            else:
                json_data = {}

            # Actualizar el JSON con los nuevos datos
            json_data.update(data)

            # Escribir los datos actualizados en el archivo
            with open(json_path_monitorap, "w") as file:
                json.dump(json_data, file, indent=4)

            print(f"Datos guardados en JSON: {data}")

            # Incrementar el índice para la siguiente fila
            fila_actual2 += 1

        except Exception as e:
            print(f"Error guardando datos: {e}")


    # Función para preparar para la siguiente medida
    def siguiente_medida_monitorap():
        try:
            # Limpiar valores de la tabla principal
            for i in range(5):
                tabla.item(f"item_{i}", values=("", "", ""))

            tabla.item("promedio", values=("Promedio", "", ""))

            # Limpiar valores de la tabla secundaria
            for i in range(5):
                tabla2.item(f"item2_{i}", values=("", "", "", "", ""))

            tabla2.item("promedio2", values=("Promedio", "", "", "", ""))

            print("Preparado para la siguiente medida.")

        except Exception as e:
            print(f"Error al preparar para la siguiente medida: {e}")

    # Botón "Guardar datos en tabla"
    guardar_btn = tk.Button(
        botones_frame_derecha_tabla2,
        text="Guardar datos en tabla",
        command=guardar_datos_en_tabla_monitorap,
        bg="light green",
        fg="black",
        font=("Arial", 10),
        width=18
    )
    guardar_btn.grid(row=0, column=0, pady=5, padx=50)

    # Botón "Siguiente medida"
    siguiente_btn = tk.Button(
        botones_frame_derecha_tabla2,
        text="Siguiente medida",
        command=siguiente_medida_monitorap,
        bg="#FFE5CC",
        fg="black",
        font=("Arial", 10),
        width=18
    )
    siguiente_btn.grid(row=1, column=0, pady=5, padx=5)


    # Tabla Resumen
    def cargar_datos_resumen():
        """Carga los datos desde el archivo condiciones.json."""
        try:
            ruta_json = os.path.join("AAA_ST_REGISTROS", "condiciones.json")
            with open(ruta_json, "r") as archivo:
                datos = json.load(archivo)
                numero_escalas = datos.get("numero_escalas", 0)
                escalas = [fila["Escala"] for fila in datos.get("tabla", [])]
                return numero_escalas, escalas
        except Exception as e:
            print(f"Error al leer el archivo condiciones.json: {e}")
            return 0, []

    # Obtener número de escalas y valores de la columna "Escala"
    numero_escalas, escalas = cargar_datos_resumen()

    # Crear la tabla resumen
    tabla_resumen_frame = tk.Frame(frame, bg="white")
    tabla_resumen_frame.pack(padx=10, pady=5)  # No se usa fill=tk.BOTH para mantener el tamaño deseado

    # Configuración de la tabla resumen
    columnas_resumen = ("Escala", "Corriente de Fuga (C)", "Intensidad (A)")
    tabla_resumen = ttk.Treeview(
        tabla_resumen_frame,
        columns=columnas_resumen,  # Definir solo las 3 columnas necesarias
        show="headings",  # Mostrar únicamente los encabezados definidos
        height=numero_escalas
    )

    # Configurar estilo de encabezados
    estilo = ttk.Style()
    estilo.configure("Treeview.Heading", font=("Arial", 10, "bold"))  
    estilo.configure("Treeview", rowheight=25)  # Altura de las filas

    # Configurar las columnas con un ancho de 20 caracteres
    ancho_caracter = 10  # Estimación de 10 píxeles por carácter
    for col in columnas_resumen:
        tabla_resumen.heading(col, text=col)
        tabla_resumen.column(
            col,
            minwidth=0,
            width=20 * ancho_caracter,  # Ancho para 20 caracteres
            stretch=False,
            anchor="center"
        )

    # Rellenar filas con los valores de "Escala" y asignar `iid` explícitos
    for i in range(numero_escalas):
        escala = escalas[i] if i < len(escalas) else f"Escala {i+1}"  # Usar valores del JSON o nombres genéricos si faltan
        tabla_resumen.insert("", "end", iid=f"item_{i}", values=(escala, "", ""))  # Asignar `iid`

    # Empaquetar la tabla
    tabla_resumen.pack(padx=10, pady=5)


    return frame
