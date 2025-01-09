import tkinter as tk
from frame_FCD_1_patron import crear_frame_FCD_1_patron
from frame_FCD_1_monitora import crear_frame_FCD_1_monitora
from frame_FCD_2_patron import crear_frame_FCD_2_patron
from frame_FCD_2_monitora import crear_frame_FCD_2_monitora

def create_factor_distancia_frame(parent):
    main_frame = tk.Frame(parent)
    main_frame.pack(expand=False)

    # Frame superior: Medidas del patron
    frame_FCD_1_patron = tk.Frame(main_frame)  # Fondo azul para distinguir
    frame_FCD_1_patron.pack(fill=tk.X, side=tk.TOP)  # Ajustado a la parte superior

    # Frame inferior: Medidas de la monitorap
    frame_FCD_1_monitora = tk.Frame(main_frame, bg="lightblue")  # Fondo verde para distinguir
    frame_FCD_1_monitora.pack(fill=tk.X, side=tk.TOP)  # Justo debajo del superior

    # Frame superior: Medidas del patron
    frame_FCD_2_patron = tk.Frame(main_frame)  # Fondo azul para distinguir
    frame_FCD_2_patron.pack(fill=tk.X, side=tk.TOP)  # Ajustado a la parte superior

    # Frame inferior: Medidas de la monitorap
    frame_FCD_2_monitora = tk.Frame(main_frame, bg="lightblue")  # Fondo verde para distinguir
    frame_FCD_2_monitora.pack(fill=tk.X, side=tk.TOP)  # Justo debajo del superior

    # Añadir contenido al frame superior
    frame_FCD_1_patron = crear_frame_FCD_1_patron(main_frame)
    if frame_FCD_1_patron:
        frame_FCD_1_patron.pack(expand=False) 

    # Añadir contenido al frame superior
    frame_FCD_1_monitora = crear_frame_FCD_1_monitora(main_frame)
    if frame_FCD_1_monitora:
        frame_FCD_1_monitora.pack(expand=False)   

    # Añadir contenido al frame superior
    frame_FCD_2_patron = crear_frame_FCD_2_patron(main_frame)
    if frame_FCD_2_patron:
        frame_FCD_2_patron.pack(expand=False) 

    # Añadir contenido al frame superior
    frame_FCD_2_monitora = crear_frame_FCD_2_monitora(main_frame)
    if frame_FCD_2_monitora:
        frame_FCD_2_monitora.pack(expand=False)  

    return main_frame



