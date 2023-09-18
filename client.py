# importando biblioteca de socket
import socket
import pickle
import os
import hashlib

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
        
        message = input('\nDeseja (Sair), abrir o (Chat) ou envie um (NomeArquivo.ext) para ver as opções: ')
        # mensagem enviada para o servidor
        info = {}
        info['process'] = "arquivo" # inicializa como arquivo por padrao
        if message.lower() == "sair":
            info['process'] = "sair"
        elif message.lower() == "chat":
            info['process'] = "chat"
            continuar = True
            while continuar: # enquanto nao for digitado sair do chat, mantém no loop
                message = input('Digite sua mensagem: ')
                info['message'] = message
                s.send(pickle_format(info))

                data = s.recv(1024)
                data = pickle.loads(data[HEADERSIZE:])

                if message.lower() == 'sair do chat' or data['status'] == 'ChatEnd':
                    continuar = False
                    break

                if data['status'] == 'Chat':
                    print("Servidor: " + data['message'])
        else:
            info['file'] = message     
             
        s.send(pickle_format(info))
 
        # mensagem recebida do servidor
        data = s.recv(1024)
        data = pickle.loads(data[HEADERSIZE:])

        # se o status esta ok, printa arquivo
        if data['status'] == 'OK':
            message = input("digite (info) para ler o arquivo ou (baixar):")
            if message.lower() == "info":
                    print(f"File name : {data['file']} \nStatus: {data['status']} \nFile size: {data['fileSize']} \nHash: {data['hash']} \nContent: {data['content']}")
            elif message.lower() =="baixar":
                try:
                    filename, filext = os.path.splitext(data['file'])
                    file_name = filename + "Download" + filext
                    file_content = data['content']
                    with open(file_name, 'wb') as file:
                        file.write(file_content.encode('utf-8'))
                        print(f"Arquivo '{file_name}' baixado com sucesso.")
                except Exception as e:
                    print(f"Erro ao salvar o arquivo: {e}")
                sha256_hash = hashlib.sha256() # define o hash
                with open(file_name, 'rb') as file: # abre como binario
                    for bloco in iter(lambda: file.read(4096), b""): # itera pelo arquivo pra fazer o hash
                        sha256_hash.update(bloco)
                        newFileHash = str(sha256_hash.hexdigest())
                print("Verificando Hash")
                if newFileHash == data['hash']:
                    print(f"\nHash Download: {newFileHash}\nHash Server: {data['hash']}\n")
                    print("\nHash Igual\n")
                else:
                    print("\nHash diferente, erro ao baixar arquivo\n")

        elif data['status'] == 'Close':
            break
            
    s.close()
        
if __name__ == '__main__':
    main()