import tkinter as tk
import json
import os

def create_factor_calibracion_frame(parent):
    """Crea un frame para la opción 'Cálculo factor de calibración'."""
    frame = tk.Frame(parent, bg="white", padx=10, pady=10)
    tk.Label(frame, text="Cálculo Factor de Calibración", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

    # Leer el valor de 'numero_escalas' y la lista de escalas desde condiciones.json
    condiciones_path = os.path.join("AAA_ST_REGISTROS", "condiciones.json")
    try:
        with open(condiciones_path, "r") as f:
            condiciones = json.load(f)
            numero_escalas = condiciones.get("numero_escalas", 0)
            tabla = condiciones.get("tabla", [])
            escalas = [item.get("Escala", "") for item in tabla]
    except (FileNotFoundError, json.JSONDecodeError):
        numero_escalas = 0
        escalas = []

    # Crear tabla fusionada
    table_frame = tk.Frame(frame, bg="white")
    table_frame.pack(pady=10, fill="x")

    # Fila 1: Lecturas de la cámara Patrón y Lecturas del instrumento
    tk.Label(
        table_frame, text="Lecturas de la cámara Patrón", bg="#add8e6", 
        font=("Arial", 10, "bold"), relief="ridge", width=100, anchor="center"
    ).grid(row=0, column=0, columnspan=5, padx=0, pady=0)

    tk.Label(
        table_frame, text="Lecturas del instrumento", bg="#90ee90", 
        font=("Arial", 10, "bold"), relief="ridge", width=40, anchor="center"
    ).grid(row=0, column=5, columnspan=2, padx=0, pady=0)

    # Fila 2: Cabecera de columnas
    columnas = [
        "Calidad (ISO4037-1)", "Escala", "Ka (uGy/s)", "H*(10) (mSv/h)", 
        "H*(10) (uSv) (300s)", "Tasa (mSv/h)", "Integrada (uSv) (300s)"
    ]

    for col_index, col_text in enumerate(columnas):
        bg_color = "#add8e6" if col_index < 5 else "#90ee90"
        tk.Label(
            table_frame, text=col_text, bg=bg_color, font=("Arial", 10, "bold"),
            relief="ridge", width=20, anchor="center"
        ).grid(row=1, column=col_index, padx=0, pady=0)

    # Filas dinámicas según el número de escalas
    for i in range(numero_escalas):
        for j in range(len(columnas)):
            bg_color = "#f0f8ff" if j < 5 else "#d0f0c0"
            if j == 1:  # Columna "Escala"
                valor = escalas[i] if i < len(escalas) else ""
                tk.Label(
                    table_frame, text=valor, bg=bg_color, font=("Arial", 10),
                    relief="ridge", width=20, anchor="center"
                ).grid(row=i + 2, column=j, padx=0, pady=0)
            else:
                tk.Entry(
                    table_frame, bg=bg_color, font=("Arial", 10), relief="ridge",
                    width=20
                ).grid(row=i + 2, column=j, padx=0, pady=0)

    return frame

# Crear ventana principal para prueba
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Cálculo Factor de Calibración")

    frame = create_factor_calibracion_frame(root)
    frame.pack(fill="both", expand=True)

    root.mainloop()
