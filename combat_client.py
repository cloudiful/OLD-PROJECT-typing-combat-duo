import socket
import threading
import gamedata

PORT = 10086
SERVER = '192.168.43.254'
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))


# use header to prevent 'sticky' package
def send(message):
    msg = message.encode(FORMAT)
    message_length = len(msg)
    send_length = str(message_length).encode(FORMAT)
    send_length += b' ' * (gamedata.HEADER - len(send_length))
    # print(send_length.decode(FORMAT))
    client.send(send_length)
    client.send(msg)


# always receiving server message
def receive():
    while True:
        try:
            # reverse steps from sending the message
            message_length = client.recv(gamedata.HEADER).decode(FORMAT)
            if message_length:
                message_length = int(message_length)
                message = client.recv(message_length).decode(FORMAT)
                print(message)
                # custom command
                if message[0:7] == '!index=':
                    gamedata.net_index = int(message[7:])
                elif message[0:7] == '!count=':
                    gamedata.client_count = int(message[7:])
                else:
                    gamedata.net_content = message
        except:
            print("An error occurred!")
            client.close()
            break


receive_thread = threading.Thread(target=receive)
receive_thread.start()
