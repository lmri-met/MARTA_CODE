import serial
import random  # Importar la biblioteca para generar números aleatorios

def obtener_temperatura_puerto(serie):
    """
    Función para obtener la temperatura desde un dispositivo MKT 50 conectado a un puerto serie.
    :param serie: Objeto serial.Serial configurado para el dispositivo.
    :return: Temperatura como string XX.XX o mensaje de error.
    """
    try:
        # Enviar comando para obtener datos
        serie.write(b"GET DATA\r")
        
        # Leer respuesta
        respuesta = serie.readlines()  # Lee todas las líneas de respuesta
        for linea in respuesta:
            linea_decodificada = linea.decode('utf-8').strip()
            if "T1=" in linea_decodificada:  # Buscar la línea con la temperatura
                temperatura = linea_decodificada.split("=")[1].strip().split(" ")[0]
                return temperatura
        
        return "not"  # Si no encuentra la temperatura, devolver "not"
    except Exception as e:
        return f"Error de comunicación: {e}"

# Configuración del puerto serie
puerto = "COM9"  # Cambiar según sea necesario
velocidad_baudos = 9600  # Según el manual

try:
    # Abrir puerto serie
    with serial.Serial(port=puerto, baudrate=velocidad_baudos, timeout=2) as serie:
        resultado = obtener_temperatura_puerto(serie)
        if resultado == "not":
            # Generar un número aleatorio entre 20.00 y 22.00
            temperatura_aleatoria = round(random.uniform(20.00, 22.00), 2)
            # print(f"{temperatura_aleatoria}")
        else:
            print(f"{resultado}")
except serial.SerialException as e:
    print(f"Error al abrir el puerto serie: {e}")
