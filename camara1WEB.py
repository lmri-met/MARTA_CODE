import os
import tkinter as tk
from PIL import Image, ImageTk
import cv2

def crear_recuadro1_imagen(frame):
    """Crea un recuadro para mostrar imágenes en directo de una cámara y botones asociados."""

    # Variable para el stream de la cámara
    camera = cv2.VideoCapture(0)  # Cámara principal

    # Carpeta para guardar las fotos
    folder = "AAA_ST_REGISTROS"

    # Función para actualizar la imagen en directo
    def actualizar_camara(canvas, camera):
        ret, frame = camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (640, 480))
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            canvas.create_image(0, 0, anchor="nw", image=img)
            canvas.image = img
        canvas.after(10, actualizar_camara, canvas, camera)

    # Función para tomar fotos
    def tomar_foto(camera):
        # Asegurar que la carpeta existe
        os.makedirs(folder, exist_ok=True)

        # Listar archivos existentes en la carpeta
        files = [f for f in os.listdir(folder) if f.startswith("Equipos_panel_") and f.endswith(".jpeg")]
        
        # Encontrar el número más alto y generar el siguiente
        numbers = [int(f.split("_")[-1].split(".")[0]) for f in files if f.split("_")[-1].split(".")[0].isdigit()]
        next_number = max(numbers) + 1 if numbers else 1
        filename = os.path.join(folder, f"Equipos_panel_{next_number:02d}.jpeg")

        # Capturar y guardar la imagen
        ret, frame = camera.read()
        if ret:
            cv2.imwrite(filename, frame)
            tk.messagebox.showinfo("Foto guardada", f"Se ha guardado la foto como {filename}")
        else:
            tk.messagebox.showwarning("Error", "No se pudo capturar la imagen.")

    # Recuadro para la imagen
    fotos_frame = tk.Frame(frame, bg="white")
    fotos_frame.pack(fill="x", pady=10)

    foto_frame = tk.Frame(fotos_frame, bg="white", relief="solid", bd=1)
    foto_frame.pack(side="left", padx=10)
    # tk.Label(foto_frame, text="Panel del equipo", bg="white").pack(pady=5)
    canvas = tk.Canvas(foto_frame, width=640, height=480, bg="#F0F0F0")
    canvas.pack()
    actualizar_camara(canvas, camera)
    tk.Button(
        foto_frame,
        text="Tomar foto",
        command=lambda: tomar_foto(camera),
        bg="#32CD32",  # Fondo verde limón (hexadecimal)
        fg="white",    # Texto blanco
        font=("Arial", 12, "bold")  # Opcional: Fuente personalizada
    ).pack(pady=10, anchor="center")  # Centrado con margen vertical

    return fotos_frame
