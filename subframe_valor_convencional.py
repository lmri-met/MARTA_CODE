import tkinter as tk
import json
import os

def create_valor_convencional_frame(parent):
    """Crea un frame para la opción 'Valor convencionalmente verdadero'."""
    frame = tk.Frame(parent, bg="white", padx=10, pady=10)
    tk.Label(frame, text="Valor Convencionalmente Verdadero", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

    # Leer el valor de 'numero_escalas' y la lista de escalas desde condiciones.json
    condiciones_path = os.path.join("AAA_ST_REGISTROS", "condiciones.json")
    try:
        with open(condiciones_path, "r") as f:
            condiciones = json.load(f)
            numero_escalas = condiciones.get("numero_escalas", 0)
            tabla_escalas = condiciones.get("tabla", [])
            valores_escalas = [item.get("Escala", "") for item in tabla_escalas]
    except (FileNotFoundError, json.JSONDecodeError):
        numero_escalas = 0
        valores_escalas = []

    # Crear tabla con 6 filas y (1 + numero_escalas) columnas
    num_filas = 7
    num_columnas = 1 + numero_escalas

    etiquetas = [
        "Escala",
        "Valor medido cámara patrón",
        "Coef. de conversión de kerma a magnitud de medida",
        "Factor de corrección del rango del electrómetro",
        "Factor de corrección de la densidad del aire",
        "Valor convencionalmente verdadero de tasa de dosis",
        "Valor convencionalmente verdadero de dosis integrada"
    ]

    table_frame = tk.Frame(frame, bg="white")
    table_frame.pack(pady=10)

    for i in range(num_filas):
        for j in range(num_columnas):
            # Determinar el color de fondo según la fila
            if i == 0:  # Fila 1 (fondo gris muy claro)
                bg_color = "#f0f0f0"
            elif i in {5, 6}:  # Filas 6 y 7 (fondo azul muy claro)
                bg_color = "#d0e7ff"
            elif i in {1, 2, 3, 4}:  # Filas 2, 3, 4 y 5 (fondo gris muy ligero)
                bg_color = "#f0f0f0"
            else:  # Fila por defecto
                bg_color = "white"

            if j == 0:
                # Columna de etiquetas
                tk.Label(
                    table_frame,
                    text=etiquetas[i],
                    bg=bg_color,
                    relief="ridge",
                    font=("Arial", 12),
                    width=50
                ).grid(row=i, column=j, padx=2, pady=5)
            else:
                # Columnas de escala
                entry = tk.Entry(
                    table_frame,
                    bg=bg_color,
                    relief="ridge",
                    font=("Arial", 12),
                    width=16
                )
                entry.grid(row=i, column=j, padx=2, pady=5)
                # Configurar valores para la fila "Escala"
                if i == 0 and j <= len(valores_escalas):
                    entry.insert(0, valores_escalas[j - 1])

    return frame
