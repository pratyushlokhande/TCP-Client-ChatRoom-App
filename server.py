import socket
import threading

# Connection Data
host = 'localhost'
port = 9999

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Print a message
print("Server started.\nWaiting for connections.")

# Lists For Clients and Their Names
clients = []
client_name = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(bytes(message, 'utf-8'))


# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024).decode()
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = client_name[index]
            broadcast('{} left!'.format(nickname))
            client_name.remove(nickname)
            break


# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send(bytes('NAME', 'utf-8'))
        nickname = client.recv(1024).decode()
        client_name.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("{} joined the chatroom.".format(nickname))
        client.send(bytes('Connected to server!', 'utf-8'))
        broadcast("{} joined!".format(nickname))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


# receive 
receive()