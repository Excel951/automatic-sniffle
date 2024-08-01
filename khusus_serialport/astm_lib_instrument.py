import serial
import astm

class InstrumentHost:
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port, baudrate, timeout=1)

    def send_record(self, record):
        try:
            record_str = str(record) if not isinstance(record, str) else record
            self.ser.write(record_str.encode())
            self.ser.flush()  # Ensure the data is sent
            response = self.ser.readline()
            if response:
                print(f'Received response: {response.decode()}')
        except serial.SerialException as e:
            print(f'Error communicating with the serial port: {e}')
        except Exception as e:
            print(f'Unexpected error: {e}')

    def instrument_host(self):
        try:
            self.send_record(astm.records.HeaderRecord())
            self.send_record(astm.records.PatientRecord(name={'last': 'foo', 'first': 'bar'}))
            self.send_record(astm.records.OrderRecord())
            self.send_record(astm.records.TerminatorRecord())
        except Exception as e:
            print(f'Error in sending records: {e}')
        finally:
            self.ser.close()

# Example instantiation and usage:
host = InstrumentHost('COM1', 9600)
host.instrument_host()
