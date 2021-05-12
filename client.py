import threading 
import socket

nick_name = input('choose any name  : ')
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host = '127.0.0.1'
port = 59002

client.connect((host,port))

def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "nick_name?":
                client.send(nick_name.encode('utf-8'))
            else:
                print(message)
        except:
            print('ERROR')
            client.close()
            break

def client_send():
    while True:
        message = f'{nick_name}:{input()}'
        client.send(message.encode('utf-8'))
        
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()