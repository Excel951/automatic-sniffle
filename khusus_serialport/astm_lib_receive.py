import serial
import astm

class InstrumentReceiver:
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        self.buffer = ""

    def receive_data(self):
        try:
            while True:
                line = self.ser.readline()
                if not line:
                    break
                self.buffer += line.decode()
        except serial.SerialException as e:
            print(f'Error communicating with the serial port: {e}')
        except Exception as e:
            print(f'Unexpected error: {e}')
        finally:
            self.ser.close()

    def parse_record(self, line):
        # Simple example parsing function based on line prefix
        if line.startswith('H'):
            return astm.records.HeaderRecord()
        elif line.startswith('P'):
            return astm.records.PatientRecord()
        elif line.startswith('O'):
            return astm.records.OrderRecord()
        elif line.startswith('L'):
            return astm.records.TerminatorRecord()
        else:
            return None

    def process_records(self):
        try:
            for line in self.buffer.split('\n'):
                record = self.parse_record(line)
                if isinstance(record, astm.records.HeaderRecord):
                    print(f"Header Record: {record}")
                elif isinstance(record, astm.records.PatientRecord):
                    print(f"Patient Record: {record}")
                elif isinstance(record, astm.records.OrderRecord):
                    print(f"Order Record: {record}")
                elif isinstance(record, astm.records.TerminatorRecord):
                    print(f"Terminator Record: {record}")
                else:
                    print(f"Unknown Record: {line}")
        except Exception as e:
            print(f'Error processing records: {e}')

# Example instantiation and usage:
receiver = InstrumentReceiver('COM2', 9600)
receiver.receive_data()
receiver.process_records()
