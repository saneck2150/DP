import socket
import threading

class TcpServer:
    def __init__(self, host="127.0.0.1", port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.clients = []
        self.running = False

    def start(self):
        """Запуск сервера."""
        self.running = True
        print("Сервер запущен.")
        threading.Thread(target=self.accept_clients, daemon=True).start()

    def stop(self):
        """Остановка сервера."""
        self.running = False
        self.server_socket.close()
        print("Сервер остановлен.")

    def accept_clients(self):
        """Приём клиентов."""
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                self.clients.append((client_socket, client_address))
                print(f"Подключен клиент: {client_address}")
                threading.Thread(target=self.handle_client, args=(client_socket, client_address), daemon=True).start()
            except Exception as e:
                print(f"Ошибка: {e}")
                break

    def handle_client(self, client_socket, client_address):
        """Обработка данных от клиента."""
        while self.running:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Сообщение от {client_address}: {data.decode()}")
            except Exception as e:
                print(f"Ошибка с клиентом {client_address}: {e}")
                break
        client_socket.close()
        self.clients.remove((client_socket, client_address))

if __name__ == "__main__":
    server = TcpServer()
    server.start()
    input("Нажмите Enter для остановки сервера...\n")
    server.stop()
