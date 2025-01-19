import os
import socket
import threading
import logging
import configparser

# Create the logs directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Logging configuration
log_file = os.path.join(LOG_DIR, "server.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Read configuration
config = configparser.ConfigParser()
config.read('server_config.ini')

HOST = config.get('SERVER', 'HOST', fallback='127.0.0.1')
PORT = config.getint('SERVER', 'PORT', fallback=8888)
MAX_CONNECTIONS = config.getint('SERVER', 'MAX_CONNECTIONS', fallback=5)

class TCPServer:
    def __init__(self, host: str, port: int, max_connections: int):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.running = False

    def start(self):
        """Start the server"""
        self.running = True
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(self.max_connections)
            logging.info(f"Server started at {self.host}:{self.port}")
            print(f"Server started at {self.host}:{self.port}")

            while self.running:
                self.server_socket.settimeout(1.0)
                try:
                    client_socket, client_address = self.server_socket.accept()
                    logging.info(f"New connection from {client_address}")
                    print(f"New connection from {client_address}")
                    client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                    client_thread.start()
                    self.clients.append(client_thread)
                except socket.timeout:
                    continue
        except Exception as e:
            logging.error(f"Error: {e}")
        finally:
            self.server_socket.close()
            logging.info("Server stopped")

    def handle_client(self, client_socket, client_address):
        """Handle a connected client"""
        try:
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                logging.info(f"Received from {client_address}: {data}")
                print(f"Received from {client_address}: {data}")
                response = f"Server received: {data}"
                client_socket.sendall(response.encode('utf-8'))
                logging.info(f"Sent to client {client_address}: {response}")
        except Exception as e:
            logging.error(f"Error handling client {client_address}: {e}")
        finally:
            client_socket.close()
            logging.info(f"Connection with {client_address} closed")

    def stop(self):
        """Stop the server"""
        self.running = False
        for client in self.clients:
            client.join()
        self.server_socket.close()
        logging.info("Server properly stopped")
        print("Server properly stopped")

if __name__ == "__main__":
    server = TCPServer(HOST, PORT, MAX_CONNECTIONS)
    server.start()
