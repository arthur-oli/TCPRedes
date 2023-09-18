# importando biblioteca de socket
import socket
import pickle

# formato das mensagens, porta, ip do servidor, endereço e headersize para o pickle
FORMAT = 'utf-8'
PORT = 12345
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
HEADERSIZE = 10

def pickle_format(info):
    msg = pickle.dumps(info)
    return bytes(f'{len(msg):<{HEADERSIZE}}', FORMAT) + msg
 
def main():
 
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 
    # conectar no server do computador local
    s.connect(ADDR)

    while True:
        
        message = input('\nDeseja (Sair), abrir o (Chat) ou ler um (NomeArquivo.ext):\n')
        # mensagem enviada para o servidor
        info = {}
        info['process'] = "arquivo" # inicializa como arquivo por padrao
        if message.lower() == "sair":
            info['process'] = "sair"
        elif message.lower() == "chat":
            info['process'] = "chat"
            message = input('Digite sua mensagem: ')
            while message.lower() != 'sair do chat': # enquanto nao for digitado sair do chat, mantém no loop
                info['message'] = message
                s.send(pickle_format(info))
                data = s.recv(1024)
                data = pickle.loads(data[HEADERSIZE:])
                if data['status'] == 'Chat':
                    print("Servidor: " + data['message'])
                message = input('Digite sua mensagem: ')

        else:
            info['file'] = message      

        s.send(pickle_format(info))
 
        # mensagem recebida do servidor
        data = s.recv(1024)
        data = pickle.loads(data[HEADERSIZE:])

        # se o status esta ok, printa arquivo
        if data['status'] == 'OK':
            print(f"File name : {data['file']} \nStatus: {data['status']} \nFile size: {data['fileSize']} \nHash: {data['hash']} \nContent: {data['content']}")
        elif data['status'] == 'Close':
            break
        else:
            print(data['status'])
            
    s.close()
        
if __name__ == '__main__':
    main()