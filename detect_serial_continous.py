import time
import serial
import serial.tools.list_ports

def checking_port(PORT):
    try:
        # open the serial port
        ser = serial.Serial(
            port=PORT,
            timeout=10
        )

        while True:
            if ser.is_open:
                print('Serial port open')

            # waiting 5 seconds
            time.sleep(5)
            # ser = 0
            checking_device(SN_USED_PORT)

    except KeyboardInterrupt:
        if ser.is_open:
            ser.close()
        print("Stopped by User")

    except Exception as e:
        print("Serial port not detected")
        print("Waiting 5 seconds")
        print_countdown(second=5)
        checking_port(PORT=PORT)

    finally:
        if ser.is_open:
            ser.close()
            print('Serial port closed')

def checking_device(sn_used_port):
    # take all ports
    ports = serial.tools.list_ports.comports()

    # loop port
    for port in ports:
        print(port.serial_number)
        if port.serial_number == sn_used_port:
            port = port.device
            checking_port(port)
    print(f"Device with serial number {sn_used_port} not detected. Check again in 5 seconds...")
    print_countdown(second=5)
    checking_device(sn_used_port)

def print_countdown(second: int):
    for i in range(second):
        print(f"{i + 1}")
        time.sleep(1)

if __name__ == '__main__':
    # identified port from list_ports
    # PORT = "COM3"
    # SN_USED_PORT = "ETAVE11BS13"
    SN_USED_PORT = "EBCME11BS13"
    ser = 0
    # baudrate => 9600 / 115200 / 921600
    # BAUD_RATE =

    # Serial number
    # EBCME11BS13
    # ETAVE11BS13

    try:
        checking_device(SN_USED_PORT)

        # read data from the serial port
        # data = ser.readline().decode().strip()
        # print(f"Received data: {data}")

        # close the serial port
        # ser.close()
    except Exception as e:
        print(f'Error: {e}')
