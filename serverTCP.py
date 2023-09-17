# No servidor TCP (deve executar antes do cliente)
# Criar uma thread com a conexão do cliente (para cada cliente). Na thread:
# Receber requisições enviadas pelo cliente:
# “Sair”
# se sim: fechar a conexão.
# Finalizar a thread.
# “Arquivo” + NOME.EXT:
# Abrir o arquivo solicitado.
# Calcular o (Hash) do arquivo com SHA (Procure um exemplo de uso do SHA), que serve como verificador de integridade.
# Escolher a ordem/como enviar (Atenção! Este será o seu protocolo, você define.)
# Nome do arquivo
# Tamanho
# Hash
# Dados
# Status (ok, nok, etc…)
# Ex.: arquivo inexistente.
import hashlib
import os
# import socket programming library
import socket
 
# import thread module
from _thread import *
import threading
 
print_lock = threading.Lock()
 
# thread function
def threaded(c):
    while True:
 
        # data received from client
        data = c.recv(1024)
        data = data.decode('ascii')
        print(data)
        if not data:
            print('Bye')
             
            # lock released on exit
            print_lock.release()
            break
            
        if data == 'Sair':
            print('Conexao fechada')
            print_lock.release()
            break

        elif data.startswith('Arquivo'):
            fileName = data[8:]
            fileSize = str(os.path.getsize(fileName))
            try:
                sha256_hash = hashlib.sha256()
                with open(fileName, 'rb') as file:
                    content = file.read().decode('ascii')
                    file.seek(0)
                    for bloco in iter(lambda: file.read(4096), b""):
                        sha256_hash.update(bloco)
                        hash_hex = str(sha256_hash.hexdigest())

                data = "Nome : " + fileName + '\n'
                data += "Tamanho : " + fileSize + '\n'
                data += "Hash : " + hash_hex + '\n'
                data += "Conteudo : " + content + '\n'
                data += "Status : " + 'ok'
            
            except FileNotFoundError:
                status = 'fnf'
            except Exception as e:
                print(f"Ocorreu um erro com o arquivo: {str(e)}")
        
        c.send(data.encode('ascii'))
 
    # connection closed
    c.close()
 
 
def Main():
    host = ""
 
    # reserve a port on your computer
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
 
    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")
 
    # a forever loop until client wants to exit
    while True:
 
        # establish connection with client
        c, addr = s.accept()
 
        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
 
        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()
 
 
if __name__ == '__main__':
    Main()