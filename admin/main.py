import sys
from PyQt5.QtWidgets import QApplication
from ui.admin_panel import AdminPanel
from services.server_service import ServerService

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Создание службы сервера
    server_service = ServerService()

    # Создание интерфейса
    window = AdminPanel(server_service)
    window.show()

    sys.exit(app.exec_())
