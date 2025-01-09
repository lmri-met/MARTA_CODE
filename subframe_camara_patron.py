import tkinter as tk
from frame_medidas_patron import crear_frame_medidas_patron
from frame_medidas_monitorap import crear_frame_medidas_monitorap

def create_camara_patron_frame(parent):
    main_frame = tk.Frame(parent)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Frame superior: Medidas del patron
    frame_patron = tk.Frame(main_frame)  # Fondo azul para distinguir
    frame_patron.pack(fill=tk.X, side=tk.TOP)  # Ajustado a la parte superior

    # Frame inferior: Medidas de la monitorap
    frame_monitorap = tk.Frame(main_frame, bg="lightblue")  # Fondo verde para distinguir
    frame_monitorap.pack(fill=tk.X, side=tk.TOP)  # Justo debajo del superior

    # Añadir contenido al frame superior
    frame_patron_content = crear_frame_medidas_patron(frame_patron)
    if frame_patron_content:
        frame_patron_content.pack(fill=tk.BOTH, expand=True)  # Asegúrate de empaquetar el contenido

    # Añadir contenido al frame inferior
    frame_monitorap_content = crear_frame_medidas_monitorap(frame_monitorap)
    if frame_monitorap_content:
        frame_monitorap_content.pack(fill=tk.BOTH, expand=True)  # Asegúrate de empaquetar el contenido

    return main_frame
