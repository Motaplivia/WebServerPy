import socket
import os

host = '127.0.0.1'  #localhost
port = 8000  #número da porta

#criação do socket TCP
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_server.bind((host, port))
tcp_server.listen(1)
print(f'Servidor iniciado em http://{host}:{port}/')

while True:
    #aceita conexao do cliente
    connection_socket, address = tcp_server.accept()
    request = connection_socket.recv(1024).decode('utf-8')

    if not request:
        continue

    #extrai o caminho do arquivo solicitado
    file_requested = request.split()[1]

    if file_requested == '/':
        file_requested = '/index.html'

    try:
        #abre o arquivo
        with open('.' + file_requested, 'rb') as file:
            response_data = file.read()
        if file_requested.endswith('.jpg'):
            mimetype = 'image/jpeg'
        elif file_requested.endswith('.css'):
            mimetype = 'text/css'
        else:
            mimetype = 'text/html'
        
        response_headers = f'HTTP/1.1 200 OK\nContent-Type: {mimetype}\n\n'
        
    except FileNotFoundError:
        response_headers = 'HTTP/1.1 404 Not Found\nContent-Type: text/plain\n\n'
        response_data = b'404 Not Found'

    #envia os cabeçalhos e dados da resposta ao cliente
    response = response_headers.encode('utf-8') + response_data
    connection_socket.sendall(response)

    #fecha a conexão com o cliente
    connection_socket.close()

#fecha o socket do servidor
tcp_server.close()
