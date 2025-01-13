from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QTextEdit, QLabel

class AdminPanel(QMainWindow):
    def __init__(self, server_service):
        super().__init__()
        self.setWindowTitle("Админ Панель - Система Пропусков")
        self.setGeometry(100, 100, 800, 600)
        self.server_service = server_service

        self.initUI()

    def initUI(self):
        # Основной виджет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Основной layout
        layout = QVBoxLayout()

        # Лог окна
        self.log_label = QLabel("События сервера:", self)
        layout.addWidget(self.log_label)

        self.log_window = QTextEdit(self)
        self.log_window.setReadOnly(True)
        layout.addWidget(self.log_window)

        # Кнопки управления сервером
        self.start_server_button = QPushButton("Запустить сервер", self)
        self.stop_server_button = QPushButton("Остановить сервер", self)
        layout.addWidget(self.start_server_button)
        layout.addWidget(self.stop_server_button)

        # Установка layout
        central_widget.setLayout(layout)

        # Сигналы
        self.start_server_button.clicked.connect(self.start_server)
        self.stop_server_button.clicked.connect(self.stop_server)

    def start_server(self):
        self.server_service.start_server()
        self.log_window.append("Сервер запущен.")

    def stop_server(self):
        self.server_service.stop_server()
        self.log_window.append("Сервер остановлен.")
