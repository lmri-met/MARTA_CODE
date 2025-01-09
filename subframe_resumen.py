import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import os

def create_resumen_frame(parent):
    frame = tk.Frame(parent, bg="white", padx=10, pady=10)
    
    # Título
    tk.Label(frame, text="Resumen y resultados", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
    
    # Resultado de Tasa de kerma en aire
    tasa_frame = tk.Frame(frame, bg="white")
    tasa_frame.pack(pady=10, fill="x")
    
    tk.Label(tasa_frame, text="Tasa de kerma en aire:", font=("Arial", 14), bg="white").pack(side="left", padx=5)
    result_label = tk.Label(tasa_frame, text="Pendiente de calcular", font=("Arial", 14, "bold"), bg="lime", fg="gray")
    result_label.pack(side="left")
    
    # Entradas de Fecha, Realizado por y Supervisado por
    entries_frame = tk.Frame(frame, bg="white")
    entries_frame.pack(pady=70, fill="x")
    
    # Selector de Fecha
    entry_frame = tk.Frame(entries_frame, bg="white")
    entry_frame.pack(fill="x", pady=5)
    tk.Label(entry_frame, text="Fecha:", font=("Arial", 12), bg="white").pack(side="left", padx=5)
    date_entry = DateEntry(entry_frame, date_pattern="dd/mm/yyyy", font=("Arial", 10))
    date_entry.pack(side="left", padx=5)
    
    # Realizado por
    entry_frame = tk.Frame(entries_frame, bg="white")
    entry_frame.pack(fill="x", pady=5)
    tk.Label(entry_frame, text="Realizado por:", font=("Arial", 12), bg="white").pack(side="left", padx=5)
    realizado_entry = ttk.Entry(entry_frame)
    realizado_entry.insert(0, "Miguel Embid Segura")
    realizado_entry.pack(side="left", fill="x", expand=True, padx=5)
    
    # Supervisado por
    entry_frame = tk.Frame(entries_frame, bg="white")
    entry_frame.pack(fill="x", pady=5)
    tk.Label(entry_frame, text="Supervisado por:", font=("Arial", 12), bg="white").pack(side="left", padx=5)
    supervisado_entry = ttk.Entry(entry_frame)
    supervisado_entry.insert(0, "Miguel Embid Segura")
    supervisado_entry.pack(side="left", fill="x", expand=True, padx=5)
    
    # Campo de Firma
    firma_frame = tk.Frame(frame, bg="white", pady=10)
    firma_frame.pack(fill="x")
    tk.Label(firma_frame, text="Firma:", font=("Arial", 12), bg="white").pack(anchor="w", padx=5)
    
    canvas = tk.Canvas(firma_frame, width=400, height=100, bg="lightgray")
    canvas.pack(pady=5)

    def start_drawing(event):
        canvas.old_coords = (event.x, event.y)

    def draw(event):
        x, y = event.x, event.y
        if hasattr(canvas, 'old_coords'):
            x1, y1 = canvas.old_coords
            canvas.create_line(x1, y1, x, y, width=2, fill="black", capstyle=tk.ROUND, smooth=True)
            canvas.old_coords = (x, y)

    def stop_drawing(event):
        canvas.old_coords = None

    def clear_canvas():
        canvas.delete("all")

    def save_signature():
        # Verifica si la carpeta existe, si no la crea
        if not os.path.exists("AAA_ST_REGISTROS"):
            os.makedirs("AAA_ST_REGISTROS")
        
        # Obtén el nombre de archivo
        filename = "AAA_ST_REGISTROS/firma.jpg"
        
        # Guarda la firma como imagen JPEG
        canvas.postscript(file="firma.ps", colormode='color')
        img = Image.open("firma.ps")
        img.save(filename, "JPEG")
        os.remove("firma.ps")  # Elimina el archivo .ps temporal
        
        print(f"Firma guardada en: {filename}")
    
    canvas.bind("<Button-1>", start_drawing)
    canvas.bind("<B1-Motion>", draw)
    canvas.bind("<ButtonRelease-1>", stop_drawing)
    
    # Botones de limpiar y guardar en la misma línea
    button_frame = tk.Frame(firma_frame, bg="white")
    button_frame.pack(pady=5)
    
    clear_button = tk.Button(button_frame, text="Limpiar", command=clear_canvas)
    clear_button.pack(side="left", padx=10)
    
    save_button = tk.Button(button_frame, text="Guardar firma", command=save_signature)
    save_button.pack(side="left", padx=10)

    # Botones de exportar con iconos y textos debajo
    export_frame = tk.Frame(frame, bg="white")
    export_frame.pack(pady=20)
    
    for text, icon_path, label_text in [
        ("WORD", "doc.png", "Certificado"), 
        ("PDF", "pdf.png", "Datos y resultados"), 
        ("EXCEL", "xls.png", "Datos y resultados")
    ]:
        button_frame = tk.Frame(export_frame, bg="white")
        button_frame.pack(side="left", padx=10)
        
        icon = Image.open(icon_path)
        icon = icon.resize((60, 60), Image.Resampling.LANCZOS)  # Doblado el tamaño de los iconos
        icon = ImageTk.PhotoImage(icon)
        button = tk.Button(button_frame, image=icon, bg="white", command=lambda t=text: print(f"Exportar a {t}"))
        button.image = icon  # Necesario para evitar que se elimine el objeto
        button.pack()
        
        tk.Label(button_frame, text=label_text, font=("Arial", 10), bg="white").pack()

    return frame

# Ventana principal para probar el frame
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Resumen de resultados")
    root.geometry("600x800")  # Cambiado el tamaño para que se ajuste al contenido
    resumen_frame = create_resumen_frame(root)
    resumen_frame.pack(fill="both", expand=True)
    root.mainloop()
