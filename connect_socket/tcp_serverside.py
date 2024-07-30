# import socket
#
# HOST = '127.0.0.1'
# PORT = 3020
#
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by', addr)
#         while True:
#             data = conn.recv(1024)
#             if not data:
#                 break
#             conn.sendall(data)

import socket

def handle_data(data):
    ENQ = b'\x05'
    ACK = b'\x06'
    EOT = b'\x04'
    LF = b'\x0A'
    for byte in data:
        if byte == ENQ:
            print('RX ENQ')
            s.send(ACK)
        elif byte == EOT:
            print('RX EOT')
            s.send(ACK)
        elif byte == ACK:
            print('RX ACK')
            s.send(EOT)
        elif byte == LF:
            print('RX LF')
            s.send(ACK)

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 3020

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print(f'Server is listening on {HOST}:{PORT}')

        try:
            while True:
                conn, addr = s.accept()

                print(f'New connection from: {addr}')

                with conn:
                    print('Connected by', addr)
                    data = conn.recv(1024)
                    handle_data(data)
                    print(data)
        except Exception as e:
            print(e)
            s.close()

        except KeyboardInterrupt:
            s.close()