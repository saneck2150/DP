#include <iostream>
#include <string>
#include <cstring>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include "idCodeTypes.hpp"

int main()
{
    std::string codeFromCard = getId();

    // 1. Создаём сокет
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        std::cerr << "Ошибка: не удалось создать сокет\n";
        return 1;
    }

    // 2. Заполняем структуру для подключения к серверу
    struct sockaddr_in serverAddr;
    std::memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(12345); 

    // Преобразуем IP‑адрес 127.0.0.1 в нужный формат
    if (inet_pton(AF_INET, "127.0.0.1", &serverAddr.sin_addr) <= 0) {
        std::cerr << "Ошибка: некорректный IP‑адрес\n";
        close(sock);
        return 1;
    }

    // 3. Подключаемся к серверу
    if (connect(sock, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) < 0) {
        std::cerr << "Ошибка: не удалось подключиться к серверу\n";
        close(sock);
        return 1;
    }

    // 4. Отправляем данные (строку codeFromCard)
    ssize_t sentBytes = send(sock, codeFromCard.c_str(), codeFromCard.size(), 0);
    if (sentBytes < 0) {
        std::cerr << "Ошибка: не удалось отправить данные\n";
    } else {
        std::cout << "Отправлено сообщение: " << codeFromCard << std::endl;
    }

    char buffer[1024];
    ssize_t recvBytes = recv(sock, buffer, sizeof(buffer)-1, 0);
    if (recvBytes > 0) {
        buffer[recvBytes] = '\0';
        std::cout << "Ответ от сервера: " << buffer << std::endl;
    }

    // 5. Закрываем соединение
    close(sock);
    return 0;
}