# importando a biblioteca para uso de classes de dados
from dataclasses import dataclass

# importando biblioteca de sistema operacional
import os

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

@dataclass
class HTTPRequest:
  metodo: str
  rota: str
  protocolo: str

#iniciando e bindando o socket no endereço
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)

def create_response():
    if(HTTPRequest.metodo == 'GET'):
        try:
            with open(HTTPRequest.rota[1:], "rb") as file:
                html_content = file.read()

            # Criação da resposta HTTP
                status_line = b"HTTP/1.1 200 OK\r\n"
                content_type = b"Content-Type: text/html\r\n"
                response = status_line + content_type + b"\r\n" + html_content

        except FileNotFoundError:
            # Em caso de erro, retorna uma resposta 404
            status_line = b"HTTP/1.1 404 Not Found\r\n"
            content_type = b"Content-Type: text/html\r\n"
            not_found_content = b"<html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1></body></html>"
            response = status_line + content_type + b"\r\n" + not_found_content
    
    else:
            # Caso o método não seja suportado (HEAD, POST, PUT, DELETE, TRACE, OPTIONS e CONNECT) retorna uma resposta 405
            status_line = b"HTTP/1.1 405 Not Supported\r\n"
            content_type = b"Content-Type: text/html\r\n"
            not_supported_content = b"<html><head><title>405 Not Supported</title></head><body><h1>405 Not Supported</h1></body></html>"
            response = status_line + content_type + b"\r\n" + not_supported_content

    return response

#lida com as requisições do cliente
def handle_client(conn, addr):
    print(f"[CONNECTION] IP: {addr[0]}, Port: {addr[1]} connected.")
    connected = True
    while connected:
        msg_http = conn.recv(8190)
        msg_str = msg_http.decode('utf-8')
        linhas = msg_str.split('\r\n')
        HTTPRequest.metodo, HTTPRequest.rota, HTTPRequest.protocolo = linhas[0].split(' ')
        conn.send(create_response())
                           
    conn.close()
    print(f"[CONNECTION] IP: {addr[0]}, Port: {addr[1]} disconnected.")
 
def main():
    s.listen(5)
    print("Server is listening")
 
    while True:
        # estabelecida a conexão com o cliente
        conn, addr = s.accept()
        # inicia uma nova thread
        response_thread = threading.Thread(target=handle_client, name=f'Connection thread', args=(conn, addr))
        response_thread.start()
 
if __name__ == '__main__':
    main()