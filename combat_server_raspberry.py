import socket
import threading

FORMAT = 'utf-8'
HEADER = 64
HOST = '192.168.43.254'
PORT = 10086

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

# list for every clients
clients = []


# use header to prevent 'sticky' package
def send(client, message):
    # encode str to bitstream
    msg = message.encode(FORMAT)
    message_length = len(msg)
    send_length = str(message_length).encode(FORMAT)
    # make this send_length HEADER total long (in this case 64)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(msg)


def send_all(message):
    for client in clients:
        # msg = message.encode(FORMAT)
        # message_length = len(msg)
        # send_length = str(message_length).encode(FORMAT)
        # send_length += b' ' * (HEADER - len(send_length))
        # client.send(send_length)
        # client.send(msg)
        send(client, message)


# handle individual client
def handle_client(client, address):
    connected = True
    while connected:
        try:
            # reverse steps from sending the message
            message_length = client.recv(HEADER).decode(FORMAT)
            if message_length:
                message_length = int(message_length)
                message = client.recv(message_length).decode(FORMAT)
                print(message)
                # custom command
                if message == "!disconnect":
                    connected = False
                elif message == '!index':
                    send(client, '!index=' + str(clients.index(client)))
                elif message == '!count':
                    send(client, '!count=' + str(len(clients)))
                elif message == '!win':
                    send_all('!win')
                else:
                    message = str(clients.index(client)) + '-' + message
                    send_all(message)
        except:
            # Removing And Closing Clients
            clients.remove(client)
            client.close()
            break

    client.close()


# listen client requests
def receive():
    server.listen(2)  # max user number
    while True:
        client, address = server.accept()
        clients.append(client)
        thread = threading.Thread(target=handle_client, args=(client, address))
        thread.start()


print("Server started...")
receive()
