# importando biblioteca de socket
import socket
 
 
def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'
 
    # porta definida
    port = 12345
 
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 
    # conectar no server do computador local
    s.connect((host,port))
 
    while True:
 
        message = input('\nDeseja (Sair) ou ler um (Arquivo NOME.EXT) :')
        # mensagem enviada para o servidor
        s.send(message.encode('ascii'))
 
        # mensagem recebida do servidor
        data = s.recv(1024)
 
        # printa a mensagem recebida
        print('Received from the server :', str(data.decode('ascii')))

    # fecha a conexão
    s.close()
 
if __name__ == '__main__':
    Main()