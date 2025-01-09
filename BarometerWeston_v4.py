import sys
import serial
import time

class Barometer:
    def __init__(self, port, baudrate, interval=1):
        self.port = port
        self.baudrate = baudrate
        self.interval = interval

    def check_port(self):
        try:
            with serial.Serial(self.port, self.baudrate, timeout=2) as ser:
                return True
        except serial.SerialException:
            return False

    def send_command(self, command):
        response = None
        try:
            with serial.Serial(self.port, self.baudrate, timeout=2) as ser:
                ser.write((command + '\r\n').encode('utf-8'))
                time.sleep(1)
                response = ''
                while ser.in_waiting > 0:
                    response += ser.read(ser.in_waiting).decode('utf-8')
                    time.sleep(0.2)
        except serial.SerialException:
            return None
        except Exception:
            return None
        
        return response.strip() if response else None

if __name__ == "__main__":
    # Asegurarse de que el script se ejecuta con un argumento válido
    if len(sys.argv) > 1 and sys.argv[1] == "read_pressure":
        port = "COM7"  # Ajustar al puerto correcto para el barómetro
        baudrate = 9600
        barometer = Barometer(port, baudrate)

        if barometer.check_port():
            pressure = barometer.send_command('$MR')
            if pressure:
                try:
                    # Extraer solo los dígitos y dividir por 1000
                    sanitized_pressure = ''.join(filter(str.isdigit, pressure)) or "0"
                    divided_pressure = float(sanitized_pressure) / 1000
                    # Imprimir el resultado con 3 decimales
                    print(f"{divided_pressure:.3f}")
                except ValueError:
                    print("0.000")  # Devuelve un valor por defecto en caso de error
            else:
                print("Error: No se pudo leer la presión.")
        else:
            print("Error: El puerto no está disponible.")
    else:
        print("Uso: python BarometerWeston_v4.py read_pressure")

