from server import TcpServer

class ServerService:
    def __init__(self):
        self.server = TcpServer()

    def start_server(self):
        self.server.start()

    def stop_server(self):
        self.server.stop()
