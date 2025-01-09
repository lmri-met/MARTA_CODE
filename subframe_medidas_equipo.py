import tkinter as tk
from frame_medidas_equipo import crear_frame_medidas_equipo
from frame_medidas_monitora import crear_frame_medidas_monitora


def crear_subframes_medidas(parent):
    """Crea y organiza los subframes para 'Medidas del Equipo' y 'Medidas de la Monitora'."""
    # Frame principal que contiene los subframes
    main_frame = tk.Frame(parent)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Frame superior: Medidas del Equipo
    frame_equipo = tk.Frame(main_frame)  # Fondo azul para distinguir
    frame_equipo.pack(fill=tk.X, side=tk.TOP)  # Ajustado a la parte superior

    # Frame inferior: Medidas de la Monitora
    frame_monitora = tk.Frame(main_frame, bg="lightblue")  # Fondo verde para distinguir
    frame_monitora.pack(fill=tk.X, side=tk.TOP)  # Justo debajo del superior

    # Añadir contenido al frame superior
    frame_equipo_content = crear_frame_medidas_equipo(frame_equipo)
    if frame_equipo_content:
        frame_equipo_content.pack(fill=tk.BOTH, expand=True)  # Asegúrate de empaquetar el contenido

    # Añadir contenido al frame inferior
    frame_monitora_content = crear_frame_medidas_monitora(frame_monitora)
    if frame_monitora_content:
        frame_monitora_content.pack(fill=tk.BOTH, expand=True)  # Asegúrate de empaquetar el contenido

    return main_frame
