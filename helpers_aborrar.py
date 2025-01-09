import tkinter as tk

def agregar_tabla_resumen_con_celdas(frame, numero_escalas, escalas):
    """
    Agrega una tabla resumen con celdas prellenadas en la columna de "Escala".
    :param frame: El marco donde se agregará la tabla.
    :param numero_escalas: Número de filas de la tabla.
    :param escalas: Lista de valores para rellenar la columna "Escala".
    """
    print(f"[DEBUG] Recibido en helpers: número_escalas={numero_escalas}, escalas={escalas}")  # DEBUG

    # Frame principal que contiene la tabla y los botones
    contenedor_frame = tk.Frame(frame, bg="white", padx=0, pady=0)
    contenedor_frame.pack(fill="x", padx=0, pady=0)

    # Crear un subframe para la tabla
    tabla_frame = tk.Frame(contenedor_frame, bg="white", padx=0, pady=0)
    tabla_frame.pack(side="left", fill="x", expand=True)

    # Títulos que abarcan varias columnas
    tk.Label(tabla_frame, text="Tasa de Fondo", bg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky="nsew")
    tk.Label(tabla_frame, text="Tasa de Dosis", bg="white", font=("Arial", 10, "bold")).grid(row=0, column=2, columnspan=4, sticky="nsew")
    tk.Label(tabla_frame, text="Tasa de Dosis Integrada", bg="white", font=("Arial", 10, "bold")).grid(row=0, column=6, columnspan=2, sticky="nsew")

    # Encabezados
    encabezados = [
        "Escala", "Lectura",
        "Lectura directa", "Presión (kPa)", "Temperatura (C)", "Lectura corregida",
        "Lectura directa", "Lectura corregida"
    ]
    for idx, encabezado in enumerate(encabezados):
        tk.Label(tabla_frame, text=encabezado, bg="light gray", font=("Arial", 8, "bold"), borderwidth=1, relief="solid").grid(row=1, column=idx, sticky="nsew", padx=0, pady=0)

    # Filas dinámicas basadas en el número de escalas
    for fila in range(numero_escalas):
        escala_valor = escalas[fila] if fila < len(escalas) else ""  # Si hay más filas que escalas, deja vacío
        print(f"[DEBUG] Escala para la fila {fila}: {escala_valor}")  # DEBUG
        for col in range(8):  # 8 columnas en total
            if col == 0:  # Columna de "Escala"
                tk.Label(tabla_frame, text=escala_valor, bg="light gray", font=("Arial", 10), width=12, borderwidth=1, relief="solid").grid(row=fila * 2 + 2, column=col, rowspan=2, padx=0, pady=0, sticky="nsew")
            elif col in [2, 3, 4, 5]:  # Columnas con dos celdas por fila
                tk.Entry(tabla_frame, justify="center", font=("Arial", 10), width=12, borderwidth=1, relief="solid").grid(row=fila * 2 + 2, column=col, padx=0, pady=0, sticky="nsew")
                tk.Entry(tabla_frame, justify="center", font=("Arial", 10), width=12, borderwidth=1, relief="solid").grid(row=fila * 2 + 3, column=col, padx=0, pady=0, sticky="nsew")
            else:  # Celdas simples
                tk.Entry(tabla_frame, justify="center", font=("Arial", 10), width=12, borderwidth=1, relief="solid").grid(row=fila * 2 + 2, column=col, rowspan=2, padx=0, pady=0, sticky="nsew")

    # Ajustar la geometría del grid
    for i in range(numero_escalas * 2 + 2):
        tabla_frame.grid_rowconfigure(i, weight=0)  # Evitar estiramiento vertical
    for j in range(8):
        tabla_frame.grid_columnconfigure(j, weight=0)  # Evitar estiramiento horizontal
