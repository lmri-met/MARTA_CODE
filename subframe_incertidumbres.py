import tkinter as tk
from math import sqrt
import json
import os
from tkinter import messagebox
import pandas as pd

def create_incertidumbres_frame(parent):
    subframe = tk.Frame(parent, bg="white", relief="solid", bd=1)

    # Título
    titulo_frame = tk.Frame(subframe, bg="#FFDAB9")  # Fondo naranja claro en todo el Frame
    titulo_frame.pack(fill="x", pady=5, padx=10)
    tk.Label(titulo_frame, text="INCERTIDUMBRE DE LA MEDIDA DE LA TASA DE KERMA EN AIRE", bg="#FFDAB9", fg="black",
             font=('Helvetica', 14, 'bold')).pack(fill="x", pady=5)

    # Configuración del ancho de las etiquetas
    label_width = 25  # Ancho uniforme para todas las etiquetas

    # Variables asociadas a los campos de entrada
    incertidumbre_vars = {
        "entry_incertTA_Ka": tk.StringVar(),
        "entry_FactorCorrecKa": tk.StringVar(),
        "entry_TiempoEfectivoKa": tk.StringVar(),
        "entry_PresionKa": tk.StringVar(),
        "entry_TemperaturaKa": tk.StringVar(),
        "entry_HumedadRelativaKa": tk.StringVar(),
        "entry_EstabilidadKa": tk.StringVar(),
        "entry_CFKa": tk.StringVar(),
        "entry_ValorBajoKa": tk.StringVar(),
    }

    def calcular_incertidumbre_automatica(*args):
        try:
            # Convertir los valores a flotantes y calcular la suma cuadrática
            valores = [float(var.get() or 0) for var in incertidumbre_vars.values()]
            incertidumbre_tipica_combinada = sqrt(sum(v**2 for v in valores))
            uk2 = incertidumbre_tipica_combinada * 2

            # Actualizar etiquetas con los resultados
            label_ITCKa_value.config(text=f"{incertidumbre_tipica_combinada:.2f}")
            label_UK2Ka_value.config(text=f"{uk2:.2f}")
        except ValueError:
            # Si ocurre un error, mostrar "Error"
            label_ITCKa_value.config(text="Error")
            label_UK2Ka_value.config(text="Error")

    # Vincular las variables al cálculo automático
    for var in incertidumbre_vars.values():
        var.trace_add("write", calcular_incertidumbre_automatica)

    # Campo "Incertidumbre Tipo A" con fondo gris claro
    row_ta = tk.Frame(subframe, bg="#F5F5F5")  # Fondo gris claro
    row_ta.pack(fill="x", pady=5, padx=10)
    tk.Label(row_ta, text="Incertidumbre Tipo A:", bg="#E0F7FF", width=label_width, anchor="w").pack(side="left")
    entry_incertTA_Ka = tk.Entry(row_ta, width=5, bg="#E0F7FF", textvariable=incertidumbre_vars["entry_incertTA_Ka"])
    entry_incertTA_Ka.pack(side="left", padx=5)
    tk.Label(row_ta, text="%    Preguntar a Marta", bg="#E0F7FF", anchor="w").pack(side="left", padx=5)

    # Texto "Incertidumbres de tipo B"
    row_tipo_b = tk.Frame(subframe, bg="#E0F7FF")  # Fondo azul claro
    row_tipo_b.pack(fill="x", pady=5, padx=10)
    tk.Label(row_tipo_b, text="Incertidumbres de tipo B", bg="#E0F7FF", font=('Helvetica', 10), anchor="w").pack(side="left")

    # Crear filas con dos campos por línea
    def add_row_quad(parent, label1_text, var1, label2_text, var2, label3_text, var3, label4_text, var4):
        row = tk.Frame(parent, bg="white")  # Fondo blanco para toda la línea
        row.pack(fill="x", pady=5, padx=10)

        # Primer campo
        frame1 = tk.Frame(row, bg="#E0F7FF")  # Fondo azul claro para el primer campo
        frame1.pack(side="left", padx=5)
        tk.Label(frame1, text=label1_text, bg="#E0F7FF", width=label_width, anchor="w").pack(side="left")
        entry1 = tk.Entry(frame1, width=5, bg="#E0F7FF", textvariable=var1)
        entry1.pack(side="left", padx=5)
        tk.Label(frame1, text="%", bg="#E0F7FF", anchor="w").pack(side="left", padx=5)

        # Segundo campo
        frame2 = tk.Frame(row, bg="#E0F7FF")  # Fondo azul claro para el segundo campo
        frame2.pack(side="left", padx=5)
        tk.Label(frame2, text=label2_text, bg="#E0F7FF", width=label_width, anchor="w").pack(side="left")
        entry2 = tk.Entry(frame2, width=5, bg="#E0F7FF", textvariable=var2)
        entry2.pack(side="left", padx=5)
        tk.Label(frame2, text="%", bg="#E0F7FF", anchor="w").pack(side="left", padx=5)

        # Tercer campo
        frame3 = tk.Frame(row, bg="#E0F7FF")  # Fondo azul claro para el tercer campo
        frame3.pack(side="left", padx=5)
        tk.Label(frame3, text=label3_text, bg="#E0F7FF", width=label_width, anchor="w").pack(side="left")
        entry3 = tk.Entry(frame3, width=5, bg="#E0F7FF", textvariable=var3)
        entry3.pack(side="left", padx=5)
        tk.Label(frame3, text="%", bg="#E0F7FF", anchor="w").pack(side="left", padx=5)

        # Cuarto campo
        frame4 = tk.Frame(row, bg="#E0F7FF")  # Fondo azul claro para el cuarto campo
        frame4.pack(side="left", padx=5)
        tk.Label(frame4, text=label4_text, bg="#E0F7FF", width=label_width, anchor="w").pack(side="left")
        entry4 = tk.Entry(frame4, width=5, bg="#E0F7FF", textvariable=var4)
        entry4.pack(side="left", padx=5)
        tk.Label(frame4, text="%", bg="#E0F7FF", anchor="w").pack(side="left", padx=5)

    # Añadir filas con 4 campos por línea
    add_row_quad(subframe, "Factor de corrección:", incertidumbre_vars["entry_FactorCorrecKa"],
                "Tiempo efectivo de medida:", incertidumbre_vars["entry_TiempoEfectivoKa"],
                "Presión:", incertidumbre_vars["entry_PresionKa"],
                "Temperatura:", incertidumbre_vars["entry_TemperaturaKa"])

    add_row_quad(subframe, "Humedad relativa:", incertidumbre_vars["entry_HumedadRelativaKa"],
                "Estabilidad a largo plazo de la cámara:", incertidumbre_vars["entry_EstabilidadKa"],
                "Corriente de fuga:", incertidumbre_vars["entry_CFKa"],
                "Valores bajos de Kair:", incertidumbre_vars["entry_ValorBajoKa"])

    # Incertidumbre típica combinada y U(k=2) en una sola línea con fondo verde claro
    row_results = tk.Frame(subframe, bg="white")  # Fondo blanco para el resto de la línea
    row_results.pack(fill="x", pady=5, padx=10)

    # Incertidumbre típica combinada
    frame_itc = tk.Frame(row_results, bg="#E0F7FF")  # Fondo verde claro
    frame_itc.pack(side="left", padx=5)
    tk.Label(frame_itc, text="Incertidumbre típica combinada:", bg="#E0F7FF", width=label_width, anchor="w").pack(side="left")
    label_ITCKa_value = tk.Label(frame_itc, text="0.00", bg="#E0F7FF", width=5, anchor="w")
    label_ITCKa_value.pack(side="left", padx=5)
    tk.Label(frame_itc, text="%", bg="#E0F7FF", anchor="w").pack(side="left", padx=5)

    # Espaciador entre los dos campos
    tk.Label(row_results, text="", bg="white", width=2).pack(side="left")

    # U(k=2)
    frame_uk2 = tk.Frame(row_results, bg="#E0F7FF")  # Fondo verde claro
    frame_uk2.pack(side="left", padx=5)
    tk.Label(frame_uk2, text="U(k=2):", bg="#E0F7FF", width=label_width, anchor="w").pack(side="left")
    label_UK2Ka_value = tk.Label(frame_uk2, text="0.00", bg="#E0F7FF", width=5, anchor="w")
    label_UK2Ka_value.pack(side="left", padx=5)
    tk.Label(frame_uk2, text="%", bg="#E0F7FF", anchor="w").pack(side="left", padx=5)

    # Título
    titulo_frame = tk.Frame(subframe, bg="#FFDAB9") 
    titulo_frame.pack(fill="x", pady=5, padx=10)
    tk.Label(titulo_frame, text="INCERTIDUMBRE DEL VALOR CONVENCIONALMENTE VERDADERO DE LA MAGNITUD DE MEDIDA", bg="#FFDAB9", fg="black",
             font=('Helvetica', 14, 'bold')).pack(fill="x", pady=5)

    # Variables asociadas a las dos columnas
    incertidumbre2_vars = {
        "entry_valorconverd_tasa": tk.StringVar(),
        "entry_valorconverd_integrada": tk.StringVar(),
        "entry_inhomogeneidad_tasa": tk.StringVar(),
        "entry_inhomogeneidad_integrada": tk.StringVar(),
        "entry_coefconv_tasa": tk.StringVar(),
        "entry_coefconv_integrada": tk.StringVar(),
        "entry_distdis_tasa": tk.StringVar(),
        "entry_distdis_integrada": tk.StringVar(),
        "entry_tiempoMI_tasa": tk.StringVar(),
        "entry_tiempoMI_integrada": tk.StringVar(),
    }

    def calcular_incertidumbre2_automatica(*args):
        try:
            # Convertir los valores de las tasas a flotantes
            valores_tasa = [float(var.get() or 0) for key, var in incertidumbre2_vars.items() if "tasa" in key]
            # Convertir los valores de las integradas a flotantes
            valores_integrada = [float(var.get() or 0) for key, var in incertidumbre2_vars.items() if "integrada" in key]

            # Calcular las incertidumbres típicas combinadas
            incertidumbre_tasa_tipica_combinada = sqrt(sum(v**2 for v in valores_tasa))
            incertidumbre_integrada_tipica_combinada = sqrt(sum(v**2 for v in valores_integrada))

            # Calcular U(k=2)
            uk2_tasa = incertidumbre_tasa_tipica_combinada * 2
            uk2_integrada = incertidumbre_integrada_tipica_combinada * 2

            # Actualizar etiquetas con los resultados
            label_ITCKa2_tasa_value.config(text=f"{incertidumbre_tasa_tipica_combinada:.2f}")
            label_ITCKa2_integrada_value.config(text=f"{incertidumbre_integrada_tipica_combinada:.2f}")
            label_UK2Ka2_tasa_value.config(text=f"{uk2_tasa:.2f}")
            label_UK2Ka2_integrada_value.config(text=f"{uk2_integrada:.2f}")
        except ValueError:
            # Si ocurre un error, mostrar "Error"
            label_ITCKa2_tasa_value.config(text="Error")
            label_ITCKa2_integrada_value.config(text="Error")
            label_UK2Ka2_tasa_value.config(text="Error")
            label_UK2Ka2_integrada_value.config(text="Error")

    # Vincular las variables al cálculo automático
    for var in incertidumbre2_vars.values():
        var.trace_add("write", calcular_incertidumbre2_automatica)

    # Encabezado para las columnas
    header_row = tk.Frame(subframe, bg="white")
    header_row.pack(fill="x", pady=5, padx=10)
    tk.Label(header_row, text="", bg="white", width=35, anchor="w").pack(side="left", padx=5)
    tk.Label(header_row, text="Incertidumbre de la tasa", bg="#E0F7FF", width=35, anchor="center").pack(side="left", padx=5)
    tk.Label(header_row, text="Incertidumbre de la integrada", bg="#B3E5FC", width=35, anchor="center").pack(side="left", padx=5)

    # Función para añadir filas con dos entradas por etiqueta
    def add_row_double_entry(parent, label_text, var_tasa, var_integrada):
        row = tk.Frame(parent, bg="white")  # Fondo blanco para toda la línea
        row.pack(fill="x", pady=5, padx=10)

        # Etiqueta principal
        tk.Label(row, text=label_text, bg="#EDE7F6", width=50, anchor="w").pack(side="left", padx=5)

        # Entrada para "Incertidumbre de la tasa"
        frame_tasa = tk.Frame(row, bg="#E0F7FF")  # Fondo azul claro
        frame_tasa.pack(side="left", padx=5)
        entry_tasa = tk.Entry(frame_tasa, width=5, bg="#E0F7FF", textvariable=var_tasa)
        entry_tasa.pack(side="left", padx=5)
        tk.Label(frame_tasa, text="%", bg="#E0F7FF", anchor="w").pack(side="left", padx=5)

        # Espaciador entre las dos entradas
        tk.Label(row, text="", bg="white", width=20).pack(side="left")

        # Entrada para "Incertidumbre de la integrada"
        frame_integrada = tk.Frame(row, bg="#B3E5FC")  # Fondo azul claro
        frame_integrada.pack(side="left", padx=5)
        entry_integrada = tk.Entry(frame_integrada, width=5, bg="#B3E5FC", textvariable=var_integrada)
        entry_integrada.pack(side="left", padx=5)
        tk.Label(frame_integrada, text="%", bg="#B3E5FC", anchor="w").pack(side="left", padx=5)

    # Añadir filas con dos entradas por etiqueta
    add_row_double_entry(subframe, "Valor convencionalmente verdadero de la tasa kerma en aire:",
                        incertidumbre2_vars["entry_valorconverd_tasa"], incertidumbre2_vars["entry_valorconverd_integrada"])
    add_row_double_entry(subframe, "Inhomogeneidad del campo de radiación:",
                        incertidumbre2_vars["entry_inhomogeneidad_tasa"], incertidumbre2_vars["entry_inhomogeneidad_integrada"])
    add_row_double_entry(subframe, "Coeficiente de conversión de kerma a magnitud de medida:",
                        incertidumbre2_vars["entry_coefconv_tasa"], incertidumbre2_vars["entry_coefconv_integrada"])
    add_row_double_entry(subframe, "Distancia distinta a la de referencia de la ISO 4037-3:",
                        incertidumbre2_vars["entry_distdis_tasa"], incertidumbre2_vars["entry_distdis_integrada"])
    add_row_double_entry(subframe, "Tiempo de medida integrada:",
                        incertidumbre2_vars["entry_tiempoMI_tasa"], incertidumbre2_vars["entry_tiempoMI_integrada"])

    # Resultados combinados para tasas e integradas
    result_row = tk.Frame(subframe, bg="white")
    result_row.pack(fill="x", pady=5, padx=10)

    # Resultados para tasas
    tk.Label(result_row, text="Incertidumbre típica combinada (Tasa):", bg="#E0F7FF", width=30, anchor="w").pack(side="left")
    label_ITCKa2_tasa_value = tk.Label(result_row, text="0.00", bg="#E0F7FF", width=8, anchor="w")
    label_ITCKa2_tasa_value.pack(side="left", padx=5)
    tk.Label(result_row, text="U(k=2) (Tasa):", bg="#E0F7FF", width=30, anchor="w").pack(side="left")
    label_UK2Ka2_tasa_value = tk.Label(result_row, text="0.00", bg="#E0F7FF", width=8, anchor="w")
    label_UK2Ka2_tasa_value.pack(side="left", padx=5)

    # Resultados para integradas
    tk.Label(result_row, text="Incertidumbre típica combinada (Integrada):", bg="#B3E5FC", width=30, anchor="w").pack(side="left")
    label_ITCKa2_integrada_value = tk.Label(result_row, text="0.00", bg="#B3E5FC", width=8, anchor="w")
    label_ITCKa2_integrada_value.pack(side="left", padx=5)
    tk.Label(result_row, text="U(k=2) (Integrada):", bg="#B3E5FC", width=30, anchor="w").pack(side="left")
    label_UK2Ka2_integrada_value = tk.Label(result_row, text="0.00", bg="#B3E5FC", width=8, anchor="w")
    label_UK2Ka2_integrada_value.pack(side="left", padx=5)

    # Título
    titulo3_frame = tk.Frame(subframe, bg="#FFDAB9") 
    titulo3_frame.pack(fill="x", pady=5, padx=10)
    tk.Label(titulo3_frame, text="INCERTIDUMBRE DEL CÁLCULO DEL FACTOR DE CALIBRACIÓN", bg="#FFDAB9", fg="black",
             font=('Helvetica', 14, 'bold')).pack(fill="x", pady=5)

    # Variables asociadas a las dos columnas
    incertidumbre3_vars = {
        "entry_incer3TA_tasa": tk.StringVar(),
        "entry_incer3TA_integrada": tk.StringVar(),
        "entry_vcvmagmed_tasa": tk.StringVar(),
        "entry_vcvmagmed_integrada": tk.StringVar(),
        "entry_cPyT_tasa": tk.StringVar(),
        "entry_cPyT_integrada": tk.StringVar(),
        "entry_pos_tasa": tk.StringVar(),
        "entry_pos_integrada": tk.StringVar(),
        "entry_escala_tasa": tk.StringVar(),
        "entry_escala_integrada": tk.StringVar(),
    }

    def calcular_incertidumbre3_automatica(*args):
        try:
            # Convertir los valores de las tasas a flotantes
            valores3_tasa = [float(var.get() or 0) for key, var in incertidumbre3_vars.items() if "tasa" in key]
            # Convertir los valores de las integradas a flotantes
            valores3_integrada = [float(var.get() or 0) for key, var in incertidumbre3_vars.items() if "integrada" in key]

            # Calcular las incertidumbres típicas combinadas
            incertidumbre3_tasa_tipica_combinada = sqrt(sum(v**2 for v in valores3_tasa))
            incertidumbre3_integrada_tipica_combinada = sqrt(sum(v**2 for v in valores3_integrada))

            # Calcular U(k=2)
            uk3_tasa = incertidumbre3_tasa_tipica_combinada * 2
            uk3_integrada = incertidumbre3_integrada_tipica_combinada * 2

            # Actualizar etiquetas con los resultados
            label_ITCKa3_tasa_value.config(text=f"{incertidumbre3_tasa_tipica_combinada:.2f}")
            label_ITCKa3_integrada_value.config(text=f"{incertidumbre3_integrada_tipica_combinada:.2f}")
            label_UK2Ka3_tasa_value.config(text=f"{uk3_tasa:.2f}")
            label_UK2Ka3_integrada_value.config(text=f"{uk3_integrada:.2f}")
        except ValueError:
            # Si ocurre un error, mostrar "Error"
            label_ITCKa3_tasa_value.config(text="Error")
            label_ITCKa3_integrada_value.config(text="Error")
            label_UK2Ka3_tasa_value.config(text="Error")
            label_UK2Ka3_integrada_value.config(text="Error")

    # Vincular las variables al cálculo automático
    for var in incertidumbre3_vars.values():
        var.trace_add("write", calcular_incertidumbre3_automatica)

    # Encabezado para las columnas
    header_row3 = tk.Frame(subframe, bg="white")
    header_row3.pack(fill="x", pady=5, padx=10)
    tk.Label(header_row3, text="", bg="white", width=35, anchor="w").pack(side="left", padx=5)
    tk.Label(header_row3, text="Incertidumbre de la tasa", bg="#E0F7FF", width=35, anchor="center").pack(side="left", padx=5)
    tk.Label(header_row3, text="Incertidumbre de la integrada", bg="#B3E5FC", width=35, anchor="center").pack(side="left", padx=5)

    # Función para añadir filas con dos entradas por etiqueta
    def add_row3_double_entry(parent, label3_text, var3_tasa, var3_integrada):
        row3 = tk.Frame(parent, bg="white")  # Fondo blanco para toda la línea
        row3.pack(fill="x", pady=5, padx=10)

        # Etiqueta principal
        tk.Label(row3, text=label3_text, bg="#EDE7F6", width=50, anchor="w").pack(side="left", padx=5)

        # Entrada para "Incertidumbre de la tasa"
        frame3_tasa = tk.Frame(row3, bg="#E0F7FF")  # Fondo azul claro
        frame3_tasa.pack(side="left", padx=5)
        entry_tasa3 = tk.Entry(frame3_tasa, width=5, bg="#E0F7FF", textvariable=var3_tasa)
        entry_tasa3.pack(side="left", padx=5)
        tk.Label(frame3_tasa, text="%", bg="#E0F7FF", anchor="w").pack(side="left", padx=5)

        # Espaciador entre las dos entradas
        tk.Label(row3, text="", bg="white", width=20).pack(side="left")

        # Entrada para "Incertidumbre de la integrada"
        frame3_integrada = tk.Frame(row3, bg="#B3E5FC")  # Fondo azul claro
        frame3_integrada.pack(side="left", padx=5)
        entry_integrada3 = tk.Entry(frame3_integrada, width=5, bg="#B3E5FC", textvariable=var3_integrada)
        entry_integrada3.pack(side="left", padx=5)
        tk.Label(frame3_integrada, text="%", bg="#B3E5FC", anchor="w").pack(side="left", padx=5)

    # Añadir filas con dos entradas por etiqueta
    add_row3_double_entry(subframe, "Incertidumbre tipo A:",
                        incertidumbre3_vars["entry_incer3TA_tasa"], incertidumbre3_vars["entry_incer3TA_integrada"])
    add_row3_double_entry(subframe, "Valor convencionalmente verdadero magnitud de medida:",
                        incertidumbre3_vars["entry_vcvmagmed_tasa"], incertidumbre3_vars["entry_vcvmagmed_integrada"])
    add_row3_double_entry(subframe, "Corrección por presión y temperatura:",
                        incertidumbre3_vars["entry_cPyT_tasa"], incertidumbre3_vars["entry_cPyT_integrada"])
    add_row3_double_entry(subframe, "Posición patrón y posición equipo:",
                        incertidumbre3_vars["entry_pos_tasa"], incertidumbre3_vars["entry_pos_integrada"])
    add_row3_double_entry(subframe, "División mínima en la escala:",
                        incertidumbre3_vars["entry_escala_tasa"], incertidumbre3_vars["entry_escala_integrada"])

    # Resultados combinados para tasas e integradas
    result_row3 = tk.Frame(subframe, bg="white")
    result_row3.pack(fill="x", pady=5, padx=10)

    # Resultados para tasas
    tk.Label(result_row3, text="Incertidumbre típica combinada (Tasa):", bg="#E0F7FF", width=30, anchor="w").pack(side="left")
    label_ITCKa3_tasa_value = tk.Label(result_row3, text="0.00", bg="#E0F7FF", width=8, anchor="w")
    label_ITCKa3_tasa_value.pack(side="left", padx=5)
    tk.Label(result_row3, text="U(k=2) (Tasa):", bg="#E0F7FF", width=30, anchor="w").pack(side="left")
    label_UK2Ka3_tasa_value = tk.Label(result_row3, text="0.00", bg="#E0F7FF", width=8, anchor="w")
    label_UK2Ka3_tasa_value.pack(side="left", padx=5)

    # Resultados para integradas
    tk.Label(result_row3, text="Incertidumbre típica combinada (Integrada):", bg="#B3E5FC", width=30, anchor="w").pack(side="left")
    label_ITCKa3_integrada_value = tk.Label(result_row3, text="0.00", bg="#B3E5FC", width=8, anchor="w")
    label_ITCKa3_integrada_value.pack(side="left", padx=5)
    tk.Label(result_row3, text="U(k=2) (Integrada):", bg="#B3E5FC", width=30, anchor="w").pack(side="left")
    label_UK2Ka3_integrada_value = tk.Label(result_row3, text="0.00", bg="#B3E5FC", width=8, anchor="w")
    label_UK2Ka3_integrada_value.pack(side="left", padx=5)

    def guardar_datos():
        try:
            # Crear la carpeta si no existe
            folder_path = "AAA_ST_REGISTROS"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            data = {}
            # Guardar las variables de `incertidumbre_vars`
            data['incertidumbre_vars'] = {key: var.get() for key, var in incertidumbre_vars.items()}
            # Guardar las variables de `incertidumbre2_vars`
            data['incertidumbre2_vars'] = {key: var.get() for key, var in incertidumbre2_vars.items()}
            # Guardar las variables de `incertidumbre3_vars`
            data['incertidumbre3_vars'] = {key: var.get() for key, var in incertidumbre3_vars.items()}

            # Añadir valores de las etiquetas
            data['resultados'] = {
                "IncertidumbreTipicaCombinada": label_ITCKa_value.cget("text"),
                "UK2": label_UK2Ka_value.cget("text"),
                "IncertidumbreTipicaTasa": label_ITCKa2_tasa_value.cget("text"),
                "UK2Tasa": label_UK2Ka2_tasa_value.cget("text"),
                "IncertidumbreTipicaIntegrada": label_ITCKa2_integrada_value.cget("text"),
                "UK2Integrada": label_UK2Ka2_integrada_value.cget("text"),
                "IncertidumbreTipicaTasa3": label_ITCKa3_tasa_value.cget("text"),
                "UK2Tasa3": label_UK2Ka3_tasa_value.cget("text"),
                "IncertidumbreTipicaIntegrada3": label_ITCKa3_integrada_value.cget("text"),
                "UK2Integrada3": label_UK2Ka3_integrada_value.cget("text"),
            }

            # Guardar en JSON
            json_path = os.path.join(folder_path, "incertidumbres.json")
            with open(json_path, "w") as json_file:
                json.dump(data, json_file, indent=4)

            # Guardar en Excel
            excel_data = {
                **{key: [var.get()] for key, var in incertidumbre_vars.items()},
                **{key: [var.get()] for key, var in incertidumbre2_vars.items()},
                **{key: [var.get()] for key, var in incertidumbre3_vars.items()},
                "IncertidumbreTipicaCombinada": [label_ITCKa_value.cget("text")],
                "UK2": [label_UK2Ka_value.cget("text")],
                "IncertidumbreTipicaTasa": [label_ITCKa2_tasa_value.cget("text")],
                "UK2Tasa": [label_UK2Ka2_tasa_value.cget("text")],
                "IncertidumbreTipicaIntegrada": [label_ITCKa2_integrada_value.cget("text")],
                "UK2Integrada": [label_UK2Ka2_integrada_value.cget("text")],
                "IncertidumbreTipicaTasa3": [label_ITCKa3_tasa_value.cget("text")],
                "UK2Tasa3": [label_UK2Ka3_tasa_value.cget("text")],
                "IncertidumbreTipicaIntegrada3": [label_ITCKa3_integrada_value.cget("text")],
                "UK2Integrada3": [label_UK2Ka3_integrada_value.cget("text")],
            }

            # Crear un DataFrame para el Excel
            df = pd.DataFrame(excel_data)
            excel_path = os.path.join(folder_path, "incertidumbres.xlsx")
            df.to_excel(excel_path, index=False)

            # Mensaje de éxito
            messagebox.showinfo("Éxito", f"Ficheros guardados correctamente en la carpeta {folder_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar los datos: {str(e)}")

    def resetear_datos():
        try:
            # Borrar los valores de todas las variables
            for var in incertidumbre_vars.values():
                var.set("")
            for var in incertidumbre2_vars.values():
                var.set("")
            for var in incertidumbre3_vars.values():
                var.set("")

            # Eliminar los archivos en la carpeta si existen
            folder_path = "AAA_ST_REGISTROS"
            json_path = os.path.join(folder_path, "incertidumbres.json")
            excel_path = os.path.join(folder_path, "incertidumbres.xlsx")
            if os.path.exists(json_path):
                os.remove(json_path)
            if os.path.exists(excel_path):
                os.remove(excel_path)

            # Eliminar la carpeta si está vacía
            if os.path.exists(folder_path) and not os.listdir(folder_path):
                os.rmdir(folder_path)

            # Mensaje de éxito
            messagebox.showinfo("Éxito", f"Ficheros eliminados correctamente de la carpeta {folder_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al eliminar los datos: {str(e)}")
    
    # Botones para guardar y resetear
    buttons_frame = tk.Frame(subframe, bg="white")
    buttons_frame.pack(fill="x", pady=10, padx=10)

    guardar_button = tk.Button(buttons_frame, text="Guardar datos", command=guardar_datos, bg="#4CAF50", fg="white")
    guardar_button.pack(side="left", padx=5)

    resetear_button = tk.Button(buttons_frame, text="Resetear datos", command=resetear_datos, bg="#F44336", fg="white")
    resetear_button.pack(side="left", padx=5)

    return subframe