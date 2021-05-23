import socket
import threading
import sqlite3
import traceback
import sys
#create a database

db = sqlite3.connect("chatroom.sqlite",check_same_thread=False)


cursor = db.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS client(name Text , chat Text)")


host = '127.0.0.1'
port = 59008

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
            decode_message = message.decode("utf-8")
            index = clients.index(client)
            nick_name = nick_names[index]
            broadcast(message)
            try:
                sql_query = "INSERT INTO client VALUES(?,?)" 
                sql_data = (nick_name,decode_message)
                cursor.execute(sql_query,sql_data)
                db.commit()
            except sqlite3.Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print("Exception class is: ", er.__class__)
                print('SQLite traceback: ')
                exc_type, exc_value, exc_tb = sys.exc_info()
                print(traceback.format_exception(exc_type, exc_value, exc_tb))
                db.rollback()
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
        print('server is running and listening....')
        client , address = server.accept()
        print(f'connection is established with{str(address)}')
        # server requesting client nick name from the client this works internaaly
        client.send('nick_name?'.encode('utf-8'))
        # server recives the nick name from the client and stored in the variable
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
        
        
