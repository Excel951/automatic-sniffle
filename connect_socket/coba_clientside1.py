import socket

HOST = '127.0.0.1'
PORT = 3020

STX = [0x02]  # Frame start delimiter
ETX = [0x03]  # Frame end delimiter
ENQ = [0x05] # ENQUIRY
ACK = [0x06] # ACKNOWLEDGE
EOT = [0x04] # END OF TEXT
LF = [0x0A] # LINE FEED

data_send = b"0b4d53487c5e7e5c267c4143203631307c48656d61746f6c6f677920416e616c797a65727c7c7c32303234303631333134333731392e303139357c7c4f52555e5230317c32337c507c322e332e310d5049447c317c7c5e5e5e5e574d7c7c5e53554c49535449594f7c7c32303031303130313030303030307c0d5056317c317c4f757470617469656e742049447c7c7c7c7c7c7c7c7c7c7c7c7c7c7c7c7c7c4f776e20657870656e73650d4f42527c317c7c323032343035323130337c30303030315e4175746f6d6174656420436f756e745e39394d52437c7c32303234303532393131303430307c32303234303532393131303330387c7c7c7c7c7c7c32303234303532393131303430307c424c44567c7c7c7c7c7c7c7c7c484d7c7c7c7c61646d696e7c7c7c7c61646d696e0d4f42587c317c49537c30383030325e426c6f6f64204d6f64655e39394d52437c7c577c7c7c7c7c7c467c7c0d4f42587c327c49537c30383030335e54657374204d6f64655e39394d52437c7c4342432b444946467c7c7c7c7c7c467c7c0d4f42587c337c4e4d7c33303532352d305e4167655e4c4e7c7c307c79727c7c7c7c7c467c7c0d4f42587c347c53547c30313030315e52656d61726b5e39394d52437c7c7c7c7c7c7c7c467c7c0d4f42587c357c49537c30313030325e5265662047726f75705e39394d52437c7c47656e6572616c7c7c7c7c7c7c467c7c0d4f42587c367c49537c30313030335e426564204e6f5e39394d52437c7c7c7c7c7c7c7c467c7c0d4f42587c377c49537c30313030342d315e437573746f6d697a6564315e39394d52437c7c437573746f6d697a656420317c7c7c7c7c7c467c7c0d4f42587c387c49537c30313030342d325e437573746f6d697a6564325e39394d52437c7c437573746f6d697a656420327c7c7c7c7c7c467c7c0d4f42587c397c49537c30313030342d335e437573746f6d697a6564335e39394d52437c7c437573746f6d697a656420337c7c7c7c7c7c467c7c0d4f42587c31307c4e4d7c363639302d325e5742435e4c4e7c7c392e34337c31302a332f754c7c342e30302d31302e30305e345e31305e312e357c7c7c7c467c7c0d4f42587c31317c4e4d7c3737302d385e4e4555255e4c4e7c7c38322e347c257c35302e302d37302e305e35305e37305e312e357c487c7c7c467c7c0d4f42587c31327c4e4d7c3733362d395e4c594d255e4c4e7c7c382e307c257c31382e302d34322e305e31385e34325e312e357c4c7c7c7c467c7c0d4f42587c31337c4e4d7c353930352d355e4d4f4e255e4c4e7c7c382e337c257c322e302d31312e305e325e31315e312e357c7c7c7c467c7c0d4f42587c31347c4e4d7c3731332d385e454f53255e4c4e7c7c302e357c257c312e302d332e305e315e335e312e357c4c7c7c7c467c7c0d4f42587c31357c4e4d7c3730362d325e424153255e4c4e7c7c302e387c257c302e302d312e305e305e315e312e357c7c7c7c467c7c0d4f42587c31367c4e4d7c3735312d385e4e4555235e4c4e7c7c372e37347c31302a332f754c7c322e30302d372e30305e325e375e312e357c487c7c7c467c7c0d4f42587c31377c4e4d7c3733312d305e4c594d235e4c4e7c7c302e37357c31302a332f754c7c302e38302d342e30305e302e385e345e312e357c4c7c7c7c467c7c0d4f42587c31387c4e4d7c3734322d375e4d4f4e235e4c4e7c7c302e37387c31302a332f754c7c302e31322d312e32305e302e31325e312e325e312e357c7c7c7c467c7c0d4f42587c31397c4e4d7c3731312d325e454f53235e4c4e7c7c302e30357c31302a332f754c7c302e30322d302e35305e302e30325e302e355e312e357c7c7c7c467c7c0d4f42587c32307c4e4d7c3730342d375e424153235e4c4e7c7c302e31317c31302a332f754c7c302e30302d302e31305e305e302e315e312e357c487c7c7c467c7c0d4f42587c32317c4e4d7c3738392d385e5242435e4c4e7c7c352e35367c31302a362f754c7c332e35302d352e35305e332e355e352e355e312e357c487c7c7c467c7c0d4f42587c32327c4e4d7c3731382d375e4847425e4c4e7c7c31372e327c672f644c7c31312e302d31362e305e31315e31365e312e357c487c7c7c467c7c0d4f42587c32337c4e4d7c3738362d345e4d4348435e4c4e7c7c33382e347c672f644c7c33322e302d3336312e305e33325e3336315e312e357c7c7c7c467c7c0d4f42587c32347c4e4d7c3738352d365e4d43485e4c4e7c7c33302e397c70677c32372e302d33342e305e32375e33345e312e357c7c7c7c467c7c0d4f42587c32357c4e4d7c3738372d325e4d43565e4c4e7c7c38302e347c664c7c38302e302d3130302e305e38305e3130305e312e357c7c7c7c467c7c0d4f42587c32367c4e4d7c3738382d305e5244572d43565e4c4e7c7c31332e307c257c31312e302d31362e305e31315e31365e312e357c7c7c7c467c7c0d4f42587c32377c4e4d7c32313030302d355e5244572d53445e4c4e7c7c34302e387c664c7c33352e302d35362e305e33355e35365e312e357c7c7c7c467c7c0d4f42587c32387c4e4d7c343534342d335e4843545e4c4e7c7c34342e377c257c33372e302d35342e305e33375e35345e312e357c7c7c7c467c7c0d4f42587c32397c4e4d7c3737372d335e504c545e4c4e7c7c34317c31302a332f754c7c3135302d3430305e3135305e3430305e312e357c4c7c7c7c467c7c0d4f42587c33307c4e4d7c33323632332d315e4d50565e4c4e7c7c32342e367c664c7c362e352d31322e305e362e355e31325e312e357c487c7c7c467c7c0d4f42587c33317c4e4d7c33323230372d335e5044575e4c4e7c7c312e307c664c7c392e302d31372e305e395e31375e312e357c4c7c7c7c467c7c0d4f42587c33327c4e4d7c31303030325e5043545e39394d52437c7c302e3130317c257c302e3131302d302e3238305e302e31315e302e32385e312e357c4c7c7c7c467c7c0d4f42587c33337c4e4d7c31303031335e504c43435e39394d52437c7c33342e37387c31302a332f754c7c33302e30302d39302e30305e33305e39305e312e357c7c7c7c467c7c0d4f42587c33347c4e4d7c31303031345e504c43525e39394d52437c7c38357c257c31312d34355e31315e34355e312e357c487c7c7c467c7c0d4f42587c33357c4e4d7c31333034362d385e2a414c59255e4c4e7c7c302e317c257c302e302d322e305e305e325e312e357c7c7c7c467c7c0d4f42587c33367c4e4d7c32363437372d305e2a414c59235e4c4e7c7c302e327c257c302e302d322e355e305e322e355e312e357c7c7c7c467c7c0d4f42587c33377c4e4d7c31303030315e2a4c4943255e39394d52437c7c302e30317c31302a332f754c7c302e30302d302e32305e305e302e325e312e357c7c7c7c467c7c0d4f42587c33387c4e4d7c31303030305e2a4c4943235e39394d52437c7c302e30327c31302a332f754c7c302e30302d302e32355e305e302e32355e312e357c7c7c7c467c7c0d4f42587c33397c49537c31323031355ee7baa2e7bb86e8839ee8819ae99b863f5e39394d52437c7c547c327c7c7c7c7c460d4f42587c34307c49537c31323030375ee6b78be5b7b4e7bb86e8839ee5878fe5b0915e39394d52437c7c547c317c7c7c7c7c460d4f42587c34317c49537c31323031385ee8a180e5b08fe69dbfe5878fe5b0915e39394d52437c7c547c337c7c7c7c7c460d1c0d"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
        print('Connected on {}:{}'.format(HOST, PORT))

        for chunk in [data_send[i:i+2] for i in range(0, len(data_send), 2)]:
            # frame = create_frame(chunk)
            print(f'Sending frame: {chunk}')
            s.sendall(chunk)

            # Receive acknowledgement
            res = s.recv(1024)
            if not res:
                break
            # if res == b'R':
            #     print('Acknowledgement error')
                # Handle retransmission or error
            if ENQ == res:
                print('RX ENQ')
                s.sendall(ACK)
            elif EOT == res:
                print('RX EOT')
                s.sendall(ACK)
            elif ACK == res:
                print('RX ACK')
                s.sendall(EOT)
            elif LF == res:
                print('RX LF')
                s.sendall(ACK)
            else:
                print(f'Data diterima: {res}')

    except Exception as e:
        print(e)

    print("Disconnected from server")
    s.close()
