# importando biblioteca de hash
import hashlib

#importando biblioteca de sistema operacional, para ver o tamanho do arquivo
import os

# importando biblioteca de socket
import socket
 
# importando multithreading
from _thread import *
import threading
 
print_lock = threading.Lock()
 
# thread
def threaded(c):
    while True:
 
        # dados recebidos do cliente
        data = c.recv(1024)
        data = data.decode('ascii')
        print(data)
        if not data:
            print('Bye')
             
            # liberando o travamento da thread
            print_lock.release()
            break
            
        if data == 'Sair':
            print('Conexao fechada')
            c.send(data.encode('ascii'))
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

                data = "\nNome : " + fileName + '\n'
                c.send(data.encode('ascii'))
                data = "Tamanho : " + fileSize + '\n'
                c.send(data.encode('ascii'))
                data = "Hash : " + hash_hex + '\n'
                c.send(data.encode('ascii'))
                data = "Conteudo : " + content + '\n'
                c.send(data.encode('ascii'))
                data = "Status : " + 'ok'
                c.send(data.encode('ascii'))
            
            except FileNotFoundError:
                status = 'nok'
            except Exception as e:
                print(f"Ocorreu um erro com o arquivo: {str(e)}")
        
        c.send(data.encode('ascii'))
 
    # fechando a conexão
    c.close()
 
 
def Main():
    host = ""
 
    # porta do computador (qualquer uma acima de 1024)
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
 
    # modo ouvinte para o socket
    s.listen(5)
    print("socket is listening")
 
    # loop infinito até a condição de parada
    while True:
 
        # estabelecida a conexão com o cliente
        c, addr = s.accept()
 
        # trava adquirida pelo cliente
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
 
        # inicia uma nova thread
        start_new_thread(threaded, (c,))
    s.close()
 
 
if __name__ == '__main__':
    Main()