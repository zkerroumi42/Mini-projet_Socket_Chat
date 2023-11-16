import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12345
HOST=socket.gethostbyname(socket.gethostname())
client_socket.connect((HOST,port))

#recieve connection message from server
recv_msg = client_socket.recv(1024) 
print(recv_msg)

#send user details to server
send_msg = input("Entrer votre Pseuodonyme (prefix avec #):")

client_socket.send(send_msg.encode('utf-8'))
pseudo=send_msg[1:]

#receive and send message from/to different user/s

while True:
    recv_msg = client_socket.recv(1024).decode('utf-8')
    print (recv_msg)
    send_msg = input('''\t\t\tPour envoyer un message privé [@user:message]\n\t\t\tPour envoyer un message par diffusion (prefix avec *)\n\t\t\tPour changer votre pseudo [%ancienne_pseu:nouv_pseu]\n\t\t\tPour lister les utilisateurs connectes envoyer/\n\t\t\tPour ajouter unutilisateur commz ami [+votre_pseu:utilisateur_pseu]\n\t\t\tPour bloquer un utilisateur [+votre_pseu:utilisateur_pseu]\n\t\t\tautre sans prefix\n''')
    if send_msg == 'exit':
        break;
    else:
        client_socket.send(send_msg.encode('utf-8'))

client_socket.close()