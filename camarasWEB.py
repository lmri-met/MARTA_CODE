import tkinter as tk
from PIL import Image, ImageTk
import cv2
import os

def crear_recuadros_imagenes(frame):
    """Crea recuadros para mostrar imágenes en directo de dos cámaras y botones asociados."""

    # Variables para los streams de las cámaras
    camera_general = cv2.VideoCapture(0)  # Cámara principal
    camera_escala = cv2.VideoCapture(1)  # Cámara secundaria

    # Función para actualizar las imágenes en directo
    def actualizar_camara(canvas, camera):
        ret, frame = camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (300, 300))
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            canvas.create_image(0, 0, anchor="nw", image=img)
            canvas.image = img
        canvas.after(10, actualizar_camara, canvas, camera)

    # Función para tomar fotos
    def tomar_foto(camera, filename):
        ret, frame = camera.read()
        if ret:
            cv2.imwrite(filename, frame)
            tk.messagebox.showinfo("Foto guardada", f"Se ha guardado la foto como {filename}")

    # Función para borrar fotos
    def borrar_foto(filename):
        if os.path.exists(filename):
            os.remove(filename)
            tk.messagebox.showinfo("Foto borrada", f"Se ha eliminado la foto {filename}")
        else:
            tk.messagebox.showwarning("Archivo no encontrado", f"No se encontró el archivo {filename}")

    # Recuadros para las imágenes
    fotos_frame = tk.Frame(frame, bg="white")
    fotos_frame.pack(fill="x", pady=10)

    # Foto General
    foto_general_frame = tk.Frame(fotos_frame, bg="white", relief="solid", bd=1)
    foto_general_frame.pack(side="left", padx=10)
    tk.Label(foto_general_frame, text="Imagen general", bg="white").pack(pady=5)
    canvas_general = tk.Canvas(foto_general_frame, width=300, height=300, bg="#F0F0F0")
    canvas_general.pack()
    actualizar_camara(canvas_general, camera_general)
    tk.Button(foto_general_frame, text="Tomar foto", command=lambda: tomar_foto(camera_general, "Imagen_general_equipo.jpg")).pack(side="left", padx=5)
    tk.Button(foto_general_frame, text="Borrar foto", command=lambda: borrar_foto("Imagen_general_equipo.jpg")).pack(side="left", padx=5)

    # Foto Escala
    foto_escala_frame = tk.Frame(fotos_frame, bg="white", relief="solid", bd=1)
    foto_escala_frame.pack(side="left", padx=10)
    tk.Label(foto_escala_frame, text="Escala del equipo", bg="white").pack(pady=5)
    canvas_escala = tk.Canvas(foto_escala_frame, width=300, height=300, bg="#F0F0F0")
    canvas_escala.pack()
    actualizar_camara(canvas_escala, camera_escala)
    tk.Button(foto_escala_frame, text="Tomar foto", command=lambda: tomar_foto(camera_escala, "Imagen_escala_equipo.jpg")).pack(side="left", padx=5)
    tk.Button(foto_escala_frame, text="Borrar foto", command=lambda: borrar_foto("Imagen_escala_equipo.jpg")).pack(side="left", padx=5)

    # Botones de guardar y resetear
    botones_frame = tk.Frame(frame, bg="white")
    botones_frame.pack(fill="x", pady=10)

    return fotos_frame
