import tkinter as tk
from tkinter import ttk

def create_subframe_inferior_izquierdo(parent):
    """Crea un subframe inferior izquierdo con los campos necesarios."""
    # Contenedor principal para el subframe
    subframe_container = tk.Frame(parent, bg="white", relief="solid", bd=1)

    # Título
    tk.Label(subframe_container, text="Medidas para el cálculo del factor de distancia", bg="lightblue", fg="black", 
             font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=5)

    # Campo: Rango del electrómetro
    tk.Label(subframe_container, text="Rango del electrómetro:", bg="white", fg="black").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    combo_rangelec = ttk.Combobox(subframe_container, values=["LOW", "HIGH"], width=35)
    combo_rangelec.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

    # Campo: Factor de corrección de distancia
    tk.Label(subframe_container, text="Factor de corrección de distancia:", bg="white", fg="black").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    combo_fcdsino = ttk.Combobox(subframe_container, values=["Sí", "No"], width=35)
    combo_fcdsino.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

    # Campo: Factor de corrección debido al rango del electrómetro
    tk.Label(subframe_container, text="Factor de corrección debido al rango del electrómetro:", bg="white", fg="black").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    factor_correccion_var = tk.StringVar(value="1.000")  # Valor inicial por defecto
    tk.Label(subframe_container, textvariable=factor_correccion_var, bg="white", fg="black").grid(row=3, column=1, sticky="w", padx=10, pady=5)

    # Función para actualizar el factor de corrección según el rango del electrómetro seleccionado
    def actualizar_factor(event):
        """Actualizar el valor del factor de corrección según el rango seleccionado."""
        rango = combo_rangelec.get()
        if rango == "LOW":
            factor_correccion_var.set("1.001")
        elif rango == "HIGH":
            factor_correccion_var.set("1.002")
        else:
            factor_correccion_var.set("1.000")

    # Vincular eventos para asegurar la actualización dinámica
    combo_rangelec.bind("<<ComboboxSelected>>", actualizar_factor)

    # Botones
    tk.Button(
        subframe, 
        text="Guardar", 
        command=guardar_datos, 
        bg="green", 
        fg="white"
    ).grid(row=99, column=0, sticky="e", padx=10, pady=10)
    
    tk.Button(
        subframe,
        text="Eliminar",
        command=borrar_datos,
        bg="red",
        fg="white"
    ).grid(row=99, column=0, sticky="e", padx=10, pady=10)

    def guardar_datos(parent):
        datos = {
            "rango_electrometro": combo_rangelec.get(),
            "factor_correccion_distancia": combo_fcdsino.get(),
            "factor_correccion_rango": factor_correccion_var.get()
        }

        # Guardar como DS3.json
        json_path = os.path.join(os.getcwd(), "DS3.json")
        with open(json_path, "w") as json_file:
            json.dump(datos, json_file, indent=4)

        # Guardar como DS3.xlsx
        xlsx_path = os.path.join(os.getcwd(), "DS3.xlsx")
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(["Rango del Electrómetro", "Factor de Corrección de Distancia", "Factor de Corrección debido al Rango"])
        sheet.append([datos["rango_electrometro"], datos["factor_correccion_distancia"], datos["factor_correccion_rango"]])
        workbook.save(xlsx_path)

        from subframe_inferior_derecho import create_subframe_inferior_derecho
        subframe_inferior_der = create_subframe_inferior_derecho(parent)
        subframe_inferior_der.grid(row=0, column=0, sticky="nsew")

    def borrar_datos():
        # Elimina los archivos DS3.json y DS3.xlsx y borra los datos del frame.
        json_path = os.path.join(os.getcwd(), "DS3.json")
        xlsx_path = os.path.join(os.getcwd(), "DS3.xlsx")

        if os.path.exists(json_path):
            os.remove(json_path)
        if os.path.exists(xlsx_path):
            os.remove(xlsx_path)

        messagebox.showinfo("Datos borrados", "Todos los datos han sido borrados.")


    return subframe_container
