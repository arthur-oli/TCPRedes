# importando biblioteca de hash
import hashlib

# importando biblioteca de sistema operacional, para ver o tamanho do arquivo
import os

# importando biblioteca de tratamento de mensagens
import pickle

# importando biblioteca de socket
import socket
 
# importando multithreading
from _thread import *
import threading
 
# formato das mensagens, porta, ip do servidor, endereço e headersize para o pickle
FORMAT = 'utf-8' 
PORT = 12345
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
HEADERSIZE = 10

# iniciando e bindando o socket no endereço
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)

# definindo o jeito que o pickle armazena mensagens
def pickle_format(info):
    msg = pickle.dumps(info)
    return bytes(f'{len(msg):<{HEADERSIZE}}', FORMAT) + msg

# parte central do programa, tratamento de mensagens pelo servidor, Chat, Sair ou Arquivo
def handle_info(info, conn):
    if info['process'] == 'chat': # se é o chat o escolhido
        info['status'] = 'Chat'
        if info['message'].lower() == 'sair do chat':
            info['status'] = 'ChatEnd'
            p = pickle_format(info)
            conn.send(p)
        
        else:
            print("Cliente: " + info['message'])
            info['message'] = input('Digite sua mensagem: ') # pede a mensagem pro server
            if info['message'].lower() == 'sair do chat':
                info['status'] = 'ChatEnd'
            p = pickle_format(info)
            conn.send(p)

        return True

    if info['process'] == 'sair': # se sair
        info['status'] = 'Close' # muda status e fecha
        p = pickle_format(info)
        conn.send(p)

        return False
    
    elif info['process'] == 'arquivo': # se arquivo
        status = 'OK'

        try:
            sha256_hash = hashlib.sha256() # define o hash
            info['fileSize'] = str(os.path.getsize(info['file'])) # tamanho do arquivo
            with open(info['file'], 'rb') as file: # abre como binario
                info['content'] = file.read().decode('ascii') # le o conteudo
                file.seek(0) # volta pro inicio
                for bloco in iter(lambda: file.read(4096), b""): # itera pelo arquivo pra fazer o hash
                    sha256_hash.update(bloco)
                    info['hash'] = str(sha256_hash.hexdigest())
        except Exception as e: # se der problema, status vira NOK
            status = 'NOK'

        info['status'] = status
        p = pickle_format(info)
        conn.send(p)

        return True
        
# lida com as mensagens do cliente
def handle_client(conn, addr):
    print(f"[CONNECTION] IP: {addr[0]}, Port: {addr[1]} connected.")

    full_msg = b''
    new_msg = True

    connected = True
    while connected:
        msg = conn.recv(1024)
        if msg != b'':
            if new_msg:
                msglen = int(msg[:HEADERSIZE])
                new_msg = False

            full_msg += msg

            if len(full_msg) - HEADERSIZE == msglen:
                info = pickle.loads(full_msg[HEADERSIZE:])
                new_msg = True
                full_msg = b''
                connected = handle_info(info, conn)
                    
            
    conn.close()
    print(f"[CONNECTION] IP: {addr[0]}, Port: {addr[1]} disconnected.")
 
 
def main():
    s.listen(5)
    print("Server is listening")
 
    while True:
 
        # estabelecida a conexão com o cliente
        c, addr = s.accept()
 
        # inicia uma nova thread
        response_thread = threading.Thread(target=handle_client, name=f'Connection thread',args=(c, addr))
        response_thread.start()
 
 
if __name__ == '__main__':
    main()