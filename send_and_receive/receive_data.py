import serial

def receive_data(port_name):
    """Receive data from the specified serial port."""
    try:
        with serial.Serial(port=port_name, baudrate=9600, timeout=1) as ser:
            print(f"Connected to {port_name}")
            while True:
                if ser.in_waiting > 0:
                    data = ser.read(ser.in_waiting).decode()
                    print(f"Received data: {data}")

    except serial.SerialException as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    PORT_NAME = 'COM2'  # Replace with your port name
    receive_data(PORT_NAME)
