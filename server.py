import socket

HOST = '127.0.0.1'  
PORT = 12345        

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Сервер запущен на {HOST}:{PORT}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Подключился клиент: {addr}")
        with client_socket:
            data = client_socket.recv(1024)
            if not data:
                break
            print("Считано от клиента:", data.decode('utf-8'))
