import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import cv2
from PIL import Image, ImageTk

def create_condiciones_frame(parent):
    """Crea un frame para la opción 'Cámara patrón y monitora'."""
    frame = tk.Frame(parent, bg="white", padx=10, pady=10)

    # Título
    titulo_frame = tk.Frame(frame, bg="#90EE90")
    titulo_frame.pack(fill="x", pady=5)
    tk.Label(
        titulo_frame,
        text="CONDICIONES DE CALIBRACIÓN",
        font=("Arial", 14, "bold"),
        bg="#90EE90",
        fg="black"
    ).pack(pady=10)

    # Variables para los streams de las cámaras
    camera_general = None
    camera_escala = None

    def activar_camara_general():
        nonlocal camera_general
        if camera_general is None or not camera_general.isOpened():
            camera_general = cv2.VideoCapture(0)
            actualizar_camara(canvas_general, camera_general)

    def desactivar_camara_general():
        nonlocal camera_general
        if camera_general and camera_general.isOpened():
            camera_general.release()
            canvas_general.delete("all")

    def activar_camara_escala():
        nonlocal camera_escala
        if camera_escala is None or not camera_escala.isOpened():
            camera_escala = cv2.VideoCapture(1)
            actualizar_camara(canvas_escala, camera_escala)

    def desactivar_camara_escala():
        nonlocal camera_escala
        if camera_escala and camera_escala.isOpened():
            camera_escala.release()
            canvas_escala.delete("all")

    def actualizar_camara(canvas, camera):
        if camera and camera.isOpened():
            ret, frame = camera.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (550, 350))
                img = ImageTk.PhotoImage(Image.fromarray(frame))
                canvas.create_image(0, 0, anchor="nw", image=img)
                canvas.image = img
            canvas.after(10, actualizar_camara, canvas, camera)

    def guardar_foto_general():
        """Captura una foto desde la cámara general y la guarda con un nombre autonumérico."""
        folder_path = "AAA_ST_REGISTROS"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Buscar el siguiente nombre disponible
        i = 1
        while True:
            filename = os.path.join(folder_path, f"equipo_general_{i:02d}.jpeg")
            if not os.path.exists(filename):
                break
            i += 1

        # Tomar la foto
        if camera_general and camera_general.isOpened():
            ret, frame = camera_general.read()
            if ret:
                cv2.imwrite(filename, frame)
                messagebox.showinfo("Éxito", f"Foto guardada como {filename}")
            else:
                messagebox.showerror("Error", "No se pudo capturar la foto. Verifique la cámara.")
        else:
            messagebox.showerror("Error", "La cámara general no está activa.")

    def guardar_foto_escala():
        """Captura una foto desde la cámara escala y la guarda con un nombre autonumérico."""
        folder_path = "AAA_ST_REGISTROS"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Buscar el siguiente nombre disponible
        i = 1
        while True:
            filename = os.path.join(folder_path, f"equipo_escala_{i:02d}.jpeg")
            if not os.path.exists(filename):
                break
            i += 1

        # Tomar la foto
        if camera_escala and camera_escala.isOpened():
            ret, frame = camera_escala.read()
            if ret:
                cv2.imwrite(filename, frame)
                messagebox.showinfo("Éxito", f"Foto guardada como {filename}")
            else:
                messagebox.showerror("Error", "No se pudo capturar la foto. Verifique la cámara.")
        else:
            messagebox.showerror("Error", "La cámara escala no está activa.")

    # Etiqueta y entrada numérica para escalas
    tk.Label(frame, text="¿Número de escalas que pide el cliente?", bg="white").pack(pady=5)
    num_escalas_var = tk.IntVar(value=0)
    num_escalas_entry = tk.Entry(frame, textvariable=num_escalas_var, width=5)
    num_escalas_entry.pack()

    # Contenedor de la tabla
    tabla_frame = tk.Frame(frame, bg="white")
    tabla_frame.pack(pady=10)

    # Almacenar referencias de las filas de la tabla
    filas_tabla = []

    # Función para actualizar la tabla
    def actualizar_tabla(*args):
        try:
            # Intentar obtener el valor de num_escalas_var
            num_escalas = num_escalas_var.get()
        except tk.TclError:
            # Si ocurre un error (entrada vacía o no válida), asignar 0 como valor por defecto
            num_escalas = 0

        # Limpiar la tabla existente
        for widget in tabla_frame.winfo_children():
            widget.destroy()
        filas_tabla.clear()

        # Centrar tabla
        tabla_frame.grid_rowconfigure(0, weight=1)
        tabla_frame.grid_columnconfigure(0, weight=1)

        # Crear cabeceros
        headers = ["Medida nº", "Escala", "Intensidad (A)", "Voltaje (kV)", "Distancia (m)"]
        for col, header in enumerate(headers):
            tk.Label(tabla_frame, text=header, bg="#E0F7FA", width=15, anchor="center", relief="solid").grid(row=0, column=col, padx=2, pady=2)

        # Crear filas
        for i in range(num_escalas):
            row = []
            tk.Label(tabla_frame, text=f"{i + 1}", bg="white", width=15, anchor="center", relief="solid").grid(row=i + 1, column=0, padx=2, pady=2)

            # Combobox para unidades
            unidades = ttk.Combobox(tabla_frame, values=["< 10 uSv ", "10 - 100 uSv", "100 uSv - 1 mSv", "> 1 mSv"], width=15)
            unidades.grid(row=i + 1, column=1, padx=2, pady=2)
            unidades.set("")
            row.append(unidades)

            # Entradas para las otras columnas
            for col in range(2, 5):
                entry = tk.Entry(tabla_frame, width=15, relief="solid")
                entry.grid(row=i + 1, column=col, padx=2, pady=2)
                row.append(entry)
            
            filas_tabla.append(row)

    # Ruta del archivo condiciones.json
    folder_path = "AAA_ST_REGISTROS"
    json_path = os.path.join(folder_path, "condiciones.json")

    # Comprobar si existe el archivo condiciones.json
    if os.path.exists(json_path):
        try:
            with open(json_path, "r") as file:
                condiciones = json.load(file)

            # Establecer el número de escalas desde el JSON
            num_escalas_var.set(condiciones.get("numero_escalas", 0))

            # Llamar a la función para crear las filas de la tabla
            actualizar_tabla()

            # Llenar la tabla con los datos del JSON
            for i, datos in enumerate(condiciones.get("tabla", [])):
                if i < len(filas_tabla):
                    fila = filas_tabla[i]
                    fila[0].insert(datos.get("Escala", ""))  # Combobox de unidades
                    fila[1].insert(0, datos.get("intensidad", ""))  # Campo intensidad
                    fila[2].insert(0, datos.get("voltaje", ""))     # Campo voltaje
                    fila[3].insert(0, datos.get("distancia", ""))   # Campo distancia
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar condiciones desde JSON: {str(e)}")


    num_escalas_var.trace_add("write", actualizar_tabla)

    # Foto General
    fotos_frame = tk.Frame(frame, bg="white")
    fotos_frame.pack(fill="x", pady=10)

    foto_general_frame = tk.Frame(fotos_frame, bg="white", relief="solid", bd=1)
    foto_general_frame.pack(side="left", padx=10)
    tk.Label(foto_general_frame, text="Imagen general", bg="white").pack(pady=5)
    canvas_general = tk.Canvas(foto_general_frame, width=550, height=350, bg="#F0F0F0")
    canvas_general.pack()

    tk.Button(foto_general_frame, text="Activar cámara", command=activar_camara_general).pack(side="left", padx=5)
    tk.Button(foto_general_frame, text="Desactivar cámara", command=desactivar_camara_general).pack(side="left", padx=5)

    # Foto Escala
    foto_escala_frame = tk.Frame(fotos_frame, bg="white", relief="solid", bd=1)
    foto_escala_frame.pack(side="left", padx=10)
    tk.Label(foto_escala_frame, text="Escala del equipo", bg="white").pack(pady=5)
    canvas_escala = tk.Canvas(foto_escala_frame, width=550, height=350, bg="#F0F0F0")
    canvas_escala.pack()

    tk.Button(foto_escala_frame, text="Activar cámara", command=activar_camara_escala).pack(side="left", padx=5)
    tk.Button(foto_escala_frame, text="Desactivar cámara", command=desactivar_camara_escala).pack(side="left", padx=5)

    # Botones de guardar y resetear
    botones_frame = tk.Frame(frame, bg="white")
    botones_frame.pack(fill="x", pady=10)

    def guardar_datos():
        try:
            folder_path = "AAA_ST_REGISTROS"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            messagebox.showinfo("Éxito", f"Datos guardados correctamente en {folder_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar los datos: {str(e)}")

    def resetear_datos():
        if camera_general and camera_general.isOpened():
            camera_general.release()
        if camera_escala and camera_escala.isOpened():
            camera_escala.release()
        canvas_general.delete("all")
        canvas_escala.delete("all")
        messagebox.showinfo("Éxito", "Datos reseteados correctamente.")

    # Botones de guardar y resetear
    botones_frame = tk.Frame(frame, bg="white")
    botones_frame.pack(fill="x", pady=10)

    def guardar_datos():
        try:
            # Crear carpeta si no existe
            folder_path = "AAA_ST_REGISTROS"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Guardar datos de la tabla
            datos_tabla = []
            for row in filas_tabla:
                datos_tabla.append({
                    "Escala": row[0].get(),
                    "intensidad": row[1].get(),
                    "voltaje": row[2].get(),
                    "distancia": row[3].get(),
                })

            # Guardar datos en JSON
            datos = {
                "numero_escalas": num_escalas_var.get(),
                "tabla": datos_tabla
            }

            # Guardar en JSON
            json_path = os.path.join(folder_path, "condiciones.json")
            with open(json_path, "w") as file:
                json.dump(datos, file, indent=4)

            # Mensaje de éxito
            messagebox.showinfo("Éxito", f"Datos guardados correctamente en {folder_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar los datos: {str(e)}")

    def resetear_datos():
        num_escalas_var.set(0)
        for widget in tabla_frame.winfo_children():
            widget.destroy()

        # Eliminar archivos
        folder_path = "AAA_ST_REGISTROS"
        json_path = os.path.join(folder_path, "condiciones.json")
        if os.path.exists(json_path):
            os.remove(json_path)

        foto_general_path = os.path.join(folder_path, "Imagen_general_equipo.jpg")
        foto_escala_path = os.path.join(folder_path, "Imagen_escala_equipo.jpg")
        if os.path.exists(foto_general_path):
            os.remove(foto_general_path)
        if os.path.exists(foto_escala_path):
            os.remove(foto_escala_path)

        # Mensaje de éxito
        messagebox.showinfo("Éxito", "Datos reseteados correctamente.")

    tk.Button(botones_frame, text="Guardar", bg="green", fg="white", command=guardar_datos).pack(side="left", padx=5)
    tk.Button(botones_frame, text="Resetear datos", bg="red", fg="white", command=resetear_datos).pack(side="left", padx=5)
    # Botones para tomar fotos
    tk.Button(foto_general_frame, text="Tomar Foto", command=guardar_foto_general).pack(side="left", padx=5)
    tk.Button(foto_escala_frame, text="Tomar Foto", command=guardar_foto_escala).pack(side="left", padx=5)

    return frame
