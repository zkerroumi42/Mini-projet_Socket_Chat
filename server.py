import socket,select
port = 12345
socket_list = []
users = {}

import sqlite3
HOST=socket.gethostbyname(socket.gethostname())
db = sqlite3.connect('db.sqlite3')

cursor = db.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        pseudo varchar(50) ,
        nom varchar(50),
        prenom varchar(50),
        password varchar(50),
        id INTEGER PRIMARY KEY AUTOINCREMENT
    )
''')
currF = db.cursor()
currF.execute('''
   CREATE TABLE IF NOT EXISTS friends(
        usr1_pseuo VARCHAR(50),
        usr2_pseuo VARCHAR(50),
        id_F INTEGER PRIMARY KEY AUTOINCREMENT
        )
''') 

db.commit()
currB = db.cursor()
currB.execute('''
   CREATE TABLE IF NOT EXISTS blocks(
        usr1_pseuo VARCHAR(50),
        usr2_pseuo VARCHAR(50),
        id_B INTEGER PRIMARY KEY AUTOINCREMENT
        )
''') 
db.commit()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST,port))
server_socket.listen()
print(HOST)
socket_list.append(server_socket)



while True:
    ready_to_read,ready_to_write,in_error = select.select(socket_list,[],[],0)
    for sock in ready_to_read:
        if sock == server_socket:
            connect, addr = server_socket.accept()
            socket_list.append(connect)
            connect.send(("You are connected from:" + str(addr)).encode('utf-8'))  
        else:
            try:
                data = sock.recv(2048).decode('utf-8')
                if data.startswith("#"):
                    pseudo=data[1:]
                    cu1=db.cursor()
                    cu1.execute("select pseudo from users")
                    user1 = cu1.fetchall()
                    for us in user1:
                        if pseudo==us[0]:
                            connect.send(("entrer votre mot de passe : ").encode('utf-8'))
                            passwo=sock.recv(2048).decode('utf-8')
                            cu2=db.cursor()
                            cu2.execute("select password from users where pseudo=?",(pseudo,))
                            pssw=cu2.fetchone()
                            if(passwo==pssw[0]):
                                users[pseudo.lower()]=connect
                                print ("l'utilisateur " + pseudo +" connecté.")
                                connect.send(("Bienvenue : "+str(data[1:])).encode('utf-8'))
                        else: 
                            pass
                elif data.startswith("@"):
                    users[data[1:data.index(':')].lower()].send((data[data.index(':')+1:]).encode('utf-8'))
                elif data.startswith("%"):
                    pseudo0=data[1:data.index(':')]
                    pseudo1=data[data.index(':')+1:]
                    print("old :"+pseudo0)
                    print("new :"+pseudo1)
                    cur4=db.cursor()
                    cur4.execute("select id from users where pseudo=?",(pseudo0,))
                    idd=cur4.fetchone()
                    print(idd[0])
                    cur3=db.cursor()
                    cur3.execute("UPDATE users SET pseudo =? where id =? ", (pseudo1,idd[0],))
                    db.commit()
                    connect.send(("Votre nouveau pseudo : "+pseudo1).encode('utf-8'))
                elif data.startswith("*"):
                    for user in users:
                        users[user].send(("Broadcast: "+str(data[1:])).encode('utf-8'))
                elif data.startswith("/"):
                    print(pseudo)
                    lista=""
                    for user in users:
                        lista+=" "+user
                    print("liste utilisateurs connectes : "+str(lista))
                    connect.send(("Utilisateurs connectes :"+lista).encode('utf-8'))
                elif data.startswith("+"):
                    usr1=data[1:data.index(':')]
                    usr2=data[data.index(':')+1:]
                    curaa=db.cursor()
                    curaa.execute('''INSERT INTO friends(usr1_pseuo,usr2_pseuo) 
                    VALUES(?,?)''',(usr1,usr2,))
                    db.commit()
                elif data.startswith("-"):
                    usr1=data[1:data.index(':')]
                    usr2=data[data.index(':')+1:]
                    curaa=db.cursor()
                    curaa.execute('''INSERT INTO blocks(usr1_pseuo,usr2_pseuo) 
                    VALUES(?,?)''',(usr1,usr2,))
                    db.commit()
            except:
                continue
server_socket.close()
