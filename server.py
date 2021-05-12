import socket
import threading

host = '127.0.0.1'
port = 59002

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((host,port))
#maximun 100 people in the chat room
server.listen(100)
# client list allthe client are stored in the client list 
clients = []
# nick name of the client
nick_names = []
# the server sending messages to the client by broadcast method
def broadcast(message):
    for client in clients:
        client.send(message)
# to handle multiple client is the below function
def handle_client(client):
    while True:
        try:
            # the message recived from the client 
            message = client.recv(1024)
            broadcast(message)
        except:
            #if message failed to recieve that client should be remove
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nick_name = nick_names[index]
            broadcast(f'{nick_name} has left the chat room'.encode('utf-8'))
            nick_names.remove(nick_name)
            break
    
def receive():
    while True:
        print('server is rrunning and listening....')
        client , address = server.accept()
        print(f'connection is established with{str(address)}')
        client.send('nick_name?'.encode('utf-8'))
        nick_name = client.recv(1024)
        nick_names.append(nick_name)
        clients.append(client)
        print(f'the nick name of this client is {nick_name}'.encode('utf-8'))
        broadcast(f'{nick_name} has connected to chatroom'.encode('utf-8'))
        client.send('you are connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client,args=(client,))
        thread.start()

if __name__ == '__main__':
    receive()
        