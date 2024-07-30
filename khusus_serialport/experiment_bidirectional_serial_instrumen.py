import os
import sys
import time
import serial
import serial.tools.list_ports
from parse_data import agd
from parse_data import exias
from parse_data import promed
from parse_data import U500Insight
from parse_data import wondfobga
from parse_data import xn1000
from parse_data.utils import convert

# sys.path.append(os.path.join(os.path.dirname(__file__), 'parse_data'))

ENQ = [0x05] # ENQUIRY
ACK = [0x06] # ACKNOWLEDGE
EOT = [0x04] # END OF TEXT
LF = [0x0A] # LINE FEED

def open_serial_port(port_name):
    """Open a serial port with the given port name."""
    try:
        ser = serial.Serial(port=port_name, timeout=None, baudrate=9600)
        return ser
    except serial.SerialException:
        return None

def checking_port(port_name):
    """Check if the serial port is open and monitor it."""
    while True:
        is_first_time_opened = False
        ser = open_serial_port(port_name)
        if ser is None:
            is_first_time_opened = False
            print(f"Failed to open port {port_name}. Retrying in 5 seconds...")
            print_countdown(5)
            continue

        try:
            while True:
                if ser.is_open and is_first_time_opened is not True:
                    is_first_time_opened = True
                    print(f'Serial port {port_name} is open')
                    ser.write("<ENQ>")
                    reply = ser.in_waiting
                    while reply == 0:
                        data_raw = ser.read(ser.in_waiting)
                        time.sleep(0.5)
                # print(f'Bytes waiting in buffer: {ser.in_waiting}')

                if data_raw:
                    ser.write("<STX>1...Data...<CR><ETX>xx<CR><LF>")
                    reply = ser.read(ser.in_waiting)
                    while reply == 0:
                        data_raw = ser.read(ser.in_waiting)
                        time.sleep(0.5)


                    # print("Data received")

                    # JANGAN DIHAPUS
                    # ===============================================
                    # print("Converting data")
                    # print(f"Received data raw: {data_raw}")
                    #     PROCESS DATA RAW DISINI
                    # print(type(data_raw))
                    # converted_data = convert.convert_hexa_to_ascii(data_raw)
                    # print(converted_data)
                    # print("Data has converted")
                    # print("Mining Data")
                    # print("==========================================================")
                    # print("Data mined")
                    # agd.ini_main(converted_data=converted_data)
                    # exias.ini_main(converted_data)
                    # wondfobga.ini_main(converted_data)
                    # xn1000.ini_main(converted_data)
                    # promed.ini_main(converted_data)
                    # U500Insight.ini_main(converted_data)
                    # ================================================
                else:
                    print(f"No data")

                # Explicitly check if the port is still connected
                ports = [port.device for port in serial.tools.list_ports.comports()]
                if port_name not in ports:
                    print(f'Serial port {port_name} has been disconnected')
                    is_first_time_opened = False
                    break

                # Wait 2 seconds
                time.sleep(2)

        except KeyboardInterrupt:
            print("Stopped by User")
            ser.close()
            is_first_time_opened = False
            sys.exit(0)

        finally:
            if ser.is_open:
                ser.close()
                is_first_time_opened = False
                print('Serial port closed')

def checking_device(sn_used_port):
    """Check for a device with a specific serial number and open its port."""
    while True:
        ports = serial.tools.list_ports.comports()
        for port in ports:
            print(f"Checking port: {port.device}, Serial: {port.serial_number}")
            if port.device == sn_used_port:
                checking_port(port.device)

        print(f"Device with serial number {sn_used_port} not detected. Checking again in 5 seconds...")
        print_countdown(5)

def print_countdown(seconds):
    """Print a countdown for the given number of seconds."""
    for i in range(seconds, 0, -1):
        print(f"{i}...")
        time.sleep(1)

if __name__ == '__main__':
    # SN_USED_PORT = "EBCME11BS13"
    DEVICE_PORT = "COM1"
    try:
        checking_device(DEVICE_PORT)
    except Exception as e:
        print(f'Error: {e}')