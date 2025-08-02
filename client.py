import sys
import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

username = ""

def receive_messages():
    global username
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'USERNAME':
                username = input('Enter your username: ')
                client.send(username.encode('utf-8'))
            elif message.startswith(f"{username}:"):
                content = message[len(username) + 1:].strip()
                print(f"You: {content}")
            else:
                print(message)
        except:
            print('An error occurred. Disconnected from server.')
            client.close()
            break

# Removing the input prompt for sending messages
def send_messages():
    while True:
        message = input('')
        sys.stdout.write('\033[F\033[K')
        sys.stdout.flush()
        client.send(message.encode('utf-8'))


recv_thread = threading.Thread(target=receive_messages)
recv_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
