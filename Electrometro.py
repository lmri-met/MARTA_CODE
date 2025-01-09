import tkinter as tk
from tkinter import ttk
import serial
import time
from threading import Thread

# Global variables to manage threads
active_thread = None
stop_thread = False

def enviar_comando(ser, comando):
    """Send a command to the device and return the response."""
    print(f"Enviando comando: {comando}")
    ser.write((comando + '\r\n').encode('utf-8'))
    time.sleep(0.5)
    respuesta = ''
    while ser.in_waiting > 0:
        respuesta += ser.read(ser.in_waiting).decode('utf-8', errors='replace')
    print(f"Respuesta del dispositivo a '{comando}': '{respuesta.strip()}'")
    return respuesta.strip()

def iniciar_medicion():
    """Start the integrated dose/charge measurement."""
    global active_thread, stop_thread

    # Stop any ongoing measurement
    stop_thread = True
    if active_thread and active_thread.is_alive():
        active_thread.join()

    # Get measurement time from the input field
    try:
        tiempo_medida = int(entry_tiempo.get())
        if tiempo_medida <= 0:
            countdown_var.set("El tiempo debe ser mayor a 0.")
            return
    except ValueError:
        countdown_var.set("Ingrese un tiempo válido.")
        return

    # Get selected range
    rango = rango_var.get()

    lectura_var.set("...")
    countdown_var.set(f"Tiempo restante: {tiempo_medida} segundos")

    def medicion():
        try:
            with serial.Serial('COM8', 9600, timeout=2) as ser:
                print("Conexión establecida con el electrómetro.")

                # Step 1: Set range
                enviar_comando(ser, f"RGE;{rango}")

                # Step 2: Set integration time
                enviar_comando(ser, f"IT;{tiempo_medida}")

                # Step 3: Start integration measurement
                enviar_comando(ser, "INT")

                # Step 4: Countdown and wait for completion
                for i in range(tiempo_medida, 0, -1):
                    if stop_thread:
                        break
                    root.after(0, countdown_var.set, f"Tiempo restante: {i} segundos")
                    time.sleep(1)

                # Step 5: Retrieve result
                resultado = enviar_comando(ser, "MV")

                # Extract the "measured value of dose rate or current"
                partes = resultado.split(';')
                if len(partes) > 4:
                    valor_dosis_corriente = partes[4]  # Assumes this is the correct index for "dose rate or current"
                else:
                    valor_dosis_corriente = "Error al interpretar MV"

                root.after(0, lectura_var.set, valor_dosis_corriente)
                root.after(0, countdown_var.set, "Medición finalizada")
        except serial.SerialException as e:
            root.after(0, lectura_var.set, f"Error de conexión: {e}")
        except Exception as e:
            root.after(0, lectura_var.set, f"Error: {str(e)}")

    # Start the measurement thread
    stop_thread = False
    active_thread = Thread(target=medicion)
    active_thread.start()

def detener_medicion():
    """Stop the ongoing measurement."""
    global stop_thread
    stop_thread = True

# Create the main window
root = tk.Tk()
root.title("Electrómetro - Medición Integrada")

# Variables
lectura_var = tk.StringVar(value="...")
countdown_var = tk.StringVar(value="...")
rango_var = tk.StringVar(value="0")  # Default to Low

# Input for measurement time
frame_tiempo = ttk.Frame(root)
frame_tiempo.pack(pady=5)

tl_tiempo = ttk.Label(frame_tiempo, text="Tiempo de medida (segundos):")
tl_tiempo.pack(side=tk.LEFT, padx=5)

entry_tiempo = ttk.Entry(frame_tiempo)
entry_tiempo.pack(side=tk.LEFT, padx=5)

# Input for range selection
frame_rango = ttk.Frame(root)
frame_rango.pack(pady=5)

tl_rango = ttk.Label(frame_rango, text="Rango de medición:")
tl_rango.pack(side=tk.LEFT, padx=5)

combo_rango = ttk.Combobox(frame_rango, textvariable=rango_var, state="readonly")
combo_rango['values'] = ["0: Low", "1: Medium", "2: High"]
combo_rango.pack(side=tk.LEFT, padx=5)
combo_rango.current(0)  # Default to Low

# Display for reading
frame_lectura = ttk.Frame(root)
frame_lectura.pack(pady=5)

tl_lectura = ttk.Label(frame_lectura, text="Resultado:")
tl_lectura.pack(side=tk.LEFT, padx=5)

entry_lectura = ttk.Label(frame_lectura, textvariable=lectura_var)
entry_lectura.pack(side=tk.LEFT, padx=5)

# Button to start the sequence
btn_start = ttk.Button(root, text="Iniciar Medición", command=iniciar_medicion)
btn_start.pack(pady=10)

# Button to stop the sequence
btn_stop = ttk.Button(root, text="Detener Medición", command=detener_medicion)
btn_stop.pack(pady=10)

# Display for countdown
frame_countdown = ttk.Frame(root)
frame_countdown.pack(pady=5)

tl_countdown = ttk.Label(frame_countdown, text="Estado:")
tl_countdown.pack(side=tk.LEFT, padx=5)

entry_countdown = ttk.Label(frame_countdown, textvariable=countdown_var)
entry_countdown.pack(side=tk.LEFT, padx=5)

# Run the application
root.mainloop()
