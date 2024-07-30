import socket

# HOST = '127.0.0.1'
# PORT = 3020
#
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b'Hello World')
#     data = s.recv(1024)
#
# print(f'Received {data}!')

def handle_data(data):
    ENQ = b'\x05'
    ACK = b'\x06'
    EOT = b'\x04'
    LF = b'\x0A'

    for byte in data:
        if byte == ENQ:
            print('RX ENQ')
            s.send(ACK)
        if byte == EOT:
            print('RX EOT')
            s.send(ENQ)
        if byte == ACK:
            print('RX ACK')
            s.send(EOT)
        if byte == LF:
            print('RX LF')
            s.send(ACK)

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 3020

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        print('CLIENT CONNECTED!')

        try:
            while True:
                # print("Tes")
                # conn, address = s.accept()
                # print("Tes1")
                # print(f'New connection from {address}')

                message = 'This is the message.  It will be repeated.'
                s.send(bytes(message, 'utf-8'))

                # Look for the response
                amount_received = 0
                amount_expected = len(message)

                while amount_received < amount_expected:
                    data = s.recv(16)
                    amount_received += len(data)
                    print(data)
                # with conn:
                #     print('Connected with {}'.format(address))
                #     data = conn.recv(1024)
                #     handle_data(data)
                #     print(data)
        except Exception as e:
            print(e)