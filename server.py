import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []

def broadcast(message, sender_client=None):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except:
            pass

def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                index = clients.index(client)
                username = usernames[index]
                broadcast(f"{username}: {message}", sender_client=client)
        except:
            index = clients.index(client)
            client.close()
            username = usernames.pop(index)
            clients.remove(client)
            broadcast(f'{username} left the chat.')
            break

def receive_connections():
    print(f'Server is running on {HOST}:{PORT}...')
    while True:
        client, address = server.accept()
        print(f'Connected with {address}')

        client.send('USERNAME'.encode('utf-8'))
        username = client.recv(1024).decode('utf-8')
        usernames.append(username)
        clients.append(client)

        print(f'Username of the client is {username}')
        broadcast(f'{username} joined the chat!')
        client.send('Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive_connections()
