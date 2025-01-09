# subframe_inferior_derecho.py
import tkinter as tk
from tkinter import messagebox
import os
import csv
import json
from PIL import ImageGrab

# Variables globales para almacenar datos
subframe_data = {
    "superior": {},
    "inferior_opcion3": {},
    "inferior_izquierdo": {}
}

def create_subframe_inferior_derecho(parent):
    """Crea un subframe inferior derecho con botones para salvar y limpiar datos."""
    subframe = tk.Frame(parent, bg="white", relief="solid", bd=1)


    def borrar_datos():
        for widget in parent.winfo_children():
            widget.grid_forget()  # Olvida los widgets pero no destruye el contenedor
        subframe_data.clear()
        messagebox.showinfo("Datos borrados", "Todos los datos han sido borrados.")


    return subframe
