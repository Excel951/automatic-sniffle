import socket

HOST = '127.0.0.1'
PORT = 3020
ENQ = [0x05] # ENQUIRY
ACK = [0x06] # ACKNOWLEDGE
EOT = [0x04] # END OF TEXT
LF = [0x0A] # LINE FEED

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print(f"Server listening on {HOST}:{PORT}")

    conn, addr = s.accept()

    with conn:
        print(f'Connected by: {addr}')

        while True:
            data = conn.recv(1024)
            if not data:
                break

            # if data[0] == ord('S'):  # Cek jika dimulai dengan 'S'
            #     data = data[1:-1]  # Hapus 'S' dan newline
            # print(f"Data diterima: {data}")
            # conn.sendall(b'R')
            if bytes(ENQ) == data:
                print('RX ENQ')
                conn.sendall(bytes(ACK))
            elif bytes(EOT) == data:
                print('RX EOT')
                conn.sendall(bytes(ACK))
            elif bytes(ACK) == data:
                print('RX ACK')
                conn.sendall(bytes(EOT))
            elif bytes(LF) == data:
                print('RX LF')
                conn.sendall(bytes(ACK))
            else:
                print(f'Data diterima: {data}')

    conn.close()
